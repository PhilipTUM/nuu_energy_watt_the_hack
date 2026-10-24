# Berechnungsgrundlagen und Technical Guardrails

Stand: 24. Oktober 2026. Verbindlicher Eingabeumfang: die 16 Spalten der lokalen `Data_Notion/buildings_eval.csv`. Die vom Nutzer vorgegebenen Preise und JAZ bleiben feste Challenge-Annahmen. Norm und TABULA dürfen fehlende Gebäudefakten nicht vortäuschen.

## 1. Lokale Quellen

- `DIN EN ISO 52016-1_2018-04-00_DE_2577376.pdf`: Begriffe, Bilanzstruktur und Datenanforderungen. Insbesondere 6.3 (Eingaben), 6.6.4 (Heizenergiebedarf), 6.6.5 (Transmission), 6.6.6 (Lüftung), 6.6.7–6.6.10 (Gewinne und Speicherwirkung). Die Normseite 138 / PDF-Seite 166 und NA.34 / PDF-Seite 18 wurden zusätzlich visuell geprüft. NA.34 enthält 16 h als Bezugszeitkonstante; der informative Anhang B nennt 15 h. Im aktuellen CSV-Modus wird keine Monatsbilanz gerechnet und folglich keiner dieser Parameter als Gebäudefakt verwendet.
- `TABULA-Analyses_DE-Typology_DataTables/TABULA-Analyses_DE-Typology_ResultData.xlsx`, Blatt `Values Output.Set.1 DE-All`: Kennwerte und Herkunft der Szenarien.
- `TABULA-Analyses_DE-Typology_DataTables/TABULA-Analyses_DE-Typology_BuildingData.xlsx`, Blatt `Gebaeudedaten`: beim Quellenüberblick geprüft; die Laufzeitdaten werden einheitlich aus ResultData extrahiert, um abweichende Flächenbezüge und Varianten nicht zu vermischen.
- `tabula-calculator.xlsx`, Blatt `Calc.Set.Building`: Formeln und Definitionen geprüft, etwa `h_Transmission = SUM(H_Transmission_...)/A_C_Ref`. `Tab.AuxCalc.Climate` enthält Referenzklimata; diese wurden mit extrahiert, werden im CSV-Modus jedoch nicht zur Standortzuordnung oder Heizlastberechnung verwendet.
- `docs/project_description_original.md`: lokale Kopie der Notion-Challenge einschließlich Technical Guardrails, insbesondere die Abschnitte Heating load, Radiators, Operating costs und Always checked by a technician. Kein behaupteter Live-Abgleich mit späteren Änderungen in Notion.
- `Data_Notion/buildings_dev.csv` und `buildings_eval.csv`: tatsächliche Gebäudeangaben; ausschließlich die eval-Eingabespalten werden übernommen. Entwicklungsreferenzen bleiben außerhalb von UI und Rechenpipeline.

`tools/import_tabula.py` erzeugt `heat_pump_ready/data/tabula_de.json` mit Dateinamen, SHA-256, Blattzeilen und Originalkennwerten. Import: 150 eindeutige deutsche Varianten mit Endung .001/.002/.003; systemseitige Varianten .011/.012/... werden nicht als weitere unabhängige Hüllszenarien gezählt. Gleiche Varianten mit abweichenden übernommenen Werten würden den Import abbrechen.

## 2. Zugelassene Eingaben

`building_id`, `construction_year`, `floor_area_m2`, `renovation_status`, `heat_distribution`, `annual_consumption_kwh`, `energy_carrier`, `energy_carrier_detail`, `radiator_info`, `pipe_system`, `flow_temperature_c`, `persons_in_household`, `hot_water_via_heating`, `rooms`, `building_notes`, `location`.

CSV-Leerfelder bleiben unbekannt, `yes/no` werden zu booleschen Werten. Bereits in kWh angegebener Ölverbrauch wird nicht anhand einer beiläufigen Literangabe nochmals umgerechnet. `gas` plus expliziter LPG-/Flüssiggasbeschreibung wird für Tarifentscheidungen als LPG behandelt, ohne das Originalfeld zu verändern. Texte gelten als Daten, nicht als Anweisungen an Berechnungsmodelle.

`rooms` ist kein Ersatz für Raumflächen oder raumweise Heizlast. Eine grobe Ortsangabe ist kein Nachweis für eine Norm-Außentemperatur. Hinweise auf Solarthermie oder Holzofen führen zu zusätzlichem Prüfbedarf; unbelegte Erträge werden nicht addiert.

