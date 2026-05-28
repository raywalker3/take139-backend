"""Take 139 Backend — Phase 1.

Handles:
- Assessment submission + storage
- Pair code generation
- PDF report generation
- Email delivery to user + admin
- Basic health check

Future phases: counselor auth, couple reports, Stripe auto-codes.
"""
import os
import json
import base64
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database import (
    init_db, get_db, Submission, ImagoSubmission,
    AccessCode, CouplePair, AuthToken,
    CODE_KIND_SINGLE, CODE_KIND_COUPLE, CODE_KIND_CONNECT,
    CODE_STATUS_ACTIVE, CODE_STATUS_REDEEMED, CODE_STATUS_EXPIRED, CODE_STATUS_REVOKED,
    CODE_SOURCE_ADMIN, CODE_SOURCE_STRIPE, CODE_SOURCE_COMP,
)
from pair_codes import generate_pair_code
import access_codes as ac
import admin_auth
import auth as user_auth
import quick_pdf
import code_gating
import stripe_purchase
import walkthroughs as wt

# Feature flag: when true, /submit and /pair/connect require valid access codes.
# Set ENFORCE_ACCESS_CODES=true on Railway when ready for paid launch.
ENFORCE_ACCESS_CODES = os.environ.get("ENFORCE_ACCESS_CODES", "false").lower() in ("1", "true", "yes")
from report_data import get_report_data
from pdf_generator import generate_report_pdf, render_email_html
from email_service import send_to_admin_and_user

# ── IMAGO imports ──────────────────────────────────────────────────────
from imago_items import ITEMS as IMAGO_ITEMS, get_items_for_assessment
from imago_scoring import score_imago
from imago_pdf_generator import generate_imago_pdf
from imago_brief_generator import generate_imago_brief_pdf
from jinja2 import Environment, FileSystemLoader

_imago_email_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    autoescape=False,
)
_imago_email_template = _imago_email_env.get_template("imago_email.html")


app = FastAPI(title="Take 139 Backend", version="1.0.0")

# CORS — allow the take139.com frontend to POST
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://take139.com",
        "https://www.take139.com",
        "https://raywalker3.github.io",
        "http://localhost:3000",  # for local dev
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
def _startup():
    init_db()


# ─── Schemas ───

class TriggerScores(BaseModel):
    DIS: float = 0
    DISC: float = 0
    INJ: float = 0
    CTRL: float = 0
    SHAM: float = 0
    SIG: float = 0


class SubmissionIn(BaseModel):
    """Payload the frontend sends when someone finishes the assessment.

    name and email are now REQUIRED — captured by the finalize gate that
    runs after the last assessment question and before results render.
    The server still treats them as Optional in the schema (so legacy
    frontends and the admin Quick PDF flow don't 400), but enforces
    non-empty values in the route handler when ENFORCE_FINALIZE_GATE is on.
    """
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    # Partner's email — collected at the finalize gate ONLY when the
    # access code is a Couple code. Stored in intake_json under the key
    # 'partner_email' so we can later match a future signup to this pair.
    partner_email: Optional[EmailStr] = None
    access_code_used: Optional[str] = None

    # Intake — home description, family structure, etc.
    intake: dict = Field(default_factory=dict)

    # All raw answers (for future recomputation/analysis)
    answers: dict = Field(default_factory=dict)

    # Already-computed primary profile identifiers
    primary_trigger: str  # e.g., "DIS"
    core_question: str    # e.g., "COMP"
    mechanism: str        # e.g., "ARCH"
    breakdown: str        # e.g., "ATTY"

    # Trigger score percentages
    trigger_scores: TriggerScores

    # Optional free-form home description ("warm and tense", etc.)
    home_desc: Optional[str] = None

    # Optional wrap-up answers captured on the final results screen.
    # Shape (both keys optional):
    #   { "mechanism": {"mc": "b", "rank": [3,0,1,4,2]},
    #     "breakdown": {"mc": "a", "rank": [2,1,0,3,4]} }
    # where "rank" is a list of original item indexes in rank order (most-true first).
    wrapup_answers: Optional[dict] = None


class SubmissionOut(BaseModel):
    pair_code: str
    email_sent_to_user: bool
    email_sent_to_admin: bool


# ─── Routes ───

