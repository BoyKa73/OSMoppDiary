# MoppDiaryOS Techstarter Edition

MoppDiaryOS ist eine moderne Tagebuch- und Organisations-App für Einzelpersonen. Sie kombiniert Kalender, Aufgabenverwaltung, Urlaubsplanung, Datei-Anhänge und motivierende Zitate in einer intuitiven Weboberfläche.

## Features

- **Benutzerverwaltung**: Registrierung, Login, Logout, Profilverwaltung, mehrere Profile möglich
- **Kalender & Aufgaben**: Einträge mit Titel, Zeitraum, Kategorie, Stimmung, Farbe, Beteiligte Personen
- **Urlaubsverwaltung**: Urlaubstage berechnen, buchen, Resturlaub anzeigen, Feiertage berücksichtigen
- **Datei-Uploads**: Anhänge zu Aufgaben (Bilder, PDFs, Office-Dokumente, uvm.)
- **Motivationszitate**: Zufällige Zitate auf der Startseite
- **Export & Drucken**: Suchergebnisse als PDF/CSV exportieren, selektierte Einträge drucken
- **Filter & Suche**: Nach Kategorie, Stimmung, Person, Datum, Datei oder Stichwort suchen
- **Counter & Events**: Persönliche Downcounter für wichtige Termine (z.B. Projekt, Geburtstag)
- **Dark/Light Mode**: Umschaltbar im Profil
- **Responsive Design**: Optimiert für Desktop und mobile Geräte

## Technischer Überblick

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login
- **Frontend**: Bootstrap 5, FullCalendar, jsPDF, Vanilla JS
- **Templates**: Jinja2 (index.html, search.html, dashboard.html, etc.)
- **Datenbank**: SQLite (diary.db), Modelle für User, Task, StaticEvent, Quote, Attachment
- **Datei-Uploads**: Speicherung im Ordner `instance/uploads/`
- **Migrationen**: Alembic für DB-Schema-Änderungen
- **Umgebung**: .env für geheimen Schlüssel (nicht verwechseln mit dem user profil passwort)

## Projektstruktur

```
├── app.py                # Haupt-Backend, Routing, Logik
├── models.py             # Datenbankmodelle
├── requirements.txt      # Python-Abhängigkeiten
├── templates/            # HTML-Templates
│   ├── index.html
│   ├── search.html
│   └── ...
├── static/               # Statische Dateien (CSS, JS, Bilder)
│   ├── style.css
│   ├── main.js
│   └── ...
├── instance/             # Ordner wird generiert wenn man installiert, wenn man die DB anlegt oder Dateianhänge erstellt
│   ├── diary.db          # SQLite-Datenbank
│   └── uploads/          # Datei-Uploads
├── migrations/           # Alembic-Migrationen
└── ...
```

## Installation & Setup

1. **Python-Umgebung vorbereiten**
   - Python 3.11+ installieren
   - Virtuelle Umgebung erstellen:
     ```bash
     python -m venv venv
     source venv/Scripts/activate # oder je nach OS: source venv/bin/activate
     ```
2. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```
3. **Datenbank initialisieren**
   ```bash
   flask db init
   flask db migrate -m "Initial migration, create empty database"
   flask db upgrade
   ```
4. **.env Datei anlegen**
   - Beispiel:
     ```env
     SECRET_KEY=dein-geheimer-schlüssel
     ```
5. **App starten**
   ```bash
   flask run
   ```
   - Standardmäßig unter http://127.0.0.1:5000 erreichbar

6. **Viel Spaß**
   Du hast jetzt den Quellcode offen, kannst ihn einsehen und verändern, deine eigene lokale DB, perfekt für dein Tagebuch!

7. **Techstarter Edition aktivieren**
   Termine rund um Techstarter und Feiertage:
   ```bash
   python seed_diary_techstarter.py
   ```

## Nutzung

- **Registrierung**: Über `/register` neuen Account anlegen
- **Login**: Über `/login` einloggen
- **Einträge erstellen**: Im Dashboard neue Aufgaben, Urlaube, Events anlegen
- **Dateien anhängen**: Beim Erstellen/Bearbeiten von Tasks
- **Suche & Filter**: Über die Suchfunktion gezielt Einträge finden
- **Export/Druck**: Selektierte Einträge als PDF/CSV exportieren oder drucken
- **Profil & Einstellungen**: Urlaubstage, Theme, Counter verwalten

## Wichtige Dateien

- `app.py`: Hauptlogik, Routing, API
- `models.py`: Datenbankmodelle (User, Task, StaticEvent, Quote, Attachment)
- `templates/index.html`: Startseite, Dashboard
- `templates/search.html`: Suchseite mit Export/Druck
- `static/main.js`: JS für Kalender, Export, Druck
- `requirements.txt`: Python-Abhängigkeiten

## Sicherheit & Hinweise

- Passwörter werden gehasht gespeichert (Werkzeug)
- Datei-Anhänge sind auf bestimmte Typen und Größe begrenzt (100 MB)
- Feiertage werden bei Urlaubsberechnung berücksichtigt
- Einträge mit Kategorie Urlaub werden korrekt berücksichtigt
- für pdf, csv, print bitte momentan über die Suche gehen, nicht über die orgabox
- StaticEvent oder all-day event genannt, sind fixe Termine die ganztägig sind, Task oder normaler Eintrag wird stundenweise angezeigt
- manches ist noch nicht implementiert aber es soll einen Blick auf die Zukunft geben oder zum Weiterentwickeln anregen

## Weiterentwicklung

- API-Endpunkte für externe Nutzung
- Mobile App (optional)
- Mehrsprachigkeit (DE/EN/FR)
- Erweiterte Exportformate

## Autoren & Danksagung

- Projektteam: Katja, Mirko, Najat
- Icons: [icon-icons.com](https://icon-icons.com/)
- Fonts: Google Fonts (Caveat)

---

Für Fragen, Feedback oder Beiträge: Bitte Issue im Repository eröffnen oder direkt Kontakt aufnehmen.

## Lizenz
MoppDiaryOS Custom License, siehe LICENSE.txt

## Weiteres über die App und den Sinn dahinter

Kalender und Erinnerer gibt es wie Sand am Meer. Tagebücher auch- in allen Formen und Farben.
Menschen, die terminlich eingespannt sind oder auf Ihre Ernährung achten möchten oder Ihre Sportbetätigung nachvollziehen können möchten, finden den Ein-oder Anderen Kalender- spzialisiert auf entweder "das Eine" (Sport oder Ernährung) oder das Andere: nur private Einträge oder Termine. Hier gibt es dank google schon sehr viele Lösungen und Möglichkeiten.

Diejenigen aber, die der Sache auf den Grund gehen möchten, ob dieser oder jener Termin, Arbeitsauftrag, Personengruppe, Ernährung  oder Aktivität mit der täglichen Stimmung oder Konstitution zu tun haben könnte und sich ein Raster übereinanderlegen wollen, die Suchen vergebens.

Diese App ist für deine  Protokollierung von  Gedankengängen, Situationen, Notizen zum Alltag, auf die man zurückgreifen möchte oder will und/oder muss.

Sie kann eine Unterstützung sein, wenn ein Stalking-Tagebuch angelegt werden muss, ein Mobbing-Tagebuch, 
ein Depressions-Tagebuch oder ein Stimmungstagebuch- um Muster zu erkennen oder sichtbar zu machen.

Im klinischen Alltag, bei Hausärzten, Fachärzten, Therapeuten und Beratern (egal welcher Couleur) herrscht überwiegend Zeitmangel. Kaum Zeit für den einzelnen Patienten.
Dabei ist das öffentliche Bild in der Gesellschaft von der Depression immernoch ein Tabu-Thema. Die Wenigstens wissen, dass dies die tödlichste Erkrankung ist- noch weit vor Krebs, dem Herzinfarkt oder Schlaganfall.
Da das klinische Bild sehr diffus ist, erhält die Beachtung dieses Themas immer noch nicht die Aufmerksamkeit, die es verdient. Leider oftmals auch nicht ersten Ansprechpartnern und bei Hausärzten, da die Symptomatik mehr als unklar und indifferent ist und es eben einfacher ist, hier einen Stimmungsaufheller zu verschreiben, dort eine Vitaminpille - und dann schaut man in 2 Wochen nochmal... Fehlende Datenerhebungsmöglichkeit, uneinheitliche Erfassungsmethoden und nicht-vorhandene Diagnostikmöglichkeiten für "auf-die-Schnelle" sind ein weiterer Baustein in der Kette.
Durch Zeitmangel nicht durchgängig oder auch unvollständig durchgeführte Amnamnestik kommt dann oft mit hinzu.

Diejenigen, die mit Depressionen zu kämpfen haben, werden von Ihrem Therapeuten/In zwecks Erhebungsbogen gefragt: Können Sie Zusammenhänge erkennen? Wann ging es Ihnen denn so oder so...? Wie lange hält diese Stimmung schon an? Was haben Sie getan, wodurch es Ihnen besser ging? An wen wenden Sie sich bei akuter Situation? 

Menschen die gestalkt werden und schutzsuchend bei der Polizei "anklopfen": Wann und um wieviel Uhr hat der/die TäterIn denn dieses oder jenes gemacht? Wann war das letztemal etwas? In welcher Form? Haben Sie Bilder? haben Sie Zeugen? Wenn ja: wen? Name?

Die Menschen, die sich Mobbing ausgesetzt sehen: Im Gespräch mit Betriebsräten/Beratern und Co ist die erste Frage: Haben Sie ein Mobbing-Tagebuch? Was war die Aktion? Wer hat wann was gesagt/getan/gesehen.....wer bekam es mit? Gibt es Nachweise?Mails? Anrufe? Wenn ja: wieviele? Mails?

Aus Stalking und Mobbing-Situationen heraus entwickelt sich nicht selten eine Depression.
Aus Erschöpfung heraus ist es den Meisten in diesen Phasen nicht möglich, strukturiert Notizen zu machen, Kalender anzulegen, Strategien zu entwickeln, zu reflektieren und all dies dann "einfach" zusammen zu sammeln oder Uhrzeiten aufzulisten oder vielleicht sortiert dar zu stellen, wenn eine Institution nachfragt ( Anwälte/Polizei/Ärzte/Therapeuten/Innen).

Mit dieser App soll diesen Menschen eine Möglichkeit gegeben werden, kurz -oder auch länger :-) -  und schnell eine Notiz, ein Foto oder Screenshots zu sammeln und im betreffenden (Datums-)Bereich zur entsprechenden Uhrzeit abzulegen. Diese Notizen liegen dann im Passwort-geschützten Bereich. 
Benötigt der Nutzer die Aufzeichnung, kann er/sie über Checkboxen die betreffenden Notizen sammeln und per PDF-Export auf einen Rechner downloaden oder dann als E-Mail-Anhang an Therapeuten/Ärzte/Polizei/Anwälte weiterleiten oder übergeben in ausgedruckter Form.
Gleichzeitig kann der Nutzer über das Tracken der Stimmung u.U. durch das übereinanderlegen der Raster für sich selbst schon ein Fazit ziehen. 
Beispielsweise: Die wöchentliche Aktivität "Wandern" tut mir nicht gut....(und Ähnliches)
Diese App soll gleichzeitig ein Baustein zum vereinfachten Amnamnese-Bogen/Beweissammler werden und eine möglichst schnellere Genesung (und Diagnostik!) und/oder Vorgehensweise ermöglichen.
Therapieansätze können daraus abgeleitete werden, sowie auch persönliche Resümmees. Wahrscheinlich auch nicht selten sicherlich eine erstaunliche Erkenntnis an Zusammenhängen.


Selbstverständlich können auch andere Stimmungen/Aktivitäten "getrackt" werden.
Die App kann ebenso als "normales" Tagebuch genutzt werden. Zum später drin schmökern,stöbern oder sich erinnern.
Oder simpel als Terminkalender mit Notiz-Funktion für Arbeit und Beruf. So dass ein transparentes Bild entsteht, welche Tage entzerrt werden können oder sollten- oder welche Aktivitäten vielleicht sogar ganz eingestellt werden sollten.


Grundsätzlich findest Du Hilfe hier:
https://www.deutsche-depressionshilfe.de/start
https://www.klicksafe.de/materialien/cyber-mobbing-leichte-hilfe-app
https://www.hilfetelefon.de/gewalt-gegen-frauen/stalking/