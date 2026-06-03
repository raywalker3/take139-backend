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


def send_magic_link(to_email: str, magic_url: str, ttl_minutes: int = 15) -> dict:
    """Email a sign-in magic link to the user.

    Always returns gracefully — missing API key returns a 'skipped' dict
    rather than raising, so /auth/request-magic-link can still respond 200.
    """
    if not RESEND_API_KEY:
        return {"skipped": True, "reason": "no RESEND_API_KEY set"}

    safe_email = (to_email or "").strip()
    if not safe_email:
        return {"skipped": True, "reason": "no recipient"}

    subject = "Your Take 139 sign-in link"
    html_body = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
  body {{ font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; margin:0; padding:0; background:#faf6ef; color:#2a2620; }}
  .container {{ max-width:520px; margin:0 auto; padding:40px 24px; }}
  .brand {{ font-size:11px; letter-spacing:0.35em; color:#c8956c; text-transform:uppercase; font-weight:600; margin-bottom:14px; }}
  h1 {{ font-family:Georgia,serif; font-size:26px; line-height:1.2; color:#2a2620; margin:0 0 16px 0; font-weight:400; }}
  p {{ line-height:1.65; font-size:15px; color:#3a342d; margin:0 0 14px 0; }}
  .cta-wrap {{ text-align:center; margin:28px 0; }}
  .cta {{ display:inline-block; background:#2a2620; color:#faf6ef !important; padding:14px 28px; border-radius:4px; text-decoration:none; font-size:14px; letter-spacing:0.08em; font-weight:600; }}
  .fallback {{ font-size:12px; color:#8a7f72; word-break:break-all; background:#fff; border:1px solid #e0d6c5; border-radius:4px; padding:12px; }}
  .footer {{ margin-top:32px; padding-top:20px; border-top:1px solid #e0d6c5; font-size:12px; color:#8a7f72; line-height:1.6; }}
  .footer .sig {{ margin-top:10px; color:#2a2620; font-weight:600; font-family:Georgia,serif; font-size:14px; }}
  a {{ color:#c8956c; text-decoration:none; }}
  a.cta:link, a.cta:visited {{ color:#faf6ef; }}
</style></head><body>
<div class="container">
  <div class="brand">Take 139</div>
  <h1>Your sign-in link</h1>
  <p>Click the button below to sign in to your Take 139 dashboard. The link is good for the next {ttl_minutes} minutes and can only be used once.</p>
  <div class="cta-wrap"><a href="{magic_url}" class="cta">Sign me in &rarr;</a></div>
  <p style="font-size:13px;color:#6b6158;">If the button doesn't work, copy and paste this URL into your browser:</p>
  <div class="fallback">{magic_url}</div>
  <p style="font-size:13px;color:#6b6158;margin-top:18px;">Didn&rsquo;t request this? You can safely ignore this email &mdash; no one can sign in without clicking the link above.</p>
  <div class="footer">
    Grace and peace,
    <div class="sig">&mdash; Dr. Chris Hilken</div>
    <div style="margin-top:14px;"><a href="https://take139.com">take139.com</a></div>
  </div>
</div>
</body></html>"""

    params = {
        "from": FROM_EMAIL,
        "to": [safe_email],
        "subject": subject,
        "html": html_body,
        "reply_to": ADMIN_EMAIL,
    }
    try:
        return resend.Emails.send(params)
    except Exception as e:
        return {"error": str(e)}


def send_results_email(
    to_email: str,
    subject: str,
    html_body: str,
    pdf_bytes: bytes,
    pdf_filename: str,
    reply_to: Optional[str] = None,
    extra_attachments: Optional[list] = None,
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

    attachments = []
    # Only attach a PDF if both filename and bytes are provided. This lets
    # callers (like the consultant inquiry form) reuse this helper without
    # forcing a fake attachment.
    if pdf_bytes and pdf_filename:
        pdf_b64 = base64.b64encode(pdf_bytes).decode("ascii")
        attachments.append({
            "filename": pdf_filename,
            "content": pdf_b64,
        })
    # Optional extra attachments. Accepts either format:
    #   {filename, bytes}   — raw bytes that we'll base64-encode here
    #   {filename, content} — pre-encoded base64 string (used by /submit)
    for extra in (extra_attachments or []):
        if "content" in extra and extra["content"]:
            content_b64 = extra["content"]
            if isinstance(content_b64, bytes):
                content_b64 = content_b64.decode("ascii")
        elif "bytes" in extra and extra["bytes"]:
            content_b64 = base64.b64encode(extra["bytes"]).decode("ascii")
        else:
            continue
        attachments.append({
            "filename": extra["filename"],
            "content": content_b64,
        })

    params = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_body,
        "attachments": attachments,
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
    extra_attachments: Optional[list] = None,
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
            extra_attachments=extra_attachments,
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
                extra_attachments=extra_attachments,
            )
        except Exception as e:
            results["user"] = {"error": str(e)}

    return results


def send_purchase_confirmation(
    to_email: str,
    kind: str,
    codes: list,
    frontend_url: str = "https://take139.com",
) -> dict:
    """Email a buyer their access code(s) after a successful Stripe purchase.

    kind: 'single' | 'couple' | 'connect'
    codes: ['T139-XXXXXX'] or ['COUPLE-XXXXXX-A', 'COUPLE-XXXXXX-B'] or ['CONNECT-XXXXXX']
    """
    if not RESEND_API_KEY:
        return {"skipped": True, "reason": "no RESEND_API_KEY set"}

    # Encode the buyer's email into the access-code link so the assessment's
    # finalize gate can pre-fill it. Saves the user from typing their email
    # twice (once at Stripe, again at the gate) and removes the cold-ask feel.
    from urllib.parse import quote as _qs
    buyer_param = f"&buyer={_qs(to_email or '')}" if to_email else ""

    # Subject + body tailored to product kind
    if kind == "single":
        subject = "Your Take 139 access code"
        product_name = "Conflict Origins (Take 139)"
        instructions = f"""
        <p>Click the link below to begin your assessment. The link auto-fills
        your code and email; you'll just enter your name when prompted.</p>
        <p style="text-align:center;margin:30px 0;">
            <a href="{frontend_url}/?code={codes[0]}{buyer_param}"
               style="background:#1d1d1b;color:#f5f1e8;padding:14px 28px;
                      text-decoration:none;border-radius:999px;
                      font-family:'Inter',sans-serif;font-weight:500;
                      display:inline-block;">
                Begin Your Assessment
            </a>
        </p>
        <p>Or visit <a href="{frontend_url}">take139.com</a> and enter your code manually:</p>
        <p style="font-family:ui-monospace,Menlo,monospace;font-size:18px;
                  text-align:center;padding:14px;background:#ece4d3;
                  border-radius:6px;">{codes[0]}</p>
        """
    elif kind == "couple":
        subject = "Your Take 139 Couple Package access codes"
        product_name = "Couple Package"
        instructions = f"""
        <p>You've received <strong>two codes</strong> — one for each spouse.
        Forward the second code to your spouse so each of you can take the
        assessment individually. After you've both completed it, you can
        connect your profiles to see your Couples Walkthrough.</p>

        <p style="text-align:center;margin:30px 0;">
            <a href="{frontend_url}/?code={codes[0]}{buyer_param}"
               style="background:#1d1d1b;color:#f5f1e8;padding:14px 28px;
                      text-decoration:none;border-radius:999px;
                      font-family:'Inter',sans-serif;font-weight:500;
                      display:inline-block;">
                Take Your Assessment (using Code A)
            </a>
        </p>

        <table style="width:100%;border-collapse:collapse;margin:24px 0;">
            <tr>
                <td style="padding:14px;background:#ece4d3;border-radius:6px;
                           font-family:ui-monospace,Menlo,monospace;">
                    <strong style="font-family:'Inter',sans-serif;font-size:12px;
                            text-transform:uppercase;letter-spacing:0.1em;
                            color:#8a4a2c;">Your code:</strong><br>
                    <span style="font-size:18px;">{codes[0]}</span>
                </td>
            </tr>
            <tr><td style="height:12px;"></td></tr>
            <tr>
                <td style="padding:14px;background:#ece4d3;border-radius:6px;
                           font-family:ui-monospace,Menlo,monospace;">
                    <strong style="font-family:'Inter',sans-serif;font-size:12px;
                            text-transform:uppercase;letter-spacing:0.1em;
                            color:#4f6b5e;">Code for your spouse:</strong><br>
                    <span style="font-size:18px;">{codes[1]}</span>
                </td>
            </tr>
        </table>

        <p style="font-size:13px;color:#6b6862;">Either of you can use Code A;
        the other uses Code B. They are otherwise identical.</p>
        """
    elif kind == "connect":
        subject = "Your Take 139 Connection Add-On code"
        product_name = "Connection Add-On"
        instructions = f"""
        <p>You'll use this code when connecting your two profiles on the
        results page (you and your spouse must each have already completed
        the Take 139 assessment).</p>
        <p style="font-family:ui-monospace,Menlo,monospace;font-size:18px;
                  text-align:center;padding:14px;background:#ece4d3;
                  border-radius:6px;">{codes[0]}</p>
        <p>This code is single-use. Once used, it cannot be re-paired.</p>
        """
    else:
        instructions = "<p>" + ", ".join(codes) + "</p>"
        subject = "Your Take 139 access code"
        product_name = "Take 139"

    html_body = f"""<!DOCTYPE html>
<html><body style="font-family:'Inter',sans-serif;color:#1d1d1b;
                    background:#f5f1e8;padding:40px 20px;line-height:1.6;">
<div style="max-width:560px;margin:0 auto;background:#f9f7f0;
            padding:40px 36px;border-radius:8px;">
    <p style="font-size:11px;letter-spacing:0.15em;text-transform:uppercase;
              color:#8a4a2c;margin:0 0 12px;">Take 139</p>
    <h1 style="font-family:Georgia,serif;font-weight:normal;font-size:28px;
               margin:0 0 24px;color:#1d1d1b;">Thank you for your purchase</h1>
    <p>Your <strong>{product_name}</strong> is ready.</p>
    {instructions}
    <hr style="border:none;border-top:1px solid #d4c39a;margin:30px 0;">
    <p style="font-size:13px;color:#6b6862;">
      <strong style="color:#1d1d1b;">Your personal dashboard.</strong><br>
      Once you finish your assessment, your full report, walkthrough, and partner pairing live at
      <a href="{frontend_url}/dashboard.html" style="color:#8a4a2c;">take139.com/dashboard</a>.
      You'll be signed in automatically the first time. Bookmark it for easy access later.
    </p>
    <p style="font-size:13px;color:#6b6862;">
        If you have any questions or need support, email us at
        <a href="mailto:hello@take139.com" style="color:#8a4a2c;">hello@take139.com</a>.
    </p>
    <p style="font-size:12px;color:#6b6862;margin-top:24px;">
        Take 139 · A counselor's framework for conflict origins<br>
        <a href="{frontend_url}" style="color:#8a4a2c;">take139.com</a>
    </p>
</div>
</body></html>"""

    try:
        params = {
            "from": FROM_EMAIL,
            "to": [to_email],
            "subject": subject,
            "html": html_body,
            "reply_to": ADMIN_EMAIL,
        }
        return resend.Emails.send(params)
    except Exception as e:
        return {"error": str(e)}


def send_couples_walkthrough(
    to_email: str,
    your_name: str,
    partner_name: str,
    pdf_bytes: bytes,
    filename: str = "Take139-Couples-Walkthrough.pdf",
) -> dict:
    """Email a couples Walkthrough PDF to one partner after they connect."""
    if not RESEND_API_KEY:
        return {"skipped": True, "reason": "no RESEND_API_KEY set"}

    your_first = (your_name or "").split()[0] or "friend"
    partner_first = (partner_name or "").split()[0] or "your partner"

    subject = f"Your Take 139 Couples Walkthrough — {your_first} & {partner_first}"

    html_body = f"""<!DOCTYPE html>
<html><body style="font-family:'Inter',sans-serif;color:#1d1d1b;
                    background:#f5f1e8;padding:40px 20px;line-height:1.6;">
<div style="max-width:560px;margin:0 auto;background:#f9f7f0;
            padding:40px 36px;border-radius:8px;">
    <p style="font-size:11px;letter-spacing:0.15em;text-transform:uppercase;
              color:#8a4a2c;margin:0 0 12px;">Take 139 · A Couples Walkthrough</p>
    <h1 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;
               margin:0 0 18px;color:#1d1d1b;">For {your_first} &amp; {partner_first}</h1>
    <p>Your couples Walkthrough is attached as a PDF.</p>
    <p>It's a counselor's read of your two wirings together &mdash; what each
    of you brings the other that you could not build alone, the small
    repeating collision your two profiles create, six commitments
    (three from each of you), a prayer for the marriage, and a six-round
    date-night conversation designed to be spoken across a table.</p>
    <p style="font-size:14px;color:#6b6862;">
        Sit with it together if you can. If not, read it separately and
        then sit down with it. Argue with what does not fit. Stay with what does.
    </p>
    <hr style="border:none;border-top:1px solid #d4c39a;margin:30px 0;">
    <p style="font-size:13px;color:#6b6862;">
        Reply to this email if you have any questions \u2014 a real person
        (a pastor) will read it.
    </p>
    <p style="font-size:12px;color:#6b6862;margin-top:24px;">
        Take 139 \u00b7 A counselor's framework for conflict origins
    </p>
</div>
</body></html>"""

    try:
        params = {
            "from": FROM_EMAIL,
            "to": [to_email],
            "subject": subject,
            "html": html_body,
            "reply_to": ADMIN_EMAIL,
            "attachments": [{
                "filename": filename,
                "content": base64.b64encode(pdf_bytes).decode("utf-8"),
            }],
        }
        return resend.Emails.send(params)
    except Exception as e:
        return {"error": str(e)}



def send_orphan_notification(
    to_email: str,
    to_name,
    former_partner_name: str,
    dashboard_url: str = "https://take139.com/dashboard.html",
) -> dict:
    """Notify a user that their former partner has re-paired with someone else.

    A short, pastoral note. No alarm. No extra prose. Says exactly what
    happened, where their own materials still live, and offers a quiet path
    to reach out if it lands hard.
    """
    if not RESEND_API_KEY:
        return {"skipped": True, "reason": "no RESEND_API_KEY set"}
    safe_email = (to_email or "").strip()
    if not safe_email:
        return {"skipped": True, "reason": "no recipient"}

    salutation = f"Hi {to_name}," if (to_name and str(to_name).strip()) else "Hi there,"
    former = (former_partner_name or "your former partner").strip() or "your former partner"

    subject = f"A note about your Take 139 pairing with {former}"

    css = (
        "body { font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; margin:0; padding:0; background:#faf6ef; color:#2a2620; }"
        ".container { max-width:560px; margin:0 auto; padding:40px 24px; }"
        ".brand { font-size:11px; letter-spacing:0.35em; color:#c8956c; text-transform:uppercase; font-weight:600; margin-bottom:14px; }"
        "h1 { font-family:Georgia,serif; font-size:24px; line-height:1.3; color:#2a2620; margin:0 0 16px 0; font-weight:400; }"
        "p { line-height:1.7; font-size:15px; color:#3a342d; margin:0 0 14px 0; }"
        ".cta-wrap { text-align:center; margin:26px 0; }"
        ".cta { display:inline-block; background:#2a2620; color:#faf6ef !important; padding:13px 26px; border-radius:4px; text-decoration:none; font-size:14px; letter-spacing:0.07em; font-weight:600; }"
        ".note { background:#fff; border-left:3px solid #c8956c; padding:14px 18px; margin:18px 0; font-size:14px; color:#3a342d; line-height:1.65; }"
        ".footer { margin-top:34px; padding-top:20px; border-top:1px solid #e0d6c5; font-size:12px; color:#8a7f72; line-height:1.6; }"
        ".footer .sig { margin-top:10px; color:#2a2620; font-weight:600; font-family:Georgia,serif; font-size:14px; }"
        "a { color:#c8956c; text-decoration:none; }"
        "a.cta:link, a.cta:visited { color:#faf6ef; }"
    )

    html_body = (
        '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>'
        + css
        + '</style></head><body>'
        + '<div class="container">'
        + '  <div class="brand">Take 139 &middot; A pastoral note</div>'
        + f'  <h1>{salutation}</h1>'
        + f'  <p>{former} has updated their Take 139 pairing and is now connected with a different partner. Because of that, the Couples Report the two of you generated together has been moved to the archive on your dashboard.</p>'
        + '  <div class="note"><strong>What this means for you:</strong> Your own profile, your full personal Walkthrough, and the original Couples Report are all still available in your dashboard. Nothing of yours has been deleted.</div>'
        + f'  <div class="cta-wrap"><a href="{dashboard_url}" class="cta">Open my dashboard &rarr;</a></div>'
        + '  <p style="font-size:13px;color:#6b6158;">If this update lands hard, please reach out &mdash; <a href="mailto:hello@take139.com">hello@take139.com</a>.</p>'
        + '  <div class="footer">'
        + '    Grace and peace,'
        + '    <div class="sig">&mdash; Dr. Chris Hilken</div>'
        + '    <div style="margin-top:14px;"><a href="https://take139.com">take139.com</a></div>'
        + '  </div>'
        + '</div></body></html>'
    )

    params = {
        "from": FROM_EMAIL,
        "to": [safe_email],
        "subject": subject,
        "html": html_body,
        "reply_to": ADMIN_EMAIL,
    }
    try:
        return resend.Emails.send(params)
    except Exception as e:
        return {"error": str(e)}


def send_partner_invitation(
    to_email: str,
    partner_name: str,
    buyer_name: str,
    access_code: str,
    relationship: str = "",
    frontend_url: str = "https://take139.com",
) -> dict:
    """Email a partner their own access code so they can take Take 139 alone.

    Called from /submit when the buyer of a Couple Package finishes their
    own assessment and supplied a partner_email + partner_gender at the
    finalize gate. The partner gets a short, warm note with their own
    pre-paid access code and a direct intake link.
    """
    if not RESEND_API_KEY:
        return {"skipped": True, "reason": "no RESEND_API_KEY set"}
    safe_email = (to_email or "").strip()
    if not safe_email:
        return {"skipped": True, "reason": "no recipient"}

    safe_buyer = (buyer_name or "your partner").strip() or "your partner"
    safe_partner = (partner_name or "").strip()
    salutation = f"Hi {safe_partner}," if safe_partner else "Hi there,"

    intake_link = (
        frontend_url.rstrip("/")
        + "/index.html?code=" + access_code
        + "&buyer=" + safe_email
    )

    css = (
        "body { font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; margin:0; padding:0; background:#faf6ef; color:#2a2620; }"
        ".container { max-width:560px; margin:0 auto; padding:40px 24px; }"
        ".brand { font-size:11px; letter-spacing:0.35em; color:#c8956c; text-transform:uppercase; font-weight:600; margin-bottom:14px; }"
        "h1 { font-family:Georgia,serif; font-size:24px; line-height:1.3; color:#2a2620; margin:0 0 16px 0; font-weight:400; }"
        "p { line-height:1.7; font-size:15px; color:#3a342d; margin:0 0 14px 0; }"
        ".cta-wrap { text-align:center; margin:26px 0; }"
        ".cta { display:inline-block; background:#2a2620; color:#faf6ef !important; padding:14px 28px; border-radius:4px; text-decoration:none; font-size:14px; letter-spacing:0.07em; font-weight:600; }"
        ".codebox { background:#fff; border:1px solid #e0d6c5; padding:14px 18px; margin:18px 0; font-family:'Courier New',monospace; font-size:18px; color:#2a2620; text-align:center; letter-spacing:0.08em; border-radius:4px; }"
        ".note { background:#fff; border-left:3px solid #c8956c; padding:14px 18px; margin:18px 0; font-size:14px; color:#3a342d; line-height:1.65; }"
        ".footer { margin-top:34px; padding-top:20px; border-top:1px solid #e0d6c5; font-size:12px; color:#8a7f72; line-height:1.6; }"
        ".footer .sig { margin-top:10px; color:#2a2620; font-weight:600; font-family:Georgia,serif; font-size:14px; }"
        "a { color:#c8956c; text-decoration:none; }"
        "a.cta:link, a.cta:visited { color:#faf6ef; }"
    )

    rel_phrase = ""
    if relationship:
        rel_map = {"married": "as their spouse", "engaged": "as their fiance(e)",
                   "dating": "in your relationship", "figuring_out": "in your relationship"}
        rel_phrase = " " + rel_map.get(relationship, "")

    subject = f"{safe_buyer} invited you to take Take 139 together"
    html_body = (
        '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>' + css
        + '</style></head><body><div class="container">'
        + '<div class="brand">Take 139 &middot; A pastoral invitation</div>'
        + f'<h1>{salutation}</h1>'
        + f'<p>{safe_buyer} just finished taking Take 139 \u2014 a fifteen-minute pastoral diagnostic written by a senior pastor with seminary training. It names the pattern underneath the conflict in a close relationship: trigger, core question, mechanism, breakdown.</p>'
        + f'<p>They\'ve invited you to take it too{rel_phrase}, so the two of you can read a Couples Walkthrough together once both of you are done. Your access code has already been paid for. Here it is:</p>'
        + f'<div class="codebox">{access_code}</div>'
        + '<div class="cta-wrap"><a href="' + intake_link + '" class="cta">Take Take 139 \u2192</a></div>'
        + '<div class="note"><strong>How it works:</strong> Take the assessment alone (it\'s about fifteen minutes). Your report will arrive by email when you\'re done. As soon as both of you have finished, the Couples Walkthrough is generated automatically and emailed to both of you.</div>'
        + '<p style="font-size:14px;color:#6b6158;">Take it privately. Be honest. The questions are designed to surface patterns you may not have words for yet \u2014 and the report is yours alone unless you choose to share it.</p>'
        + '<p style="font-size:13px;color:#8a7f72;">Questions? Reply to this email or write us at <a href="mailto:hello@take139.com">hello@take139.com</a>.</p>'
        + '<div class="footer">Grace and peace,'
        + '<div class="sig">&mdash; Dr. Chris Hilken</div>'
        + '<div style="margin-top:14px;"><a href="https://take139.com">take139.com</a></div>'
        + '</div></div></body></html>'
    )

    params = {
        "from": FROM_EMAIL,
        "to": [safe_email],
        "subject": subject,
        "html": html_body,
        "reply_to": ADMIN_EMAIL,
    }
    try:
        return resend.Emails.send(params)
    except Exception as e:
        return {"error": str(e)}


def send_his_her_couple_codes(
    his_name: str,
    his_email: str,
    his_code: str,
    her_name: str,
    her_email: str,
    her_code: str,
    relationship: str = "",
    frontend_url: str = "https://take139.com",
) -> dict:
    """Email each partner their own access code after a his_her_v1 Couple
    Package purchase. Sends two separate emails, each addressed by name,
    each containing only that partner's own code.

    Returns: {his_email_status: ..., her_email_status: ...}
    """
    out = {"his_email_status": None, "her_email_status": None}
    if not RESEND_API_KEY:
        out["error"] = "no RESEND_API_KEY set"
        return out

    css = (
        "body { font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; margin:0; padding:0; background:#faf6ef; color:#2a2620; }"
        ".container { max-width:560px; margin:0 auto; padding:40px 24px; }"
        ".brand { font-size:11px; letter-spacing:0.35em; color:#c8956c; text-transform:uppercase; font-weight:600; margin-bottom:14px; }"
        "h1 { font-family:Georgia,serif; font-size:24px; line-height:1.3; color:#2a2620; margin:0 0 16px 0; font-weight:400; }"
        "p { line-height:1.7; font-size:15px; color:#3a342d; margin:0 0 14px 0; }"
        ".cta-wrap { text-align:center; margin:26px 0; }"
        ".cta { display:inline-block; background:#2a2620; color:#faf6ef !important; padding:14px 28px; border-radius:4px; text-decoration:none; font-size:14px; letter-spacing:0.07em; font-weight:600; }"
        ".codebox { background:#fff; border:1px solid #e0d6c5; padding:14px 18px; margin:18px 0; font-family:'Courier New',monospace; font-size:20px; color:#2a2620; text-align:center; letter-spacing:0.08em; border-radius:4px; }"
        ".codelabel { font-size:11px; letter-spacing:0.3em; text-transform:uppercase; color:#8a7f72; text-align:center; margin-bottom:6px; }"
        ".note { background:#fff; border-left:3px solid #c8956c; padding:14px 18px; margin:18px 0; font-size:14px; color:#3a342d; line-height:1.65; }"
        ".footer { margin-top:34px; padding-top:20px; border-top:1px solid #e0d6c5; font-size:12px; color:#8a7f72; line-height:1.6; }"
        ".footer .sig { margin-top:10px; color:#2a2620; font-weight:600; font-family:Georgia,serif; font-size:14px; }"
        "a { color:#c8956c; text-decoration:none; }"
        "a.cta:link, a.cta:visited { color:#faf6ef; }"
    )

    def _build_html(my_name, my_code, intake_link):
        salutation = f"Hi {my_name}" if my_name else "Hi there"
        return (
            '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>' + css
            + '</style></head><body><div class="container">'
            + '<div class="brand">Take 139 &middot; Your access code</div>'
            + f'<h1>{salutation},</h1>'
            + '<p>Thank you for being part of Take 139. Your access code for the assessment is below.</p>'
            + f'<div class="codebox">{my_code}</div>'
            + f'<div class="cta-wrap"><a href="{intake_link}" class="cta">Take Take 139 &rarr;</a></div>'
            + '<p>The assessment takes about fifteen minutes. Take it alone, somewhere quiet. Your personal report arrives by email when you finish. Once both you and your partner have completed the assessment, the Couples Walkthrough is generated automatically and emailed to both of you.</p>'
            + '<p style="font-size:13px;color:#8a7f72;">Questions? Reply to this email or write us at <a href="mailto:hello@take139.com">hello@take139.com</a>.</p>'
            + '<div class="footer">Grace and peace,'
            + '<div class="sig">&mdash; Dr. Chris Hilken</div>'
            + '<div style="margin-top:14px;"><a href="https://take139.com">take139.com</a></div>'
            + '</div></div></body></html>'
        )

    subject = "Your Take 139 access code"

    # His email
    his_intake_link = frontend_url.rstrip("/") + "/index.html?code=" + his_code + "&buyer=" + his_email
    his_html = _build_html(my_name=his_name, my_code=his_code, intake_link=his_intake_link)
    try:
        out["his_email_status"] = resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [his_email],
            "subject": subject,
            "html": his_html,
            "reply_to": ADMIN_EMAIL,
        })
    except Exception as e:
        out["his_email_status"] = {"error": str(e)}

    # Her email
    her_intake_link = frontend_url.rstrip("/") + "/index.html?code=" + her_code + "&buyer=" + her_email
    her_html = _build_html(my_name=her_name, my_code=her_code, intake_link=her_intake_link)
    try:
        out["her_email_status"] = resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [her_email],
            "subject": subject,
            "html": her_html,
            "reply_to": ADMIN_EMAIL,
        })
    except Exception as e:
        out["her_email_status"] = {"error": str(e)}

    return out
