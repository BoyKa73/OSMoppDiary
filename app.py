
#   Willkommen bei MoppDiaryOS – Techstarter Edition!
#
#   🚀 Entdecke, wie ein Tagebuch digital funktioniert.
#   👀 Tipp: Lies die Kommentare, sie verraten dir die Logik!
#   ✨ Challenge: Finde die Stelle, wo ein Eintrag gespeichert wird.
#   💡 Du kannst alles anpassen – probier es aus!
#   📚 Mehr Infos im README.md


# --- Imports und Setup ---
# Flask: Web-Framework, render_template für das serverseitige rendern von html templates
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory, abort, make_response
# SQLAlchemy: ORM für Datenbankzugriff
from flask_sqlalchemy import SQLAlchemy
# Datumsfunktionen
from datetime import datetime, timedelta, date, time
import pytz
from sqlalchemy import extract
# Datenbank-Objekt aus externer models.py
from models import db, Task, StaticEvent, Quote, User, Attachment
# Flask-Migrate: Migrationstool für DB-Schema
from flask_migrate import Migrate
# werden wir garantiert brauchen für die resp der Routen
from flask import json, jsonify
# SimpleNamespace: Für einfache Objekte, die nur Attribute haben-komplexe Obj.erstellung jetzt im Python-Code statt im Template
from types import SimpleNamespace
# Flask-Login: Für User-Management (Login, Logout, Session)
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
# für später, dass die Passwörter gehasht in der DB gespeichert werden
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
# für die Urlaubs-Berechnung ein feiertags-Cache
from functools import lru_cache
import random
import logging
from fpdf import FPDF
# --- .env laden ---
from dotenv import load_dotenv
import os
load_dotenv()


###############################################################
# Flask App & Konfiguration
#
# Hier wird die Flask-App erstellt und konfiguriert.
# Die Datenbank, Upload-Ordner und geheime Schlüssel werden festgelegt.
###############################################################
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'  # SQLite DB
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')  # Aus .env oder Fallback
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # max 100 MB Gesamtgröße der Anhänge bei einem Upload-Vorgang
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "png", "gif", "txt", "odf", "ods", "doc", "docx"}

###############################################################
# DB & Migration initialisieren
#
# Initialisiert die Datenbank und das Migrationstool (Alembic).
# Damit kannst du später das Datenbankschema ändern und migrieren.
###############################################################
db.init_app(app)
migrate = Migrate(app, db)

###############################################################
# Flask-Login initialisieren
#
# Ermöglicht Login, Logout und Session-Handling für User.
# Die Funktion load_user lädt den User aus der Datenbank anhand der Session-ID.
###############################################################
# Die Login-Route (login_user(user)) speichert nur die User-ID in der Session.
# Bei jedem neuen Request ruft Flask-Login automatisch load_user mit dieser ID auf, um das User-Objekt aus der Datenbank zu laden.
# So ist current_user immer korrekt gesetzt und du hast Zugriff auf alle User-Daten.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Rücksprung für nicht eingeloggte User
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

###############################################################
# Zufälligen Quote aus der DB holen
#
# Gibt ein zufälliges Zitat aus der Datenbank zurück.
# Wird z.B. im Dashboard angezeigt.
###############################################################
def get_daily_quote():
    # Hole alle Zitate aus der Datenbank
    quotes = Quote.query.all()
    if quotes:
        # Erzeuge einen stabilen Seed aus dem aktuellen Datum
        # Das Datum wird als String genommen, z.B. '2025-08-17'
        today_str = datetime.now().strftime('%Y-%m-%d')
        # Der Seed wird berechnet, indem die Unicode-Werte aller Zeichen des Datums aufsummiert werden
        # Dadurch ist der Seed für jeden Tag unterschiedlich, aber für alle Nutzer gleich
        seed = sum(ord(c) for c in today_str)
        # Setze den Zufallszahlengenerator auf diesen Seed
        # Das sorgt dafür, dass random.choice immer das gleiche Zitat für den Tag auswählt
        random.seed(seed)
        # Wähle ein zufälliges Zitat aus der Liste
        quote = random.choice(quotes)
        # Gib den Inhalt des Zitats zurück
        return quote.content
    else:
        # Falls keine Zitate vorhanden sind, gib einen Platzhaltertext zurück
        return "Kein Zitat gefunden."

###############################################################
# Dateiupload: nur bestimmte Dateitypen erlauben
###############################################################
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

###############################################################
# Feiertags-Cache Berechnung Deutschland
#
# Prüft, ob ein Datum ein Feiertag ist (bundesweit, teils manuell ergänzt).
###############################################################
@lru_cache(maxsize=None)
def is_holiday(date_obj):
    year = date_obj.year
    return date_obj.strftime('%Y-%m-%d') in GERMAN_HOLIDAYS.get(year, [])