@app.get("/")
def root():
    return {
        "service": "Take 139 Backend",
        "status": "alive",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.post("/submit", response_model=SubmissionOut)
def submit_assessment(payload: SubmissionIn, db: Session = Depends(get_db)):
    """Receive a completed assessment, store it, email the results."""

    # ─── Code gate (only when ENFORCE_ACCESS_CODES=true) ───
    consumed_code = None
    if ENFORCE_ACCESS_CODES:
        consumed_code = code_gating.enforce_assessment_code(
            db, payload.access_code_used, user_email=payload.email
        )

    # Generate unique pair code
    existing = {row[0] for row in db.query(Submission.pair_code).all()}
    pair_code = generate_pair_code(existing_codes=existing)

    # ─── Finalize gate: require name + email ───
    # The frontend now captures these on a dedicated 'finalize' screen
    # AFTER the last question. If either is missing here, the gate was
    # bypassed or a stale client is calling /submit. Refuse to render
    # the report so we never produce another walkthrough that calls
    # someone by their archetype instead of their actual name.
    finalize_name = (payload.name or "").strip()
    finalize_email = (payload.email or "").strip().lower() if payload.email else ""
    if not finalize_name or not finalize_email:
        raise HTTPException(
            status_code=400,
            detail="Please tell us your name and email so we can write your report to you.",
        )

    # Merge partner_email into intake so it persists with the submission.
    intake_with_partner = dict(payload.intake) if payload.intake else {}
    if payload.partner_email:
        intake_with_partner["partner_email"] = str(payload.partner_email).strip().lower()

    # Store
    sub = Submission(
        pair_code=pair_code,
        name=finalize_name,
        email=finalize_email,
        access_code_used=payload.access_code_used,
        intake_json=json.dumps(intake_with_partner),
        answers_json=json.dumps(payload.answers),
        results_json=json.dumps({
            "primary_trigger": payload.primary_trigger,
            "core_question": payload.core_question,
            "mechanism": payload.mechanism,
            "breakdown": payload.breakdown,
            "trigger_scores": payload.trigger_scores.dict(),
            "home_desc": payload.home_desc,
            "wrapup_answers": payload.wrapup_answers,
        }),
        primary_trigger=payload.primary_trigger,
        primary_core_question=payload.core_question,
        primary_mechanism=payload.mechanism,
        primary_breakdown=payload.breakdown,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)

    # Auto-create (or update) the User row tied to this email so the
    # submission shows up in the user's dashboard the next time they sign in.
    if payload.email:
        try:
            user_auth.get_or_create_user(db, email=str(payload.email), name=payload.name)
        except Exception as e:
            print(f"[AUTH] get_or_create_user failed for {payload.email}: {e}")

    # Build report data
    data = get_report_data(
        primary_trigger=payload.primary_trigger,
        core_question=payload.core_question,
        mechanism=payload.mechanism,
        breakdown=payload.breakdown,
        trigger_scores=payload.trigger_scores.dict(),
        home_desc=payload.home_desc or "",
        name=payload.name or "",
        pair_code=pair_code,
        wrapup_answers=payload.wrapup_answers,
    )

    # Generate PDF
    try:
        pdf_bytes = generate_report_pdf(data)
    except Exception as e:
        # Log but don't fail the submission — they still have their results on-screen
        print(f"[PDF ERROR] {e}")
        return SubmissionOut(
            pair_code=pair_code,
            email_sent_to_user=False,
            email_sent_to_admin=False,
        )

    # Render email body
    email_html = render_email_html(data)

    # Send emails
    safe_name = (payload.name or "friend").replace(" ", "-")
    pdf_filename = f"Take139-Profile-{safe_name}.pdf"
    email_subject = "Take 139 Assessment Profile"

    # ─── Build the personal Walkthrough PDF as a second attachment ───
    walkthrough_attachments = []
    try:
        walkthrough_pdf = wt.build_personal_walkthrough(sub, db=db)
        walkthrough_filename = f"Take139-Walkthrough-{safe_name}.pdf"
        walkthrough_attachments = [{
            "filename": walkthrough_filename,
            "content": base64.b64encode(walkthrough_pdf).decode("utf-8"),
        }]
    except Exception as e:
        print(f"[WALKTHROUGH GEN ERROR] {e}")

    try:
        send_result = send_to_admin_and_user(
            user_email=payload.email,
            subject=email_subject,
            html_body=email_html,
            pdf_bytes=pdf_bytes,
            pdf_filename=pdf_filename,
            user_name=payload.name,
            extra_attachments=walkthrough_attachments or None,
        )
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        send_result = {"admin": None, "user": None}

    user_sent = bool(send_result.get("user") and not send_result["user"].get("error"))
    admin_sent = bool(send_result.get("admin") and not send_result["admin"].get("error"))

    sub.emailed_to_user = user_sent
    sub.emailed_to_admin = admin_sent
    db.commit()

    # ─── Consume the access code ONLY AFTER the submission committed ───
    if consumed_code is not None:
        try:
            code_gating.mark_assessment_code_consumed(
                db, consumed_code,
                submission_pair_code=pair_code,
                user_email=payload.email,
            )
        except Exception as e:
            # Code marking failed but submission succeeded — log, don't fail user.
            print(f"[CODE CONSUME ERROR] {e}")

    return SubmissionOut(
        pair_code=pair_code,
        email_sent_to_user=user_sent,
        email_sent_to_admin=admin_sent,
    )


@app.get("/submissions/recent")
def recent_submissions(limit: int = 20, db: Session = Depends(get_db)):
    """Admin-only placeholder — returns recent submissions. Will be auth-gated in Phase 2."""
    # Phase 2 will add counselor authentication. For now, this is open (bad — add basic auth soon).
    rows = (
        db.query(Submission)
        .order_by(Submission.created_at.desc())
        .limit(min(limit, 100))
        .all()
    )
    return [
        {
            "pair_code": r.pair_code,
            "name": r.name,
            "email": r.email,
            "primary_mechanism": r.primary_mechanism,
            "primary_breakdown": r.primary_breakdown,
            "access_code_used": r.access_code_used,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


# ═════════════════ PAIR CODE LOOKUP / CONNECT (Take 139) ════════════════
#
# When a couple wants to connect their two Take 139 profiles for a side-by-side
# / synthesis view, the second person enters their partner's pair code on the
# results page. The frontend calls:
#
#   GET  /pair/{code}            — fetch partner's scored summary (no free-text)
#   POST /pair/connect           — mark two codes as paired (sets paired_with_code)
#
# Pair codes expire 30 days after submission. After that, /pair/{code} returns 404.
# The full answers/intake never leave the server — only the scored summary does.

PAIR_CODE_EXPIRY_DAYS = 30


def _scored_summary(sub: Submission) -> dict:
    """Build the partner-visible scored summary. Excludes free-text answers,
    intake details, and any other PII beyond first name."""
    return {
        "pair_code": sub.pair_code,
        "name": sub.name or "Your partner",
        "primary_trigger": sub.primary_trigger,
        "primary_core_question": sub.primary_core_question,
        "primary_mechanism": sub.primary_mechanism,
        "primary_breakdown": sub.primary_breakdown,
        # results_json contains the structured trigger/mechanism/breakdown
        # scores + wrap-up answers. Frontend will use this for the side-by-side
        # view + the synthesis page.
        "results": json.loads(sub.results_json) if sub.results_json else {},
        "created_at": sub.created_at.isoformat() if sub.created_at else None,
    }


@app.get("/pair/{code}")
def get_pair_profile(code: str, db: Session = Depends(get_db)):
    """Fetch a partner's scored summary by pair code.

    Returns 404 if the code does not exist, or if the submission is older than
    PAIR_CODE_EXPIRY_DAYS (we treat expired codes as not-found for privacy).
    """
    code = (code or "").strip().upper()
    if not code:
        raise HTTPException(status_code=400, detail="Pair code is required")

    sub = db.query(Submission).filter(Submission.pair_code == code).first()
    if sub is None:
        raise HTTPException(status_code=404, detail="Pair code not found")

    # 30-day expiration
    if sub.created_at:
        age = datetime.utcnow() - sub.created_at
        if age.days > PAIR_CODE_EXPIRY_DAYS:
            raise HTTPException(
                status_code=404,
                detail=f"This pair code has expired (codes are valid for {PAIR_CODE_EXPIRY_DAYS} days)",
            )

    return _scored_summary(sub)


class PairConnectIn(BaseModel):
    my_code: str
    partner_code: str
    # Connection access code — ignored unless ENFORCE_ACCESS_CODES=true.
    # Either a CONNECT-XXXXX ($10 add-on, single-use) or a COUPLE-XXXXX-A/B
    # (whose sibling has also been used by the other spouse).
    connection_code: Optional[str] = None


@app.post("/pair/connect")
def connect_pair(payload: PairConnectIn, db: Session = Depends(get_db)):
    """Mark two pair codes as paired. Sets paired_with_code on both records.

    When ENFORCE_ACCESS_CODES is true, also requires a `connection_code`
    in the payload — either a 'connect' kind code (single-use, $10 add-on)
    or a 'couple' kind code whose sibling has also been redeemed.

    Idempotent: pairing the same two codes again is a no-op.
    Re-pair lock: pairing a profile that's already in a different CouplePair
    is rejected with 409 (must purchase a new Connect code).
    """
    my_code = (payload.my_code or "").strip().upper()
    partner_code = (payload.partner_code or "").strip().upper()
    if not my_code or not partner_code:
        raise HTTPException(status_code=400, detail="Both codes required")
    if my_code == partner_code:
        raise HTTPException(status_code=400, detail="You cannot pair with yourself")

    me = db.query(Submission).filter(Submission.pair_code == my_code).first()
    partner = db.query(Submission).filter(Submission.pair_code == partner_code).first()
    if me is None or partner is None:
        raise HTTPException(status_code=404, detail="One or both codes not found")

    # Expiration check on both
    now = datetime.utcnow()
    for sub in (me, partner):
        if sub.created_at and (now - sub.created_at).days > PAIR_CODE_EXPIRY_DAYS:
            raise HTTPException(status_code=404, detail="One or both codes have expired")

    # ─── Re-pair lock (enforced regardless of feature flag) ───
    code_gating.check_repair_lock(db, my_code, partner_code)

    # ─── Connection code gate ───
    connection_code_used = None
    if ENFORCE_ACCESS_CODES:
        connection_code_used = code_gating.enforce_connection_code(
            db,
            connection_code=getattr(payload, "connection_code", None),
            me_pair_code=my_code,
            partner_pair_code=partner_code,
        )

    # Set both sides of the pairing on the Submission rows (legacy field)
    me.paired_with_code = partner_code
    me.paired_at = now
    partner.paired_with_code = my_code
    partner.paired_at = now
    db.commit()

    # ─── Record the bond in CouplePair (the locked record) ───
    code_gating.record_couple_pair(
        db,
        me_pair_code=my_code,
        partner_pair_code=partner_code,
        authorised_by_code=connection_code_used.code if connection_code_used else None,
    )

    # Consume the connection code if it was a single-use connect
    if connection_code_used is not None:
        code_gating.mark_connection_code_consumed(
            db, connection_code_used, my_code, partner_code
        )

    # ─── Generate the couples Walkthrough and email it to both partners ───
    # Refactored 2026-05-27: send_status surfaces precisely what happened.
    # The original flow swallowed all exceptions silently and returned ok,
    # which is how the Hilkens didn't get their email and only found out by
    # noticing it never arrived.
    email_status = _send_couples_email_pair(db, me, partner)

    return {
        "ok": True,
        "my_code": my_code,
        "partner_code": partner_code,
        "partner": _scored_summary(partner),
        "me": _scored_summary(me),
        "email_status": email_status,
    }


def _submissions_for_email(db: Session, email: str) -> list:
    """Return all Submissions owned by this email, looking up via BOTH
    Submission.email AND AccessCode.redeemed_by_email so signed-in users
    who never clicked "Email My Report" still see their results.

    This is the cornerstone bug-fix for the "my couples report never
    arrived" bug: the original lookup missed every submission whose
    Submission.email was NULL even though the user owned it.
    """
    e = (email or "").strip().lower()
    if not e:
        return []
    direct = (
        db.query(Submission)
        .filter(Submission.email == e)
        .order_by(Submission.created_at.desc())
        .all()
    )
    # Plus anything attached to an access code redeemed by this email.
    via_codes = (
        db.query(AccessCode)
        .filter(AccessCode.redeemed_by_email == e)
        .filter(AccessCode.redeemed_by_submission_pair_code.isnot(None))
        .all()
    )
    pair_codes = {a.redeemed_by_submission_pair_code for a in via_codes}
    extra = []
    if pair_codes:
        existing_ids = {s.id for s in direct}
        for s in (
            db.query(Submission)
            .filter(Submission.pair_code.in_(pair_codes))
            .order_by(Submission.created_at.desc())
            .all()
        ):
            if s.id not in existing_ids:
                extra.append(s)
    combined = direct + extra
    combined.sort(key=lambda s: s.created_at or datetime.min, reverse=True)
    return combined


def _resolve_email_for_submission(db: Session, sub: Submission) -> Optional[str]:
    """Return the best email to deliver this submission's report to.

    Submission.email is set when the user clicks "Email My Report" on the
    results page. But signed-in users who skipped that step won't have it,
    and the AccessCode.redeemed_by_email carries the email of the user who
    redeemed the code. Falling back closes that gap.
    """
    if sub.email and sub.email.strip():
        return sub.email.strip().lower()
    if sub.access_code_used:
        ac = db.query(AccessCode).filter(AccessCode.code == sub.access_code_used).first()
        if ac and ac.redeemed_by_email and ac.redeemed_by_email.strip():
            return ac.redeemed_by_email.strip().lower()
    return None


def _send_couples_email_pair(db: Session, me: Submission, partner: Submission) -> dict:
    """Build the Couples PDF and email it to both partners. Returns a
    structured status dict so callers (frontend) can show precise messaging
    instead of pretending it succeeded.
    """
    status = {
        "pdf_generated": False,
        "me":      {"email": None, "sent": False, "reason": None},
        "partner": {"email": None, "sent": False, "reason": None},
    }

    try:
        couples_pdf = wt.build_couples_walkthrough(me, partner, db=db)
        status["pdf_generated"] = True
    except Exception as e:
        msg = f"PDF generation failed: {type(e).__name__}: {e}"
        print(f"[COUPLES WALKTHROUGH GEN ERROR] {msg}")
        status["me"]["reason"] = msg
        status["partner"]["reason"] = msg
        return status

    from email_service import send_couples_walkthrough
    filename = f"Take139-Couples-{me.pair_code}-{partner.pair_code}.pdf"

    me_email = _resolve_email_for_submission(db, me)
    partner_email = _resolve_email_for_submission(db, partner)
    status["me"]["email"] = me_email
    status["partner"]["email"] = partner_email

    def _attempt(side_key: str, to_email: Optional[str], your_name: str,
                 partner_name: str) -> None:
        if not to_email:
            status[side_key]["reason"] = "No email on file for this submission."
            return
        try:
            r = send_couples_walkthrough(
                to_email=to_email,
                your_name=your_name,
                partner_name=partner_name,
                pdf_bytes=couples_pdf,
                filename=filename,
            )
            if isinstance(r, dict) and r.get("skipped"):
                status[side_key]["reason"] = f"Skipped: {r.get('reason') or 'unknown'}"
            elif isinstance(r, dict) and r.get("error"):
                status[side_key]["reason"] = f"Resend error: {r['error']}"
            else:
                status[side_key]["sent"] = True
        except Exception as e:
            msg = f"{type(e).__name__}: {e}"
            print(f"[COUPLES EMAIL {side_key.upper()} ERROR] {msg}")
            status[side_key]["reason"] = msg

    _attempt("me", me_email, me.name or "", partner.name or "")
    if partner_email and partner_email == me_email:
        status["partner"]["reason"] = "Same email as Person A; not sending twice."
    else:
        _attempt("partner", partner_email, partner.name or "", me.name or "")

    return status


# ═════════════════ CONSULTANT INQUIRY (For Churches form) ════════════════
#
# When someone fills out the form on /for-churches.html, the payload posts here
# and we email the inquiry to Chris's admin address. No data persistence — the
# email IS the record. Keeps the database clean and avoids retention concerns.

# ════════════════════════════════════════════════════════════════════════════
# Public code preflight — frontend validates a typed code BEFORE the user
# spends 15 min on the assessment. No side effects.
# ════════════════════════════════════════════════════════════════════════════

@app.get("/codes/check/{code_str}")
def check_code(code_str: str, db: Session = Depends(get_db)):
    """Preflight: is this code valid for use right now?

    Returns shape: {valid: bool, kind: str, status: str, reason: str, ...}
    The frontend can call this when the user types a code on the landing page
    and show ✓ / ✗ in real time before they start the assessment.
    """
    return code_gating.check_code_preflight(db, code_str)


@app.get("/codes/enforcement")
def codes_enforcement_status():
    """Lets the frontend know whether access-code gating is currently enforced.

    Public endpoint — returns just the feature flag value so the frontend
    can hide/show the 'enter your code' UI accordingly.
    """
    return {"enforced": ENFORCE_ACCESS_CODES}


# ════════════════════════════════════════════════════════════════════════════
# Stripe purchase flow — three products
# ════════════════════════════════════════════════════════════════════════════

class PurchaseCheckoutIn(BaseModel):
    kind: str  # "single" | "couple" | "connect"
    email: str


@app.get("/purchase/products")
def list_products():
    """Public catalog — lets the frontend show prices."""
    return {
        "configured": stripe_purchase.is_configured(),
        "products": stripe_purchase.PRODUCTS,
    }


@app.post("/purchase/checkout")
def purchase_checkout(payload: PurchaseCheckoutIn):
    """Create a Stripe Checkout Session for the chosen product.

    Returns: {"checkout_url": "...", "session_id": "..."}
    Frontend should redirect the user to checkout_url.
    """
    return stripe_purchase.create_checkout_session(
        kind=payload.kind,
        email=payload.email.strip().lower(),
    )


@app.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Receive Stripe webhook events.

    On checkout.session.completed: generate code(s) and email them to buyer.
    Idempotent (Stripe may deliver the same event more than once).
    """
    payload_bytes = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    event = stripe_purchase.verify_webhook(payload_bytes, sig_header)

    event_type = event.get("type")
    if event_type != "checkout.session.completed":
        return {"ok": True, "ignored": event_type}

    result = stripe_purchase.handle_checkout_completed(db, event)
    if "error" in result:
        print(f"[STRIPE WEBHOOK ERROR] {result}")
        return {"ok": False, "error": result["error"]}

    # Send confirmation email to buyer (only on first delivery)
    if not result.get("idempotent"):
        try:
            from email_service import send_purchase_confirmation
            frontend_url = os.environ.get("FRONTEND_URL", "https://take139.com").rstrip("/")
            send_purchase_confirmation(
                to_email=result["email"],
                kind=result["kind"],
                codes=result["codes"],
                frontend_url=frontend_url,
            )
        except Exception as e:
            print(f"[STRIPE EMAIL ERROR] Code(s) created but email failed: {e}")

    return {
        "ok": True,
        "codes_created": len(result["codes"]),
        "idempotent": result.get("idempotent", False),
    }


# ════════════════════════════════════════════════════════════════════════════
# Walkthrough PDF generation — personal + couples
#
# Two endpoints:
#   GET /walkthrough/personal/{pair_code}
#     Returns the personal Walkthrough PDF for that submission.
#     Available to anyone with the pair code (it's their own data).
#
#   GET /walkthrough/couples/{pair_code_a}/{pair_code_b}
#     Returns the couples Walkthrough PDF for two paired submissions.
#     Only succeeds if the two are already bonded in CouplePair.
# ════════════════════════════════════════════════════════════════════════════

@app.get("/walkthrough/personal/{pair_code}")
def get_personal_walkthrough(pair_code: str, db: Session = Depends(get_db)):
    """Generate and return the personal Walkthrough PDF for a submission."""
    pair_code = (pair_code or "").strip().upper()
    sub = db.query(Submission).filter(Submission.pair_code == pair_code).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Pair code not found")

    pdf_bytes = wt.build_personal_walkthrough(sub, db=db)
    filename = f"Take139-Walkthrough-{pair_code}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "private, max-age=300",
        },
    )


@app.get("/walkthrough/couples/{pair_code_a}/{pair_code_b}")
def get_couples_walkthrough(pair_code_a: str, pair_code_b: str, db: Session = Depends(get_db)):
    """Generate and return the couples Walkthrough PDF.

    Requires the two submissions to already be bonded in CouplePair.
    """
    code_a = (pair_code_a or "").strip().upper()
    code_b = (pair_code_b or "").strip().upper()

    # Verify bond exists in either order
    bonded = db.query(CouplePair).filter(
        ((CouplePair.pair_code_a == code_a) & (CouplePair.pair_code_b == code_b))
        | ((CouplePair.pair_code_a == code_b) & (CouplePair.pair_code_b == code_a))
    ).first()
    if not bonded:
        raise HTTPException(
            status_code=403,
            detail="These two profiles are not paired. Connect them first.",
        )

    sub_a = db.query(Submission).filter(Submission.pair_code == code_a).first()
    sub_b = db.query(Submission).filter(Submission.pair_code == code_b).first()
    if not sub_a or not sub_b:
        raise HTTPException(status_code=404, detail="One or both pair codes not found")

    pdf_bytes = wt.build_couples_walkthrough(sub_a, sub_b, db=db)
    filename = f"Take139-Couples-{code_a}-{code_b}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "private, max-age=300",
        },
    )


class ConsultantInquiryIn(BaseModel):
    name: str
    email: str
    role: Optional[str] = None
    organization: Optional[str] = None
    inquiry_type: Optional[str] = None
    message: Optional[str] = None


@app.post("/consultant-inquiry")
def consultant_inquiry(payload: ConsultantInquiryIn):
    """Receive a consultant-inquiry form submission and email it to Chris."""
    name = (payload.name or "").strip()
    email = (payload.email or "").strip()
    if not name or not email:
        raise HTTPException(status_code=400, detail="Name and email are required")

    # Build an HTML email body
    rows = [
        ("Name",           name),
        ("Email",          email),
        ("Role",           (payload.role or "").strip() or "—"),
        ("Organization",   (payload.organization or "").strip() or "—"),
        ("Inquiry type",   (payload.inquiry_type or "").strip() or "—"),
    ]
    rows_html = "".join(
        f"<tr><td style='padding:4px 16px 4px 0;color:#8b8475;font-size:13px;letter-spacing:0.06em;text-transform:uppercase;'>{k}</td>"
        f"<td style='padding:4px 0;color:#1d1d1b;font-size:14px;'>{v}</td></tr>"
        for k, v in rows
    )
    message_html = (
        f"<div style='margin-top:24px;padding:16px;background:#f5f1e8;border-left:3px solid #8a4a2c;'>"
        f"<div style='font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:#8a4a2c;font-weight:600;margin-bottom:6px;'>Message</div>"
        f"<div style='color:#1d1d1b;font-size:14px;line-height:1.6;white-space:pre-wrap;'>{(payload.message or '').strip() or '(none)'}</div>"
        f"</div>"
    )
    html_body = (
        f"<div style='font-family:Helvetica,Arial,sans-serif;max-width:600px;'>"
        f"<h2 style='font-family:Georgia,serif;color:#1d1d1b;margin:0 0 8px 0;'>New Consultant Inquiry</h2>"
        f"<p style='color:#5d564b;margin:0 0 20px 0;font-size:14px;'>Take 139 · For Churches form</p>"
        f"<table style='border-collapse:collapse;'>{rows_html}</table>"
        f"{message_html}"
        f"<p style='color:#8b8475;font-size:12px;margin-top:24px;'>Reply directly to this email to respond to {name}.</p>"
        f"</div>"
    )

    subject = f"Consultant inquiry from {name}"
    if payload.organization:
        subject += f" ({payload.organization})"

    # Send to admin only — not the inquirer (no PDF attachment needed here)
    try:
        from email_service import send_results_email, ADMIN_EMAIL
        send_results_email(
            to_email=ADMIN_EMAIL,
            subject=subject,
            html_body=html_body,
            pdf_bytes=b"",  # no attachment
            pdf_filename="",
            reply_to=email,  # makes Chris's reply go to the inquirer
        )
    except Exception as e:
        # We never expose the actual error to the user, but log it server-side
        print(f"[consultant-inquiry] email send failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not deliver your inquiry right now. Please email us directly.",
        )

    return {"ok": True}


# ═════════════════ IMAGO ENDPOINTS ══════════════════════════

class ImagoSubmissionIn(BaseModel):
    """Incoming IMAGO assessment submission from the frontend."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    access_code_used: Optional[str] = None

    # answers: {item_id: 1-5}
    # All 100 items expected; partial responses allowed but flagged in scoring
    answers: dict = Field(default_factory=dict)

    # Optional: link to a Take 139 pair code if this person already took it
    take139_pair_code: Optional[str] = None


class ImagoSubmissionOut(BaseModel):
    pair_code: str
    letter_type: str
    soul_shape: str
    archetype: str
    email_sent_to_user: bool
    email_sent_to_admin: bool
    # Optional fields the frontend uses for richer display
    letter_breakdown: list = []   # [{letter, case, borderline}]
    summary: Optional[str] = None


# =========================================================
# Magic-link sign-in (Phase 2)
# =========================================================

class MagicLinkRequestIn(BaseModel):
    email: EmailStr


class MagicLinkRequestOut(BaseModel):
    ok: bool
    message: str


class VerifyOut(BaseModel):
    session_token: str
    email: str


class MeSubmissionOut(BaseModel):
    pair_code: str
    name: Optional[str] = None
    primary_mechanism: Optional[str] = None
    primary_trigger: Optional[str] = None
    primary_core_question: Optional[str] = None
    paired_with_code: Optional[str] = None
    created_at: Optional[str] = None


class MeOut(BaseModel):
    email: str
    name: Optional[str] = None
    submissions: list  # list[MeSubmissionOut]
    imago_count: int = 0
    has_password: bool = False
    email_verified: bool = False


@app.post("/auth/request-magic-link", response_model=MagicLinkRequestOut)
def request_magic_link(
    payload: MagicLinkRequestIn,
    request: Request,
    db: Session = Depends(get_db),
):
    """Issue a single-use magic-link email.

    We ALWAYS return ok=true regardless of whether the email is registered,
    so an attacker cannot enumerate users by probing this endpoint.
    """
    email = str(payload.email).strip().lower()
    ip = user_auth.get_client_ip(request)

    # Rate-limit per email: only issue if no token has been issued in the
    # last 30 seconds. Quietly drop further requests.
    from datetime import datetime as _dt, timedelta as _td
    recent = (
        db.query(user_auth.AuthToken)
        .filter(user_auth.AuthToken.email == email)
        .filter(user_auth.AuthToken.created_at > _dt.utcnow() - _td(seconds=30))
        .first()
    )
    if recent is None:
        try:
            token_row = user_auth.create_magic_link_token(
                db, email=email, purpose="signin", requester_ip=ip
            )
            magic_url = user_auth.build_magic_link_url(token_row.token)
            from email_service import send_magic_link as _send_ml
            _send_ml(email, magic_url, ttl_minutes=user_auth.MAGIC_LINK_TTL_MIN)
        except Exception as e:
            print(f"[AUTH] magic-link issue failed for {email}: {e}")

    return MagicLinkRequestOut(
        ok=True,
        message="If that email is valid, a sign-in link is on its way. Check your inbox (and spam folder) within the next minute.",
    )


@app.get("/auth/verify", response_model=VerifyOut)
def verify_magic_link(
    token: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Validate a magic-link token and mint a session.

    Side effects:
    - Creates a User row if one doesn't exist yet for this email
    - Marks email_verified_at on the User
    - Records last_signin_at
    """
    row = user_auth.consume_token(db, token)
    if row is None:
        raise HTTPException(
            status_code=400,
            detail="This sign-in link is invalid, expired, or already used. Please request a fresh link.",
        )
    ip = user_auth.get_client_ip(request)
    sess = user_auth.create_session(db, email=row.email, requester_ip=ip)

    # Ensure a User row exists and mark email verified.
    try:
        user = user_auth.get_or_create_user(db, email=row.email)
        user_auth.mark_email_verified(db, user)
        user.last_signin_at = datetime.utcnow()
        db.add(user); db.commit()
    except Exception as e:
        print(f"[AUTH] user upsert in /auth/verify failed: {e}")

    return VerifyOut(session_token=sess.session_token, email=sess.email)


@app.get("/auth/me")  # response model relaxed to dict to allow partner field
def auth_me(
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Return everything we know about the signed-in user."""
    email = sess.email
    user = user_auth.get_user_by_email(db, email)
    # Bug-fix 2026-05-27: use the unified lookup so submissions whose
    # Submission.email is NULL (signed-in users who skipped Email My Report)
    # still show on the dashboard.
    subs = _submissions_for_email(db, email)
    name = (user.name if user and user.name else None)
    if not name:
        for s in subs:
            if s.name:
                name = s.name
                break
    sub_list = []
    for s in subs:
        sub_list.append({
            "pair_code": s.pair_code,
            "name": s.name,
            "primary_mechanism": s.primary_mechanism,
            "primary_trigger": s.primary_trigger,
            "primary_core_question": s.primary_core_question,
            "paired_with_code": s.paired_with_code,
            "created_at": s.created_at.isoformat() if s.created_at else None,
        })
    imago_count = (
        db.query(ImagoSubmission)
        .filter(ImagoSubmission.email == email)
        .count()
    )
    # Enrich the most-recent submission with partner details if paired.
    partner_info = None
    if sub_list and sub_list[0].get("paired_with_code"):
        partner_pc = sub_list[0]["paired_with_code"]
        partner_sub = db.query(Submission).filter(Submission.pair_code == partner_pc).first()
        if partner_sub:
            partner_info = {
                "pair_code": partner_sub.pair_code,
                "name": partner_sub.name,
                "primary_mechanism": partner_sub.primary_mechanism,
                "primary_trigger": partner_sub.primary_trigger,
                "primary_core_question": partner_sub.primary_core_question,
            }

    return {
        "email": email,
        "name": name,
        "submissions": sub_list,
        "imago_count": imago_count,
        "has_password": bool(user and user.password_hash),
        "email_verified": bool(user and user.email_verified_at),
        "partner": partner_info,
    }


class ResendCouplesIn(BaseModel):
    my_pair_code: Optional[str] = None


@app.post("/pair/resend-couples")
def pair_resend_couples(
    payload: ResendCouplesIn,
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Re-send the Couples Walkthrough email to both partners.

    Useful when the original send from /pair/connect failed silently, or
    when the user lost the original email. Sign-in required; rate-limited
    to one resend per minute per signed-in user.
    """
    pc = (payload.my_pair_code or "").strip().upper() or None
    if pc:
        me = db.query(Submission).filter(Submission.pair_code == pc).first()
        if not me:
            raise HTTPException(status_code=404, detail="Submission not found.")
        owner_email = (_resolve_email_for_submission(db, me) or "").lower()
        if owner_email != sess.email:
            raise HTTPException(status_code=403, detail="You don't own that pair code.")
    else:
        subs = _submissions_for_email(db, sess.email)
        me = subs[0] if subs else None
    if not me:
        raise HTTPException(status_code=404, detail="No submission found for your account.")
    if not me.paired_with_code:
        raise HTTPException(status_code=400, detail="You're not paired with a partner yet.")
    partner = db.query(Submission).filter(Submission.pair_code == me.paired_with_code).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner's submission could not be found.")

    # Rate-limit reuse of AuthToken with a dedicated purpose
    from datetime import datetime as _dt, timedelta as _td
    cooldown = 60
    recent = (
        db.query(AuthToken)
        .filter(AuthToken.email == sess.email, AuthToken.purpose == "resend_couples")
        .filter(AuthToken.created_at > _dt.utcnow() - _td(seconds=cooldown))
        .first()
    )
    if recent is not None:
        raise HTTPException(
            status_code=429,
            detail="You just requested a resend — please wait a minute before trying again.",
        )

    email_status = _send_couples_email_pair(db, me, partner)

    db.add(AuthToken(
        token=user_auth._new_token(16),
        email=sess.email,
        purpose="resend_couples",
        created_at=_dt.utcnow(),
        expires_at=_dt.utcnow() + _td(seconds=cooldown),
    ))
    db.commit()

    return {"ok": True, "email_status": email_status}


@app.post("/auth/signout")
def auth_signout(
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Sign the user out by revoking their session."""
    user_auth.revoke_session(db, sess.session_token)
    return {"ok": True}


# ----- Password endpoints -------------------------------------------------

class SignupIn(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class SignupOut(BaseModel):
    ok: bool
    message: str
    needs_verification: bool = True


class SigninPasswordIn(BaseModel):
    email: EmailStr
    password: str


class SetPasswordIn(BaseModel):
    new_password: str
    current_password: Optional[str] = None  # required only if user already has one


class UpdateNameIn(BaseModel):
    name: str


@app.post("/auth/signup", response_model=SignupOut)
def auth_signup(
    payload: SignupIn,
    request: Request,
    db: Session = Depends(get_db),
):
    """Create an account with a password.

    Flow:
    1. Validate password strength.
    2. Upsert User; set password_hash.
    3. If email_verified_at is None, send a magic-link to verify the email.
       (The user can then click the link to verify + sign in. We do NOT
       immediately sign them in here — verifying email first is safer.)
    """
    email = str(payload.email).strip().lower()
    err = user_auth.validate_password_strength(payload.password)
    if err:
        raise HTTPException(status_code=400, detail=err)

    user = user_auth.get_or_create_user(db, email=email, name=payload.name)
    if user.password_hash:
        # Account exists with a password. Do NOT overwrite; treat as a hint
        # that this person already has an account.
        return SignupOut(
            ok=True,
            message="An account with this email already exists. Try signing in, or use \"forgot password\" if needed.",
            needs_verification=user.email_verified_at is None,
        )

    user_auth.set_user_password(db, user, payload.password)
    if payload.name and not user.name:
        user.name = payload.name
        db.add(user); db.commit()

    # Always send a magic link to verify email + offer instant sign-in.
    try:
        ip = user_auth.get_client_ip(request)
        tk = user_auth.create_magic_link_token(db, email=email, purpose="signin", requester_ip=ip)
        from email_service import send_magic_link as _sml
        _sml(email, user_auth.build_magic_link_url(tk.token), ttl_minutes=user_auth.MAGIC_LINK_TTL_MIN)
    except Exception as e:
        print(f"[AUTH] signup magic-link send failed: {e}")

    return SignupOut(
        ok=True,
        message="Account created. Check your email for a verification link to finish setting up your account.",
        needs_verification=user.email_verified_at is None,
    )


@app.post("/auth/signin-password", response_model=VerifyOut)
def auth_signin_password(
    payload: SigninPasswordIn,
    request: Request,
    db: Session = Depends(get_db),
):
    """Sign in with email + password. Returns a session token.

    Generic error message on any failure so attackers can't enumerate users.
    """
    email = str(payload.email).strip().lower()
    user = user_auth.get_user_by_email(db, email)
    if user is None or not user.password_hash or not user_auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    if user.email_verified_at is None:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email first. Check your inbox for the verification link, or use \"Forgot password\" to request a fresh one.",
        )
    ip = user_auth.get_client_ip(request)
    sess = user_auth.create_session(db, email=email, requester_ip=ip)
    user.last_signin_at = datetime.utcnow()
    db.add(user); db.commit()
    return VerifyOut(session_token=sess.session_token, email=email)


@app.post("/auth/set-password")
def auth_set_password(
    payload: SetPasswordIn,
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Set or change the signed-in user's password.

    If the user already has a password, current_password is required.
    If they don't (magic-link only account), current_password is ignored.
    """
    err = user_auth.validate_password_strength(payload.new_password)
    if err:
        raise HTTPException(status_code=400, detail=err)
    user = user_auth.get_user_by_email(db, sess.email)
    if user is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    if user.password_hash:
        if not payload.current_password or not user_auth.verify_password(
            payload.current_password, user.password_hash
        ):
            raise HTTPException(status_code=401, detail="Current password is incorrect.")
    user_auth.set_user_password(db, user, payload.new_password)
    return {"ok": True, "message": "Password updated."}


# ----- Signed-in convenience endpoints (/me/*) ---------------------------

def _require_user_owns_pair(
    db: Session,
    sess: "user_auth.AuthSession",
    pair_code: str,
) -> Submission:
    """Look up a submission and verify the signed-in user owns it.
    Uses _resolve_email_for_submission so submissions with blank email
    still resolve correctly via the redeemed AccessCode owner.
    """
    pc = (pair_code or "").strip().upper()
    sub = db.query(Submission).filter(Submission.pair_code == pc).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found.")
    resolved = (_resolve_email_for_submission(db, sub) or "").lower()
    if resolved != sess.email:
        raise HTTPException(status_code=403, detail="You don't have access to this submission.")
    return sub


def _user_default_submission(db: Session, email: str) -> Optional[Submission]:
    """Most-recent submission for this email — used when caller doesn't pass
    a specific pair_code. Uses the unified lookup so blank-email subs still
    resolve.
    """
    subs = _submissions_for_email(db, email)
    return subs[0] if subs else None


@app.get("/me/pdf/personal")
def me_personal_pdf(
    pair_code: Optional[str] = None,
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Download the user's personal report PDF (the 10-page profile)."""
    if pair_code:
        sub = _require_user_owns_pair(db, sess, pair_code)
    else:
        sub = _user_default_submission(db, sess.email)
        if sub is None:
            raise HTTPException(status_code=404, detail="No assessment found for this account yet.")
    # Rebuild data dict and regenerate the PDF on demand.
    try:
        results = json.loads(sub.results_json or "{}")
        intake = json.loads(sub.intake_json or "{}")
    except Exception:
        results, intake = {}, {}
    home_atmos = (intake.get("atmosphere") or [])
    home_family = intake.get("family_type") or ""
    home_desc = (", ".join(home_atmos) + (" " if home_atmos else "") + str(home_family or "")).strip()
    data = get_report_data(
        primary_trigger=sub.primary_trigger or "",
        core_question=sub.primary_core_question or "",
        mechanism=sub.primary_mechanism or "",
        breakdown=sub.primary_breakdown or "",
        trigger_scores=(results.get("trigger_scores") or {}),
        home_desc=home_desc,
        name=sub.name or "",
        pair_code=sub.pair_code,
        wrapup_answers=results.get("wrapup_answers"),
    )
    try:
        pdf_bytes = generate_report_pdf(data)
    except Exception as e:
        print(f"[ME PDF ERROR] personal: {e}")
        raise HTTPException(status_code=500, detail="Could not generate your PDF. Please try again in a moment.")
    safe_name = (sub.name or "profile").replace(" ", "-")
    fname = f"Take139-Profile-{safe_name}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{fname}"',
            "Cache-Control": "private, no-cache",
        },
    )


@app.get("/me/pdf/walkthrough")
def me_walkthrough_pdf(
    pair_code: Optional[str] = None,
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Download the user's personal Walkthrough PDF (the deep-dive companion)."""
    if pair_code:
        sub = _require_user_owns_pair(db, sess, pair_code)
    else:
        sub = _user_default_submission(db, sess.email)
        if sub is None:
            raise HTTPException(status_code=404, detail="No assessment found for this account yet.")
    try:
        pdf_bytes = wt.build_personal_walkthrough(sub, db=db)
    except Exception as e:
        print(f"[ME PDF ERROR] walkthrough: {e}")
        raise HTTPException(status_code=500, detail="Could not generate your walkthrough. Please try again.")
    safe_name = (sub.name or "profile").replace(" ", "-")
    fname = f"Take139-Walkthrough-{safe_name}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{fname}"',
            "Cache-Control": "private, no-cache",
        },
    )


@app.get("/me/pdf/couples")
def me_couples_pdf(
    pair_code: Optional[str] = None,
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Download the Couples Report PDF.

    400 if the user's submission isn't bonded to a partner yet.
    """
    if pair_code:
        sub = _require_user_owns_pair(db, sess, pair_code)
    else:
        sub = _user_default_submission(db, sess.email)
        if sub is None:
            raise HTTPException(status_code=404, detail="No assessment found for this account yet.")
    partner_code = (sub.paired_with_code or "").strip().upper()
    if not partner_code:
        raise HTTPException(
            status_code=400,
            detail="Your profile is not connected to a partner yet. Use the Connect button on your results page first.",
        )
    partner = db.query(Submission).filter(Submission.pair_code == partner_code).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner's submission not found.")
    try:
        pdf_bytes = wt.build_couples_walkthrough(sub, partner, db=db)
    except Exception as e:
        print(f"[ME PDF ERROR] couples: {e}")
        raise HTTPException(status_code=500, detail="Could not generate the couples report. Please try again.")
    fname = f"Take139-Couples-{sub.pair_code}-{partner_code}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{fname}"',
            "Cache-Control": "private, no-cache",
        },
    )


# Track last resend per email so we can rate-limit
_resend_cooldown_seconds = 60


@app.post("/me/resend-report")
def me_resend_report(
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Email the user's most recent personal report (PDF + walkthrough) to
    the signed-in account's email.
    """
    sub = _user_default_submission(db, sess.email)
    if sub is None:
        raise HTTPException(status_code=404, detail="No assessment found for this account yet.")

    # Rate limit: only one resend per minute per user.
    from datetime import datetime as _dt, timedelta as _td
    last = (
        db.query(AuthToken)  # piggy-back on AuthToken table to track last action
        .filter(AuthToken.email == sess.email, AuthToken.purpose == "resend")
        .filter(AuthToken.created_at > _dt.utcnow() - _td(seconds=_resend_cooldown_seconds))
        .first()
    )
    if last is not None:
        raise HTTPException(
            status_code=429,
            detail="You just requested a resend — please wait a minute before trying again.",
        )

    # Build report and walkthrough fresh.
    try:
        results = json.loads(sub.results_json or "{}")
        intake = json.loads(sub.intake_json or "{}")
    except Exception:
        results, intake = {}, {}
    home_atmos = (intake.get("atmosphere") or [])
    home_family = intake.get("family_type") or ""
    home_desc = (", ".join(home_atmos) + (" " if home_atmos else "") + str(home_family or "")).strip()
    data = get_report_data(
        primary_trigger=sub.primary_trigger or "",
        core_question=sub.primary_core_question or "",
        mechanism=sub.primary_mechanism or "",
        breakdown=sub.primary_breakdown or "",
        trigger_scores=(results.get("trigger_scores") or {}),
        home_desc=home_desc,
        name=sub.name or "",
        pair_code=sub.pair_code,
        wrapup_answers=results.get("wrapup_answers"),
    )
    try:
        pdf_bytes = generate_report_pdf(data)
    except Exception as e:
        print(f"[ME RESEND] pdf gen failed: {e}")
        raise HTTPException(status_code=500, detail="Could not generate the report just now. Please try again in a moment.")

    email_html = render_email_html(data)
    safe_name = (sub.name or "profile").replace(" ", "-")
    pdf_filename = f"Take139-Profile-{safe_name}.pdf"

    walkthrough_attachments = []
    try:
        wt_bytes = wt.build_personal_walkthrough(sub, db=db)
        walkthrough_attachments = [{
            "filename": f"Take139-Walkthrough-{safe_name}.pdf",
            "content": base64.b64encode(wt_bytes).decode("utf-8"),
        }]
    except Exception as e:
        print(f"[ME RESEND] walkthrough gen failed (continuing without): {e}")

    from email_service import send_results_email
    try:
        send_results_email(
            to_email=sess.email,
            subject="Take 139 Assessment Profile",
            html_body=email_html,
            pdf_bytes=pdf_bytes,
            pdf_filename=pdf_filename,
            extra_attachments=walkthrough_attachments or None,
        )
    except Exception as e:
        print(f"[ME RESEND] send failed: {e}")
        raise HTTPException(status_code=500, detail="Email service is unavailable. Please try again shortly.")

    # Stamp the resend so the rate limit holds.
    stamp = AuthToken(
        token=user_auth._new_token(16),
        email=sess.email,
        purpose="resend",
        created_at=_dt.utcnow(),
        expires_at=_dt.utcnow() + _td(seconds=_resend_cooldown_seconds),
    )
    db.add(stamp); db.commit()

    return {"ok": True, "message": f"Your report is on the way to {sess.email}."}


class MyCodeOut(BaseModel):
    code: str
    kind: str
    status: str
    sibling_code: Optional[str] = None
    price_cents: Optional[int] = None
    created_at: Optional[str] = None
    redeemed_at: Optional[str] = None
    redeemed_by_email: Optional[str] = None


@app.get("/me/codes")
def me_codes(
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Return access codes the signed-in user purchased.

    A code is considered the user's if the Stripe customer email matches the
    signed-in email. Magic-link sessions still expose this since auth verifies
    they own the email.
    """
    rows = (
        db.query(AccessCode)
        .filter(AccessCode.stripe_customer_email == sess.email)
        .order_by(AccessCode.created_at.desc())
        .all()
    )
    out = []
    for c in rows:
        out.append(MyCodeOut(
            code=c.code,
            kind=c.kind,
            status=c.status,
            sibling_code=c.sibling_code,
            price_cents=c.price_cents,
            created_at=c.created_at.isoformat() if c.created_at else None,
            redeemed_at=c.redeemed_at.isoformat() if c.redeemed_at else None,
            redeemed_by_email=c.redeemed_by_email,
        ))
    return {"codes": [c.dict() for c in out], "count": len(out)}


@app.post("/auth/update-name")
def auth_update_name(
    payload: UpdateNameIn,
    sess: "user_auth.AuthSession" = Depends(user_auth.require_session),
    db: Session = Depends(get_db),
):
    """Update the signed-in user's display name."""
    new_name = (payload.name or "").strip()
    if len(new_name) < 1 or len(new_name) > 200:
        raise HTTPException(status_code=400, detail="Name must be 1–200 characters.")
    user = user_auth.get_user_by_email(db, sess.email)
    if user is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    user.name = new_name
    db.add(user); db.commit()
    return {"ok": True, "name": new_name}


# =========================================================
# Admin Quick-PDF — generate Personal/Walkthrough/Couples PDFs
# from a hand-selected profile without taking the assessment.
# =========================================================

class QuickPdfProfile(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    trigger: str       # DIS / DISC / INJ / CTRL / SHM / SIG
    core_question: str # COMP / LOV / PROT / FREE / ACC / REM
    mechanism: str     # ARCH / ISLE / AMB / VAULT / ADPT / CAMP
    breakdown: str     # ATTY / GHOST / FLOOD / MASK / VERD / PLEA
    email: Optional[str] = None


class QuickPdfPersonalIn(BaseModel):
    profile: QuickPdfProfile
    include_walkthrough: bool = True


class QuickPdfCouplesIn(BaseModel):
    person_a: QuickPdfProfile
    person_b: QuickPdfProfile


class QuickPdfEmailIn(BaseModel):
    profile: QuickPdfProfile  # "to" is profile.email
    partner: Optional[QuickPdfProfile] = None  # if set, send Couples Report instead


@app.get("/admin/quick-pdf/options")
def admin_quick_pdf_options(_: None = Depends(admin_auth.require_admin)):
    """Return the dropdown option lists for the quick-PDF page."""
    return {
        "triggers": quick_pdf.TRIGGERS,
        "core_questions": quick_pdf.CORE_QUESTIONS,
        "mechanisms": quick_pdf.MECHANISMS,
        "breakdowns": quick_pdf.BREAKDOWNS,
    }


def _build_personal_pdf_bytes(p: QuickPdfProfile) -> bytes:
    """Build the 10-page Personal Report PDF from a ghost profile."""
    try:
        gs = quick_pdf.build_ghost_submission(
            name=p.name, trigger=p.trigger, core_question=p.core_question,
            mechanism=p.mechanism, breakdown=p.breakdown, email=p.email,
        )
    except quick_pdf.ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    results = json.loads(gs.results_json)
    data = get_report_data(
        primary_trigger=gs.primary_trigger,
        core_question=gs.primary_core_question,
        mechanism=gs.primary_mechanism,
        breakdown=gs.primary_breakdown,
        trigger_scores=results.get("trigger_scores") or {},
        home_desc="",
        name=gs.name,
        pair_code=gs.pair_code,
        wrapup_answers=None,
    )
    return generate_report_pdf(data), gs


@app.post("/admin/quick-pdf/personal")
def admin_quick_pdf_personal(
    payload: QuickPdfPersonalIn,
    _: None = Depends(admin_auth.require_admin),
):
    """Generate the Personal Report PDF (the 10-page profile)."""
    pdf_bytes, gs = _build_personal_pdf_bytes(payload.profile)
    safe_name = (gs.name or "profile").replace(" ", "-")
    fname = f"Take139-Profile-{safe_name}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{fname}"',
            "Cache-Control": "private, no-cache",
        },
    )


@app.post("/admin/quick-pdf/walkthrough")
def admin_quick_pdf_walkthrough(
    payload: QuickPdfPersonalIn,
    db: Session = Depends(get_db),
    _: None = Depends(admin_auth.require_admin),
):
    """Generate the Personal Walkthrough PDF for a profile."""
    try:
        gs = quick_pdf.build_ghost_submission(
            name=payload.profile.name, trigger=payload.profile.trigger,
            core_question=payload.profile.core_question,
            mechanism=payload.profile.mechanism, breakdown=payload.profile.breakdown,
            email=payload.profile.email,
        )
    except quick_pdf.ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        pdf_bytes = wt.build_personal_walkthrough(gs, db=db)
    except Exception as e:
        print(f"[QUICK-PDF] walkthrough gen failed: {e}")
        raise HTTPException(status_code=500, detail="Walkthrough generation failed. The (mechanism, breakdown) combination may not have a builder yet \u2014 the system fell back but errored. Check server logs.")
    safe_name = (gs.name or "profile").replace(" ", "-")
    fname = f"Take139-Walkthrough-{safe_name}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{fname}"',
            "Cache-Control": "private, no-cache",
        },
    )


@app.post("/admin/quick-pdf/couples")
def admin_quick_pdf_couples(
    payload: QuickPdfCouplesIn,
    db: Session = Depends(get_db),
    _: None = Depends(admin_auth.require_admin),
):
    """Generate the Couples Walkthrough PDF for two hand-picked profiles."""
    try:
        gs_a = quick_pdf.build_ghost_submission(
            name=payload.person_a.name, trigger=payload.person_a.trigger,
            core_question=payload.person_a.core_question,
            mechanism=payload.person_a.mechanism, breakdown=payload.person_a.breakdown,
            email=payload.person_a.email,
        )
        gs_b = quick_pdf.build_ghost_submission(
            name=payload.person_b.name, trigger=payload.person_b.trigger,
            core_question=payload.person_b.core_question,
            mechanism=payload.person_b.mechanism, breakdown=payload.person_b.breakdown,
            email=payload.person_b.email,
        )
    except quick_pdf.ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        pdf_bytes = wt.build_couples_walkthrough(gs_a, gs_b, db=db)
    except Exception as e:
        print(f"[QUICK-PDF] couples gen failed: {e}")
        raise HTTPException(status_code=500, detail="Couples report generation failed. Check server logs for the specific error.")
    safe_a = (gs_a.name or "a").replace(" ", "-")
    safe_b = (gs_b.name or "b").replace(" ", "-")
    fname = f"Take139-Couples-{safe_a}-{safe_b}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{fname}"',
            "Cache-Control": "private, no-cache",
        },
    )


