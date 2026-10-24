# Heat Pump Ready? – nuuEnergy Challenge

> Eine ehrliche erste Einschätzung zur Wärmepumpeneignung in weniger als drei Minuten.

**Track:** Buildings & Everyday Energy  
**Challenge-Partner:** nuuEnergy  
**Betrieb:** lokal im Standardbrowser  
**Leitgedanke:** Transparenz vor Scheingenauigkeit.

Die ursprüngliche, unbereinigte Beschreibung ist in [docs/project_description_original.md](docs/project_description_original.md) erhalten. Dieses Dokument konsolidiert die Challenge-Anforderungen. Unsere technische Umsetzung und Entscheidungen stehen in [KONZEPT.md](KONZEPT.md); Startanweisungen in [README.md](README.md).

## 1. Problem und Zielgruppe

Viele Hauseigentümer heizen mit Gas oder Öl und wissen nicht, ob eine Wärmepumpe in ihrem Gebäude funktionieren würde. Häufig wird irrtümlich angenommen, Fußbodenheizung oder eine vollständige Sanierung seien zwingend notwendig. Eine belastbare Planung erfordert einen Fachbetrieb; die Unsicherheit davor verhindert oft schon den ersten Schritt.

Die Anwendung soll anhand vorhandener Informationen eine verständliche Ersteinschätzung ermöglichen: Jahresabrechnung, Baualter, Heizsystem, Standort und Smartphone-Fotos. Sie soll erklären, was sich abschätzen lässt und welche Fragen ein Techniker vor Ort beantworten muss.

## 2. Auftrag und Erfolgskriterien

Ein funktionierender Browser-Prototyp soll:

1. In unter drei Minuten zu einer ersten Einschätzung führen; Laufzeit auf der Demo-Hardware messen.
2. Heizbedarf beziehungsweise Heizlast näherungsweise bestimmen.
3. Eine begründete Eignungsampel anzeigen.
4. Annahmen, fehlende Daten und Widersprüche sichtbar machen.
5. Die offenen Prüfungen für einen Fachbetrieb konkret nennen.
6. Die Energiekosten mit den festen Challenge-Annahmen vergleichen.

Eine sichere Antwort trotz unzureichender Daten ist ausdrücklich schlechter als ein begründetes „noch nicht beurteilbar“.

## 3. Eingaben

- Baujahr, beheizte Fläche und vorhandene Sanierungsangaben.
- Energieträger, Jahresverbrauch und Verbrauchseinheit.
- Heizflächen, Rohrsystem und gegebenenfalls erforderliche Vorlauftemperatur.
- Personenanzahl und Art der Warmwasserbereitung.
- Standort oder Adresse, soweit vorhanden.
- Fotos von Heizkörpern, Anschlüssen, Anlage und möglichem Außenstandort.
- Hinweise auf weitere Wärmequellen oder Besonderheiten.

Leere Werte bedeuten unbekannte Information. Die Beispieldaten enthalten bewusst unvollständige und teilweise widersprüchliche Angaben. Eine genaue Adresse ist für die beschriebenen einfachen Rechenmethoden nicht erforderlich.

## 4. Ergebnisse und Ampel

| Ampel | Bedeutung laut Challenge |
|---|---|
| Grün | Aufgrund der verfügbaren Informationen wahrscheinlich geeignet. |
| Gelb | Potenziell geeignet; wichtige Angaben oder Prüfungen bleiben offen. |
| Rot | Keine ausreichenden Belege für eine positive Ersteinschätzung. |

**Rot bedeutet nicht automatisch technische Ungeeignetheit.** Die Anwendung muss zwischen einem konkreten Hindernis und einer unzureichenden Datenlage unterscheiden. Alle Farben benötigen eine verständliche textliche Begründung.

Zusätzlich anzeigen: Heizlastschätzungen, Energiekosten, Annahmen und offene Fachprüfungen.

### Projektbezogene Erweiterung: Investitionsentscheidung

Zusätzlich zur Challenge-Ampel soll unsere Anwendung beantworten, ob sich eine Investition anhand der berechneten Kennzahlen lohnt. Dafür werden Investitionskosten, Förderung und Betrachtungszeitraum ergänzt. Die wirtschaftliche Entscheidung bleibt von technischer Eignung getrennt und darf bei fehlenden Angaben „noch nicht beurteilbar“ lauten. Eine vereinfachte Demonstrationsrechnung ist ausdrücklich als solche zu kennzeichnen.

## 5. Fachliche Rechenvorgaben

### 5.1 Heizlast aus Fläche und Gebäudezustand

