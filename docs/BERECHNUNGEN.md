# Berechnungsdokumentation und Quellenprüfung

**Stand: 24. Oktober 2026.** Dokumentiert wird der tatsächlich vorhandene Code, nicht eine geplante bessere Version. Formeln mit „Weiterentwicklung“ sind noch nicht implementiert. Die Anwendung wurde für diese Recherche nicht fachlich verändert.

## 1. Ergebnis der Quellenprüfung

Die Rechenoperationen sind überwiegend einfache Energiebilanzen. Die Unsicherheit liegt vor allem in den Faktoren und der Zuordnung zum konkreten Haus. Für **0,88 Jahresnutzungsgrad, genau 1.000 kWh Warmwasser pro Person, pauschal 2.000 h, die konkreten Baualtersklassen und die drei festen JAZ-Werte** wurde in dieser kleinen Recherche kein offizieller Beleg gefunden, der ihre allgemeine Gültigkeit für jedes Gebäude rechtfertigt. Ihre verbindliche Herkunft im Projekt ist die [Challenge-Beschreibung](../project_description.md).

Offizielle Quellen stützen die zugrunde liegenden Verfahren und zeigen, welche individuellen Angaben fehlen. Das ist keine unabhängige Bestätigung jedes Challenge-Faktors. Feste Challenge-Preise bleiben aus Vergleichsgründen unverändert; aktuelle Marktpreise wurden nicht recherchiert.

## 2. Quellen und Zugriffsumfang

Nur Veröffentlichungen der verantwortlichen Organisationen: Behörden, Norm-/Richtlinienherausgeber, Forschungseinrichtung, offizieller Fachverband und technische Herstellerunterlagen. Herstellerangaben gelten nur im angegebenen Produkt-/Verfahrenskontext. Keine Blogs, Vergleichsportale oder Drittanbieter-Normkopien werden als Beleg verwendet.

| ID | Offizielle Quelle | Was sie hier belegt | Grenze |
|---|---|---|---|
| Q1 | [Bundesnetzagentur: Rechnungen][Q1] | Gasumrechnung über Brennwert und Zustandszahl | Kein einheitlicher Gebäudefaktor 10 |
| Q2 | [Verbraucherportal Bayern: Strom-/Gasrechnung][Q2] | Faktor 10 nur als Überschlag, Zusammenhang mit Heizöl | Keine genaue Brennstoffanalyse |
| Q3 | [Umweltbundesamt: Wärmepumpen][Q3] | Definition JAZ und Einfluss niedriger Systemtemperaturen | Keine feste JAZ-Zusage für dieses Haus |
| Q4 | [DIN Media: DIN/TS 12831-1:2020-04][Q4] | Anwendungsrahmen von detaillierter und vereinfachter Heizlastermittlung | Öffentliche Beschreibung, Volltext nicht gelesen |
| Q5 | [dena/Gebäudeforum: BWP-Heizlastrechner][Q5] | Verfahren und Grenzen eines fachlichen Vergleichswerkzeugs | Rechner ist kein Ersatz für Auslegungsplanung |
| Q6 | [DWD: Klimafaktoren, v22.3][Q6] | Definition und räumlich-zeitliche Zuordnung von Klimafaktoren | Referenzklima für Verbrauchsausweise, kein pauschaler Heizlastfaktor |
| Q7 | [VDI 4650 Blatt 1, öffentliche Vorschau 2024][Q7] | Bilanzgrenze, getrennte Heiz-/Warmwasserbetrachtung, Gesamtsystem | Keine vollständige Normimplementierung aus der Vorschau |
| Q8 | [VDI 2067 Blatt 1, öffentliche Vorschau 2012][Q8] | Kostenarten, Lebenszyklus und Annuitätenmethodik | Keine vollständige Wirtschaftlichkeitsrechnung nach Richtlinie implementiert |
| Q9 | [Kermi: technische Unterlage Konvektoren 2025][Q9] | Temperaturabhängige Heizkörperleistungsumrechnung | Faktoren nur mit passenden Randbedingungen verwenden |
| Q10 | [Fraunhofer ISE: Feldprojekt, 03.11.2025][Q10] | Gemessene JAZ streuen zwischen realen Anlagen | Mittelwerte sind keine Einzelgebäudeprognose |
| Q11 | [BWP: Update Heizlastrechner, 21.06.2024][Q11] | Einbezug von DWD-Klimadaten bei Verbrauchsschätzungen | Keine Bestätigung unserer 2.000 h |
| Q12 | [Bosch Home Comfort: Heizleistungsberechnung][Q12] | Erklärte physikalische Bestandteile der Heizlast | Herstellererläuterung, kein Normvolltext |