@app.post("/admin/quick-pdf/email")
def admin_quick_pdf_email(
    payload: QuickPdfEmailIn,
    db: Session = Depends(get_db),
    _: None = Depends(admin_auth.require_admin),
):
    """Email the generated PDFs to the recipient. Uses the polished email
    template + Resend service. For couples, the report goes to person A's
    email (and partner's email if set).
    """
    to_email = (payload.profile.email or "").strip()
    if not to_email or "@" not in to_email:
        raise HTTPException(status_code=400, detail="A valid email address is required to send the PDF.")

    # Build the personal report + walkthrough as attachments.
    pdf_bytes, gs = _build_personal_pdf_bytes(payload.profile)
    data_for_email = get_report_data(
        primary_trigger=gs.primary_trigger,
        core_question=gs.primary_core_question,
        mechanism=gs.primary_mechanism,
        breakdown=gs.primary_breakdown,
        trigger_scores=json.loads(gs.results_json).get("trigger_scores") or {},
        home_desc="", name=gs.name, pair_code=gs.pair_code,
        wrapup_answers=None,
    )
    email_html = render_email_html(data_for_email)
    safe_name = (gs.name or "profile").replace(" ", "-")
    profile_filename = f"Take139-Profile-{safe_name}.pdf"

    attachments = []
    try:
        wt_bytes = wt.build_personal_walkthrough(gs, db=db)
        attachments = [{
            "filename": f"Take139-Walkthrough-{safe_name}.pdf",
            "bytes": wt_bytes,
        }]
    except Exception as e:
        print(f"[QUICK-PDF EMAIL] walkthrough gen skipped: {e}")

    # Couples report attached if partner is provided.
    couples_recipients = []
    if payload.partner is not None:
        try:
            gs_b = quick_pdf.build_ghost_submission(
                name=payload.partner.name, trigger=payload.partner.trigger,
                core_question=payload.partner.core_question,
                mechanism=payload.partner.mechanism, breakdown=payload.partner.breakdown,
                email=payload.partner.email,
            )
        except quick_pdf.ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        try:
            couples_pdf = wt.build_couples_walkthrough(gs, gs_b, db=db)
            safe_b = (gs_b.name or "b").replace(" ", "-")
            attachments.append({
                "filename": f"Take139-Couples-{safe_name}-{safe_b}.pdf",
                "bytes": couples_pdf,
            })
        except Exception as e:
            print(f"[QUICK-PDF EMAIL] couples gen failed: {e}")
        if payload.partner.email and "@" in (payload.partner.email or ""):
            couples_recipients.append(payload.partner.email)

    from email_service import send_results_email
    sent = {"primary": None, "partner": None}
    try:
        sent["primary"] = send_results_email(
            to_email=to_email,
            subject="Take 139 Assessment Profile",
            html_body=email_html,
            pdf_bytes=pdf_bytes,
            pdf_filename=profile_filename,
            extra_attachments=attachments or None,
        )
    except Exception as e:
        print(f"[QUICK-PDF EMAIL] primary send failed: {e}")
        raise HTTPException(status_code=500, detail="Email service is unavailable. Please try again shortly.")

    # Also send to partner (if their email was provided and we have couples PDF).
    for partner_email in couples_recipients:
        try:
            sent["partner"] = send_results_email(
                to_email=partner_email,
                subject="Take 139 Assessment Profile",
                html_body=email_html,
                pdf_bytes=pdf_bytes,
                pdf_filename=profile_filename,
                extra_attachments=attachments or None,
            )
        except Exception as e:
            print(f"[QUICK-PDF EMAIL] partner send failed: {e}")

    return {
        "ok": True,
        "sent_to": [to_email] + couples_recipients,
        "message": f"Sent to {to_email}" + (f" and {couples_recipients[0]}" if couples_recipients else ""),
    }


