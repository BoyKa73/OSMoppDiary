"""
ACHTUNG: NUR EINMAL AUSFÜHREN!!!

Zentrales Seeding-Skript für alle Tabellen: User, Task, StaticEvent, Quote, Attachment
Führe dieses Skript im Flask-Shell-Kontext oder als separates Python-Skript aus.
"""
from models import db, User, Task, StaticEvent, Quote, Attachment
from datetime import datetime

# --- User Seeding ---
def seed_users():
    num_deleted = db.session.query(User).delete()
    db.session.commit()
    users = [
        User(
            username="Anna",
            password="scrypt:32768:8:1$AQcCYxp8OzdG9dyj$91c21e2286e8f4b00c71518eb1800af07daef9cf142b1dcebb98ae79526d45be2d558d5332f743dd539b8e4a4aee94a9e49361b6c6cbe04be570704ddf54b2a0",
            is_admin=False,
            postal_code="10115",
            selected_theme="light",
            total_vac_days=28,
            created_at=datetime.utcnow()
        )
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()
    print(f"{len(users)} User wurden hinzugefügt.")

# --- Task Seeding ---
def seed_tasks():
    seed_tasks = [
        Task(title="Spaziergang im Park", start_date=datetime(2025, 8, 1, 15, 0), end_date=datetime(2025, 8, 1, 16, 30), color="#4735e7", content="Spaziergang mit Anna im Park", people="Anna", created_at=datetime(2025, 8, 1, 15, 0), user_id=1, category="Alltag", mood="fröhlich"),
        Task(title="Streit mit Kollege", start_date=datetime(2025, 8, 1, 10, 0), end_date=datetime(2025, 8, 1, 11, 0), color="#e40c4f", content="Streit mit Max wegen Projekt", people="Max", created_at=datetime(2025, 8, 1, 10, 30), user_id=1, category="Konflikt", mood="wütend"),
        Task(title="Reflexion über Ziele", start_date=datetime(2025, 7, 31, 21, 0), end_date=datetime(2025, 7, 31, 22, 0), color="#cf0df0", content="Reflexion über persönliche Ziele", people="", created_at=datetime(2025, 7, 31, 21, 0), user_id=1, category="Reflexion", mood="neutral"),
        Task(title="Kaffee mit Lisa", start_date=datetime(2025, 7, 30, 9, 0), end_date=datetime(2025, 7, 30, 10, 0), color="#09b20f", content="Kaffee mit Lisa im Café", people="Lisa", created_at=datetime(2025, 7, 30, 9, 0), user_id=1, category="Zwischenmenschlich", mood="fröhlich"),
        Task(title="Allein zu Hause gefühlt", start_date=datetime(2025, 7, 29, 20, 0), end_date=datetime(2025, 7, 29, 21, 0), color="#e5c90c", content="Abends allein zu Hause", people="", created_at=datetime(2025, 7, 29, 20, 0), user_id=1, category="Alltag", mood="traurig"),
        Task(title="Feedbackgespräch Chef", start_date=datetime(2025, 7, 28, 14, 0), end_date=datetime(2025, 7, 28, 15, 0), color="#8a0730", content="Feedbackgespräch mit Chef", people="Chef", created_at=datetime(2025, 7, 28, 14, 0), user_id=1, category="Konflikt", mood="neutral"),
        Task(title="Tagebuch geschrieben", start_date=datetime(2025, 7, 27, 22, 0), end_date=datetime(2025, 7, 27, 22, 30), color="#95cfb5", content="Tagebuch geschrieben und reflektiert", people="", created_at=datetime(2025, 7, 27, 22, 0), user_id=1, category="Reflexion", mood="fröhlich"),
        Task(title="Einkaufen gewesen", start_date=datetime(2025, 7, 26, 17, 0), end_date=datetime(2025, 7, 26, 18, 0), color="#3df010", content="Einkaufen im Supermarkt", people="", created_at=datetime(2025, 7, 26, 17, 0), user_id=1, category="Alltag", mood="neutral"),
        # Neue Tasks für 9.8. bis 18.8.2025
        Task(title="Morgenspaziergang am Fluss", start_date=datetime(2025, 8, 9, 7, 30), end_date=datetime(2025, 8, 9, 8, 15), color="#3df010", content="Frische Luft und Ruhe genossen.", people="", created_at=datetime(2025, 8, 9, 7, 30), user_id=1, category="Alltag", mood="entspannt"),
        Task(title="Telefonat mit Mama", start_date=datetime(2025, 8, 9, 18, 0), end_date=datetime(2025, 8, 9, 18, 30), color="#e5c90c", content="Langes Gespräch über die Familie.", people="Mama", created_at=datetime(2025, 8, 9, 18, 0), user_id=1, category="Familie", mood="glücklich"),
        Task(title="Arzttermin", start_date=datetime(2025, 8, 10, 10, 0), end_date=datetime(2025, 8, 10, 10, 45), color="#e40c4f", content="Routineuntersuchung beim Hausarzt.", people="Dr. Weber", created_at=datetime(2025, 8, 10, 10, 0), user_id=1, category="Gesundheit", mood="neutral"),
        Task(title="Lesen im Garten", start_date=datetime(2025, 8, 10, 15, 0), end_date=datetime(2025, 8, 10, 16, 30), color="#cf0df0", content="Neues Buch angefangen: 'Der Alchimist'.", people="", created_at=datetime(2025, 8, 10, 15, 0), user_id=1, category="Freizeit", mood="zufrieden"),
        Task(title="Projektmeeting", start_date=datetime(2025, 8, 11, 9, 0), end_date=datetime(2025, 8, 11, 10, 30), color="#4735e7", content="Wichtige Entscheidungen getroffen.", people="Team", created_at=datetime(2025, 8, 11, 9, 0), user_id=1, category="Arbeit", mood="fokussiert"),
        Task(title="Kochen mit Freunden", start_date=datetime(2025, 8, 11, 19, 0), end_date=datetime(2025, 8, 11, 21, 0), color="#09b20f", content="Italienischer Abend mit Pasta.", people="Tom, Sarah", created_at=datetime(2025, 8, 11, 19, 0), user_id=1, category="Zwischenmenschlich", mood="fröhlich"),
        Task(title="Yoga-Session", start_date=datetime(2025, 8, 12, 6, 30), end_date=datetime(2025, 8, 12, 7, 15), color="#95cfb5", content="Entspannt in den Tag gestartet.", people="", created_at=datetime(2025, 8, 12, 6, 30), user_id=1, category="Gesundheit", mood="ausgeglichen"),
        Task(title="Einkaufen für Geburtstagsparty", start_date=datetime(2025, 8, 12, 17, 0), end_date=datetime(2025, 8, 12, 18, 30), color="#e5c90c", content="Deko und Getränke besorgt.", people="", created_at=datetime(2025, 8, 12, 17, 0), user_id=1, category="Alltag", mood="vorfreudig"),
        Task(title="Geburtstagsparty von Lisa", start_date=datetime(2025, 8, 13, 19, 0), end_date=datetime(2025, 8, 13, 23, 30), color="#e40c4f", content="Tolle Stimmung und viele Gespräche.", people="Lisa, Freunde", created_at=datetime(2025, 8, 13, 19, 0), user_id=1, category="Feier", mood="glücklich"),
        Task(title="Spaziergang im Wald", start_date=datetime(2025, 8, 14, 16, 0), end_date=datetime(2025, 8, 14, 17, 0), color="#3df010", content="Vögel beobachtet und frische Luft genossen.", people="", created_at=datetime(2025, 8, 14, 16, 0), user_id=1, category="Freizeit", mood="entspannt"),
        Task(title="Arbeiten an Tagebuch-App", start_date=datetime(2025, 8, 15, 14, 0), end_date=datetime(2025, 8, 15, 17, 0), color="#4735e7", content="Neue Features programmiert.", people="", created_at=datetime(2025, 8, 15, 14, 0), user_id=1, category="Arbeit", mood="produktiv"),
        Task(title="Filmabend", start_date=datetime(2025, 8, 15, 20, 0), end_date=datetime(2025, 8, 15, 22, 30), color="#cf0df0", content="'Inception' mit Freunden geschaut.", people="Freunde", created_at=datetime(2025, 8, 15, 20, 0), user_id=1, category="Freizeit", mood="begeistert"),
        Task(title="Reflexion: Ziele für den Herbst", start_date=datetime(2025, 8, 16, 21, 0), end_date=datetime(2025, 8, 16, 22, 0), color="#95cfb5", content="Pläne für die nächsten Monate gemacht.", people="", created_at=datetime(2025, 8, 16, 21, 0), user_id=1, category="Reflexion", mood="motiviert"),
        Task(title="Kaffee mit Max", start_date=datetime(2025, 8, 17, 10, 0), end_date=datetime(2025, 8, 17, 11, 0), color="#09b20f", content="Alte Zeiten besprochen.", people="Max", created_at=datetime(2025, 8, 17, 10, 0), user_id=1, category="Zwischenmenschlich", mood="nostalgisch"),
        Task(title="Familienausflug ins Museum", start_date=datetime(2025, 8, 18, 13, 0), end_date=datetime(2025, 8, 18, 16, 30), color="#e5c90c", content="Kunst und Geschichte erlebt.", people="Familie", created_at=datetime(2025, 8, 18, 13, 0), user_id=1, category="Familie", mood="begeistert"),
    ]
    db.session.bulk_save_objects(seed_tasks)
    db.session.commit()
    print(f"{len(seed_tasks)} Tasks wurden hinzugefügt.")

# --- StaticEvent Seeding ---
def seed_staticevents():
    events = [
        StaticEvent(title="🛠 Karriere-WorkShop 'LinkedIn'", start_date=datetime(2025, 7, 23, 9, 0), end_date=datetime(2025, 7, 23, 17, 0), color='#cf0df0', created_at=datetime(2025, 7, 1, 10, 0)),
        StaticEvent(title='🌴Techstarter-Frei', start_date=datetime(2025, 4, 17, 8, 0), end_date=datetime(2025, 4, 17, 18, 0), color='#e40c4f', created_at=datetime(2025, 4, 1, 9, 0)),
        StaticEvent(title='⚒ Tag der Arbeit-Feiertag', start_date=datetime(2025, 5, 1, 0, 0), end_date=datetime(2025, 5, 1, 23, 59), color='#e5c90c', created_at=datetime(2025, 4, 15, 8, 0)),
        StaticEvent(title='🛫Christi Himmelfahrt-Feiertag', start_date=datetime(2025, 5, 29, 0, 0), end_date=datetime(2025, 5, 29, 23, 59), color='#e5c90c', created_at=datetime(2025, 5, 1, 12, 0)),
        StaticEvent(title='🙏 Karfreitag', start_date=datetime(2025, 4, 18, 0, 0), end_date=datetime(2025, 4, 18, 23, 59), color='#e5c90c', created_at=datetime(2025, 3, 30, 14, 0)),
        StaticEvent(title='🙏 Ostern', start_date=datetime(2025, 4, 20, 0, 0), end_date=datetime(2025, 4, 22, 23, 59), color='#e5c90c', created_at=datetime(2025, 4, 5, 15, 0)),
        StaticEvent(title='🙏 Pfingsten', start_date=datetime(2025, 6, 8, 0, 0), end_date=datetime(2025, 6, 10, 23, 59), color='#e5c90c', created_at=datetime(2025, 5, 20, 16, 0)),
        StaticEvent(title='🌴 Sommer-Ferien', start_date=datetime(2025, 8, 11, 8, 0), end_date=datetime(2025, 8, 18, 18, 0), color='#e40c4f', created_at=datetime(2025, 7, 20, 17, 0)),
        StaticEvent(title='🛠 Projekt X für Präsi 18.08.2025', start_date=datetime(2025, 7, 30, 9, 0), end_date=datetime(2025, 8, 9, 17, 0), color='#09b20f', created_at=datetime(2025, 7, 10, 18, 0)),
        StaticEvent(title='🎓 ITCS Messe Köln 10-16:00 Uhr', start_date=datetime(2025, 9, 12, 10, 0), end_date=datetime(2025, 9, 12, 16, 0), color='#cf0df0', created_at=datetime(2025, 8, 15, 19, 0)),
        StaticEvent(title='🛠 AWS-Summit Hamburg', start_date=datetime(2025, 6, 5, 9, 0), end_date=datetime(2025, 6, 5, 17, 0), color='#cf0df0', created_at=datetime(2025, 5, 25, 20, 0)),
        StaticEvent(title='🌴 Feiertag Reformationstag', start_date=datetime(2025, 10, 31, 0, 0), end_date=datetime(2025, 10, 31, 23, 59), color='#e5c90c', created_at=datetime(2025, 10, 1, 21, 0)),
        StaticEvent(title='🌴 Feiertag Allerheiligen', start_date=datetime(2025, 11, 1, 0, 0), end_date=datetime(2025, 11, 1, 23, 59), color='#cf0df0', created_at=datetime(2025, 10, 10, 22, 0)),
        StaticEvent(title='🌴 Feiertag Tag d.Deutschen Einheit', start_date=datetime(2025, 10, 3, 0, 0), end_date=datetime(2025, 10, 3, 23, 59), color='#e5c90c', created_at=datetime(2025, 9, 20, 23, 0)),
        StaticEvent(title="🛠 Karriere-WorkShop 'New Work'", start_date=datetime(2025, 7, 15, 9, 0), end_date=datetime(2025, 7, 15, 17, 0), color='#95cfb5', created_at=datetime(2025, 6, 30, 8, 0)),
        StaticEvent(title="🛠 Karriere-WorkShop 'Marke ICH'", start_date=datetime(2025, 8, 6, 9, 0), end_date=datetime(2025, 8, 6, 17, 0), color='#95cfb5', created_at=datetime(2025, 7, 25, 9, 0)),
        StaticEvent(title='🎓Projekt-Vorstellung', start_date=datetime(2025, 8, 18, 10, 0), end_date=datetime(2025, 8, 18, 16, 0), color='#cf0df0', created_at=datetime(2025, 8, 1, 10, 0)),
        StaticEvent(title="🛠 Karriere-WorkShop 'Werte'", start_date=datetime(2025, 10, 8, 9, 0), end_date=datetime(2025, 10, 8, 17, 0), color='#95cfb5', created_at=datetime(2025, 9, 15, 11, 0)),
        StaticEvent(title="🛠 Karriere-WorkShop 'Anschreiben'", start_date=datetime(2025, 11, 12, 9, 0), end_date=datetime(2025, 11, 12, 17, 0), color='#95cfb5', created_at=datetime(2025, 10, 20, 12, 0)),
        StaticEvent(title="🛠 Karriere-WorkShop 'Bewerbungsgesprch& Gehaltsverhandlung'", start_date=datetime(2025, 12, 3, 9, 0), end_date=datetime(2025, 12, 3, 17, 0), color='#95cfb5', created_at=datetime(2025, 11, 10, 13, 0)),
        StaticEvent(title='🕯 1.Advent', start_date=datetime(2025, 11, 30, 0, 0), end_date=datetime(2025, 11, 30, 23, 59), color='#e5c90c', created_at=datetime(2025, 11, 1, 14, 0)),
        StaticEvent(title='🕯 2.Advent', start_date=datetime(2025, 12, 7, 0, 0), end_date=datetime(2025, 12, 7, 23, 59), color='#e5c90c', created_at=datetime(2025, 11, 15, 15, 0)),
        StaticEvent(title='🕯 3.Advent', start_date=datetime(2025, 12, 14, 0, 0), end_date=datetime(2025, 12, 14, 23, 59), color='#e5c90c', created_at=datetime(2025, 11, 22, 16, 0)),
        StaticEvent(title='🕯 4.Advent', start_date=datetime(2025, 12, 21, 0, 0), end_date=datetime(2025, 12, 21, 23, 59), color='#e5c90c', created_at=datetime(2025, 11, 29, 17, 0)),
        StaticEvent(title='🌉 Brückentag-Urlaub genommen', start_date=datetime(2025, 12, 22, 8, 0), end_date=datetime(2025, 12, 22, 18, 0), color='#8a0730', created_at=datetime(2025, 12, 1, 18, 0)),
        StaticEvent(title='⛸ Winter-Ferien', start_date=datetime(2025, 12, 23, 8, 0), end_date=datetime(2026, 1, 5, 18, 0), color='#e40c4f', created_at=datetime(2025, 12, 5, 19, 0)),
        StaticEvent(title='🎄 HeiligAbend', start_date=datetime(2025, 12, 24, 0, 0), end_date=datetime(2025, 12, 24, 23, 59), color='#e5c90c', created_at=datetime(2025, 12, 10, 20, 0)),
        StaticEvent(title='🎄 1.+2. WeihnachtsTag', start_date=datetime(2025, 12, 25, 0, 0), end_date=datetime(2025, 12, 26, 23, 59), color='#e5c90c', created_at=datetime(2025, 12, 15, 21, 0)),
        StaticEvent(title='🧨Silvester', start_date=datetime(2025, 12, 31, 0, 0), end_date=datetime(2025, 12, 31, 23, 59), color='#e5c90c', created_at=datetime(2025, 12, 20, 22, 0)),
        StaticEvent(title='✨Neujahr', start_date=datetime(2026, 1, 1, 0, 0), end_date=datetime(2026, 1, 1, 23, 59), color='#e5c90c', created_at=datetime(2025, 12, 25, 23, 0)),
        StaticEvent(title='🎓Abschluss 12-Monats-Kurs Techstarter', start_date=datetime(2026, 1, 20, 9, 0), end_date=datetime(2026, 1, 20, 17, 0), color='#cf0df0', created_at=datetime(2026, 1, 1, 8, 0)),
        StaticEvent(title="🛠 Abschluss-Projekt-Vorstellung 'ProjektX'", start_date=datetime(2026, 1, 12, 9, 0), end_date=datetime(2026, 1, 20, 17, 0), color='#95cfb5', created_at=datetime(2026, 1, 5, 9, 0)),
    ]
    db.session.bulk_save_objects(events)
    db.session.commit()
    print(f"{len(events)} StaticEvents wurden hinzugefügt.")

# --- Quote Seeding ---
def seed_quotes():
    quotes = [
        Quote(content='Der Weg ist das Ziel.', author='Konfuzius'),
        Quote(content='Carpe diem!', author='Horaz'),
        Quote(content='Das Leben ist zu kurz für später.', author='Unbekannt'),
        Quote(content='Wer kämpft, kann verlieren. Wer nicht kämpft, hat schon verloren.', author='Bertolt Brecht'),
        Quote(content='Phantasie ist wichtiger als Wissen.', author='Albert Einstein'),
        Quote(content='Achte auf deine Gefühle, denn sie werden zu Gedanken.', author='Unbekannt'),
        Quote(content='Alles besitzen zu wollen, geht selten damit einher, sich auch über die kleinen Dinge des Lebens zu freuen.', author='Unbekannt'),
        Quote(content='Am Abend wird man klug für den vergangenen Tag, doch niemals klug für den, der kommen mag.', author='Unbekannt'),
        Quote(content='Bewirft dich jemand mit Dreck, wirf mit Blumen zurück, aber vergiss die Vase dabei nicht.', author='Unbekannt'),
        Quote(content='Das Leben besteht nicht aus atmen, sondern aus den Menschen, die uns den Atem rauben.', author='Unbekannt'),
        Quote(content='Im Leben geht es nicht darum, gute Karten zu haben, sondern auch mit einem schlechten Blatt gut zu spielen.', author='Unbekannt'),
        Quote(content='Ich weiß nicht, ob es besser werden wird, wenn es anders werden wird, aber soviel ist gewiss, dass es anders werden muss, wenn es gut werden soll.', author='Unbekannt'),
        Quote(content='Ich lebe in einem Traum und habe keinerlei Interesse an der Realität.', author='Unbekannt'),
        Quote(content='Es sind die Augenblicke, die zählen – nicht die Dinge.', author='Unbekannt'),
        Quote(content='Ein Raum ohne Bücher ist wie ein Körper ohne Seele.', author='Unbekannt'),
        Quote(content='Ein erfülltes Leben ist wie eine Schatzsuche, wobei man hin und wieder auf kleine Kostbarkeiten und große Juwelen stößt.', author='Unbekannt'),
        Quote(content='Der Mensch allein ist unvollkommen. Er braucht einen zweiten, um glücklich zu sein.', author='Unbekannt'),
        Quote(content='Den Sinn des Lebens zu suchen ist legitim, doch sollte man damit nicht zu viel Zeit verbrauchen, sonst zieht das Leben an einem vorbei.', author='Unbekannt'),
        Quote(content='Wenn kein Pfad für dich der richtige scheint, gehe einen neuen und ebne ihn für andere nach dir.', author='Unbekannt'),
        Quote(content='Wahre Freundschaft hält ewig.', author='Unbekannt'),
        Quote(content='Stark sein bedeutet nicht, nie zu fallen, stark sein bedeutet immer wieder aufzustehen.', author='Unbekannt'),
        Quote(content='Phantasie ist das Auge der Seele.', author='Unbekannt'),
        Quote(content='Nimm es nicht zu schwer, dann wird auch alles leicht.', author='Unbekannt'),
        Quote(content='Mut ist nicht, keine Angst zu haben, sondern die eigene Angst zu überwinden.', author='Unbekannt'),
        Quote(content='Lebenskünstler ist, wer seinen Sommer so erlebt, dass er ihm noch den Winter wärmt.', author='Unbekannt'),
        Quote(content='Das Leben ist wie eine Pusteblume, wenn die Zeit gekommen ist, muss jeder für sich alleine fliegen.', author='Unbekannt'),
        Quote(content='Man spricht vergebens viel, um zu versagen. Der andere hört von allem nur das Nein.', author='Unbekannt'),
        Quote(content='Musik ist die schönste Kunst, einem Menschen zu sagen, was man wirklich für ihn empfindet.', author='Unbekannt'),
        Quote(content='Menschen, die niemals Zeit haben, tun wahrlich am wenigsten.', author='Unbekannt'),
        Quote(content='Du musst Wunder geschehen lassen, damit sie passieren.', author='Unbekannt'),
        Quote(content='Liebe ist ein Käfig mit Gitterstäben aus Glück.', author='Unbekannt'),
    ]
    db.session.bulk_save_objects(quotes)
    db.session.commit()
    print(f"{len(quotes)} Quotes wurden hinzugefügt.")

# --- Attachment Seeding ---
def seed_attachments():
    attachments = [
        Attachment(filename="bild1.jpg", task_id=1),
        Attachment(filename="notiz1.txt", task_id=2),
        Attachment(filename="dokument.pdf", task_id=3),
        Attachment(filename="foto2.png", task_id=4),
    ]
    db.session.bulk_save_objects(attachments)
    db.session.commit()
    print(f"{len(attachments)} Attachments wurden hinzugefügt.")

# --- Zentrale Seeding-Funktion ---
def seed_all():
    # Techstarter Edition


    # nur wenn man Testuser Anna ausprobieren will, ihr Passwort: 1234
    # seed_users() 

    # Testdaten für Anna, Vorsicht ggf user_id anpassen:
    # seed_tasks()

    # Feiertage und Techstarter Termine:
    seed_staticevents()

    # Zitate:
    seed_quotes()

    # braucht man nicht momentan: 
    # seed_attachments() braucht man nicht


    print("Alle Tabellen wurden erfolgreich geseedet.")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        seed_all()