Heizlast in kW ≈ beheizte Fläche in m² × spezifische Heizlast in W/m² ÷ 1.000.

| Gebäudeklasse | Richtwert |
|---|---:|
| Unsaniert, vor 1979 | 120–180 W/m² |
| Baujahr 1980er–1990er | 80–120 W/m² |
| Saniert oder Baujahr ab 2002 | 40–60 W/m² |
| Niedrigenergiehaus / entsprechender Neubau | 15–40 W/m² |

Die Klassen sind grobe Richtwerte, keine normgerechte Berechnung. Baujahr 1979, 2000–2001 und unklare beziehungsweise teilweise Sanierung sind nicht vollständig spezifiziert. Eigene Ergänzungen müssen gekennzeichnet werden. „Neubau“ und „ab 2002“ überlappen; eine bessere Gebäudeklasse braucht eine begründete Zuordnung.

### 5.2 Heizlast aus Verbrauch

1. Brennstoffverbrauch bei Bedarf in kWh umrechnen: 1 Liter Heizöl ≈ 10 kWh; 1 m³ Erdgas ≈ 10 kWh.
2. Nutzwärme ≈ Jahresverbrauch × 0,88.
3. Bei zentraler Warmwasserbereitung ungefähr 1.000 kWh pro Person und Jahr für Warmwasser abziehen.
4. Raumwärmebedarf durch ungefähr 2.000 Volllaststunden teilen: Ergebnis in kW.

Beide Heizlastmethoden anzeigen, wenn die Angaben vorliegen. Abweichungen offenlegen, statt ohne Begründung einen präzisen Mittelwert zu bilden. Über ungefähr 75 W/m² können bessere Fenster oder Dämmung sinnvoll zu prüfen sein; das ist kein Ausschlusskriterium.

### 5.3 Heizflächen und Vorlauftemperatur

Die benötigte Vorlauftemperatur ist entscheidend. Bis etwa 55 °C ist ein effizienter Betrieb plausibel; 55–60 °C führt bei den vorgegebenen Annahmen zu höherem Stromverbrauch. Technische Erreichbarkeit höherer Temperaturen ist nicht mit Wirtschaftlichkeit gleichzusetzen.

- Fußbodenheizung ist ein günstiges Indiz, aber keine Voraussetzung.
- Große beziehungsweise neuere Plattenheizkörper können geeignet sein.
- Kleine alte Heizkörper oder Einrohrsysteme brauchen zusätzliche Prüfung.
- Typ 11 / 22 / 33 bezeichnet Platten und Konvektorlagen.
- Bei ungefähr 55 °C kann die Leistung grob etwa halb so groß wie bei einer Nennangabe für 75 °C sein. Ohne definierte Randbedingungen, Maße und Raumlast ist das keine belastbare Dimensionierung.

### 5.4 Feste Energiekostenannahmen

| Energieträger | Preis |
|---|---:|
| Wärmepumpenstrom | 0,26 €/kWh |
| Erdgas | 0,11 €/kWh |
| Heizöl | 1,70 €/Liter ≈ 0,17 €/kWh |

| Heizsystem / Vorlauftemperatur | JAZ |
|---|---:|
| Fußbodenheizung, ungefähr 35 °C | 4,0 |
| Heizkörper bis 55 °C | 3,5 |
| Heizkörper über 55 bis 60 °C | 2,8 |

Wärmepumpen-Energiekosten = gelieferte Nutzwärme ÷ JAZ × Strompreis.

Heutige Energiekosten = Brennstoffverbrauch × passender Brennstoffpreis.

Beide Seiten müssen denselben Wärmelieferumfang abbilden. Warmwasser darf zur Heizlastberechnung abgezogen werden, aber nicht versehentlich aus dem jährlichen Kostenvergleich verschwinden. Wartung, Grundpreise und Investition sind in diesen Energieformeln nicht enthalten.

Die Challenge definiert keine vollständigen Tarife für Flüssiggas, Fernwärme oder direkte elektrische Heizung und keine JAZ über 60 °C. Solche Lücken dürfen nicht stillschweigend mit Erdgaswerten ersetzt werden.

## 6. Einrohr- und Zweirohrsysteme

### Funktionsweise

**Zweirohrsystem:** Heizkörper erhalten Vorlauf aus einer gemeinsamen Zuleitung und führen abgekühltes Wasser über einen separaten Rücklauf zurück. Die Vorlauftemperaturen sind ähnlich.