# =========================================================
# IMAGO endpoints
# =========================================================

@app.get("/imago/items")
def get_imago_items(shuffle: bool = False):
    """Return the IMAGO item set the frontend should display.

    Args:
        shuffle: If True, items are shuffled (recommended for production to
                 avoid response-set bias). The scoring is identical.

    Returns:
        Dict with `items` (list of {item_id, item_text, aspect_code, domain})
        and `total` (count).
    """
    items = get_items_for_assessment(shuffle=shuffle)
    # Only expose the public-safe fields (no direction/source to avoid response bias)
    public_items = [
        {
            "item_id": it["item_id"],
            "item_text": it["item_text"],
            "aspect_code": it["aspect_code"],
            "domain": it["domain"],
        }
        for it in items
    ]
    return {"items": public_items, "total": len(public_items)}


@app.post("/imago/submit", response_model=ImagoSubmissionOut)
def imago_submit(payload: ImagoSubmissionIn, db: Session = Depends(get_db)):
    """Receive a completed IMAGO assessment, score it, generate PDF, email."""

    # Validate answers
    if not payload.answers:
        raise HTTPException(status_code=400, detail="No answers provided")

    # Normalize answer values to int
    clean_answers = {}
    for item_id, val in payload.answers.items():
        try:
            clean_answers[item_id] = int(val)
        except (ValueError, TypeError):
            continue  # silently skip malformed

    # Score the submission
    result = score_imago(clean_answers, IMAGO_ITEMS)

    # Generate a unique pair code (avoid collision across BOTH Take 139 and IMAGO tables)
    existing = {row[0] for row in db.query(Submission.pair_code).all()}
    existing |= {row[0] for row in db.query(ImagoSubmission.pair_code).all()}
    pair_code = generate_pair_code(existing_codes=existing)

    name = (payload.name or "").strip() or "Friend"

    # Persist before generating PDF (so we have a record even if PDF/email fails)
    sub = ImagoSubmission(
        pair_code=pair_code,
        name=payload.name,
        email=payload.email,
        access_code_used=payload.access_code_used,
        answers_json=json.dumps(clean_answers),
        results_json=json.dumps(result.to_dict()),
        letter_type=result.letter_type,
        soul_shape=result.soul_shape,
        archetype=result.archetype,
        take139_pair_code=payload.take139_pair_code,
    )
    db.add(sub)
    db.commit()

    # Generate PDF + one-page brief
    try:
        pdf_bytes = generate_imago_pdf(result, name=name, pair_code=pair_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

    try:
        brief_bytes = generate_imago_brief_pdf(result, name=name, pair_code=pair_code)
    except Exception as e:
        # Don't fail the request if the brief errors — just skip it.
        brief_bytes = None
        print(f"[imago_submit] brief generation failed: {e}")

    # Render email body
    email_html = _imago_email_template.render(
        name=name,
        soul_shape=result.soul_shape,
        archetype=result.archetype,
        letter_type=result.letter_type,
        pair_code=pair_code,
    )

    # Send email to user (if email given) + always to admin
    extra_attachments = []
    if brief_bytes:
        extra_attachments.append({
            "filename": f"IMAGO-{name.replace(' ', '-')}-{pair_code}-BRIEF.pdf",
            "bytes": brief_bytes,
        })

    email_results = send_to_admin_and_user(
        user_email=payload.email,
        subject=f"Your IMAGO Hardwiring Profile — The {result.archetype}",
        html_body=email_html,
        pdf_bytes=pdf_bytes,
        pdf_filename=f"IMAGO-{name.replace(' ', '-')}-{pair_code}.pdf",
        user_name=name,
        extra_attachments=extra_attachments,
    )

    user_sent = (
        email_results.get("user") is not None
        and not isinstance(email_results.get("user"), dict)
        or (isinstance(email_results.get("user"), dict) and "error" not in email_results["user"] and not email_results["user"].get("skipped"))
    )
    admin_sent = (
        email_results.get("admin") is not None
        and (not isinstance(email_results.get("admin"), dict) or ("error" not in email_results["admin"] and not email_results["admin"].get("skipped")))
    )

    sub.emailed_to_user = bool(user_sent and payload.email)
    sub.emailed_to_admin = bool(admin_sent)
    db.commit()

    # Build the letter_breakdown for the frontend's borderline-underline display
    letter_breakdown = []
    domain_codes_in_order = [code for code, _ in [("I",""),("M",""),("A",""),("G",""),("O","")]]
    for i, ch in enumerate(result.letter_type):
        domain_code = domain_codes_in_order[i] if i < len(domain_codes_in_order) else ch.upper()
        letter_breakdown.append({
            "letter": ch,
            "case": "upper" if ch.isupper() else "lower",
            "borderline": domain_code in result.letter_type_borderline,
        })

    # Short pastoral summary for the results page
    summary = (
        f"You are The {result.soul_shape}, and within that shape your wiring "
        f"reads as The {result.archetype}. The full report names what we found, "
        f"with the scripture and reflection that belong to your pattern."
    )

    return ImagoSubmissionOut(
        pair_code=pair_code,
        letter_type=result.letter_type,
        soul_shape=result.soul_shape,
        archetype=result.archetype,
        email_sent_to_user=sub.emailed_to_user,
        email_sent_to_admin=sub.emailed_to_admin,
        letter_breakdown=letter_breakdown,
        summary=summary,
    )


@app.get("/imago/submissions/recent")
def imago_recent_submissions(limit: int = 20, db: Session = Depends(get_db)):
    """Admin placeholder — will be auth-gated in Phase 2."""
    rows = (
        db.query(ImagoSubmission)
        .order_by(ImagoSubmission.created_at.desc())
        .limit(min(limit, 100))
        .all()
    )
    return [
        {
            "pair_code": r.pair_code,
            "name": r.name,
            "email": r.email,
            "letter_type": r.letter_type,
            "soul_shape": r.soul_shape,
            "archetype": r.archetype,
            "access_code_used": r.access_code_used,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


# ════════════════════════════════════════════════════════════════════════════
# Admin endpoints
# All require Authorization: Bearer <token> (obtained from POST /admin/login).
# ════════════════════════════════════════════════════════════════════════════

from fastapi import Depends as _Depends


class AdminLoginIn(BaseModel):
    password: str


class AdminLoginOut(BaseModel):
    ok: bool
    token: str
    expires_in_hours: int


@app.post("/admin/login", response_model=AdminLoginOut)
def admin_login(payload: AdminLoginIn):
    """Exchange the admin password for a session token."""
    if not admin_auth.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = admin_auth.issue_token()
    return AdminLoginOut(
        ok=True,
        token=token,
        expires_in_hours=admin_auth.ADMIN_TOKEN_TTL_HOURS,
    )


@app.get("/admin/whoami")
def admin_whoami(_: None = _Depends(admin_auth.require_admin)):
    """Token validity check for the admin UI."""
    return {"ok": True, "admin": True}


class CreateCodesIn(BaseModel):
    kind: str  # "single" | "couple" | "connect"
    quantity: int = 1
    source: str = CODE_SOURCE_ADMIN  # "admin" | "comp" (stripe is server-only)
    batch_label: Optional[str] = None
    notes: Optional[str] = None
    expires_in_days: Optional[int] = None
    price_cents: Optional[int] = None  # override default; useful for comp ($0)


@app.post("/admin/codes")
def admin_create_codes(
    payload: CreateCodesIn,
    db: Session = Depends(get_db),
    _: None = _Depends(admin_auth.require_admin),
):
    """Generate a batch of access codes.

    For couple kind: each unit of quantity produces TWO codes (A + B).
    For single/connect kind: each unit of quantity produces ONE code.
    """
    if payload.kind not in (CODE_KIND_SINGLE, CODE_KIND_COUPLE, CODE_KIND_CONNECT):
        raise HTTPException(status_code=400, detail=f"Unknown kind: {payload.kind}")
    if payload.source not in (CODE_SOURCE_ADMIN, CODE_SOURCE_COMP):
        raise HTTPException(status_code=400, detail="source must be 'admin' or 'comp' from this endpoint")
    if payload.quantity < 1 or payload.quantity > 500:
        raise HTTPException(status_code=400, detail="quantity must be between 1 and 500")

    created = []
    price_cents = payload.price_cents if payload.price_cents is not None else (0 if payload.source == CODE_SOURCE_COMP else None)

    for _i in range(payload.quantity):
        if payload.kind == CODE_KIND_SINGLE:
            code = ac.create_single_code(
                db,
                source=payload.source,
                batch_label=payload.batch_label,
                notes=payload.notes,
                expires_in_days=payload.expires_in_days,
                price_cents=price_cents,
            )
            created.append(ac.code_to_dict(code))
        elif payload.kind == CODE_KIND_CONNECT:
            code = ac.create_connect_code(
                db,
                source=payload.source,
                batch_label=payload.batch_label,
                notes=payload.notes,
                expires_in_days=payload.expires_in_days,
                price_cents=price_cents,
            )
            created.append(ac.code_to_dict(code))
        elif payload.kind == CODE_KIND_COUPLE:
            code_a, code_b = ac.create_couple_code_pair(
                db,
                source=payload.source,
                batch_label=payload.batch_label,
                notes=payload.notes,
                expires_in_days=payload.expires_in_days,
            )
            created.append(ac.code_to_dict(code_a))
            created.append(ac.code_to_dict(code_b))

    return {"ok": True, "created_count": len(created), "codes": created}


@app.get("/admin/codes")
def admin_list_codes(
    kind: Optional[str] = None,
    status_filter: Optional[str] = None,
    source: Optional[str] = None,
    batch_label: Optional[str] = None,
    limit: int = 200,
    db: Session = Depends(get_db),
    _: None = _Depends(admin_auth.require_admin),
):
    """List codes with optional filters."""
    # Auto-sweep expired codes on every list call (cheap)
    ac.sweep_expired(db)

    q = db.query(AccessCode).order_by(AccessCode.created_at.desc())
    if kind:
        q = q.filter(AccessCode.kind == kind)
    if status_filter:
        q = q.filter(AccessCode.status == status_filter)
    if source:
        q = q.filter(AccessCode.source == source)
    if batch_label:
        q = q.filter(AccessCode.batch_label == batch_label)
    rows = q.limit(min(limit, 1000)).all()
    return {
        "count": len(rows),
        "codes": [ac.code_to_dict(c) for c in rows],
    }


@app.get("/admin/stats")
def admin_stats(
    db: Session = Depends(get_db),
    _: None = _Depends(admin_auth.require_admin),
):
    """Dashboard stats."""
    ac.sweep_expired(db)

    def count_by(kind, status_):
        return db.query(AccessCode).filter(
            AccessCode.kind == kind,
            AccessCode.status == status_,
        ).count()

    def revenue_cents(kind, source):
        """Sum price_cents for redeemed paid codes."""
        rows = db.query(AccessCode).filter(
            AccessCode.kind == kind,
            AccessCode.source == source,
            AccessCode.status == CODE_STATUS_REDEEMED,
            AccessCode.price_cents != None,  # noqa: E711
        ).all()
        return sum((r.price_cents or 0) for r in rows)

    stats = {
        "submissions": {
            "take139_total": db.query(Submission).count(),
            "imago_total": db.query(ImagoSubmission).count(),
            "couples_paired": db.query(CouplePair).count(),
        },
        "codes": {
            "single": {
                "active": count_by(CODE_KIND_SINGLE, CODE_STATUS_ACTIVE),
                "redeemed": count_by(CODE_KIND_SINGLE, CODE_STATUS_REDEEMED),
                "expired": count_by(CODE_KIND_SINGLE, CODE_STATUS_EXPIRED),
                "revoked": count_by(CODE_KIND_SINGLE, CODE_STATUS_REVOKED),
            },
            "couple": {
                "active": count_by(CODE_KIND_COUPLE, CODE_STATUS_ACTIVE),
                "redeemed": count_by(CODE_KIND_COUPLE, CODE_STATUS_REDEEMED),
                "expired": count_by(CODE_KIND_COUPLE, CODE_STATUS_EXPIRED),
                "revoked": count_by(CODE_KIND_COUPLE, CODE_STATUS_REVOKED),
            },
            "connect": {
                "active": count_by(CODE_KIND_CONNECT, CODE_STATUS_ACTIVE),
                "redeemed": count_by(CODE_KIND_CONNECT, CODE_STATUS_REDEEMED),
                "expired": count_by(CODE_KIND_CONNECT, CODE_STATUS_EXPIRED),
                "revoked": count_by(CODE_KIND_CONNECT, CODE_STATUS_REVOKED),
            },
        },
        "revenue_cents": {
            "single_paid": revenue_cents(CODE_KIND_SINGLE, CODE_SOURCE_STRIPE),
            "couple_paid": revenue_cents(CODE_KIND_COUPLE, CODE_SOURCE_STRIPE),
            "connect_paid": revenue_cents(CODE_KIND_CONNECT, CODE_SOURCE_STRIPE),
        },
    }
    return stats


class RevokeCodeIn(BaseModel):
    reason: Optional[str] = None


@app.post("/admin/codes/{code_str}/revoke")
def admin_revoke_code(
    code_str: str,
    payload: RevokeCodeIn,
    db: Session = Depends(get_db),
    _: None = _Depends(admin_auth.require_admin),
):
    """Manually kill a code (and its sibling if it's a couple code)."""
    code = ac.lookup_code(db, code_str)
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    ac.revoke_code(db, code, reason=payload.reason)
    revoked = [ac.code_to_dict(code)]
    if code.sibling_code:
        sibling = ac.lookup_code(db, code.sibling_code)
        if sibling and sibling.status == CODE_STATUS_ACTIVE:
            ac.revoke_code(db, sibling, reason=(payload.reason or "sibling revoked"))
            revoked.append(ac.code_to_dict(sibling))
    return {"ok": True, "revoked": revoked}


@app.get("/admin/codes/{code_str}")
def admin_get_code(
    code_str: str,
    db: Session = Depends(get_db),
    _: None = _Depends(admin_auth.require_admin),
):
    """Detail view for one code."""
    code = ac.lookup_code(db, code_str)
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    return ac.code_to_dict(code)


# ─── Admin: one-time backfill for blank submission names ───
@app.post("/admin/backfill-submission-names")
def admin_backfill_submission_names(
    db: Session = Depends(get_db),
    _: None = _Depends(admin_auth.require_admin),
):
    """Backfill Submission.name for rows where it is currently NULL/blank.

    Looks up the user who redeemed each submission's access code (via
    AccessCode.redeemed_by_email → User) and copies User.name onto the
    Submission. This patches submissions completed by signed-in users
    whose intake skipped re-asking for a name.

    Safe to run multiple times — only touches rows where name is blank.
    Returns a report of what changed.
    """
    candidates = (
        db.query(Submission)
          .filter((Submission.name.is_(None)) | (Submission.name == ""))
          .all()
    )

    fixed = []
    skipped = []

    for sub in candidates:
        candidate_email = None
        if sub.access_code_used:
            access = (
                db.query(AccessCode)
                  .filter(AccessCode.code == sub.access_code_used)
                  .first()
            )
            if access and access.redeemed_by_email:
                candidate_email = access.redeemed_by_email.strip().lower()
        if not candidate_email and sub.email:
            candidate_email = sub.email.strip().lower()

        resolved_name = None
        if candidate_email:
            user = db.query(User).filter(User.email == candidate_email).first()
            if user and user.name and user.name.strip():
                resolved_name = user.name.strip()
            else:
                # Humanizing fallback: capitalize the email local-part.
                local = candidate_email.split("@", 1)[0]
                for sep in (".", "_", "+", "-"):
                    local = local.split(sep, 1)[0]
                if local and local.isalpha():
                    resolved_name = local.capitalize()

        if resolved_name:
            sub.name = resolved_name
            fixed.append({
                "pair_code": sub.pair_code,
                "email": candidate_email,
                "resolved_name": resolved_name,
            })
        else:
            skipped.append({
                "pair_code": sub.pair_code,
                "reason": "no User row and no usable email local-part",
            })

    if fixed:
        db.commit()

    return {
        "total_candidates": len(candidates),
        "fixed_count": len(fixed),
        "skipped_count": len(skipped),
        "fixed": fixed,
        "skipped": skipped,
    }


# ─── Local dev entry point ───
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