###############################################################
# Arbeitstage definieren und Feiertage für mehrere Jahre
###############################################################
WORKING_DAYS = {0, 1, 2, 3, 4}  # Montag bis Freitag
# Deutsche Feiertage 2025 (bundesweit)
GERMAN_HOLIDAYS = {
    2025: [
        '2025-01-01',  # Neujahr
        '2025-04-18',  # Karfreitag
        '2025-04-21',  # Ostermontag
        '2025-05-01',  # Tag der Arbeit
        '2025-05-29',  # Christi Himmelfahrt
        '2025-06-09',  # Pfingstmontag
        '2025-10-03',  # Tag der Deutschen Einheit
        '2025-10-31',  # Reformationstag - manuell hinzugefügt wegen Techstarter Sitz HH
        '2025-11-01',  # Allerheiligen - manuell hinzugefügt; Feiertag NRW,BW,BY, RP, SL, HE
        '2025-12-25',  # 1. Weihnachtsfeiertag
        '2025-12-26'   # 2. Weihnachtsfeiertag
    ],
    2026: [
        '2026-01-01',  # Neujahr
        '2026-01-06',  # Heilige Drei Könige - manuell hinzugefügt; Feiertag BW, BY, ST
        '2026-04-06',  # Ostermontag
        '2026-05-14',  # Christi Himmelfahrt
        '2026-05-25',  # Pfingstmontag
        '2026-10-03',  # Tag der Deutschen Einheit
        '2026-12-25',  # 1. Weihnachtstag
        '2026-12-26'   # 2. Weihnachtstag
    ],
    2027: [
        '2027-01-01',  # Neujahr
        '2027-01-06',  # Heilige Drei Könige (BW, BY, ST)
        '2027-03-26',  # Karfreitag
        '2027-03-29',  # Ostermontag
        '2027-05-01',  # Tag der Arbeit
        '2027-05-06',  # Christi Himmelfahrt
        '2027-05-17',  # Pfingstmontag
        '2027-10-03',  # Tag der Deutschen Einheit
        '2027-10-31',  # Reformationstag (BB, MV, SN, ST, TH, HH)
        '2027-11-01',  # Allerheiligen (BW, BY, NW, RP, SL)
        '2027-12-25',  # 1. Weihnachtsfeiertag
        '2027-12-26'   # 2. Weihnachtsfeiertag
    ],
    2028: [
        '2028-01-01',  # Neujahr
        '2028-01-06',  # Heilige Drei Könige (BW, BY, ST)
        '2028-04-14',  # Karfreitag
        '2028-04-17',  # Ostermontag
        '2028-05-01',  # Tag der Arbeit
        '2028-05-25',  # Christi Himmelfahrt
        '2028-06-05',  # Pfingstmontag
        '2028-10-03',  # Tag der Deutschen Einheit
        '2028-10-31',  # Reformationstag (BB, MV, SN, ST, TH, HH)
        '2028-11-01',  # Allerheiligen (BW, BY, NW, RP, SL)
        '2028-12-25',  # 1. Weihnachtsfeiertag
        '2028-12-26'   # 2. Weihnachtsfeiertag
    ]

    }

###############################################################
# Hilfsfunktion: Arbeitstage zwischen zwei Daten berechnen
#
# Zählt alle Werktage (Mo-Fr), die keine Feiertage sind.
###############################################################
def calculate_workdays_between(start_date, end_date):
    """Berechnet Arbeitstage zwischen zwei Daten (ohne Wochenenden und Feiertage)"""
    workdays = 0
    current = start_date
    while current <= end_date:
        # Zähle nur Werktage, die keine Feiertage sind
        if current.weekday() < 5 and not is_holiday(current):
            workdays += 1
        current += timedelta(days=1)
    return workdays

###############################################################
# Registrierung eines neuen Users
#
# Zeigt das Registrierungsformular und legt bei POST einen neuen User an.
# Prüft, ob der Name schon existiert und ob die Felder ausgefüllt sind.
###############################################################
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        if not username or not password:
            flash("Bitte Benutzername und Passwort angeben.", "danger")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("Benutzername existiert bereits!", "danger")
            return render_template("register.html")
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registrierung erfolgreich! Bitte einloggen.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

###############################################################
# Login eines Users
#
# Zeigt das Login-Formular und prüft die Zugangsdaten.
# Bei Erfolg wird der User eingeloggt und zur Startseite weitergeleitet.
###############################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Login erfolgreich!", "success")
            return redirect(url_for("index"))
        else:
            flash("Der Zugang blieb verwehrt. Prüfe Benutzername und Passwort und versuche es erneut!", "danger")
    return render_template("login.html")

###############################################################
# Route: Benutzernamen ändern
#
# User kann seinen Namen ändern, wenn er noch nicht vergeben ist.
###############################################################
@app.route('/settings/change_username', methods=['POST'])
@login_required
def change_username():
    new_username = request.form.get('new_username', '').strip()
    if not new_username:
        flash('Bitte einen Benutzernamen eingeben!', 'danger')
        return redirect(url_for('profile'))
    # Prüfe, ob der Name schon vergeben ist
    if User.query.filter_by(username=new_username).first():
        flash('Benutzername existiert bereits!', 'danger')
        return redirect(url_for('profile'))
    current_user.username = new_username
    db.session.commit()
    flash('Benutzername erfolgreich geändert!', 'success')
    return redirect(url_for('profile'))
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")    

@app.route("/profile")
@login_required
def profile():
    from collections import Counter
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.start_date.asc()).all()
    task_count = len(tasks)
    # Statistiken berechnen
    categories = [t.category for t in tasks if t.category]
    moods = [t.mood for t in tasks if t.mood]
    cat_counter = Counter(categories)
    mood_counter = Counter(moods)
    max_category = cat_counter.most_common(1)[0][0] if cat_counter else "–"
    max_mood = mood_counter.most_common(1)[0][0] if mood_counter else "–"
    first_entry = tasks[0].start_date.date() if tasks else None
    last_entry = tasks[-1].start_date.date() if tasks else None
    # Streak berechnen (max. aufeinanderfolgende Tage mit Eintrag)
    streak = 0
    if tasks:
        dates = sorted(set(t.start_date.date() for t in tasks))
        max_streak = 1
        current_streak = 1
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        streak = max_streak
    # Tage seit Registrierung
    reg_days = (datetime.now().date() - current_user.created_at.date()).days if current_user.created_at else 0
    return render_template(
        "profile.html",
        user=current_user,
        task_count=task_count,
        tasks=tasks,
        max_category=max_category,
        max_mood=max_mood,
        first_entry=first_entry,
        last_entry=last_entry,
        reg_days=reg_days,
        streak=streak
    )

