import os
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class TokenManager:
    """Klasa zarządzająca generowaniem i odświeżaniem tokena OAuth2."""
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    def __init__(self, credentials_file="credentials.json", token_file="token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file

    def get_authorization_url(self):
        """
        Generuje URL do autoryzacji.
        Użytkownik musi otworzyć URL w przeglądarce.
        :return: URL do logowania OAuth2.
        """
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.SCOPES,
            redirect_uri="urn:ietf:wg:oauth:2.0:oob"  # Specjalny redirect_uri dla aplikacji bez serwera
        )
        authorization_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )
        self.flow = flow
        return authorization_url

    def fetch_token(self, auth_code):
        """
        Pobiera token OAuth2 na podstawie kodu autoryzacyjnego.
        :param auth_code: Kod autoryzacyjny wklejony przez użytkownika.
        :return: Credentials (obiekt poświadczeń).
        """
        if not self.flow:
            raise RuntimeError("Najpierw wywołaj `get_authorization_url()`.")

        # Wymiana kodu autoryzacyjnego na token
        self.flow.fetch_token(code=auth_code)
        creds = self.flow.credentials

        # Zapisuje token do pliku
        with open(self.token_file, "w") as token_file:
            token_file.write(creds.to_json())
        print("Token został zapisany do pliku token.json.")

        return creds

    def get_token(self):
        """
        Sprawdza, czy istnieje ważny token. Jeśli nie, wymaga autoryzacji.
        :return: Credentials (obiekt poświadczeń).
        """
        creds = None

        # Jeśli istnieje plik z tokenem, próbuje go załadować
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        # Jeśli token nie istnieje lub jest nieważny, wymaga autoryzacji
        if not creds or not creds.valid:
            raise RuntimeError("Brak ważnego tokena. Użyj `get_authorization_url()` i `fetch_token()`.")

        return creds
