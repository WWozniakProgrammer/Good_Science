import os
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class TokenManager:
    """Klasa zarządzająca generowaniem i odświeżaniem tokena OAuth2."""
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/userinfo.email",  # Dodany zakres do pobierania e-maila użytkownika
        "openid"  # Dodany zakres OpenID Connect
    ]

    def __init__(self, credentials_file="credentials.json", token_file="token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.flow = None

    def get_authorization_url(self):
        """
        Generuje URL do autoryzacji.
        Użytkownik musi otworzyć URL w przeglądarce.
        :return: URL do logowania OAuth2.
        """
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.SCOPES,
            redirect_uri="urn:ietf:wg:oauth:2.0:oob"
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

        # Jeśli token nie istnieje, jest nieważny lub nie ma wymaganych zakresów
        if not creds or not creds.valid or not creds.has_scopes(self.SCOPES):
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print("Błąd podczas odświeżania tokena:", str(e))
                    raise RuntimeError("Nie można odświeżyć tokena. Użyj `get_authorization_url()` i `fetch_token()`.")
            else:
                raise RuntimeError("Brak ważnego tokena lub brak wymaganych zakresów. Użyj `get_authorization_url()` i `fetch_token()`.")

        return creds


class EmailSender:
    """Klasa odpowiedzialna za wysyłanie e-maili przy użyciu Gmail API."""

    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.service = None

    def authenticate(self):
        """Autoryzuje klienta Gmail API przy użyciu tokena."""
        creds = self.token_manager.get_token()
        self.service = build("gmail", "v1", credentials=creds)

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


class CalendarManager:
    """Klasa odpowiedzialna za umawianie spotkań w kalendarzu Google użytkownika."""

    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.service = None
        self.user_email = None

    def authenticate(self):
        """Autoryzuje klienta Google Calendar API przy użyciu tokena i pobiera e-mail użytkownika."""
        creds = self.token_manager.get_token()
        self.service = build("calendar", "v3", credentials=creds)

        # Pobieranie adresu e-mail zalogowanego użytkownika
        user_info_service = build('oauth2', 'v2', credentials=creds)
        user_info = user_info_service.userinfo().get().execute()
        self.user_email = user_info.get('email')
        print(f"Zalogowany jako: {self.user_email}")

    def create_event(self, summary, description, start_time, end_time, attendees_emails):
        """
        Tworzy nowe wydarzenie w kalendarzu użytkownika.
        :param summary: Temat wydarzenia.
        :param description: Opis wydarzenia.
        :param start_time: Czas rozpoczęcia w formacie ISO.
        :param end_time: Czas zakończenia w formacie ISO.
        :param attendees_emails: Lista adresów e-mail zaproszonych użytkowników.
        :return: Utworzone wydarzenie.
        """
        if not self.service:
            raise RuntimeError("Nieautoryzowany. Najpierw wywołaj `authenticate()`.")

        # Dodanie informacji o organizatorze do tematu spotkania
        summary_with_organizer = f"{summary} (Organizator: {self.user_email})"

        event = {
            'summary': summary_with_organizer,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Europe/Warsaw',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Europe/Warsaw',
            },
            'attendees': [{'email': email} for email in attendees_emails],
            'organizer': {
                'email': self.user_email
            }
        }

        try:
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event,
                sendUpdates='all'
            ).execute()
            print(f"Utworzono wydarzenie: {created_event.get('htmlLink')}")
            return created_event
        except HttpError as error:
            print(f"Wystąpił błąd: {error}")
            return None


if __name__ == "__main__":
    # Tworzenie menedżera tokenów
    token_manager = TokenManager()

    # Sprawdzanie, czy istnieje token
    try:
        creds = token_manager.get_token()
        print("Użyto istniejącego tokena.")
    except RuntimeError as e:
        print(str(e))
        print("Rozpoczynam proces autoryzacji...")
        auth_url = token_manager.get_authorization_url()
        print(f"Otwórz ten URL w przeglądarce, aby się zalogować:\n{auth_url}")

        # Użytkownik wkleja kod autoryzacyjny
        auth_code = input("Wprowadź kod autoryzacyjny z przeglądarki: ")
        creds = token_manager.fetch_token(auth_code)

    # Tworzenie klienta wysyłania e-maili
    email_sender = EmailSender(token_manager)

    # Autoryzacja
    email_sender.authenticate()

    # Konfiguracja wiadomości e-mail
    nadawca_email = "goodscience682@gmail.com"
    odbiorca_email = ""
    temat_email = "Testowy e-mail z Gmail API - manualna autoryzacja"
    tresc_email = "To jest testowy e-mail wysłany przy użyciu Gmail API z manualną autoryzacją."

    # Wysyłanie wiadomości
    email_sender.send_email(nadawca_email, odbiorca_email, temat_email, tresc_email)

    # Tworzenie menedżera kalendarza
    calendar_manager = CalendarManager(token_manager)

    # Autoryzacja i pobranie e-maila użytkownika
    calendar_manager.authenticate()

    # Konfiguracja spotkania
    temat_spotkania = "Trolololo"
    opis_spotkania = "Omówienie postępów projektu i kolejnych kroków."
    czas_rozpoczecia = "2024-11-25T10:00:00+02:00"  # Upewnij się, że czas jest w przyszłości
    czas_zakonczenia = "2024-11-25T11:00:00+02:00"
    zaproszeni_uzytkownicy = [""]

    # Tworzenie wydarzenia
    calendar_manager.create_event(temat_spotkania, opis_spotkania, czas_rozpoczecia, czas_zakonczenia, zaproszeni_uzytkownicy)