Abruf/Recherchestand für diese Liste: 24.10.2026. Bei Normen Ausgabe und spätere Berichtigungen vor einer fachlichen Implementierung über den Herausgeber prüfen. Keine Norm wurde gekauft und keine Übereinstimmung mit ungelesenem Volltext behauptet. Der direkte BWP-Rechner war beim Abruf nicht zuverlässig erreichbar; seine Funktion wurde über Q5 und Q11 eingeordnet. Eine gefundene Stiebel-Eltron-Warmwasser-PDF war direkt nicht mehr abrufbar und wird deshalb nicht als tragender Beleg verwendet.

## 3. Größen und Bilanzgrenzen

| Symbol | Bedeutung | Einheit |
|---|---|---|
| E_fuel | Jährliche eingesetzte Brennstoffenergie | kWh/a |
| η | Jahresnutzungsgrad mit festgelegter Energiebezugsbasis | dimensionslos |
| Q_useful | Vom Kessel bereitgestellte Nutzwärme, vereinfachte Bilanz | kWh/a |
| Q_ww | Dem betrachteten Heizsystem zugeordnete Warmwasserwärme | kWh/a |
| Q_space | Raumwärmeanteil des betrachteten Systems | kWh/a |
| P | Geschätzte Heizleistung | kW |
| h_full | Äquivalente Volllaststunden | h/a |
| A | Beheizte Grundfläche | m² |
| q | Spezifische Heizleistung | W/m² |
| J | Jahresarbeitszahl | dimensionslos |
| p | Energiearbeitspreis | €/kWh |
| C | Jährliche Energiekosten | €/a |
| I_net | Investition nach angegebener Förderung | € |
| S | Jährliche Energiekostenersparnis | €/a |
| t_pb | Einfache Amortisationsdauer | Jahre |

**Heizlast ist Leistung, Verbrauch ist Energie.** Die Grundfläche allein liefert im aktuellen Modul eine Heizlastspanne, keinen Jahreswärmeverbrauch. Wärme am Kesselausgang und Wärme in den Räumen sind bei Verteilungs-/Speicherverlusten nicht identisch. Diese Bilanzgrenze ist im MVP vereinfacht und muss fachlich präzisiert werden.

## 4. Gemeinsamer Modulvertrag

Jedes Modul liest `UserInput` und einen unveränderlichen `CalculationOutput`, liefert genau ein `MetricResult` und trifft keine Investitionsentscheidung. Nur der Orchestrator setzt das Ergebnis ein.

`available` bedeutet „unter diesen Eingaben/Annahmen berechnet“, nicht „fachlich bestätigt“. `missing_input` bedeutet fehlende Angaben, `blocked` eine fehlende Vorberechnung, `disabled` ein ausgelassenes Modul und `failed` einen technischen Extraktionsfehler. Quellen, Annahmen und Unsicherheit sind Teil jedes Ergebnisses.

## 5. Alle 15 Berechnungsmodule

### M01 – AnnualConsumptionModule / annual_consumption

**Code:** [annual_consumption.py](../heat_pump_ready/calculation/modules/annual_consumption.py).

**Eingabe:** Nutzerverbrauch und Einheit, Energieträger; ersatzweise Rechnungsbild. **Vorberechnung:** keine. **Output:** jährliche Brennstoffenergie in kWh/a.

Aktuell:

```text
Bei kWh: E_fuel = eingegebener Jahresverbrauch
Bei Erdgas in m³: E_fuel ≈ Volumen × 10 kWh/m³
Bei Heizöl in Litern: E_fuel ≈ Volumen × 10 kWh/l
```

