"""Database models and setup for Take 139."""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Use persistent volume path on Railway, fallback to local for dev
DB_PATH = os.environ.get("DATABASE_PATH", "./take139.db")

# Ensure the parent directory exists (Railway volume mount may be empty at first)
_db_dir = os.path.dirname(DB_PATH)
if _db_dir and not os.path.exists(_db_dir):
    try:
        os.makedirs(_db_dir, exist_ok=True)
        print(f"[database] Created directory: {_db_dir}")
    except Exception as e:
        print(f"[database] Could not create {_db_dir}: {e}")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Submission(Base):
    """A completed assessment submission."""
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    pair_code = Column(String(32), unique=True, index=True, nullable=False)

    # Identity
    name = Column(String(200), nullable=True)
    email = Column(String(200), nullable=True, index=True)

    # Captured at intake. Stored canonically as 'M' | 'F' | 'X' (unspecified).
    # Used to gate which couples walkthrough variant we render (gendered
    # prose only when both genders match the writer's hardcoded assumption;
    # otherwise we fall through to the gender-neutral pair PDF).
    gender = Column(String(2), nullable=True, index=True)
    birthdate = Column(String(20), nullable=True)
    relationship_status = Column(String(40), nullable=True)

    # Access context — which code was used? tracks to counselor later
    access_code_used = Column(String(100), nullable=True, index=True)

    # Intake answers (JSON stored as text)
    intake_json = Column(Text, nullable=True)

    # All answers (JSON stored as text)
    answers_json = Column(Text, nullable=False)

    # Computed results
    results_json = Column(Text, nullable=False)

    # The primary profile identifiers for quick filtering
    primary_trigger = Column(String(50), nullable=True, index=True)
    primary_core_question = Column(String(100), nullable=True, index=True)
    primary_mechanism = Column(String(50), nullable=True, index=True)
    primary_breakdown = Column(String(50), nullable=True, index=True)

    # Couple linking — once paired to a partner
    paired_with_code = Column(String(32), nullable=True, index=True)
    paired_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    emailed_to_user = Column(Boolean, default=False)
    emailed_to_admin = Column(Boolean, default=False)

    # Soft-archive marker. When a user resets-and-retakes, the old submission
    # is marked archived (not deleted), and the access code is re-freed so
    # they can use it again. Dashboard / pair lookups filter on this.
    archived_at = Column(DateTime, nullable=True, index=True)
    archived_reason = Column(String(80), nullable=True)


class ImagoSubmission(Base):
    """A completed IMAGO assessment submission.

    Parallel to Submission (which is for Take 139). Lives in the same
    database so a single user can have both records linked by email
    or pair_code in the future.
    """
    __tablename__ = "imago_submissions"

    id = Column(Integer, primary_key=True, index=True)
    pair_code = Column(String(32), unique=True, index=True, nullable=False)

    # Identity
    name = Column(String(200), nullable=True)
    email = Column(String(200), nullable=True, index=True)

    # Access context
    access_code_used = Column(String(100), nullable=True, index=True)

    # All raw item answers (JSON: {item_id: 1-5})
    answers_json = Column(Text, nullable=False)

    # Computed result (JSON of ImagoResult.to_dict())
    results_json = Column(Text, nullable=False)

    # Quick-filter columns from results
    letter_type = Column(String(10), nullable=True, index=True)
    soul_shape = Column(String(50), nullable=True, index=True)
    archetype = Column(String(50), nullable=True, index=True)

    # Linkage to a Take 139 submission (if the same person took both)
    take139_pair_code = Column(String(32), nullable=True, index=True)

    # Couple linking (for future couple's report)
    paired_with_code = Column(String(32), nullable=True, index=True)
    paired_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    emailed_to_user = Column(Boolean, default=False)
    emailed_to_admin = Column(Boolean, default=False)


# ──────────────────────────────────────────────────────────────────────
# Access codes — for the paid launch (Take 139, Couples, Connection add-on)
# ──────────────────────────────────────────────────────────────────────

# Code kinds
CODE_KIND_SINGLE = "single"        # T139-XXXXX  — $20 single assessment
CODE_KIND_COUPLE = "couple"        # COUPLE-XXXXX-A/B — $40 couples package (issued in pairs)
CODE_KIND_CONNECT = "connect"      # CONNECT-XXXXX — $10 add-on to pair two existing submissions

# Code statuses
CODE_STATUS_ACTIVE = "active"      # generated, not yet used
CODE_STATUS_REDEEMED = "redeemed"  # used by a submission/pair
CODE_STATUS_EXPIRED = "expired"    # passed expires_at without use
CODE_STATUS_REVOKED = "revoked"    # manually killed by admin

# Code sources (how it was created)
CODE_SOURCE_ADMIN = "admin"        # hand-issued by Chris via /admin
CODE_SOURCE_STRIPE = "stripe"      # auto-issued by Stripe purchase
CODE_SOURCE_COMP = "comp"          # complimentary (church members, conference attendees, etc.)