@app.route('/settings/update_profile', methods=['POST'])
@login_required
def update_profile_settings():
    # Allgemeine Profileinstellungen
    pass

###############################################################
# Route: Urlaub eintragen
#
# Berechnet die Arbeitstage im gewünschten Zeitraum und prüft, ob genug Urlaubstage übrig sind.
# Legt einen neuen Urlaubseintrag an.
###############################################################
@app.route('/add_vacation', methods=['POST'])
@login_required
def add_vacation():
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

    # Berechnung + Debug in einem Durchgang
    working_days = 0
    current = start_date
    debug_output = []
    
    while current <= end_date:
        is_weekday = current.weekday() < 5
        is_holiday_date = is_holiday(current)
        
        if is_weekday and not is_holiday_date:
            working_days += 1
            day_type = "Arbeitstag"
        else:
            day_type = "Wochenende" if not is_weekday else "Feiertag"
        
        debug_output.append(f"{current.strftime('%a %d.%m.%Y')}: {day_type}")
        current += timedelta(days=1)
    
    # Debug-Ausgabe
    print("\n=== Urlaubsberechnung ===")
    print(f"Zeitraum: {start_date} bis {end_date}")
    print("\n".join(debug_output))
    print(f"Berechnete Arbeitstage: {working_days}\n")

    # Prüfe verfügbare Urlaubstage
    used_days = calculate_used_vacation_days(current_user.id)
    remaining = (current_user.total_vac_days or 30) - used_days
    
    if working_days > remaining:
        flash(f'Nicht genug Urlaubstage übrig. Verfügbar: {remaining}, benötigt: {working_days}', 'error')
        return redirect(url_for('index'))
    
    # Erstelle neuen Urlaubstask
    vacation = Task(
        title=f'Urlaub ({working_days} Tage)',
        start_date=start_date,
        end_date=end_date,
        category='Urlaub',
        user_id=current_user.id
    )
    db.session.add(vacation)
    db.session.commit()
    
    flash(f'Urlaub über {working_days} Arbeitstage erfolgreich gebucht – Zeit für neue Abenteuer und Erholung!', 'success')
    return redirect(url_for('index'))
 
# --- Route zum Aktualisieren der Urlaubseinstellungen ---
@app.route('/settings/update_vacation', methods=['POST'])
@login_required
def update_vacation_settings():
    try:
        current_user.total_vac_days = request.form.get('total_vac_days', type=int)
        db.session.commit()
        flash('Urlaubskontingent aktualisiert', 'success')
    except ValueError:
        flash('Ungültige Eingabe für Urlaubstage', 'error')
    return redirect(url_for('index'))


###############################################################
# Hilfsfunktion: Genutzte Urlaubstage berechnen
#
# Zählt alle Urlaubstage des Users im aktuellen Jahr.
###############################################################
def calculate_used_vacation_days(user_id):
    """Berechnet die bereits verbrauchten Urlaubstage für den aktuellen Benutzer im laufenden Jahr"""
    current_year = datetime.now().year
    
    vacation_tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.category == 'Urlaub',
        extract('year', Task.start_date) == current_year
    ).all()
    
    used_days = 0
    for task in vacation_tasks:
        current_day = task.start_date
        end_day = task.end_date
        
        while current_day <= end_day:
            if current_day.weekday() < 5 and not is_holiday(current_day):
                used_days += 1
            current_day += timedelta(days=1)
            
    return used_days

# --- Route zum Berechnen der Arbeitstage im aktuellen Jahr ---
def calculate_working_days(year):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    total_days = (end_date - start_date).days + 1
    
    # Wochenenden berechnen
    weekends = sum(
        1 for single_date in (start_date + timedelta(days=n) for n in range(total_days))
        if single_date.weekday() >= 5
    )
    
    # Feiertage berechnen (nur Werktage)
    holidays = sum(
        1 for holiday in GERMAN_HOLIDAYS.get(year, [])
        if datetime.strptime(holiday, '%Y-%m-%d').weekday() < 5
    )
    
    # DEBUG-Ausgabe
    print(f"\nArbeitstage-Berechnung für {year}:")
    print(f"Kalendertage: {total_days}")
    print(f"Wochenenden: {weekends}")
    print(f"Feiertage: {holidays}")
    
    return {
        'total_days': total_days,
        'weekends': weekends,
        'holidays': holidays,
        'working_days': total_days - weekends - holidays
    }

# ---Route zum berechnen für Downcounter REALE ARBEITSTAGE bis zu einem Event, bzw Berechnung zw.zwei Daten---
def calculate_working_days_until(target_date):
    today = datetime.now().date()
    working_days = 0
    
    current_day = today
    while current_day <= target_date:
        if current_day.weekday() < 5 and not is_holiday(current_day):  # Montag-Freitag und kein Feiertag
            working_days += 1
        current_day += timedelta(days=1)
    
    return working_days

