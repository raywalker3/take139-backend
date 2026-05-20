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
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database import (
    init_db, get_db, Submission, ImagoSubmission,
    AccessCode, CouplePair,
    CODE_KIND_SINGLE, CODE_KIND_COUPLE, CODE_KIND_CONNECT,
    CODE_STATUS_ACTIVE, CODE_STATUS_REDEEMED, CODE_STATUS_EXPIRED, CODE_STATUS_REVOKED,
    CODE_SOURCE_ADMIN, CODE_SOURCE_STRIPE, CODE_SOURCE_COMP,
)
from pair_codes import generate_pair_code
import access_codes as ac
import admin_auth
import code_gating
import stripe_purchase

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
    """Payload the frontend sends when someone finishes the assessment."""
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
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

    # Store
    sub = Submission(
        pair_code=pair_code,
        name=payload.name,
        email=payload.email,
        access_code_used=payload.access_code_used,
        intake_json=json.dumps(payload.intake),
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

    try:
        send_result = send_to_admin_and_user(
            user_email=payload.email,
            subject=email_subject,
            html_body=email_html,
            pdf_bytes=pdf_bytes,
            pdf_filename=pdf_filename,
            user_name=payload.name,
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

    return {
        "ok": True,
        "my_code": my_code,
        "partner_code": partner_code,
        "partner": _scored_summary(partner),
        "me": _scored_summary(me),
    }


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


# ─── Local dev entry point ───
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