Einheit/Energieträger müssen zusammenpassen. LPG-Liter werden nicht mit dem Öl-Faktor umgerechnet. Ein Nutzerwert hat Vorrang vor LLM-Extraktion.

**Beleg und bessere Daten:** Die Bundesnetzagentur beschreibt `E = V × Brennwert × Zustandszahl`. Brennwert und Zustandszahl stehen auf der Rechnung beziehungsweise stammen vom Netzbetreiber. Beispielsweise ergeben frei gewählte 2.000 m³ × 11,2 kWh/m³ × 0,95 genau 21.280 kWh; der aktuelle Faktor 10 ergäbe 20.000 kWh. Dies ist ein Rechenbeispiel, kein typischer örtlicher Brennwert. [Bundesnetzagentur][Q1]

Das bayerische Behördenportal ordnet 10 kWh pro m³ und ungefähr pro Liter Heizöl ausdrücklich als überschlägige Größen ein. [Verbraucherportal Bayern][Q2]

**Offen:** Abrechnungszeitraum, Teiljahre, Heizwert/Brennwertbezug, Öl-Tankbestände und separate Brennstofffaktoren. Eine Öllieferung ist nicht automatisch der Verbrauch desselben Jahres.

### M02 – UsefulHeatModule / useful_heat

**Code:** [useful_heat.py](../heat_pump_ready/calculation/modules/useful_heat.py).

**Eingabe:** Energieträger. **Abhängigkeit:** annual_consumption. **Output:** kWh/a.

```text
η = Q_useful / E_fuel
Q_useful = E_fuel × η
Aktuell η = 0,88
Beispiel: 24.000 × 0,88 = 21.120 kWh/a
```

Die Formel folgt aus der Definition des Nutzungsgrades. **Der Wert 0,88 kommt ausschließlich aus der Challenge**, nicht aus einer Herstellerberechnung für den vorhandenen Kessel. Für Gas, Öl und LPG angewandt; Fernwärme und direkte Elektroheizung bleiben unbekannt.

**Ermittlung für ein reales Haus:** Thermischen Ertrag und Brennstoffenergie über dieselbe Periode und dieselbe Bilanzgrenze messen oder ein geeignetes fachliches Anlagenmodell verwenden. Ein punktuell gemessener Abgasverlust ist nicht gleich Jahresverlust durch Abgas, Bereitschaft, Taktung und Verteilung. Der Nenner muss zum Heizwert-/Brennwertbezug passen. Ein Faktorwechsel ohne diese Klärung wäre Scheingenauigkeit.

### M03 – HotWaterDemandModule / hot_water_demand

**Code:** [hot_water_demand.py](../heat_pump_ready/calculation/modules/hot_water_demand.py).

**Eingaben:** Personenanzahl und Warmwasser über Heizung. **Abhängigkeit:** keine. **Output:** kWh/a des betrachteten Heizsystems.

```text
Warmwasser separat: Q_ww = 0
Warmwasser zentral: Q_ww = Personen × 1.000 kWh/(Person·a)
Warmwasser unbekannt oder zentrale Personenanzahl fehlt: missing_input
Beispiel: 3 × 1.000 = 3.000 kWh/a
```

Null bei separater Erzeugung bedeutet nicht, dass der Haushalt kein Warmwasser verbraucht, sondern dass dieses nicht von der betrachteten Heizung bereitgestellt wird.

**Herkunft:** Der konkrete Pauschalwert stammt aus der Challenge. Die öffentliche Beschreibung des BWP-Rechners unterscheidet Verfahren nach Personen, Fläche und Nutzungseinheiten; sie belegt nicht unseren festen Wert. [dena/Gebäudeforum][Q5]

**Physikalische Herleitung für die Weiterentwicklung:** `Q = Masse × spezifische Wärmekapazität × Temperaturhub`, über alle Entnahmen im Jahr summiert; Speicher-/Zirkulationsverluste und Solarwärme zusätzlich bilanziert. Dafür benötigt man Volumen, Temperaturen, Nutzungsprofil und Systemgrenze. Aus der Physik allein lässt sich ohne diese Angaben kein pauschaler Jahreswert pro Person ableiten. 1.000 wird daher nicht nachträglich als „offiziell berechnet“ bezeichnet.