###############################################################
# Hauptseite: Einträge anzeigen und neue Einträge anlegen
#
# Zeigt alle Einträge des Users und berechnet Statistiken (Arbeitstage, Urlaub, Events).
# Bei POST wird ein neuer Eintrag oder Event angelegt.
# Anhänge werden verarbeitet und gespeichert.
###############################################################
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Wenn ein Formular abgeschickt wurde (POST):
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        all_day = request.form.get("all_day")
        content = request.form.get("content", "").strip()
        people = request.form.get("people", "").strip()
        category = request.form.get("category", "").strip()
        mood = request.form.get("mood", "").strip()
        color = request.form.get("color", "#4735e7").strip()
        start_date_str = request.form.get("start_date", "").strip()
        end_date_str = request.form.get("end_date", "").strip()
        start_time_str = request.form.get("start_time", "08:00").strip()
        end_time_str = request.form.get("end_time", "17:00").strip()
        if not title:
            return "⚠️ Das Titelfeld darf nicht leer sein."

        try:
            # Kombiniere Datum und Uhrzeit zu datetime
            if start_date_str and start_time_str:
                start_date = datetime.strptime(f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M")
            elif start_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            else:
                start_date = datetime.now()

            if end_date_str and end_time_str:
                end_date = datetime.strptime(f"{end_date_str} {end_time_str}", "%Y-%m-%d %H:%M")
            elif end_date_str:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            else:
                end_date = start_date
        except ValueError:
            return "❗ Ungültiges Start- oder Enddatum/Uhrzeit! Format: JJJJ-MM-TT und HH:MM"
        if all_day == "on":
            try:
                new_event = StaticEvent(
                    title=title,
                    start_date=start_date,
                    end_date=end_date,
                    color=color,
                    created_at=datetime.now()
                )
                db.session.add(new_event)
                db.session.commit()
                flash("Eintrag wurde gespeichert!", "success")
                return redirect("/")
            except Exception as e:
                db.session.rollback()
                print("Fehler beim Speichern des StaticEvents:", e)
                return "❗ Fehler beim Speichern des StaticEvents."
        else:
            try:
                new_task = Task(
                    title=title,
                    content=content,
                    people=people,
                    start_date=start_date,
                    end_date=end_date,
                    color=color,
                    user_id=current_user.id,
                    category=category,
                    mood=mood,
                    created_at=datetime.now()
                )
                db.session.add(new_task)
                db.session.flush()
                # Mehrere Anhänge verarbeiten
                uploaded_files = request.files.getlist("attachments")
                for file in uploaded_files:
                    if file and file.filename and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        task_folder = os.path.join(app.config["UPLOAD_FOLDER"], str(new_task.id))
                        try:
                            os.makedirs(task_folder, exist_ok=True)
                        except Exception as e:
                            print(f"Fehler beim Erstellen des Upload-Ordners: {e}")
                        file_path = os.path.join(task_folder, filename)
                        try:
                            file.save(file_path)
                        except Exception as e:
                            print(f"Fehler beim Speichern der Datei: {e}")
                        rel_path = f"{new_task.id}/{filename}"
                        attachment = Attachment(filename=rel_path, task_id=new_task.id)
                        db.session.add(attachment)
                db.session.commit()
                flash("Dein besonderer Tag wurde festgehalten – ein Lichtpunkt in deinem Kalender!", "success")
                return redirect("/")
            except Exception as e:
                db.session.rollback()
                print("Fehler beim Speichern:", e)
                return "❗ Fehler beim Speichern des Eintrags oder der Datei."

    # Hole die total_vac_days aus dem User-Profil (Standardwert 30 falls nicht gesetzt)
    current_year = datetime.now().year
    used_vac_days = calculate_used_vacation_days(current_user.id)
    total_vac_days = current_user.total_vac_days or 30

    # Berechne Arbeitstage und Feiertage für das aktuelle Jahr
    start_date = date(current_year, 1, 1)
    end_date = date(current_year, 12, 31)
    weekends = 0
    holidays = 0
    workdays_count = 0
    current_day = start_date
    while current_day <= end_date:
        is_weekday = current_day.weekday() < 5
        if is_weekday:
            if is_holiday(current_day):
                holidays += 1
            else:
                workdays_count += 1
        else:
            weekends += 1
        current_day += timedelta(days=1)
    total_days = (end_date - start_date).days + 1

    # Erstelle working_days dictionary mit allen benötigten Werten
    working_days = {
        'total_days': total_days,
        'weekends': weekends,
        'holidays': holidays,
        'working_days': workdays_count,
        'used_vac_days': used_vac_days,
        'remaining_working': workdays_count - used_vac_days,
        'remaining_vac_days': max(total_vac_days - used_vac_days, 0)
    }

    # Berechnung der Arbeitstage bis zu den Winterferien (22.12.2025)
    today = datetime.now().date()
    winter_ferien = date(2025, 12, 23)
    # Berechne Arbeitstage nach Abzug der Feiertage
    workdays_total = calculate_workdays_between(today, winter_ferien)
    # Urlaubstage im Zeitraum abziehen
    vacation_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.category == 'Urlaub',
        Task.end_date >= today,
        Task.start_date <= winter_ferien
    ).all()
    user_vacation_days = 0
    for task in vacation_tasks:
        task_start = task.start_date.date() if hasattr(task.start_date, 'date') else task.start_date
        task_end = task.end_date.date() if hasattr(task.end_date, 'date') else task.end_date
        vac_start = max(task_start, today)
        vac_end = min(task_end, winter_ferien)
        if vac_start > vac_end:
            continue
        current_day = vac_start
        while current_day <= vac_end:
            if current_day.weekday() < 5 and not is_holiday(current_day):
                user_vacation_days += 1
            current_day += timedelta(days=1)
    working_days_until_ferien = max(workdays_total - user_vacation_days, 0)
    working_days_until_ferien -= 1  # quickfix, da 23.12. mitgezählt wurde

    # Erstelle die next_events Liste
    next_events = [
        SimpleNamespace(id=44, title='NETTO ARB.TAGE BIS FERIEN', date='2025-12-23T00:00:00', working_days=working_days_until_ferien),
        SimpleNamespace(id=33, title='WEIHNACHTEN🌲', date='2025-12-24T18:00:00'),
        SimpleNamespace(id=17, title='ABSCHLUSS-PROJEKT', date='2026-01-20T10:30:00')
    ]

    all_counters = [
        {"id": "urlaub", "name": "Urlaub"},
        {"id": "geburtstag", "name": "Geburtstag"},
        {"id": "projekt", "name": "Projekt"},
        {"id": "schulung", "name": "Schulung"},
        {"id": "feiertag", "name": "Nächster Feiertag"}
    ]

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.start_date.desc()).all()

    return render_template("index.html", 
                        tasks=tasks, 
                        today=datetime.now().date(), 
                        working_days=working_days,
                        total_vac_days=total_vac_days,
                        used_vac_days=used_vac_days,
                        next_events=next_events,
                        all_counters=all_counters,
                        timedelta=timedelta,
                        is_holiday=is_holiday)


