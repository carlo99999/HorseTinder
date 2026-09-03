"""Server-side authentication, session, and CSRF operations."""

import base64
import binascii
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import Settings
from app.db.migrations import make_engine
from app.db.models import Account, AccountSession

SESSION_COOKIE = "horse_tinder_session"
CSRF_HEADER = "x-csrf-token"


class AuthError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 401) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code


def utc_now() -> datetime:
    return datetime.now(UTC)


def _b64(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _sign(secret: str, value: str) -> str:
    return hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()


def _token_hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
    return f"pbkdf2_sha256$600000${_b64(salt)}${_b64(digest)}"


def password_matches(password: str, stored: str) -> bool:
    try:
        algorithm, iterations, salt, expected = stored.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), base64.urlsafe_b64decode(salt + "=="), int(iterations)
        )
        return hmac.compare_digest(_b64(actual), expected)
    except (TypeError, ValueError, binascii.Error):
        return False


def anonymous_csrf_token(settings: Settings) -> str:
    nonce = secrets.token_urlsafe(32)
    return f"{nonce}.{_sign(settings.app_secret, nonce)}"


def valid_anonymous_csrf(settings: Settings, token: str | None) -> bool:
    if not token or "." not in token:
        return False
    nonce, signature = token.rsplit(".", 1)
    return hmac.compare_digest(_sign(settings.app_secret, nonce), signature)


class AuthService:
    def __init__(self, settings: Settings, engine: Engine | None = None) -> None:
        self.settings = settings
        self.engine: Engine = engine or make_engine(settings.database_url)

    def register(self, email: str, password: str) -> tuple[Account, str, str]:
        normalized = email.strip().lower()
        if not normalized or "@" not in normalized or len(normalized) > 320:
            raise AuthError("validation_failed", "Please enter a valid email address.", 422)
        if len(password) < 12 or len(password) > 256:
            raise AuthError("validation_failed", "Password must contain 12 to 256 characters.", 422)
        with Session(self.engine) as db:
            if db.scalar(select(Account.id).where(Account.email == normalized)):
                raise AuthError("registration_failed", "We could not create that account.", 400)
            account = Account(email=normalized, password_hash=password_hash(password))
            db.add(account)
            db.flush()
            token, csrf = self._new_session(db, account.id)
            try:
                db.commit()
            except IntegrityError as exc:
                db.rollback()
                raise AuthError(
                    "registration_failed", "We could not create that account.", 400
                ) from exc
            return account, token, csrf

    def sign_in(self, email: str, password: str) -> tuple[Account, str, str]:
        with Session(self.engine) as db:
            account = db.scalar(select(Account).where(Account.email == email.strip().lower()))
            if account is None or not password_matches(password, account.password_hash):
                raise AuthError("authentication_failed", "Email or password is incorrect.")
            token, csrf = self._new_session(db, account.id)
            db.commit()
            return account, token, csrf

    def _new_session(self, db: Session, account_id: UUID) -> tuple[str, str]:
        token = secrets.token_urlsafe(48)
        csrf_secret = secrets.token_urlsafe(32)
        session = AccountSession(
            account_id=account_id,
            token_hash=_token_hash(token),
            csrf_secret=csrf_secret,
            expires_at=utc_now() + timedelta(seconds=self.settings.session_ttl_seconds),
        )
        db.add(session)
        return token, _sign(csrf_secret, token)

    def actor(self, token: str | None) -> tuple[AccountSession, Account]:
        if not token:
            raise AuthError("unauthorized", "Sign in is required.")
        with Session(self.engine) as db:
            result = db.execute(
                select(AccountSession, Account)
                .join(Account, Account.id == AccountSession.account_id)
                .where(AccountSession.token_hash == _token_hash(token))
            ).first()
            if result is None:
                raise AuthError("unauthorized", "Sign in is required.")
            session, account = result
            if (
                session.revoked_at is not None
                or session.expires_at.replace(tzinfo=UTC) <= utc_now()
            ):
                raise AuthError("unauthorized", "Your session has expired. Please sign in again.")
            db.expunge(session)
            db.expunge(account)
            return session, account

    def sign_out(self, token: str) -> None:
        with Session(self.engine) as db:
            session = db.scalar(
                select(AccountSession).where(AccountSession.token_hash == _token_hash(token))
            )
            if (
                session is None
                or session.revoked_at is not None
                or session.expires_at.replace(tzinfo=UTC) <= utc_now()
            ):
                raise AuthError("unauthorized", "Sign in is required.")
            session.revoked_at = utc_now()
            db.commit()


def valid_session_csrf(session: AccountSession, token: str, csrf: str | None) -> bool:
    return bool(csrf) and hmac.compare_digest(_sign(session.csrf_secret, token), csrf)