**Einrohrsystem:** Eine Leitung verbindet Heizkörper als Ring. Jeder Heizkörper entnimmt einen Teil des Wassers und führt es wieder in den Ring zurück. Die Temperatur sinkt entlang des Rings.

Einrohrsysteme waren insbesondere in Gebäuden der 1960er- und 1970er-Jahre verbreitet. Das Baujahr allein ist kein Nachweis.

### Bedeutung für Wärmepumpen

Einrohrsysteme können höhere Vorlauftemperaturen benötigen und sind hydraulisch schwieriger abzugleichen. Wärmepumpen sind dennoch nicht grundsätzlich ausgeschlossen. Größere Heizkörper, Anpassungen an der Hydraulik oder teilweise Umbauten müssen gegebenenfalls geprüft werden. Ein bestätigtes Einrohrsystem ist ohne weitere Prüfung selten ein eindeutiges Grün.

### Hinweise aus Fotos

| Beobachtung | Mögliche Aussage |
|---|---|
| Getrennte Vorlauf- und Rücklaufleitungen ohne sichtbare Verbindung | Indiz für Zweirohr, kein vollständiger Systemnachweis |
| Leitung von Heizkörper zu Heizkörper, sichtbarer Bypass | Indiz für Einrohr |
| Gemeinsamer unterer Anschlussblock | Nicht eindeutig; Varianten für beide Systeme existieren |
| H-Block mit zwei Leitungen | Allein nicht unterscheidbar |
| Einstellbarer Bypass am Ventil | Zusätzliches Einrohrindiz |

Zwei Anschlüsse am Heizkörper beweisen kein Zweirohrsystem. Ein einzelner neuer Heizkörper sagt nichts Sicheres über das gesamte Gebäude aus. Aussagekräftiger sind Leitungsverlauf, Ventilkennzeichnungen und Heizraum.

Wenn `pipe_system` bekannt ist, diese Angabe verwenden. Sonst darf eine Schätzung mit Begründung und Unsicherheit erfolgen. Bei unzureichenden Bildern bleibt das Ergebnis unbekannt.

## 7. Immer erforderliche Fachprüfungen

- Exakte Heizlast, gegebenenfalls nach DIN EN 12831.
- Raumweise Heizkörperdimensionierung bei der vorgesehenen Temperatur.
- Elektrische Anschlussleistung und Zählerschrank.
- Hydraulik und Abgleich.
- Außenaufstellung, Platzverhältnisse und Schall.
- Gegebenenfalls erforderliche Genehmigungen.

Der Prototyp ersetzt diese Prüfungen auch bei grüner Ampel nicht.

## 8. Beispieldatensatz

Die Challenge kündigt fünf anonymisierte Gebäude als CSV und JSON an: drei Entwicklungsfälle mit Referenzen und zwei Evaluierungsfälle mit zurückgehaltenen Referenzen. Namen und genaue Adressen fehlen; Flächen und Verbräuche sind leicht gerundet.

### Gebäudeübersicht

| ID | Set | Baujahr | Fläche | Heizflächen | Rohrsystem | Energieträger | Jahresverbrauch | Region |
|---|---|---:|---:|---|---|---|---:|---|
| B-01 | dev | 2001 | 195 m² | Heizkörper | unbekannt | Flüssiggas | 10.000 kWh | München, 82xxx |
| B-02 | dev | 2005 | 180 m² | Fußbodenheizung | unbekannt | Gas | 15.500 kWh | München, 82xxx |
| B-03 | dev | 1970 | 200 m² | Heizkörper | Zweirohr | Öl | 40.000 kWh | Hamburg, 21xxx |
| B-04 | eval | 1987 | 160 m² | Heizkörper | Einrohr | Öl | 25.000 kWh | München, 85xxx |
| B-05 | eval | 2006 | 125 m² | gemischt | unbekannt | Gas | 27.000 kWh | München, 85xxx |

### Referenzen nur für die Auswertung

| ID | Referenzheizlast | Erwartete Ampel |
|---|---:|---|
| B-01 | 9,6 kW | Grün |
| B-02 | 9,7 kW | Grün |
| B-03 | 14,5 kW | Gelb |

Referenzwerte dürfen nicht als Eingaben in die Berechnung oder in Modellprompts einfließen.

### Angekündigte Dateien

- `buildings_dev.csv` und `buildings_dev.json`
- `buildings_eval.csv` und `buildings_eval.json`

Diese Quelldateien lagen bei der ersten Umsetzung nicht im Repository vor. Die Demo verwendet ausschließlich die oben transkribierten Angaben und erfindet keine fehlenden Gebäudefakten.