###############################################################
# Route: Kalender mit Events
#
# Gibt alle Events und Tasks als JSON für den Kalender aus.
###############################################################
@app.route("/events")
def get_events():
    events = []
    from datetime import timedelta
    # ➕ StaticEvents hinzufügen
    static_events = StaticEvent.query.all()
    for e in static_events:
        end_date_fc = e.end_date + timedelta(days=1)
        events.append({
            "id": f"static-event-{e.id}",
            "title": e.title,
            "start": e.start_date.isoformat(),
            "end": end_date_fc.isoformat(),
            "allDay": True,
            "color": e.color
        })
    # ➕ Nur Tasks des eingeloggten Users hinzufügen
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    for t in user_tasks:
        events.append({
            "id": f"task-{t.id}",
            "title": t.title or "🔹 Eintrag",
            "start": t.start_date.isoformat() if hasattr(t, "start_date") else None,
            "end": t.end_date.isoformat() if hasattr(t, "end_date") else None,
            "allDay": False,
            "color": t.color if hasattr(t, "color") else "#151269",
            "extendedProps": {
                "content": t.content,
                "category": t.category,
                "mood": t.mood,
                "created": t.created_at.strftime("%d.%m.%Y %H:%M") if hasattr(t, "created_at") and t.created_at else None,
                "attachments": [a.filename for a in t.attachments] if hasattr(t, "attachments") else []
            }
        })
    return jsonify(events)

###############################################################
# Route: Start/Ende von Events per Drag&Drop im Kalender ändern
#
# Aktualisiert die Datenbank, wenn ein Event im Kalender verschoben wird.
###############################################################
@app.route("/resize/<id>", methods=["POST"])
@login_required
def resize(id):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    obj = None
    obj_type = None
    logging.debug(f"resize: id={id}")
    if id.startswith("task-"):
        real_id = id[len("task-"):]
        obj = Task.query.filter_by(id=real_id).first()
        obj_type = 'task'
    elif id.startswith("static-event-"):
        real_id = id[len("static-event-"):]
        obj = StaticEvent.query.filter_by(id=real_id).first()
        obj_type = 'static_event'
    else:
        logging.error(f"Unbekannter Typ für id: {id}")
        abort(404)
    if not obj:
        logging.error(f"Kein Objekt gefunden für id: {id}")
        abort(404)
    # Zugriffsschutz: Nur Besitzer darf bearbeiten (nur für Tasks)
    if obj_type == 'task' and obj.user_id != current_user.id:
        logging.warning(f"Zugriffsverletzung: user_id={current_user.id} task_user_id={obj.user_id}")
        abort(403)
    if request.is_json:
        data = request.get_json()
        logging.debug(f"Empfangene JSON-Daten: {data}")
        start_raw = data.get("start_date")
        end_raw = data.get("end_date")
        logging.info(f"Empfangen: start_date={start_raw}, end_date={end_raw}")
        try:
            berlin = pytz.timezone('Europe/Berlin')
            def parse_utc_to_local(dt_str):
                if not dt_str:
                    return None
                dt_str = dt_str.replace('Z', '')
                dt_utc = datetime.fromisoformat(dt_str)
                dt_utc = dt_utc.replace(tzinfo=pytz.utc)
                return dt_utc.astimezone(berlin).replace(tzinfo=None)
            start_dt = parse_utc_to_local(start_raw)
            end_dt = parse_utc_to_local(end_raw)
            logging.info(f"Parsed (lokal): start_date={start_dt}, end_date={end_dt}")
            if start_dt:
                obj.start_date = start_dt
            if end_dt:
                # Für static-event: Enddatum um 1 Tag verkürzen (FullCalendar gibt +1 Tag zurück)
                if obj_type == 'static_event':
                    obj.end_date = end_dt - timedelta(days=1)
                else:
                    obj.end_date = end_dt
            db.session.commit()
            logging.info(f"Update erfolgreich: id={id} start_date={obj.start_date} end_date={obj.end_date}")
            return ("", 204)
        except Exception as e:
            db.session.rollback()
            logging.error(f"Fehler beim Update: {e}")
            return f"Fehler: {e}", 400
    logging.warning("Ungültiges Format (kein JSON)")
    return "Ungültiges Format", 400