**Wichtig für B-02:** Solarthermie kann den vom Gas zu deckenden Warmwasseranteil reduzieren. Der pauschale volle Abzug ist dort ungeprüft.

### M04 – SpaceHeatingDemandModule / space_heating_demand

**Code:** [space_heating_demand.py](../heat_pump_ready/calculation/modules/space_heating_demand.py).

**Abhängigkeiten:** useful_heat, hot_water_demand. **Output:** kWh/a.

```text
Q_space = Q_useful − Q_ww
Beispiel: 21.120 − 3.000 = 18.120 kWh/a
```

Das ist eine Bilanz, keine zusätzliche empirische Konstante. Negative Ergebnisse bleiben erhalten und werden vom Validator als Widerspruch markiert.

**Offen:** Bei zusätzlichem Holzofen ist der berechnete Rest nur der vom bilanzierten Kessel gedeckte Anteil. Der gesamte Gebäudewärmebedarf ist damit nicht erfasst. Unbeheizte Räume und unvollständige Verbrauchsperioden verändern die Aussage ebenfalls.

### M05 – ConsumptionHeatLoadModule / heat_load_consumption

**Code:** [heat_load_consumption.py](../heat_pump_ready/calculation/modules/heat_load_consumption.py).

**Abhängigkeit:** space_heating_demand. **Output:** kW.

```text
h_full = Jahres-Raumwärme / Auslegungsleistung
P_consumption ≈ Q_space / h_full
Aktuell h_full = 2.000 h/a
Beispiel: 18.120 / 2.000 = 9,06 kW
```

Volllaststunden sind äquivalente Stunden bei voller Leistung, nicht die tatsächlichen Einschaltstunden einer modulierenden Heizung.

DIN Media beschreibt ein überschlägiges Verfahren aus Wärmemengen-/Verbrauchsmessungen in DIN/TS 12831-1. Die öffentliche Beschreibung bestätigt nicht, dass genau 2.000 h für jedes Haus gelten. [DIN Media][Q4]

**Wie der Faktor fachlich entstehen müsste:** passende Klimadaten, Nutzungsbedingungen, Heizgrenze, Gebäudecharakteristik und eine definierte Methode verwenden. Alternativ lässt sich aus unabhängiger Referenzlast und gemessenem Raumwärmebedarf ein beobachteter Vergleichswert `h_full = Q/P_ref` bestimmen. Diesen nicht pro Eval-Fall nachträglich so wählen, dass die Referenz getroffen wird.

**Weiterentwicklung Witterung:** Der DWD definiert Klimafaktoren aus Referenzgradtagen und den örtlichen Gradtagwerten eines Zeitraums. Postleitzahl und gleitende Zwölfmonatsperiode sind relevant. Der Referenzort ist bei diesem Datensatz Potsdam. Das ist eine Verbrauchsnormierung, keine unmittelbare lokale Norm-Heizlast. [DWD-Datensatzbeschreibung][Q6] Der BWP hat Klimadaten in seinen Verbrauchsrechner integriert. [BWP][Q11]

### M06 – AreaHeatLoadModule / heat_load_area

**Code:** [heat_load_area.py](../heat_pump_ready/calculation/modules/heat_load_area.py).

**Eingaben:** Fläche, Baujahr, Sanierungsstatus. **Abhängigkeit:** keine. **Output:** (Untergrenze, Obergrenze) in kW.

```text
P_low  = A × q_low / 1.000
P_high = A × q_high / 1.000
Beispiel: 180 m² × (40–60 W/m²) / 1.000 = 7,2–10,8 kW
```

Aktuelle Reihenfolge der Bedingungen:

