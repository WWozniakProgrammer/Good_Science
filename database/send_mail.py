import os
import base64
import json
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class EmailSender:
    """Klasa odpowiedzialna za wysyłanie e-maili przy użyciu Gmail API."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    def __init__(self, token_json=None):
        self.token_json = token_json
        self.credentials = None
        self.service = None

    def load_credentials_from_json(self):
        """Ładuje istniejący token z JSON."""
        if not self.token_json:
            raise RuntimeError("Token JSON jest pusty. Wymagana jest autoryzacja.")

        self.credentials = Credentials.from_authorized_user_info(json.loads(self.token_json), self.SCOPES)
        if not self.credentials or not self.credentials.valid:
            raise RuntimeError("Token jest nieważny lub wygasł. Wymagana jest ponowna autoryzacja.")

        print("Token został załadowany poprawnie.")

    def authenticate(self):
        """Autoryzuje klienta Gmail API przy użyciu załadowanego tokena."""
        if not self.credentials:
            raise RuntimeError("Nie załadowano poświadczeń. Wywołaj najpierw `load_credentials_from_json()`.")

        self.service = build("gmail", "v1", credentials=self.credentials)

    def create_message(self, sender, recipient, subject, body):
        """Tworzy zakodowaną wiadomość MIME."""
        message = MIMEText(body)
        message["to"] = recipient
        message["from"] = sender
        message["subject"] = subject
        return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_email(self, sender, recipient, subject, body):
        """Wysyła wiadomość e-mail."""
        if not self.service:
            raise RuntimeError("Nieautoryzowany. Najpierw wywołaj `authenticate()`.")

        try:
            # Tworzy wiadomość
            message = self.create_message(sender, recipient, subject, body)

            # Wysyła wiadomość za pomocą Gmail API
            sent_message = self.service.users().messages().send(userId="me", body=message).execute()
            print(f"Wiadomość została wysłana: {sent_message['id']}")
            return sent_message

        except HttpError as error:
            print(f"Wystąpił błąd podczas wysyłania wiadomości: {error}")
            return None
