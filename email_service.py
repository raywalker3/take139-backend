"""Email delivery via Resend — sends branded results to user + admin."""
import os
import base64
from typing import Optional
import resend


ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "christopher.hilken@gmail.com")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "Take 139 <results@take139.com>")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


def send_results_email(
    to_email: str,
    subject: str,
    html_body: str,
    pdf_bytes: bytes,
    pdf_filename: str,
    reply_to: Optional[str] = None,
) -> dict:
    """Send a results email with PDF attachment.

    Args:
        to_email: Recipient
        subject: Subject line
        html_body: Full HTML email body
        pdf_bytes: Binary PDF content
        pdf_filename: Name for the attachment
        reply_to: Optional reply-to address

    Returns:
        Resend response dict or {'skipped': True} if no API key
    """
    if not RESEND_API_KEY:
        return {"skipped": True, "reason": "no RESEND_API_KEY set"}

    pdf_b64 = base64.b64encode(pdf_bytes).decode("ascii")

    params = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_body,
        "attachments": [
            {
                "filename": pdf_filename,
                "content": pdf_b64,
            }
        ],
    }
    if reply_to:
        params["reply_to"] = reply_to

    return resend.Emails.send(params)


def send_to_admin_and_user(
    user_email: Optional[str],
    subject: str,
    html_body: str,
    pdf_bytes: bytes,
    pdf_filename: str,
    user_name: Optional[str] = None,
) -> dict:
    """Send results to both admin and user (if user provided email)."""
    results = {"admin": None, "user": None}

    # Always send to admin
    admin_subject = f"{subject}" + (f" — {user_name}" if user_name else "")
    try:
        results["admin"] = send_results_email(
            to_email=ADMIN_EMAIL,
            subject=admin_subject,
            html_body=html_body,
            pdf_bytes=pdf_bytes,
            pdf_filename=pdf_filename,
        )
    except Exception as e:
        results["admin"] = {"error": str(e)}

    # Send to user if they provided email
    if user_email:
        try:
            results["user"] = send_results_email(
                to_email=user_email,
                subject=subject,
                html_body=html_body,
                pdf_bytes=pdf_bytes,
                pdf_filename=pdf_filename,
                reply_to=ADMIN_EMAIL,
            )
        except Exception as e:
            results["user"] = {"error": str(e)}

    return results
