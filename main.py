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

from database import init_db, get_db, Submission, ImagoSubmission
from pair_codes import generate_pair_code
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
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
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


# ─── Local dev entry point ───
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