| Priorität | Bedingung im Code | W/m² | Status |
|---|---|---:|---|
| 1 | low_energy | 15–40 | Challenge-Richtwert |
| 2 | fully ODER Baujahr ≥ 2002 | 40–60 | Challenge-Richtwert; pauschale Zuordnung |
| 3 | Baujahr < 1979 UND unrenovated | 120–180 | Challenge-Richtwert |
| 4 | 1980–1999 UND unrenovated | 80–120 | Challenge-Richtwert; zusätzliche Einschränkung im Code |
| 5 | Baujahr bekannt, keine obige Klasse | 40–180 | Eigener Demo-Fallback |
| 6 | Fläche fehlt oder keine Klasse bestimmbar | kein Wert | missing_input |

Baujahr 1979, 2000/2001, alte teilsanierte Häuser und unbekannte Sanierung landen häufig im Demo-Fallback. Baujahr ab 2002 überschreibt faktisch eine unklare Sanierungsangabe. Die Spanne ist **kein statistisch kalibriertes Konfidenzintervall**.

**Wie q belastbarer entsteht:** Zunächst Heizlast aus Hüllflächen, U-Werten, Innen-/Außentemperaturen, Lüftung und gegebenenfalls weiteren Zuschlägen ermitteln, anschließend `q = 1.000 × P / A`. Vereinfacht: `P_transmission = Σ(U_i × A_i × ΔT_i)`; Lüftung hängt unter anderem von Luftvolumenstrom und Temperaturdifferenz ab. Das ist ein erklärendes physikalisches Schema, keine vollständige Normrechnung. [Bosch: Heizleistungsbestandteile][Q12]

Die Fläche A in U×A ist die jeweilige Hüllfläche; sie ist nicht pauschal die beheizte Grundfläche. Die recherchierten Quellen liefern keinen allgemeinen Beleg für genau unsere vier W/m²-Tabellenzeilen.

### M07 – AnnualPerformanceFactorModule / annual_performance_factor

**Code:** [annual_performance_factor.py](../heat_pump_ready/calculation/modules/annual_performance_factor.py).

**Eingabe:** Heizflächenart und benötigte Vorlauftemperatur. **Abhängigkeit:** keine. **Output:** JAZ.

| Aktueller Fall | Ergebnis |
|---|---:|
| Fußbodenheizung, Temperatur fehlt | 4,0; Betrieb ungefähr 35 °C angenommen |
| Fußbodenheizung, Temperatur ≤ 35 °C | 4,0 |
| Bekannte Heizflächen, Temperatur ≤ 55 °C | 3,5 |
| Bekannte Heizflächen, 55 < Temperatur ≤ 60 °C | 2,8 |
| Temperatur > 60 °C oder sonstige notwendige Angaben fehlen | unbekannt |

Die Funktion berechnet die JAZ nicht aus einem konkreten Gerät. Sie ordnet Challenge-Werte zu. Bei gemischter Heizung gilt im MVP der eingegebene gemeinsame Vorlauf; die tatsächliche Hydraulik ist nicht modelliert.

Das UBA definiert die JAZ als jährlich abgegebene Wärmemenge geteilt durch die eingesetzte elektrische Energie. Der COP gilt dagegen für einen Betriebspunkt und darf nicht ungeprüft als JAZ eingesetzt werden. [Umweltbundesamt][Q3]

Die offizielle VDI-Vorschau weist eigene Abschnitte für Bilanzgrenzen, Raumheizung, Trinkwasser, Solarunterstützung und Gesamtjahresarbeitszahl aus. Die drei Konstanten ersetzen diese Anlagenbetrachtung nicht. [VDI 4650 – offizielle Vorschau][Q7]

Fraunhofer ISE berichtet im Feldprojekt 2025 für Luft/Wasser-Anlagen einen Mittelwert von 3,4 und eine Spanne 2,6–4,9. Das belegt reale Streuung, nicht die Richtigkeit einer exakten temperaturabhängigen Zuordnung für unser Haus. [Fraunhofer ISE][Q10]

### M08 – CurrentEnergyCostModule / current_energy_cost

**Code:** [current_energy_cost.py](../heat_pump_ready/calculation/modules/current_energy_cost.py).

**Abhängigkeit:** annual_consumption. **Output:** €/a.

```text
C_old = E_fuel × p_fuel
Erdgas: p = 0,11 €/kWh
Heizöl: p = 0,17 €/kWh
Beispiel Gas: 24.000 × 0,11 = 2.640 €/a
```