class AccessCode(Base):
    """A purchasable / issuable access code.

    Three kinds:
    - single ($20): one Take 139 assessment + personal walkthrough
    - couple ($40): issued in pairs (one COUPLE-XXXXX-A, one COUPLE-XXXXX-B);
      each gives one assessment + personal walkthrough, and they auto-pair
      to produce the couples walkthrough
    - connect ($10): for two existing $20 buyers to bond their results
      into a couples walkthrough

    Once redeemed, a code's bond is locked. Re-pairing requires a new
    connect code.
    """
    __tablename__ = "access_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(64), unique=True, index=True, nullable=False)
    kind = Column(String(20), nullable=False, index=True)
    status = Column(String(20), nullable=False, default=CODE_STATUS_ACTIVE, index=True)
    source = Column(String(20), nullable=False, default=CODE_SOURCE_ADMIN, index=True)

    # Pricing context (for accounting, even on comp codes)
    price_cents = Column(Integer, nullable=True)  # 2000, 4000, 1000

    # Batch/admin context — so Chris can label e.g. "college-ave-spring-2026"
    batch_label = Column(String(100), nullable=True, index=True)
    notes = Column(Text, nullable=True)

    # For couple codes: links the A code to the B code (and vice versa)
    sibling_code = Column(String(64), nullable=True, index=True)

    # Stripe context — for paid codes
    stripe_session_id = Column(String(200), nullable=True, index=True)
    stripe_customer_email = Column(String(200), nullable=True, index=True)

    # Lifecycle
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=True, index=True)
    redeemed_at = Column(DateTime, nullable=True)
    redeemed_by_submission_pair_code = Column(String(32), nullable=True, index=True)
    redeemed_by_email = Column(String(200), nullable=True, index=True)


class CouplePair(Base):
    """A locked pairing between two submissions.

    Once two submissions are paired via /pair/connect, that bond is permanent
    for the purposes of the couples walkthrough. To re-pair with someone
    else, the user needs a fresh CONNECT code OR uses the free re-pair flow
    (POST /me/repair-with-new-partner) which archives this row and creates
    a new one.
    """
    __tablename__ = "couple_pairs"

    id = Column(Integer, primary_key=True, index=True)
    pair_code_a = Column(String(32), nullable=False, index=True)
    pair_code_b = Column(String(32), nullable=False, index=True)

    # Which access code authorised this pairing (could be a COUPLE-A code, a CONNECT code, etc.)
    authorised_by_code = Column(String(64), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Soft-delete: set when superseded by a re-pair. Active pairs have NULL.
    archived_at = Column(DateTime, nullable=True, index=True)
    archived_reason = Column(String(80), nullable=True)


class User(Base):
    """A signed-in account. Keyed by email (canonical, lowercased).

    A User row is created lazily:
    - When someone takes the assessment (auto-created in /submit)
    - When someone explicitly signs up via /auth/signup
    - When someone magic-links in for the first time with a fresh email

    Password is optional. Magic-link-only users have password_hash = None;
    they can sign in via magic-link forever, or set a password on the
    account-settings page.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=True)
    password_hash = Column(String(255), nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_signin_at = Column(DateTime, nullable=True)


class AuthToken(Base):
    """A single-use magic-link token sent by email.

    Tokens are short-lived (15 min default) and consumed on first valid
    verification. They are tied to an email and a purpose; we keep purpose
    flexible so we can reuse the table later for things like email-change
    confirmation, password reset, etc.
    """
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(200), index=True, nullable=False)
    purpose = Column(String(40), default="signin", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    consumed_at = Column(DateTime, nullable=True)
    requester_ip = Column(String(64), nullable=True)


class AuthSession(Base):
    """A signed-in session token. Stored in localStorage on the client,
    sent on each authenticated request as the X-Session-Token header.

    Sessions live for 30 days from issue and roll forward on each use
    (`last_seen_at`). We do not currently expire them server-side on a
    schedule — we simply check `expires_at` on every request.
    """
    __tablename__ = "auth_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(120), unique=True, index=True, nullable=False)
    email = Column(String(200), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    last_seen_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    requester_ip = Column(String(64), nullable=True)


class RepairHistory(Base):
    """A historical record of a re-pair event.

    Each time a signed-in user breaks their current Couples bond and
    re-pairs with someone new (via /me/repair-with-new-partner), we
    record one row here. This drives:
      - The 30-day cooldown between re-pairs (per user)
      - The lifetime cap of 5 free re-pairs (per user)
      - The 'past partners' history shown on the Couples Report
      - The orphan-notification audit trail
    """
    __tablename__ = "repair_history"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(200), index=True, nullable=False)
    user_pair_code = Column(String(32), index=True, nullable=False)
    old_partner_pair_code = Column(String(32), nullable=True, index=True)
    old_partner_email = Column(String(200), nullable=True)
    new_partner_pair_code = Column(String(32), nullable=False, index=True)
    new_partner_email = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    orphan_email_sent = Column(Boolean, default=False, nullable=False)
    orphan_email_sent_at = Column(DateTime, nullable=True)


def _safe_add_column(table: str, col_def: str) -> None:
    """Tiny SQLite migration helper — adds a column if it doesn't exist."""
    try:
        from sqlalchemy import text as _text
        with engine.begin() as conn:
            cols = conn.execute(_text(f"PRAGMA table_info({table})")).fetchall()
            existing = {row[1] for row in cols}
            new_col_name = col_def.split()[0]
            if new_col_name not in existing:
                conn.execute(_text(f"ALTER TABLE {table} ADD COLUMN {col_def}"))
                print(f"[migration] Added {table}.{new_col_name}")
    except Exception as _exc:
        print(f"[migration] Could not add {table} column: {_exc}")


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    # Soft migrations for existing prod DBs
    _safe_add_column("couple_pairs", "archived_at DATETIME")
    _safe_add_column("couple_pairs", "archived_reason VARCHAR(80)")
    _safe_add_column("submissions", "gender VARCHAR(2)")
    _safe_add_column("submissions", "birthdate VARCHAR(20)")
    _safe_add_column("submissions", "relationship_status VARCHAR(40)")
    _safe_add_column("submissions", "archived_at DATETIME")
    _safe_add_column("submissions", "archived_reason VARCHAR(80)")


def get_db():
    """Dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
