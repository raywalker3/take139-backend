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

from database import init_db, get_db, Submission
from pair_codes import generate_pair_code
from report_data import get_report_data
from pdf_generator import generate_report_pdf, render_email_html
from email_service import send_to_admin_and_user


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


# ─── Local dev entry point ───
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