###############################################################
# Route: Adventskalender anzeigen
###############################################################
@app.route('/adventskalender')
@login_required
def adventskalender():
    return render_template('adventskalender.html')

###############################################################
# Route: Passwort ändern
###############################################################
@app.route('/settings/change_password', methods=['POST'])
@login_required
def change_password():
    password = request.form.get('password', '').strip()
    if not password:
        flash('Bitte ein Passwort eingeben!', 'danger')
        return redirect(url_for('index'))
    current_user.password = generate_password_hash(password)
    db.session.commit()
    flash('Passwort erfolgreich geändert!', 'success')
    return redirect(url_for('index'))

###############################################################
# Route: Urlaubstage im Profil ändern
###############################################################
@app.route('/settings/profile', methods=['POST'])
@login_required
def update_profile():
    # Update Urlaubstage
    new_vac_days = request.form.get('total_vac_days', type=int)
    if new_vac_days:
        current_user.total_vac_days = new_vac_days
        db.session.commit()
        flash('Urlaubsdaten aktualisiert', 'success')
    return redirect(url_for('index'))

###############################################################
# Route: Dark Mode aktivieren/deaktivieren
#
# Speichert die Theme-Einstellung im User-Profil und als Cookie.
###############################################################
# Hier kann der User den Dark Mode aktivieren/deaktivieren
@app.route('/settings/style', methods=['POST'])
@login_required
def update_style():
    try:
        # Checkbox-Input auswerten
        dark_mode = request.form.get('dark_mode') == 'on'
        current_user.selected_theme = 'dark' if dark_mode else 'light'
        
        db.session.commit()

        # Ziel-URL bestimmen (Fallback: Dashboard)
        redirect_url = request.form.get('redirect_to', url_for('dashboard'))

        # HTTP-Response mit Cookie erstellen
        response = make_response(redirect(redirect_url))
        response.set_cookie(
            'theme',
            current_user.selected_theme,
            max_age=30 * 24 * 60 * 60,   # 30 Tage in Sekunden
            httponly=False,              # JS darf lesen (für Client-Switch)
            samesite='Lax'
        )
        return response

    except Exception as e:
        db.session.rollback()
        flash('Fehler beim Speichern der Einstellungen', 'error')
        return redirect(url_for('dashboard'))

###############################################################
# Route: Task oder Event bearbeiten
#
# Zeigt das Bearbeitungsformular und verarbeitet Änderungen inkl. Anhänge.
###############################################################
# Hiermit können User ihre Tasks bearbeiten, inklusive Anhänge
# für das Modal 
@app.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    obj = None
    obj_type = None
    if str(id).startswith("task-"):
        real_id = str(id)[len("task-"):]
        obj = Task.query.filter_by(id=real_id).first()
        obj_type = 'task'
    elif str(id).startswith("static-event-"):
        real_id = str(id)[len("static-event-"):]
        obj = StaticEvent.query.filter_by(id=real_id).first()
        obj_type = 'static_event'
    else:
        obj = Task.query.filter_by(id=id).first()
        obj_type = 'task' if obj else None
        if not obj:
            obj = StaticEvent.query.filter_by(id=id).first()
            obj_type = 'static_event' if obj else None
    if not obj:
        abort(404)
    # Zugriffsschutz: Nur Besitzer darf bearbeiten (nur für Tasks)
    if obj_type == 'task' and obj.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        if obj_type == 'task':
            obj.title = request.form["title"]
            obj.content = request.form["content"]
            obj.people = request.form["people"]
            obj.category = request.form["category"]
            obj.mood = request.form["mood"]
            obj.color = request.form.get("color", "#4735e7")
            start_date_str = request.form.get("start_date", "")
            end_date_str = request.form.get("end_date", "")
            try:
                if start_date_str:
                    obj.start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
                if end_date_str:
                    obj.end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                return "❌ Ungültiges Datum/Zeitformat! Bitte das Datum im Format JJJJ-MM-TT hh:mm eingeben."
            files = request.files.getlist("attachments")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    task_folder = os.path.join(app.config["UPLOAD_FOLDER"], str(obj.id))
                    os.makedirs(task_folder, exist_ok=True)
                    file_path = os.path.join(task_folder, filename)
                    file.save(file_path)
                    rel_path = f"{obj.id}/{filename}"
                    db.session.add(Attachment(filename=rel_path, task_id=obj.id))
            db.session.commit()
            return redirect("/")
        else:
            # StaticEvent bearbeiten (nur Datum/Uhrzeit)
            try:
                obj.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%dT%H:%M")
                obj.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%dT%H:%M")
            except ValueError:
                return "❌ Ungültiges Datum/Zeitformat!"
            db.session.commit()
            return redirect("/")
    return render_template("edit.html", task=obj)

