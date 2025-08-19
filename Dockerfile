# Dockerfile für MoppDiaryOS
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# requirements.txt kopieren und Abhängigkeiten installieren
COPY requirements.txt .
# Die Option --no-cache-dir bei pip install sorgt dafür, dass Pip keine Installationsdateien im Cache speichert. 
# Das spart Speicherplatz im Docker-Image
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY . .


# Umgebungsvariablen für Flask setzen
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Port freigeben
EXPOSE 5000

# Datenbank initialisieren und seeden
RUN flask db upgrade && python seed_diary_techstarter.py

# Startbefehl
CMD ["flask", "run"]