Bei Öl folgt 0,17 aus den Challenge-Annahmen 1,70 €/l ÷ 10 kWh/l. Wird der Energieumrechnungsfaktor später geändert, muss der Preisbezug konsistent bleiben oder direkt in Litern gerechnet werden.

Gas-, Öl- und Strompreise sind vorgegebene Vergleichspreise, keine extern verifizierten aktuellen Tarife. LPG, Fernwärme und Elektroheizung liefern hier unbekannt. Grundpreise und weitere laufende Kosten fehlen.

### M09 – HeatPumpEnergyCostModule / heat_pump_energy_cost

**Code:** [heat_pump_energy_cost.py](../heat_pump_ready/calculation/modules/heat_pump_energy_cost.py).

**Abhängigkeiten:** useful_heat, annual_performance_factor. **Output:** €/a.

```text
E_electric = Q_useful / J
C_hp = E_electric × p_electric
Beispiel: 21.120 / 3,5 = 6.034,285714 kWh/a Strom
C_hp = 6.034,285714 × 0,26 = 1.568,914286 €/a
```

Die Division ergibt sich algebraisch aus der JAZ-Definition, nicht aus einem zusätzlichen Wirkungsgradfaktor. [Umweltbundesamt][Q3]

Warmwasser bleibt in der zu ersetzenden Gesamtwärme enthalten. Der Warmwasserabzug aus M04 darf hier nicht erneut den Lieferumfang verkleinern.

**Vereinfachung:** Eine JAZ wird für Heizung und Warmwasser gemeinsam verwendet. Für eine spätere getrennte Bilanz wäre `E = Q_space/J_space + Q_ww/J_ww` eine mögliche Struktur, sofern alle Systemgrenzen und zusätzlichen elektrischen Verbraucher konsistent erfasst sind. Diese Formel ist ein Entwicklungsvorschlag, keine bereits implementierte VDI-Berechnung.

### M10 – AnnualSavingsModule / annual_savings

**Code:** [annual_savings.py](../heat_pump_ready/calculation/modules/annual_savings.py).

**Abhängigkeiten:** current_energy_cost, heat_pump_energy_cost. **Output:** €/a.

```text
S = C_old − C_hp
Beispiel: 2.640 − 1.568,914286 = 1.071,085714 €/a
```

Negative Ersparnis ist erlaubt und bedeutet höhere modellierte Energiekosten. Dies sind nicht die gesamten jährlichen Einsparungen einschließlich Wartung, Finanzierung oder Grundgebühren.

### M11 – NetInvestmentModule / net_investment

**Code:** [net_investment.py](../heat_pump_ready/calculation/modules/net_investment.py).

**Eingaben:** Investition und Förderung. **Output:** €.

```text
I_net = I_gross − G
Beispiel: 20.000 − 8.000 = 12.000 €
```

Beide Angaben müssen explizit vorliegen, einschließlich 0 € Förderung. Fehlende Förderung wird nicht als null interpretiert. Förderung über Investition erzeugt einen negativen Wert, den der Validator beanstandet.

8.000 € sind ausschließlich synthetische Demonstrationsdaten. Es gibt keine Berechnung oder Prüfung eines Förderanspruchs. Für einen realen Vergleich sind verbindliche Angebote, gleicher Leistungsumfang und die alternative Investition zu klären.

### M12 – PaybackPeriodModule / payback_period

**Code:** [payback_period.py](../heat_pump_ready/calculation/modules/payback_period.py).

**Abhängigkeiten:** annual_savings, net_investment. **Output:** Jahre oder `no_finite_payback`.

```text
Für S > 0: t_pb = I_net / S
Für S ≤ 0: no_finite_payback
Beispiel: 12.000 / 1.071,085714 = 11,203584 Jahre
```

Immer `demonstration=True`. Es werden konstante jährliche Einsparungen und keine weiteren Zahlungen angenommen. Der Grenzfall I_net=0 und S=0 wird derzeit ebenfalls als keine endliche Amortisation ausgegeben; das muss semantisch geklärt werden.

