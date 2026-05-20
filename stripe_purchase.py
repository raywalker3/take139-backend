"""Stripe purchase flow — three products, webhook-driven code generation.

Three products:
    SINGLE   $20    Conflict Origins (Take 139)
    COUPLE   $40    Couple package (issues 2 codes: A + B)
    CONNECT  $10    Connection add-on (for 2 existing single-buyers)

Architecture:
    1. Frontend POSTs /purchase/checkout with {kind, email}
    2. Backend creates a Stripe Checkout Session with metadata {kind, email}
    3. Stripe handles payment UI
    4. On success, Stripe fires checkout.session.completed webhook
    5. /stripe/webhook verifies signature, generates code(s), emails buyer
    6. Stripe redirects user to FRONTEND_URL/?code=THE_CODE for instant access

Security:
    - Webhook MUST verify stripe-signature header against STRIPE_WEBHOOK_SECRET
    - The ?code= URL parameter is only a convenience; the code itself must
      exist in the codes table (which only the webhook can do).
"""
import os
from typing import Optional

import stripe
from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import CODE_KIND_SINGLE, CODE_KIND_COUPLE, CODE_KIND_CONNECT, CODE_SOURCE_STRIPE
import access_codes as ac

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://take139.com").rstrip("/")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


# Product catalog — single source of truth for pricing
PRODUCTS = {
    CODE_KIND_SINGLE: {
        "name": "Conflict Origins (Take 139)",
        "description": "One assessment + your personal Walkthrough PDF.",
        "price_cents": 2000,
    },
    CODE_KIND_COUPLE: {
        "name": "Couple Package",
        "description": "Two assessments (one for each spouse), two personal Walkthroughs, plus the Couples Walkthrough when you connect.",
        "price_cents": 4000,
    },
    CODE_KIND_CONNECT: {
        "name": "Connection Add-On",
        "description": "Already each took the assessment? Connect your two profiles into a Couples Walkthrough.",
        "price_cents": 1000,
    },
}


def is_configured() -> bool:
    """Has Stripe been set up with secret + webhook secret?"""
    return bool(STRIPE_SECRET_KEY) and bool(STRIPE_WEBHOOK_SECRET)


def create_checkout_session(
    kind: str,
    email: str,
    success_path: str = "/",
    cancel_path: str = "/",
) -> dict:
    """Create a Stripe Checkout Session for the chosen product.

    Returns: {"checkout_url": "...", "session_id": "..."}
    Raises HTTPException on any validation/Stripe error.
    """
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe is not configured on this server. Try again later.",
        )

    if kind not in PRODUCTS:
        raise HTTPException(status_code=400, detail=f"Unknown product kind: {kind}")

    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="A valid email is required.")

    product = PRODUCTS[kind]

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            customer_email=email,
            line_items=[{
                "quantity": 1,
                "price_data": {
                    "currency": "usd",
                    "unit_amount": product["price_cents"],
                    "product_data": {
                        "name": product["name"],
                        "description": product["description"],
                    },
                },
            }],
            metadata={
                "kind": kind,
                "buyer_email": email,
            },
            # We'll embed the placeholder {CHECKOUT_SESSION_ID} so the success
            # page can read it back. The actual code goes in the email + webhook
            # also fires regardless.
            success_url=f"{FRONTEND_URL}{success_path}?stripe_session={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}{cancel_path}?stripe_cancelled=1",
            # Reasonable expiry so abandoned sessions don't sit forever
            expires_at=None,  # default 24 hours
        )
        return {"checkout_url": session.url, "session_id": session.id}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=502, detail=f"Stripe error: {str(e)}")


def verify_webhook(payload_bytes: bytes, signature_header: str) -> dict:
    """Verify a Stripe webhook signature and return the parsed event.

    Raises HTTPException(400) on invalid signature.
    """
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Webhook secret not configured.",
        )
    try:
        event = stripe.Webhook.construct_event(
            payload_bytes, signature_header, STRIPE_WEBHOOK_SECRET
        )
        return event
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")


def handle_checkout_completed(db: Session, event: dict) -> dict:
    """Process a checkout.session.completed event.

    Generates the appropriate code(s) and returns:
        {"codes": [str, ...], "kind": "single|couple|connect", "email": "...", "session_id": "..."}

    Idempotent: if a code with this stripe_session_id already exists,
    return the existing codes (Stripe may deliver webhooks more than once).
    """
    session_data = event["data"]["object"]
    session_id = session_data["id"]
    metadata = session_data.get("metadata", {}) or {}
    kind = metadata.get("kind")
    email = metadata.get("buyer_email") or session_data.get("customer_email") or session_data.get("customer_details", {}).get("email")

    if not kind or kind not in PRODUCTS:
        return {"error": f"Missing or unknown kind in session metadata: {kind!r}", "session_id": session_id}

    if not email:
        return {"error": "Could not determine buyer email", "session_id": session_id}

    # Idempotency: if codes for this session already exist, return them
    from database import AccessCode
    existing = db.query(AccessCode).filter(
        AccessCode.stripe_session_id == session_id
    ).all()
    if existing:
        return {
            "codes": [c.code for c in existing],
            "kind": kind,
            "email": email,
            "session_id": session_id,
            "idempotent": True,
        }

    # Generate the right code(s)
    if kind == CODE_KIND_SINGLE:
        code = ac.create_single_code(
            db,
            source=CODE_SOURCE_STRIPE,
            price_cents=PRODUCTS[kind]["price_cents"],
            stripe_session_id=session_id,
            stripe_customer_email=email,
            notes=f"Stripe purchase by {email}",
        )
        codes = [code.code]
    elif kind == CODE_KIND_CONNECT:
        code = ac.create_connect_code(
            db,
            source=CODE_SOURCE_STRIPE,
            price_cents=PRODUCTS[kind]["price_cents"],
            stripe_session_id=session_id,
            stripe_customer_email=email,
            notes=f"Stripe connect-purchase by {email}",
        )
        codes = [code.code]
    elif kind == CODE_KIND_COUPLE:
        a, b = ac.create_couple_code_pair(
            db,
            source=CODE_SOURCE_STRIPE,
            stripe_session_id=session_id,
            stripe_customer_email=email,
            notes=f"Stripe couples purchase by {email}",
        )
        codes = [a.code, b.code]
    else:
        return {"error": f"Cannot generate code for kind: {kind}", "session_id": session_id}

    return {
        "codes": codes,
        "kind": kind,
        "email": email,
        "session_id": session_id,
        "idempotent": False,
    }
