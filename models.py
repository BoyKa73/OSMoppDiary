# --- SQLAlchemy Setup ---
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Das db-Objekt wird hier initialisiert und in app.py importiert
db = SQLAlchemy()

# --- Datenbankmodelle ---
# Hier werden die Datenbankklassen definiert, die auf Tabellen gemappt werden.


# --- User-Modell ---
# Repräsentiert einen Benutzer (für Authentifizierung und Zuordnung von Tasks).
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jeden User
    username = db.Column(db.String(100), unique=True, nullable=False)  # Benutzername, muss eindeutig sein
    password = db.Column(db.String(200), nullable=False)  # Passwort (gehasht gespeichert)
    postal_code = db.Column(db.String(10), nullable=True)  # Postleitzahl des Users (optional)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)  # Gibt an, ob der User Adminrechte hat
    total_vac_days = db.Column(db.Integer, default=30)  # Urlaubstage pro Jahr
    selected_theme = db.Column(db.String(20), default="light")  # Gewähltes Theme, z.B. "dark" oder "light"
    # Beziehung: Ein User kann mehrere Tasks haben
    tasks = db.relationship("Task", backref="user", lazy=True)  # Liste aller Tasks des Users

# --- Task-Modell ---
# Repräsentiert eine Aufgabe oder ein Ereignis im Tagebuch.
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jeden Task
    title = db.Column(db.String(200), nullable=False)  # Titel des Tasks/Ereignisses
    start_date = db.Column(db.DateTime, nullable=False)  # Startdatum und Uhrzeit des Tasks/Ereignisses
    end_date = db.Column(db.DateTime, nullable=False)  # Enddatum und Uhrzeit des Tasks/Ereignisses
    color = db.Column(db.String(20), default="#4735e7")  # Farbe für Kalenderanzeige (wie StaticEvent)
    content = db.Column(db.String(1800), nullable=True)  # Beschreibung oder Notiz zum Task (optional)
    people = db.Column(db.String(100))  # Beteiligte Personen (optional)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))  # Erstellungszeitpunkt (UTC)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Verweis auf den User
    category = db.Column(db.String(50))  # Kategorie des Tasks (optional)
    mood = db.Column(db.String(20))  # Stimmung zum Task (optional)
    # Beziehung: Ein Task kann mehrere Attachments haben
    attachments = db.relationship('Attachment', back_populates='task', cascade='all, delete-orphan')  # Liste aller Anhänge


# --- StaticEvent-Modell ---
# Repräsentiert ein festes Ereignis (z.B. Ferien, Feiertage).
class StaticEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jedes StaticEvent
    title = db.Column(db.String(200), nullable=False)  # Titel des festen Ereignisses
    start_date = db.Column(db.DateTime, nullable=False)  # Startdatum und Uhrzeit des Ereignisses
    end_date = db.Column(db.DateTime, nullable=False)  # Enddatum und Uhrzeit des Ereignisses
    color = db.Column(db.String(20), default="#3df010")  # Farbe für Kalenderanzeige
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))  # Erstellungszeitpunkt (UTC)

# --- Quote-Modell ---
# Repräsentiert ein Zitat, das im Tagebuch angezeigt werden kann.
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jedes Zitat
    content = db.Column(db.String(500), nullable=False)  # Zitattext
    author = db.Column(db.String(100), nullable=True)    # Autor des Zitats (optional)


# --- Attachment-Modell ---
# Repräsentiert eine Datei, die an einen Task angehängt ist.
class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jeden Anhang
    filename = db.Column(db.String(255), nullable=False)  # Dateiname des Anhangs
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)  # Verweis auf den zugehörigen Task
    # Beziehung: Attachment gehört zu genau einem Task
    task = db.relationship('Task', back_populates='attachments')  # Der Task, zu dem der Anhang gehört

