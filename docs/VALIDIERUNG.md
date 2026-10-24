# Validierungsstand – 24. Oktober 2026

## Erfolgreich geprüft

- 17 automatisierte Tests mit `python3 -B -m unittest discover -s tests -v`.
- Python-Syntaxprüfung aller Anwendungsmodule.
- JavaScript-Syntaxprüfung mit dem Node-VM-Parser.
- HTTP-Auslieferung von HTML, CSS, JavaScript, Healthcheck und Konfiguration.
- HTTP-Berechnung des vollständigen synthetischen Beispiels.
- HTTP-Berechnung mit deaktiviertem Verbrauchsmodul: abhängige Kennzahlen blockiert, Entscheidung offen.
- Ungültige Eingabe liefert HTTP 400.
- Manueller Funktionsablauf in Safari über die native Bedienoberfläche: localhost öffnen, synthetisches Beispiel auswählen, Berechnung starten und Ergebnis im Accessibility-Baum prüfen.

Das Beispiel ergab 9,06 kW verbrauchsbasierte Heizlast, 7,2–10,8 kW flächenbasierte Heizlast, 1.071,09 €/a Energieersparnis und rund 11,2 Jahre einfache Amortisation. In der Benutzeroberfläche werden Werte lesbar gerundet. Das Ergebnis bleibt als vereinfachte Demonstrationsentscheidung gekennzeichnet.

## Grenzen der Prüfung

- Keine vollständige visuelle Layoutabnahme oder mobile Browserprüfung; der native Screenshotzugriff war nicht zuverlässig.
- Kein echter API-Aufruf ohne konfigurierten Anbieter und keine lokale MLX-Inferenz ohne installierte Modellumgebung. Extraktionsverhalten wurde mit kontrollierten Testantworten geprüft.
- Kein vollständiger Vergleich mit Original-CSV-/JSON-Daten, weil diese noch fehlen.
- PDF-Inhaltsanalyse, Außenaufstellungsanalyse und fachliche Interpretation von Freitext sind noch nicht implementiert.
- Keine Messung der Modelllaufzeit auf Zielhardware; die Drei-Minuten-Anforderung ist für echte multimodale Verarbeitung noch zu verifizieren.