### Felder

| Feld | Typ / Werte | Bedeutung |
|---|---|---|
| `building_id` | String | Gebäude-ID |
| `construction_year` | Integer | Baujahr |
| `floor_area_m2` | Zahl | Beheizte Fläche |
| `renovation_status` | unrenovated / partially / fully, optional | Sanierung |
| `heat_distribution` | radiators / underfloor / mixed | Heizflächen |
| `annual_consumption_kwh` | Zahl | Jährlicher Brennstoffverbrauch |
| `energy_carrier` | gas / oil / district / electric | Energieträger |
| `energy_carrier_detail` | String | Etwa Erdgas oder LPG |
| `radiator_info` | String | Freitext zu Heizkörpern und Ventilen |
| `pipe_system` | two-pipe / single-pipe / unknown | Rohrsystem |
| `flow_temperature_c` | Zahl, optional | Vorlauftemperatur |
| `persons_in_household` | Integer | Haushaltsgröße |
| `hot_water_via_heating` | Boolean | Warmwasser über Heizung |
| `rooms` | Integer, optional | Raumzahl |
| `building_notes` | String | Besonderheiten und zusätzliche Wärmequellen |
| `location` | String | Ungefährer Standort |
| `reference_heating_load_kw` | Zahl, nur dev | Referenz zur Auswertung |
| `expected_verdict` | green / yellow / red, nur dev | Referenz zur Auswertung |

In unserer Eingabedataclass wird Flüssiggas ausdrücklich als `lpg` unterschieden, damit der Erdgaspreis nicht versehentlich verwendet wird. Für einen späteren Dateiimport müssen die Originalfelder bewusst auf die internen Verträge abgebildet werden.

## 9. Abgabe und Bonus

Pflicht: lokal lauffähiger Browser-Prototyp, Ergebnisse für die zwei Evaluierungsgebäude im Pitch und eine Live-Demo statt einer reinen Folienpräsentation.

Optional: automatische Rechnungserkennung und Erkennung räumlicher Aufstellungsrisiken aus Fotos.

## 10. Bewertung und Preis

| Kriterium | Punkte |
|---|---:|
| Technische Umsetzung und Zuverlässigkeit | 25 |
| Problemlösung und Nutzen | 25 |
| Erklärbarkeit und Umgang mit Unsicherheit | 20 |
| Innovation und sinnvoller Technologieeinsatz | 15 |
| Machbarkeit und Skalierbarkeit | 15 |
| **Gesamt** | **100** |

Angekündigter Preis: 1.000 €, ein Tischkicker und ein Tech Day mit dem nuuEnergy-Produktteam.

## 11. Glossar

- **Heizlast:** Benötigte Heizleistung am Auslegungspunkt, in kW; nicht gleich Jahresverbrauch.
- **Vorlauftemperatur:** Temperatur des Wassers zu den Heizflächen, in °C.
- **JAZ:** Verhältnis jährlich gelieferter Wärme zu eingesetztem Strom.
- **Volllaststunden:** Rechengröße aus Jahreswärme und Heizleistung; Challenge-Näherung 2.000 h, ursprünglicher Hintergrundbereich etwa 1.800–2.100 h.
- **Kesselnutzungsgrad:** Anteil des Brennstoffenergieeinsatzes, der als Nutzwärme ankommt; hier pauschal 0,88.
- **Heizkörpertyp:** Erste Ziffer beschreibt Plattenzahl, zweite Konvektorlagen.
- **Fußbodenheizung:** Flächenheizung mit typischerweise niedrigem Temperaturniveau; günstig, aber nicht zwingend.

## 12. Bereinigte Widersprüche und offene Quellen

1. Ein ursprünglicher Abgabeabschnitt nennt drei Evaluierungsfälle. Datensatz und übrige Beschreibung nennen zwei; dieses Dokument verwendet zwei.
2. Platzhalter `image.png`, Fotos von nuuEnergy und die erwähnte SWM-Musterrechnung enthalten keine nutzbaren Dateien beziehungsweise Links. Es werden keine Quellen erfunden.
3. Der Abschnitt „Most common no-go decisions“ war unvollständig und enthält keine anwendbaren Regeln.
4. Konkrete Investitionskosten, Förderregeln und Finanzierungsbedingungen fehlen. Unsere Wirtschaftlichkeitsprüfung ist deshalb zunächst ein transparentes Demonstrationsmodell.
5. Numerische Richtwerte sind Challenge-Annahmen, keine aktuelle Produkt-, Tarif- oder Förderberatung.
