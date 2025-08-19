● Das "Works on my machine"-Problem: Welchen entscheidenden Vorteil bietet
dein Docker-Container im Vergleich dazu, wenn du einem Kollegen einfach nur
deinen Code-Ordner schicken würdest?

Ein Docker-Container löst dieses Problem, weil er die komplette Laufzeitumgebung (Betriebssystem, Abhängigkeiten, Konfiguration) kapselt. So läuft die App überall gleich – unabhängig von lokalen Installationen, Systemversionen oder Einstellungen. Ein Kollege muss nur Docker installieren und kann das Image direkt nutzen, ohne manuelle Einrichtung.

● Blaupause für die Infrastruktur: Erkläre in deinen eigenen Worten, warum das
Dockerfile als "Infrastructure as Code" bezeichnet werden kann.

Das Dockerfile beschreibt alle Schritte, um die Umgebung für die App bereitzustellen (Basis-Image, Installationen, Konfigurationen). Es ist wie ein Rezept, das immer wieder reproduzierbar ausgeführt werden kann. Deshalb nennt man es „Infrastructure as Code“: Die Infrastruktur wird als Code dokumentiert und ist versionierbar, überprüfbar und automatisierbar.

● Trennung von Code und Abhängigkeiten: Warum ist es (insbesondere bei
Node.js und Python) eine gute Praxis, die Abhängigkeiten (node_modules oder
virtuelle Umgebungen) nicht direkt in das Image zu kopieren, sondern sie durch
einen RUN-Befehl im Dockerfile installieren zu lassen?

Es ist gute Praxis, die Abhängigkeiten im Dockerfile per RUN-Befehl zu installieren, weil:

Das Image bleibt schlank und enthält nur die wirklich benötigten Pakete.
Lokale Abhängigkeiten könnten inkompatibel oder unvollständig sein.
Die Installation ist reproduzierbar und unabhängig von lokalen Installationspfaden.
So werden keine unnötigen Dateien (z.B. dev-Abhängigkeiten, Cache) ins Image kopiert.

● Ports: Was ist der Unterschied zwischen dem Port, den du mit EXPOSE im
Dockerfile angibst, und dem Port, den du im docker run -p Befehl verwendest?

EXPOSE im Dockerfile deklariert, auf welchem Port die Anwendung im Container lauscht. Es ist eine Dokumentation und hat keine direkte Auswirkung auf die Netzwerkkonfiguration.
Mit docker run -p <hostport>:<containerport> wird der Container-Port auf einen Port des Host-Rechners gemappt, sodass die App von außen erreichbar ist. EXPOSE ist optional, das Mapping im Run-Befehl ist entscheidend für die Erreichbarkeit.
