# Umsetzungskonzept – CSV-basierter Prototyp

## Eingabe und Quellen

Der aktuelle, vom Nutzer eingeschränkte Eingabevertrag ist exakt das Schema von `Data_Notion/buildings_eval.csv` mit 16 Spalten. Formularfelder, `UserInput` und API-Validierung verwenden dieselben Variablennamen. Nicht erlaubte zusätzliche Felder werden mit HTTP 400 abgelehnt. CSV-Leerfelder bleiben unbekannt, yes/no wird korrekt eingelesen.

Die echten CSV-Fälle sind als auf dieses Schema reduzierte Kopien beigepackt; Entwicklungsreferenzen werden nicht übernommen. Die Originalquellen bleiben unverändert. Das synthetische Beispiel verwendet dieselben 16 Eingaben.

## Datenfluss

1. Browserformular oder JSON-API → `build_user_input` → unveränderliche `UserInput`.
2. `CalculationOrchestrator` führt die Module in expliziter Abhängigkeitsreihenfolge aus.
3. Jedes Modul liefert eine `MetricResult` mit Einheit, Herkunft, Annahmen und Unsicherheit. `CalculationOutput` bleibt unveränderlich.
4. `validate_and_decide` prüft Plausibilität und technische Belege. Aus den CSV-Daten entsteht keine Investitionsentscheidung, weil deren Eingaben fehlen.
5. Browser zeigt technische Ampel, Kennzahlen, offene Angaben und Fachprüfungen; JSON-Export ist möglich.

Fehlende Produzenten oder ausgeschaltete Module blockieren nur ihre abhängigen Berechnungen. Typologische Vergleichsszenarien ersetzen keinen fehlenden Verbrauch.

## Module

| Zweig | Module / Verantwortung |
|---|---|
| Verbrauch | `annual_consumption`: kWh aus CSV; `useful_heat`: ×0,88; `hot_water_demand`: zentrale Warmwasserabgrenzung; `space_heating_demand`: Differenz |
| Heizlast | `heat_load_consumption`: Raumwärme /2.000; `heat_load_area`: grobe Challenge-Gebäudeklasse; `heat_load_range`: äußere Grenzen beider Methoden |
| TABULA | `transmission_heat_transfer`, `ventilation_heat_transfer`, `tabula_space_heating_demand`: belegte Baualters-/Varianten-Szenariospannen mit korrektem Flächenbezug |
| Heizsystem | `radiator_type`: ausdrücklich dokumentierter Typ; `pipe_system`: CSV-Angabe; `annual_performance_factor`: feste JAZ anhand Heizflächen und Temperatur |
| Energiekosten | `current_energy_cost`, `heat_pump_energy_cost`, `annual_savings`: feste Challenge-Tarife und gleicher Wärmelieferumfang |
| Investition | `net_investment` und `horizon` melden die fehlenden CSV-Variablen; `payback_period` bleibt dadurch blockiert |

Die bestehenden LLM-Runner und Experimentdateien bleiben erhalten. Der aktuelle CSV-Stack führt keine Bild-/Dokumentinferenz aus und akzeptiert keine Upload-Eingaben.

## Norm und Guardrails

Normabschnitte, TABULA-Spalten, Szenarioauswahl und Grenzen sind in [Berechnungsgrundlagen](docs/BERECHNUNGSGRUNDLAGEN.md) beschrieben. Die Norm unterstützt die saubere Trennung von Wärmeverlusten, Gewinnen, Jahresenergie und Leistung. Für eine individuelle Monatsbilanz oder Norm-Heizlast reichen die zugelassenen Daten nicht aus. Es werden deshalb keine zusätzlichen Nutzereingaben dafür eingeführt.

Die Ampel bewertet wahrscheinliche technische Eignung, keinen sicheren Dimensionierungsnachweis. Einrohr, unbekannte Vorlauftemperatur, Zusatzwärme oder widersprüchliche Heizlastmethoden erzeugen Prüfbedarf. Hohe spezifische Last ist ein Dämmhinweis, kein automatisches Ausschlusskriterium.

## Betrieb

Python-Standardbibliothek, HTML/CSS/JavaScript ohne Build. Der Server bindet ausschließlich an 127.0.0.1 und ist für die lokale Hackathon-Demo vorgesehen. Datenquellen werden bei der Entwicklung extrahiert; zur Laufzeit wird nur lokales CSV/JSON gelesen. Start und Tests stehen in [README.md](README.md), Prüfergebnisse in [docs/VALIDIERUNG.md](docs/VALIDIERUNG.md).