###############################################################
# Erweiterte Edit-Route für Tasks und StaticEvents (Drag&Drop im Kalender)
###############################################################
@app.route("/edit_event/<id>", methods=["POST"])
@login_required
def edit_event(id):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    obj = None
    obj_type = None
    logging.debug(f"/edit_event/<id>: id={id}")
    if id.startswith("task-"):
        real_id = id[len("task-"):]
        obj = Task.query.filter_by(id=real_id).first()
        obj_type = 'task'
    elif id.startswith("static-event-"):
        real_id = id[len("static-event-"):]
        obj = StaticEvent.query.filter_by(id=real_id).first()
        obj_type = 'static_event'
    else:
        obj = Task.query.filter_by(id=id).first()
        obj_type = 'task' if obj else None
        if not obj:
            obj = StaticEvent.query.filter_by(id=id).first()
            obj_type = 'static_event' if obj else None
    if not obj:
        logging.error(f"Objekt nicht gefunden für id={id}")
        abort(404)
    # Zugriffsschutz: Nur Besitzer darf bearbeiten (nur für Tasks)
    if obj_type == 'task' and obj.user_id != current_user.id:
        logging.warning(f"Zugriffsverletzung: user_id={current_user.id} task_user_id={obj.user_id}")
        abort(403)

    if not request.method == "POST":
        logging.warning("/edit_event/<id> wurde ohne POST aufgerufen!")
        return "Nur POST erlaubt", 405

    # JSON-Daten (FullCalendar Drag&Drop)
    if request.is_json:
        data = request.get_json()
        logging.debug(f"Empfangene JSON-Daten: {data}")
        start_raw = data.get("start_date")
        end_raw = data.get("end_date")
        logging.info(f"Empfangen: start_date={start_raw}, end_date={end_raw}")
        try:
            berlin = pytz.timezone('Europe/Berlin')
            # FullCalendar liefert UTC, z.B. 2025-08-14T10:00:00.000Z
            def parse_utc_to_local(dt_str):
                if not dt_str:
                    return None
                # Entferne 'Z' falls vorhanden
                dt_str = dt_str.replace('Z', '')
                # Parse als naive UTC
                dt_utc = datetime.fromisoformat(dt_str)
                dt_utc = dt_utc.replace(tzinfo=pytz.utc)
                # In lokale Zeit umwandeln
                return dt_utc.astimezone(berlin).replace(tzinfo=None)
            start_dt = parse_utc_to_local(start_raw)
            end_dt = parse_utc_to_local(end_raw)
            logging.info(f"Parsed (lokal): start_date={start_dt}, end_date={end_dt}")
            if start_dt:
                obj.start_date = start_dt
            if end_dt:
                obj.end_date = end_dt
            db.session.commit()
            logging.info(f"Update erfolgreich: id={id} start_date={obj.start_date} end_date={obj.end_date}")
            return ("", 204)
        except Exception as e:
            db.session.rollback()
            logging.error(f"Fehler beim Update: {e}")
            return f"Fehler: {e}", 400
    # Fallback: Formulardaten (sollte im Normalfall nicht vorkommen)
    logging.warning("Kein JSON empfangen, prüfe Formulardaten...")
    start_raw = request.form.get("start_date")
    end_raw = request.form.get("end_date")
    logging.info(f"Empfangen (Form): start_date={start_raw}, end_date={end_raw}")
    try:
        start_dt = datetime.strptime(start_raw, "%Y-%m-%dT%H:%M") if start_raw else None
        end_dt = datetime.strptime(end_raw, "%Y-%m-%dT%H:%M") if end_raw else None
        logging.info(f"Parsed (Form): start_date={start_dt}, end_date={end_dt}")
        if start_dt:
            obj.start_date = start_dt
        if end_dt:
            obj.end_date = end_dt
        db.session.commit()
        logging.info(f"Update erfolgreich (Form): id={id} start_date={obj.start_date} end_date={obj.end_date}")
        return ("", 204)
    except Exception as e:
        db.session.rollback()
        logging.error(f"Fehler beim Update (Form): {e}")
        return f"Fehler: {e}", 400

###############################################################
# Route: Task oder Event löschen
#
# Löscht den Eintrag aus der Datenbank Tasks oder StaticEvents
###############################################################
@app.route('/delete/<id>', methods=['POST'])
@login_required
def delete_entry(id):
    entry = None
    obj_type = None
    if id.startswith("task-"):
        real_id = id[len("task-"):]
        entry = Task.query.filter_by(id=real_id).first()
        obj_type = 'task'
    elif id.startswith("static-event-"):
        real_id = id[len("static-event-"):]
        entry = StaticEvent.query.filter_by(id=real_id).first()
        obj_type = 'static_event'
    else:
        # Fallback: versuche als Task-ID
        entry = Task.query.filter_by(id=id).first()
        obj_type = 'task' if entry else None
        if not entry:
            entry = StaticEvent.query.filter_by(id=id).first()
            obj_type = 'static_event' if entry else None
    if not entry:
        abort(404)
    # Zugriffsschutz: Nur Besitzer darf Task löschen
    if obj_type == 'task' and entry.user_id != current_user.id:
        abort(403)
    # Wenn es sich um einen Task handelt, lösche alle zugehörigen Attachments von der Festplatte
    if obj_type == 'task':
        attachments = Attachment.query.filter_by(task_id=entry.id).all()
        for att in attachments:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], att.filename)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                # Falls Ordner leer, entferne Ordner (optional)
                folder = os.path.dirname(file_path)
                if os.path.isdir(folder) and not os.listdir(folder):
                    os.rmdir(folder)
            except Exception as e:
                print(f"Fehler beim Löschen des Anhangs: {e}")
            db.session.delete(att)
    # StaticEvents können von jedem gelöscht werden, kein Zugriffsschutz nötig
    db.session.delete(entry)
    db.session.commit()
    flash("Eintrag erfolgreich gelöscht.", "success")
    return redirect(url_for("index"))
        
