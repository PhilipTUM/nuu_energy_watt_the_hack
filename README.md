# Heat Pump Ready

Lokaler Browser-Prototyp für die nuuEnergy Challenge. Der aktuelle Eingabevertrag besteht **ausschließlich aus den 16 Spalten von `Data_Notion/buildings_eval.csv`**. Zusätzliche Gebäudedaten, Uploads oder Investitionsangaben werden nicht abgefragt; zusätzliche API-Eingabefelder werden abgelehnt.

## Start unter Windows

Im Ordner `Prototype/nuu_energy_watt_the_hack`:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -B -m heat_pump_ready --runner disabled
```

Danach **http://localhost:8000** öffnen. Terminal geöffnet lassen, beenden mit `Ctrl+C`. Alternativer Port: `--port 8001`. Bei korrekt eingerichtetem Python funktioniert auch `python -m heat_pump_ready`.

Python ab 3.9, keine Pflichtpakete, keine Modellinferenz beim Standardstart.

## Verwendung

B-01 bis B-05 auswählen und berechnen. Die Beispiele stammen jetzt aus den tatsächlichen lokalen Notion-CSV-Dateien; fehlende Werte werden unverändert übernommen. Die beigepackten Kopien enthalten bei den Entwicklungsfällen keine Referenzheizlast oder erwartete Ampel. Alternativ Angaben in denselben 16 Formularfeldern eingeben. Das synthetische Beispiel verwendet ebenfalls ausschließlich dieses Schema.

- Heizlast aus Verbrauch und Gebäudeklasse sowie deren gemeinsame Spanne.
- TABULA-Vergleichsspannen für Transmission, Lüftung und jährlichen Raumwärmebedarf.
- Technische Ampel mit Gründen, offenen Angaben und Fachprüfungen.
- Energiekosten und Ersparnis, sofern Energieträger und JAZ bestimmbar sind.
- Quellen, Umrechnung der Energiebezugsfläche und Annahmen an jeder Kennzahl.
- Ergebnisse als JSON herunterladbar.

Investitionskosten, Förderung und Betrachtungszeitraum fehlen im zugelassenen Schema. Deshalb werden Nettoinvestition und Amortisation **nicht berechnet**. Beide Evaluierungsfälle haben keine dokumentierte Vorlauftemperatur; ihre JAZ, Wärmepumpenkosten und Ersparnis bleiben offen.

## Feste Annahmen

| Größe | Wert |
|---|---:|
| Wärmepumpenstrom | 0,26 €/kWh |
| Erdgas | 0,11 €/kWh |
| Heizöl | 1,70 €/Liter ≈ 0,17 €/kWh bei 10 kWh/Liter |
| JAZ Fußbodenheizung | 4,0 |
| JAZ Heizkörper bis einschließlich 55 °C | 3,5 |
| JAZ über 55 bis einschließlich 60 °C | 2,8 |
| Jahresnutzungsgrad | 0,88 |
| Zentrales Warmwasser | 1.000 kWh / Person und Jahr |
| Volllaststunden | 2.000 h/a |

Mischsysteme benötigen die gemeinsame Vorlauftemperatur. LPG wird über `energy_carrier_detail` von Erdgas unterschieden und erhält keinen erfundenen Vergleichstarif. `annual_consumption_kwh` enthält bereits kWh, auch bei Öl; Literangaben im Beschreibungstext werden nicht nochmals umgerechnet.

## Quellen und Grenzen

[Berechnungsgrundlagen](docs/BERECHNUNGSGRUNDLAGEN.md) dokumentiert die Normabschnitte, TABULA-Datenfelder und Technical Guardrails. [KONZEPT.md](KONZEPT.md) beschreibt den aktuellen Datenfluss, [Validierung](docs/VALIDIERUNG.md) die Prüfungen.

Die Norm liefert die Bilanzstruktur, keinen vollständigen Gebäudenachweis aus diesen wenigen Eingaben. Bauteilgeometrien, eindeutige U-Werte mit Flächen, Luftwechsel, Klimazeitreihen und Wärmeerträge fehlen. Eine Gebäude-Monatsbilanz oder Norm-Heizlast wird deshalb nicht behauptet. TABULA-Spannen sind Szenarien über passende Baualtersklassen und Gebäudetypen, keine statistischen Konfidenzintervalle und keine Messwerte des Hauses.

Bild-/Rechnungserkennung ist im CSV-Modus nicht angebunden. Die vorhandenen Runner und Experimentdateien bleiben als Erweiterungsbestand erhalten. Der Server ist ausschließlich für lokalen Hackathon-Betrieb vorgesehen.

## Tests und Datenimport

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -B -m unittest discover -s tests -v
```

Die versionierten Daten benötigen keine Excel-Bibliothek zur Laufzeit. Zum erneuten Import sind `openpyxl` und die lokalen Originaldateien nötig:

```powershell
python tools/import_tabula.py --source-root "..\.."
python -m tools.import_building_cases --source-root "..\.."
```

Die Original-PDF, Excel- und CSV-Dateien bleiben unverändert.