Die öffentliche VDI-2067-Vorschau unterscheidet kapital-, bedarfs-, betriebsgebundene und sonstige Kosten sowie die Annuitätenmethode. Unsere Quotientenrechnung ist keine VDI-2067-Implementierung. [VDI 2067 – offizielle Vorschau][Q8]

**Weiterentwicklung:** Vergleichsvarianten mit gleicher Funktion definieren und Zahlungsströme über den Betrachtungszeitraum erfassen. Eine Kapitalwert- oder Annuitätenrechnung benötigt zusätzlich Zinssatz, Zeitpunkte, Ersatzinvestitionen, Restwert und laufende Kosten. Dafür keine scheinbar offiziellen Defaults erfinden.

### M13 – HorizonModule / horizon

**Code:** [horizon.py](../heat_pump_ready/calculation/modules/horizon.py).

Übernimmt `horizon_years` unverändert als Kennzahl, damit der Validator nur den Output lesen muss. Standard 20 Jahre, formaler Eingabebereich 1–50 Jahre. Die Zahl 20 ist ein UI-Standard, keine bestätigte Lebensdauer der gesamten Anlage und keine Amortisationsgarantie.

### M14 – RadiatorTypeModule / radiator_type

**Code:** [radiator_type.py](../heat_pump_ready/calculation/modules/radiator_type.py).

Keine numerische Rechnung. Für genau ein Heizkörperfoto darf der LLMRunner den Typ 11, 22 oder 33 als String liefern; sonst unbekannt. Bei mehreren Heizkörperfotos verweigert der MVP eine einzelne pauschale Zuordnung. Der Typ fließt derzeit nicht in eine Leistungsberechnung ein.

**Nötiger nächster Schritt:** Herstellerleistung, Maße, Temperaturpaar und Raumlast erfassen. Kermi zeigt für passende Randbedingungen 75/65/20 gegenüber 55/45/20 eine Umrechnung `P = P_norm/F`, mit F=1,96 im gezeigten Beispiel: 1.960 W werden 1.000 W. „Bei 55 °C halbe Leistung“ gilt also nicht ohne Rücklauf, Raumtemperatur und passende Produktkennwerte. [Kermi – technische Unterlage][Q9]

### M15 – PipeSystemModule / pipe_system

**Code:** [pipe_system.py](../heat_pump_ready/calculation/modules/pipe_system.py).

Keine numerische Rechnung. Bekannte Nutzerangabe wird übernommen, andernfalls passende Rohrbilder per Runner ausgewertet. Erlaubte Kategorien: `single-pipe` und `two-pipe`; nicht belegbar → unbekannt. Die Modellkonfidenz ist eine Selbsteinschätzung, keine kalibrierte Wahrscheinlichkeit.

Herkunft der Erkennungsheuristiken ist die Challenge. Für eine fachliche Validierung werden Installateurbestätigung, Ventilunterlagen und Leitungsverlauf benötigt. Ein Foto mit zwei Anschlüssen allein ist kein Systemnachweis. Es wurde keine offizielle Quelle gefunden, die unsere konkreten LLM-Prompts als zuverlässige Klassifikation bestätigt.

## 6. Validator: eigene Regeln, keine weiteren Berechnungsmodule

**Code:** [validator.py](../heat_pump_ready/validator.py).

- Negative Werte sind außer bei Ersparnis unplausibel; nicht endliche Werte und umgekehrte Spannen werden beanstandet.
- Heizlastkonflikt aktuell bei `P_consumption > 2 × P_area_high` oder `2 × P_consumption < P_area_low`. Faktor 2 ist eine eigene Demoheuristik.
- Grün aktuell bei verfügbarer JAZ, bestätigtem Zweirohrsystem und keinen Plausibilitätsproblemen. Das prüft keine Raumleistungsdeckung.
- Wirtschaftlich positiv bei vollständigen Pflichtkennzahlen, keiner entscheidungsrelevanten unbestätigten Extraktion, positiver Ersparnis, Amortisation ≤ Horizont und technischer Ampel Grün.
- Bei negativer Ersparnis oder zu langer Amortisation wirtschaftlich negativ im Modell; sonst offen.