###############################################################
# Route: Download von Anhängen
#
# Ermöglicht das Herunterladen von Anhängen, wenn der User berechtigt ist.
###############################################################
@app.route("/attachments/<int:task_id>/<path:filename>")
@login_required
def download_attachment(task_id, filename):
    # Prüfen, ob der Anhang existiert und zum User gehört
    attachment = Attachment.query.filter_by(filename=f"{task_id}/{filename}").first()
    if not attachment:
        abort(404)
    # Zugriffsschutz: Nur Besitzer darf herunterladen
    task = Task.query.get(attachment.task_id)
    if not task or task.user_id != current_user.id:
        abort(403)
    # Datei aus dem richtigen Unterordner bereitstellen
    directory = os.path.join(app.config["UPLOAD_FOLDER"], str(task_id))
    return send_from_directory(directory, filename, as_attachment=True)

###############################################################
# Route: Anhang löschen
#
# Löscht einen Anhang und entfernt ggf. den leeren Ordner.
###############################################################
@login_required
def delete_attachment(attachment_id):
    attachment = Attachment.query.get_or_404(attachment_id)
    # Zugriffsschutz: Nur Besitzer des Tasks darf Attachment löschen
    task = Task.query.get(attachment.task_id)
    if not task or task.user_id != current_user.id:
        abort(403)
    try:
        # Datei aus Unterordner löschen
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], attachment.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        # Falls Ordner leer, entferne Ordner (optional)
        folder = os.path.dirname(file_path)
        if os.path.isdir(folder) and not os.listdir(folder):
            os.rmdir(folder)
        db.session.delete(attachment)
        db.session.commit()
        flash("Anhang gelöscht – ein Blatt fällt aus deinem Tagebuch.", "success")
    except Exception as e:
        print("Fehler beim Löschen des Anhangs:", e)
        flash("Fehler beim Löschen des Anhangs", "danger")
    return redirect(request.referrer or "/")

@app.route("/dashboard")
@login_required
def dashboard():
    quote_of_the_day = get_daily_quote()
    next_events = (
        StaticEvent.query
        .filter(StaticEvent.start_date >= datetime.now().date())
        .order_by(StaticEvent.start_date.asc())
        .limit(3)
        .all()
    )
    return render_template("dashboard.html", quote_of_the_day=quote_of_the_day, next_events=next_events)

###############################################################
# Kontext-Processor: Zitat des Tages
#
# Macht das Zitat in allen Templates verfügbar.
###############################################################
# Damit das Zitat in allen Templates verfügbar ist, ohne es explizit zu übergeben
@app.context_processor
def inject_quote():
    return dict(quote_of_the_day=get_daily_quote())

@app.route("/search", methods=["GET"])
@login_required
def search():

    # Parameter auslesen
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    mood = request.args.get("mood", "")

    # Schritt 1: Nur Tasks des aktuellen Users
    user_tasks = Task.query.filter_by(user_id=current_user.id)

    # Schritt 2: Filter für Suchbegriff (im Titel, Inhalt, Personen, Start/Enddatum)
    suchfilter = db.or_(
        Task.title.ilike(f"%{query}%") if hasattr(Task, 'title') else False,
        Task.content.ilike(f"%{query}%"),
        Task.people.ilike(f"%{query}%") if hasattr(Task, 'people') else False,
        db.cast(Task.start_date, db.String).ilike(f"%{query}%") if hasattr(Task, 'start_date') else False,
        db.cast(Task.end_date, db.String).ilike(f"%{query}%") if hasattr(Task, 'end_date') else False
    )
    filtered_tasks = user_tasks.filter(suchfilter)

    # Kategorie-Filter anwenden, falls gesetzt
    if category:
        filtered_tasks = filtered_tasks.filter(Task.category == category)

    # Stimmung-Filter anwenden, falls gesetzt
    if mood:
        filtered_tasks = filtered_tasks.filter(Task.mood == mood)

    results = filtered_tasks.order_by(Task.start_date.desc() if hasattr(Task, 'start_date') else Task.id.desc()).all()

    # Schritt 3: Suche nach Attachments mit passendem Dateinamen
    attachment_results = Attachment.query.filter(Attachment.filename.ilike(f"%{query}%")).all()
    # Zu jedem Attachment den zugehörigen Task holen (nur wenn User Besitzer ist)
    attachment_tasks = []
    for att in attachment_results:
        task = Task.query.filter_by(id=att.task_id, user_id=current_user.id).first()
        # Filter auch auf Kategorie und Stimmung anwenden
        if task:
            if (not category or task.category == category) and (not mood or task.mood == mood):
                if task not in results:
                    attachment_tasks.append(task)

    # Kombiniere Tasks aus normaler Suche und aus Attachment-Suche
    combined_results = results + attachment_tasks
    # Duplikate entfernen (falls ein Task mehrfach vorkommt)
    unique_tasks = {t.id: t for t in combined_results}.values()
    return render_template("search.html", tasks=unique_tasks, query=query, category=category, mood=mood)


###############################################################
# App-Start
#
# Startet die Flask-App im Debug-Modus.
###############################################################
if __name__ == '__main__':
    app.run(debug=True)