## 3. Verbrauch und Flächenheizlast

- Nutzwärme: `annual_consumption_kwh × 0,88`, für Gas, Öl und LPG.
- Bei zentralem Warmwasser: `Personen × 1.000 kWh/a` abziehen. Bei ausdrücklich separatem Warmwasser: 0 kWh innerhalb dieses Heizungslieferumfangs. Unbekannte Warmwasserbereitung blockiert die verbrauchsbasierte Raumwärme und Heizlast.
- Raumwärme / 2.000 h/a ergibt die verbrauchsbasierte Heizlastabschätzung.
- Flächenheizlast nach den groben Challenge-Klassen: 120–180, 80–120, 40–60 oder 15–40 W/m². Unklare Zustände bleiben mit breiter Spanne gekennzeichnet; kein behaupteter TABULA-Wert.
- `heat_load_range` zeigt die äußersten Grenzen beider Methoden, ohne Mittelwert. Eine starke Abweichung wird geprüft.

Diese Methoden sind keine Norm-Heizlast. Verbrauch ist weder witterungsbereinigt noch auf volle Beheizung oder Zusatzwärme korrigiert. Über etwa 75 W/m² wird auf Fenster/Dämmung hingewiesen, ohne einen Wärmepumpen-Ausschluss zu behaupten.

## 4. TABULA-Szenarien

Ein einzelner Typ wäre aus den CSV-Spalten nicht belegbar. Deshalb werden alle deutschen Referenzvarianten der passenden Baualtersklasse berücksichtigt. Unbekannte, teilweise oder vollständig beschriebene Sanierung wird nicht automatisch mit einem bestimmten TABULA-Maßnahmenpaket gleichgesetzt. Nur die ausdrückliche Angabe `unrenovated` beschränkt auf die erste Variante. Gebäudetyp und Geometrie bleiben Szenarien, keine zusätzlich erfundenen Eingaben. Die Quelle enthält auch eine offene Altersklasse ab 2016 mit Endjahr 9999; das ist die historische Quellklassifikation, kein Nachweis heutiger Neubauanforderungen.

Pro Szenario erfolgt die Umrechnung:

`übertragene A_C_Ref = floor_area_m2 × A_C_Ref / A_C_Living`.

Die CSV-Fläche wird dabei ausdrücklich als beheizte Wohnfläche interpretiert. Die Verhältnisübertragung setzt ein geometrisch ähnliches Szenario voraus. Direkte Multiplikation wohnflächenbezogener Eingaben mit energiebezugsflächenbezogenen Kennwerten wäre falsch.

| Ergebnis | Originalspalte | Einheit / Verwendung |
|---|---|---|
| Transmission H_T | KL `h_Transmission` × übertragene A_C_Ref | W/K, einschließlich bestehender Wärmebrücken-/Bauteilkorrekturen |
| Lüftung H_V | KM `h_Ventilation` × übertragene A_C_Ref | W/K, vor systemseitiger Wärmerückgewinnung |
| TABULA-Raumwärme | KS `q_h_nd` × übertragene A_C_Ref | kWh/a, ursprüngliches Referenzklima, vor systemseitiger Wärmerückgewinnung |

Flächen: HZ `A_C_Ref`, HX `A_C_Living`. Die Ergebnisgrenzen werden **pro Kennzahl** aus den einzelnen Szenarien bestimmt. Unter- und Obergrenze weisen jeweils Code, Blattzeile und Flächenverhältnis aus; Grenzen verschiedener Kennzahlen gehören nicht zwingend zum gleichen Haus und dürfen nicht zu einem neuen künstlichen Szenario kombiniert werden.

Beim Import wurde für alle 150 Datensätze `h_Transmission` gegen die Summe der elf `H_Transmission_*`-Bauteil-/Wärmebrückenbeiträge geteilt durch `A_C_Ref` abgeglichen. Beispiel: Zeile 712, `DE.N.SFH.05.Gen.ReEx.001.001`: A_C_Ref 121,22 m², A_C_Living 110,2 m², h_T 4,0893795957 W/(m²K), q_h_nd 275,6346195752 kWh/(m²a).

`q_h_nd` ist bewusst nicht `q_h_nd_net`: Letzteres hängt zusätzlich von systemseitiger Wärmerückgewinnung ab, die aus den CSV-Spalten nicht bestimmbar ist. Ebenso ist H_V kein bereits um den Anlagen-WRG-Wirkungsgrad reduzierter Koeffizient.