**Offene Inkonsistenzen:** Eine fehlende Heizlast verhindert technisches Grün nicht zwingend. Nicht jede Unsicherheitsquelle wird geprüft. Unbekanntes Rohrsystem bei Fußbodenheizung führt pauschal zu Gelb. Die Freitexthinweise aus den dev-Daten beeinflussen keine dieser Regeln. Diese Punkte stehen in der [Checkliste](OFFENE_PUNKTE.md).

## 7. Vollständiges Rechenbeispiel

Synthetisch, keine Förder- oder Preisempfehlung:

| Stufe | Rechnung | Ergebnis |
|---|---|---:|
| Verbrauch | 24.000 kWh gegeben | 24.000 kWh/a |
| Nutzwärme | 24.000 × 0,88 | 21.120 kWh/a |
| Warmwasser | 3 × 1.000 | 3.000 kWh/a |
| Raumwärme | 21.120 − 3.000 | 18.120 kWh/a |
| Verbrauchsheizlast | 18.120 / 2.000 | 9,06 kW |
| Flächenheizlast | 180 × (40–60) / 1.000 | 7,2–10,8 kW |
| JAZ | Heizkörper, 50 °C → Tabelle | 3,5 |
| Kosten bisher | 24.000 × 0,11 | 2.640 €/a |
| Kosten Wärmepumpe | 21.120 / 3,5 × 0,26 | 1.568,914286 €/a |
| Ersparnis | Differenz | 1.071,085714 €/a |
| Nettoinvestition | 20.000 − 8.000 | 12.000 € |
| Amortisation | 12.000 / 1.071,085714 | 11,203584 Jahre |
| Horizont | Nutzerwert | 20 Jahre |

Erst danach interpretiert der Validator. Dezimalstellen im Test dienen der Reproduzierbarkeit, nicht einer behaupteten Prognosegenauigkeit.

## 8. Schlussfolgerung für die Weiterarbeit

Formeln und Konstanten nicht gemeinsam als „validiert“ abhaken. Drei getrennte Fragen prüfen: Ist die Rechenoperation richtig implementiert? Ist der Faktor für diesen Anwendungsfall begründet? Reichen Daten und Modellgrenzen für die Entscheidung? Die Umsetzung erfüllt bereits Teile der ersten Frage; zweite und dritte benötigen die Arbeitspakete und Daten aus [TESTPROTOKOLL.md](TESTPROTOKOLL.md).

[Q1]: https://www.bundesnetzagentur.de/DE/Vportal/Energie/RechnungenSperrungen/start.html
[Q2]: https://vis.bayern.de/produkte_energie/preise_kosten/strom_gasrechnung.htm
[Q3]: https://www.umweltbundesamt.de/themen/klima-energie/erneuerbare-energien/umgebungswaerme-waermepumpen
[Q4]: https://www.dinmedia.de/de/vornorm/din-ts-12831-1/316645651
[Q5]: https://www.gebaeudeforum.de/service/toolbox/heizlastrechner/
[Q6]: https://opendata.dwd.de/climate_environment/CDC/derived_germany/techn/monthly/climate_correction_factor/recent/BESCHREIBUNG_derivgermany_techn_monthly_climate_correction_factor_recent_de.pdf
[Q7]: https://www.vdi.de/fileadmin/pages/vdi_de/redakteure/richtlinien/inhaltsverzeichnisse/3497537.pdf
[Q8]: https://www.vdi.de/fileadmin/pages/vdi_de/redakteure/richtlinien/inhaltsverzeichnisse/1885127.pdf
[Q9]: https://www.kermi.com/media/documents/KITI_PL_Konvektoren_I-2025_DE.pdf
[Q10]: https://www.ise.fraunhofer.de/de/presse-und-medien/presseinformationen/2025/waermepumpen-heizen-auch-im-altbau-klimafreundlich-forschungsprojekt-des-fraunhofer-ise-abgeschlossen.html
[Q11]: https://www.waermepumpe.de/presse/pressemitteilungen/details/update-fuer-den-bwp-heizlastrechner/
[Q12]: https://www.bosch-homecomfort.com/de/de/wohngebaeude/wissen/heizungsratgeber/heizleistung-berechnen/
