"""OAuth2 credential management for Google Calendar and Gmail APIs."""

import base64
import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

DEFAULT_TOKEN_PATH = os.getenv("GOOGLE_TOKEN_PATH", "token.json")
DEFAULT_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")


def get_credentials(
    token_path: str = DEFAULT_TOKEN_PATH,
    credentials_path: str = DEFAULT_CREDENTIALS_PATH,
) -> Credentials:
    """Load credentials from token.json or GOOGLE_TOKEN_JSON env var.

    Falls back to running the OAuth2 authorization flow if no valid token exists.
    """
    creds = _load_token(token_path)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _save_token(creds, token_path)
        return creds

    if creds and creds.valid:
        return creds

    creds = run_auth_flow(credentials_path)
    _save_token(creds, token_path)
    return creds


def run_auth_flow(credentials_path: str = DEFAULT_CREDENTIALS_PATH) -> Credentials:
    """Run interactive OAuth2 flow. Opens a browser for user authorization."""
    client_config = _load_client_config(credentials_path)
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    return flow.run_local_server(port=0)


def _load_token(token_path: str) -> Credentials | None:
    """Load token from file or GOOGLE_TOKEN_JSON env var."""
    raw_json = os.getenv("GOOGLE_TOKEN_JSON")
    if raw_json:
        try:
            token_data = json.loads(base64.b64decode(raw_json).decode())
            return Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception:
            return None

    if os.path.exists(token_path):
        return Credentials.from_authorized_user_file(token_path, SCOPES)

    return None


def _save_token(creds: Credentials, token_path: str) -> None:
    """Persist refreshed token to file (skipped in CI/GitHub Actions)."""
    if os.getenv("GOOGLE_TOKEN_JSON"):
        return
    with open(token_path, "w") as f:
        f.write(creds.to_json())


def _load_client_config(credentials_path: str) -> dict:
    """Load OAuth2 client config from file or GOOGLE_CREDENTIALS_JSON env var."""
    raw_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if raw_json:
        return json.loads(base64.b64decode(raw_json).decode())

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"File credenziali non trovato: {credentials_path}\n"
            "Scaricalo da Google Cloud Console → API & Services → Credentials.\n"
            "Oppure imposta la variabile GOOGLE_CREDENTIALS_JSON (base64)."
        )

    with open(credentials_path) as f:
        return json.load(f)


if __name__ == "__main__":
    print("Avvio flusso di autorizzazione OAuth2...")
    creds = run_auth_flow()
    _save_token(creds, DEFAULT_TOKEN_PATH)
    print(f"Token salvato in: {DEFAULT_TOKEN_PATH}")
    print(
        "\nPer GitHub Actions, esegui:\n"
        f"  base64 -i {DEFAULT_TOKEN_PATH} | tr -d '\\n'\n"
        "e salvalo come secret GOOGLE_TOKEN_JSON nel repository."
    )