Die jährliche TABULA-Raumwärme bleibt von Verbrauch und Kosten getrennt. Kein Ersatz fehlenden Brennstoffverbrauchs, keine willkürliche Mittelung, keine Umrechnung von Jahres-kWh in Norm-kW.

## 5. Was die Norm mit diesen Eingaben zulässt

Die Bilanzstruktur trennt Transmission, Lüftung, interne/solare Gewinne und zeitliche Speicherung. Eine individuelle Monatsbilanz nach 6.6 benötigt passende Geometrie- und Klimadaten, Randbedingungen und Gewinne. Eine Lastberechnung benötigt außerdem einen Auslegungsfall beziehungsweise entsprechende zeitliche Randbedingungen. Diese Größen sind im zugelassenen CSV-Schema nicht vollständig dokumentiert.

Daher liefert der Prototyp typologische Vergleichsspannen sowie die Challenge-Heizlastmethoden. Er behauptet weder eine vollständige DIN-EN-ISO-52016-Bilanz noch eine Norm-Heizlast nach DIN EN 12831. Es werden keine zusätzlichen Felder für U-Werte, Fensterflächen, Klimastation oder Auslegungstemperatur eingeführt. Selbst die U-Werte in B-01 ersetzen ohne Bauteilflächen keine Hüllbilanz.

## 6. Kosten und JAZ bleiben feste Vorgaben

Wärmepumpenstrom 0,26 €/kWh; Erdgas 0,11 €/kWh; Heizöl 0,17 €/kWh (1,70 €/Liter bei 10 kWh/Liter). Fußbodenheizung JAZ 4,0; Heizkörper bis einschließlich 55 °C JAZ 3,5; über 55 bis einschließlich 60 °C JAZ 2,8. Mischsysteme nach gemeinsamer Vorlauftemperatur. Fehlende Temperatur wird nicht aus Alter, Heizkörpertyp oder Fußbodenheizungsanteil geraten. Über 60 °C gibt es für Heizkörper keine vorgegebene JAZ.

Heutige Kosten = jährliche Brennstoffenergie × Tarif. Wärmepumpenkosten = gesamte bisher gelieferte Nutzwärme / JAZ × 0,26 €/kWh. Zentrales Warmwasser bleibt damit im Kostenvergleich enthalten, auch wenn es zur Heizlastbestimmung abgezogen wurde. Keine erfundenen LPG-/Fernwärme-/Direktstromtarife. Keine Marktpreis-, Förder- oder Kapitalwertberatung.

Nettoinvestition, Amortisation und Betrachtungszeitraum bleiben mangels CSV-Eingaben unbekannt. Die technische Ampel wird unabhängig davon angezeigt.

## 7. Technical Guardrails

- Grün bedeutet wahrscheinlich geeignet, Gelb Prüfbedarf, Rot unzureichende Belege. Fehlende Daten sind kein Ungeeignetheitsnachweis.
- Heizlastmethoden und gemeinsame Spanne bleiben sichtbar. Abweichungen werden nicht durch Mittelung verborgen.
- Einrohrsysteme führen zu hydraulischem Prüfbedarf. Ventilblöcke, zwei Anschlüsse oder Baujahr beweisen kein Zweirohrsystem.
- Nur explizite Typangaben 11/22/33 aus `radiator_info` werden übernommen. Anzahl, Alter oder Ventilvoreinstellung beweisen weder Typ noch ausreichende Leistung.
- Die grobe Leistungsabnahme bei niedrigerer Vorlauftemperatur ist ein Fachprüfhinweis. Ohne Maße, Nennleistung und Raumlast wird kein belastbarer Leistungsfaktor oder Eignungsnachweis errechnet.
- Vorlauftemperatur, Heizlast und Rohrsystem müssen hinreichend belegt sein, bevor die vereinfachte Ampel grün werden kann. Zusatzwärmequellen halten die Wärmebilanz offen.
- Exakte Heizlast, raumweise Heizkörperdimensionierung, Elektroanschluss, Zählerschrank, Hydraulik, Außenaufstellung, Schall und Genehmigungen bleiben Fachprüfungen.
- Die drei Entwicklungsreferenzen fließen weder als Eingabe noch als Parameter in die Module ein. Keine Optimierung auf zurückgehaltene Evaluierungsreferenzen.
