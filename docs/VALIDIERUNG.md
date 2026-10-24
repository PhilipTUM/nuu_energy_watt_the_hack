# Validierungsstand – 24. Oktober 2026

Aktueller Stand: CSV-only-Eingaben gemäß Nutzerauftrag, TABULA-Vergleichsspannen und Technical Guardrails aus der lokalen Notion-Projektbeschreibung.

## Durchgeführte Prüfungen

- **24 automatisierte Tests** erfolgreich: exaktes Eingabeschema, Ablehnung zusätzlicher Variablen und Referenzlabels, CSV-Leerwerte/yes-no, Verbrauchs-/Warmwasserbilanz, feste Preis-/JAZ-Werte und Temperaturgrenzen, LPG-Abgrenzung, keine doppelte Ölkonversion, Modulabhängigkeiten, Datenunveränderlichkeit, Typologien und Flächenumrechnung, Szenariospannen, Beleglage und Fachprüfungen.
- Original-Evaluierungsheader beim Datenimport gegen `UserInput` abgeglichen: exakt 16 Spalten. Formular enthält dieselben 16 benannten Eingaben.
- 150 deutsche TABULA-Varianten beim Import auf widersprüchliche Dubletten geprüft. `h_Transmission` für alle Varianten mit der Summe der ursprünglichen Bauteil-/Wärmebrückenkoeffizienten dividiert durch `A_C_Ref` abgeglichen.
- Repräsentative TABULA-Quellzeile 712 mit Fläche und Kennwerten im Test fixiert. Skalierung der Vergleichswerte mit Fläche geprüft.
- JavaScript-Syntaxprüfung mit Node erfolgreich; `git diff --check` ohne Whitespacefehler.
- HTTP 200 für HTML, CSS, JavaScript, Healthcheck und Konfiguration. Alle fünf echten CSV-Fälle über `/api/assessments` erfolgreich berechnet.
- Nicht erlaubte Eingabe `investment_eur` über HTTP geprüft: **400** statt stiller Annahme eines zusätzlichen Eingabefelds.
- B-04 und B-05 im Browser ausgewählt und berechnet. Sichtbare Eingaben, fehlende Temperaturen, technische Ampel, Heizlast, Kosten und offene Angaben über den Accessibility-Baum geprüft. Desktop-Ergebnisansicht von B-05 zusätzlich visuell kontrolliert.
- Die lokalen Normseiten zur Monatswärmekapazität / Ausnutzungsgrad und zum deutschen Bezugsparameter wurden visuell geprüft. Wegen des eingeschränkten Eingabeschemas wird keine individuelle Monatsbilanz gerechnet.

## Ergebnisse der tatsächlichen CSV-Fälle

| Gebäude | Heizlast aus Verbrauch | Energiekosten heute | JAZ | Technik |
|---|---:|---:|---|---|
| B-01 | 2,40 kW | offen, LPG-Tarif fehlt | offen | Gelb |
| B-02 | 5,32 kW | 1.705 €/a | 4,0 | Gelb |
| B-03 | 16,60 kW | 6.800 €/a | offen | Gelb |
| B-04 | 9,50 kW | 4.250 €/a | offen | Gelb |
| B-05 | 10,38 kW | 2.970 €/a | offen | Gelb |

Gelb ist kein Ungeeignetheitsnachweis. Bei B-04 ist das Einrohrsystem dokumentiert; B-05 hat ein unbekanntes Rohrsystem, keine Temperaturangabe und Solarthermie. B-02 hat unbekanntes Rohrsystem und zusätzliche Wärmequellen. Die konservative Belegregel wird nicht auf die grünen Entwicklungsreferenzen zurechtgebogen. Alle Referenzwerte bleiben aus den Eingaben ausgeschlossen.

Für B-04 ergibt die breite flächenbasierte Methode 6,4–28,8 kW, da Sanierung unbekannt ist. B-05 ergibt 5,0–7,5 kW aus Fläche und 5,0–10,38 kW als gemeinsame Methodenspanne. Diese Spannen sind keine statistischen Unsicherheiten.

Das synthetische CSV-Beispiel bleibt numerisch bei 9,06 kW Verbrauchsheizlast und ungefähr 1.071,09 €/a Ersparnis. Die frühere Demo-Amortisation entfällt: Investitionskosten, Förderung und Betrachtungszeitraum sind keine zugelassenen Eingaben mehr.

## Grenzen der Prüfung

- Keine vollständige Normvalidierung, Gebäude-Monatsbilanz oder raumweise Heizkörperdimensionierung. Dafür fehlen erforderliche Eingaben.
- Keine behauptete Kalibrierung oder Übereinstimmung mit zurückgehaltenen Evaluierungsreferenzen.
- Keine Witterungsbereinigung, keine Ertragsrekonstruktion für Holzofen/Solarthermie und keine aus der PLZ erfundene Außentemperatur.
- Keine mobile Layoutabnahme; Desktop-Formular und Ergebnisbereich wurden geprüft.
- Keine Live-Verifikation späterer Änderungen in Notion. Verwendet wurde die im Projekt vorhandene Originalbeschreibung.
- Keine API-/MLX-Inferenzprüfung; der CSV-Modus führt keine Inferenz aus.
