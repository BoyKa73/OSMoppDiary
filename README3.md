# MoppDiary – Flask Tagebuch App


## Projektbeschreibung
MoppDiary ist eine einfache Tagebuch-Webanwendung auf Basis von Flask und SQLite. Sie ermöglicht das Anlegen, Anzeigen, Bearbeiten und Löschen von Tagebucheinträgen. Die App ist als Lernprojekt für Python, Flask und Datenbankmigrationen gedacht.

## Features
- Einträge mit Datum, Titel und Text speichern
- Einträge anzeigen, bearbeiten und löschen (CRUD)
- Authentifizierung (Admin-Modus, geplant)
- Datenbankmigrationen mit Flask-Migrate (optional)
- Responsive Weboberfläche mit HTML/CSS (geplant)

## Installation
1. Repository klonen:
   ```bash
   git clone <repo-url>
   cd MoppDiary
   ```
2. Virtuelle Umgebung anlegen und aktivieren:
   ```bash
   python -m venv venv
   source venv/bin/activate  # oder venv\Scripts\activate auf Windows
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install flask flask_sqlalchemy flask_migrate
   ```

## Nutzung
1. App starten:
   ```bash
   python app.py
   ```
2. Im Browser öffnen: [http://localhost:5000](http://localhost:5000)

## Datenbankmigrationen (optional)
Falls Flask-Migrate genutzt wird:
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

## Projektstruktur
```
app.py           # Hauptanwendung
templates/       # HTML-Templates (geplant)
static/          # Statische Dateien (CSS/JS, geplant)
tagebuch.db      # SQLite-Datenbank
```

## Lizenz
MIT License

## Über die App und den Sinn dahinter

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










