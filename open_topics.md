# Offene Themen: Ursachen der Abweichungen im Entwicklungsdatensatz

**Stand: 24. Oktober 2026**

Dieses Dokument hält die Analyse der drei vorhandenen Entwicklungsgebäude fest. Es trennt belegte Angaben, rechnerische Befunde und noch unbestätigte Ursachen. Es werden keine neuen Faktoren festgelegt und keine Berechnungen im Anwendungscode geändert.

## 1. Grundlagen und wichtigste Erkenntnis

Die Abweichungen haben wahrscheinlich unterschiedliche Ursachen:

- **B-01:** Ein erheblicher Widerspruch zwischen dokumentiertem Verbrauch und Referenzheizlast ist noch ungeklärt.
- **B-02:** Holzofen und Solarthermie sind ausdrücklich dokumentiert, fehlen aber in der aktuellen Energiebilanz.
- **B-03:** Die kleinere Überschätzung könnte durch abweichende Betriebsannahmen, Verbrauchsbedingungen oder Referenzgrenzen erklärt werden.

Ein gemeinsamer Korrekturfaktor wäre nicht begründet: B-01 und B-02 werden unterschätzt, B-03 wird überschätzt.

### Verwendete Grundlagen

- [Entwicklungsdaten JSON](data/dev_csv/buildings_dev.json)
- [Entwicklungsdaten CSV](data/dev_csv/buildings_dev.csv)
- [Berechnungskonfiguration](heat_pump_ready/config.py)
- [Verbrauchsbasierte Heizlast](heat_pump_ready/calculation/modules/heat_load_consumption.py)
- [Flächenbasierte Heizlast](heat_pump_ready/calculation/modules/heat_load_area.py)
- [Validator](heat_pump_ready/validator.py)

Die Verbrauchs- und Referenzwerte stimmen zwischen CSV und JSON überein. Die festgestellten Textkodierungsprobleme im JSON erklären diese numerischen Abweichungen nicht.

Der Vergleich bezieht sich auf die **vollständigen Entwicklungsangaben mit explizitem Feldmapping**, nicht auf die verkürzten, fest hinterlegten Browser-Beispiele. Referenzwerte werden ausschließlich zur nachträglichen Auswertung verwendet.

## 2. Aktueller Rechenweg und Ergebnisse

Für alle drei Gebäude ist Warmwasser über die Heizung angegeben. Der aktuelle Rechenweg lautet:

```text
Nutzwärme = Jahresbrennstoffverbrauch × 0,88
Warmwasser = Personenanzahl × 1.000 kWh/a
Raumwärme = Nutzwärme − Warmwasser
Heizlast ≈ Raumwärme / 2.000 h/a
```

| Gebäude | Brennstoffverbrauch | Nutzwärme | Warmwasserabzug | Raumwärmerest | Heizlast berechnet | Referenz | Relative Abweichung |
|---|---:|---:|---:|---:|---:|---:|---:|
| B-01 | 10.000 kWh/a | 8.800 kWh/a | 4.000 kWh/a | 4.800 kWh/a | 2,40 kW | 9,60 kW | −75,00 % |
| B-02 | 15.500 kWh/a | 13.640 kWh/a | 3.000 kWh/a | 10.640 kWh/a | 5,32 kW | 9,70 kW | −45,15 % |
| B-03 | 40.000 kWh/a | 35.200 kWh/a | 2.000 kWh/a | 33.200 kWh/a | 16,60 kW | 14,50 kW | +14,48 % |

Die Rechenoperationen entsprechen der implementierten Formel. Das bestätigt jedoch nicht die Eignung der Faktoren für jedes Gebäude.

### Gemeinsame offene Frage: Was genau ist die Referenz?

Der Datensatz nennt keine Berechnungsmethode, Auslegungsaußentemperatur oder genaue Bilanzgrenze der Referenzheizlasten. Ungeklärt ist insbesondere:

- Handelt es sich um eine gebäudebasierte Auslegungsheizlast oder eine verbrauchsbasierte Schätzung?
- Welche Flächen und Räume sind eingeschlossen?
- Sind Warmwasserleistung, Wiederaufheizung oder andere Zuschläge enthalten?
- Welche Innentemperaturen und Nutzungsbedingungen wurden angenommen?
- Welche Gebäudedaten lagen dem Referenzersteller zusätzlich vor?

Eine verbrauchsbasierte Schätzung bildet tatsächlichen Energieeinsatz unter bestimmten Nutzungsbedingungen ab. Eine Auslegungsheizlast kann sich auf vollständige Beheizung bei einer festgelegten Außentemperatur beziehen. Diese Ergebnisse sind nur bei geklärten Randbedingungen unmittelbar vergleichbar. Der offizielle BWP-Rechner unterscheidet mehrere Heizlastverfahren; die dena beschreibt deren Einsatz und Grenzen. [dena/Gebäudeforum: Heizlastrechner](https://www.gebaeudeforum.de/service/toolbox/heizlastrechner/)

## 3. B-01: Große, noch ungeklärte Verbrauchsdiskrepanz

### 3.1 Belegte Angaben

- Baujahr 2001, Fläche 195 m².
- Jahresverbrauch 10.000 kWh; Detailangabe: Flüssiggas/LPG.
- Vier Personen; Warmwasser über Heizung.
- Keine Sanierung dokumentiert.
- Eigentümerangaben zu U-Werten: Fenster 1,1; Außenwand 0,21; Kellerwand 0,35; Dach ungefähr 0,24; Bodenplatte ungefähr 0,35 W/(m²K).
- 14 Heizkörper mit voreinstellbaren, bereits voreingestellten Ventilen.
- Heizkörpertyp, Vorlauftemperatur und Rohrsystem nicht ausreichend dokumentiert.
- Referenzheizlast 9,6 kW; erwartete Ampel Grün.

**„Keine Sanierung dokumentiert“ bedeutet nicht automatisch „energetisch schlechter Zustand“.** Die vorhandenen Bauteilangaben müssen eigenständig betrachtet werden.

### 3.2 Warmwasserabzug verstärkt die Abweichung, erklärt sie aber nicht vollständig

Der Warmwasserabzug beträgt 4.000 von 8.800 kWh Nutzwärme, also ungefähr 45 %.

| Variante | Geschätzte Heizlast |
|---|---:|
| Aktueller Warmwasserabzug | 2,4 kW |
| Kein Warmwasserabzug | 4,4 kW |
| Referenz | 9,6 kW |

Selbst das vollständige Weglassen des Abzugs erreicht die Referenz nicht. Eine Änderung allein am Warmwasserfaktor wäre keine ausreichende Erklärung.

### 3.3 Rückwärtsrechnung zur Größenordnung

Unter unveränderten Annahmen wären für die Referenz nötig:

```text
Raumwärme = 9,6 kW × 2.000 h/a = 19.200 kWh/a
Gesamte Nutzwärme = 19.200 + 4.000 = 23.200 kWh/a
Brennstoffverbrauch = 23.200 / 0,88 ≈ 26.364 kWh/a
```

Das entspricht ungefähr dem 2,64-Fachen des dokumentierten Verbrauchs. Gegenüber dem aktuell berechneten Raumwärmerest fehlen rechnerisch 14.400 kWh/a.

Alternativ ergäben sich aus 4.800 kWh/a Raumwärme und 9,6 kW Referenz nur 500 äquivalente Volllaststunden pro Jahr. **Dieser rückwärts ermittelte Wert ist keine Empfehlung für einen neuen Modellparameter.**

### 3.4 Mögliche Ursachen und Beleglage

| Mögliche Ursache | Einordnung | Benötigter Nachweis |
|---|---|---|
| Verbrauch umfasst kein vollständiges, normal genutztes Jahr | Unbestätigte Hypothese | Abrechnungszeitraum und Verbrauch mehrerer Jahre |
| Nur Teile des Gebäudes wurden beheizt oder niedrigere Temperaturen genutzt | Unbestätigte Hypothese | Tatsächlich beheizte Räume, Nutzung und Temperaturen |
| Verbrauch oder Einheit wurde vor der Datenübergabe falsch aufbereitet | Unbestätigte Hypothese, wegen LPG gezielt prüfen | Originalrechnung und ursprüngliche Einheit |
| Referenz bezieht sich auf einen anderen Gebäude-/Leistungsumfang | Offen, Referenzmethode fehlt | Referenzberechnung |
| Zusätzliche Wärmequelle ist nicht dokumentiert | Möglich, aber keinerlei konkreter Nachweis bei B-01 | Rückfrage beim Datengeber |

**Kein aktueller LPG-Umrechnungsfehler nachgewiesen:** Die Eingabe liegt bereits in kWh vor und wird im aktuellen Modul nicht nochmals mit Faktor 10 multipliziert. Ein möglicher Einheitenfehler wäre daher bereits bei der Erstellung des Datensatzes entstanden. Die Unterscheidung LPG/Erdgas bleibt für den Kostenvergleich wichtig.

### 3.5 Flächenmethode nutzt vorhandene Informationen nicht

Die Referenz entspricht ungefähr 49,2 W/m². Das Baujahr 2001 fällt jedoch in eine Lücke unserer konkreten Gebäudeklassen. Deshalb liefert das Modul den Demo-Fallback:

```text
195 m² × 40–180 W/m² / 1.000 = 7,8–35,1 kW
```

Die U-Werte werden nicht verwendet. Die breite Spanne enthält die Referenz, ist aber kein Nachweis guter Schätzqualität. Für eine bauteilbasierte Gegenrechnung fehlen unter anderem die zugehörigen Hüllflächen.

### 3.6 Offene Prüfpunkte

- [ ] Original-LPG-Abrechnung und ursprüngliche Verbrauchseinheit prüfen.
- [ ] Zeitraum, Vollständigkeit und mehrere Verbrauchsjahre klären.
- [ ] Tatsächlich beheizte Fläche und Nutzungsbedingungen ermitteln.
- [ ] Referenzmethode und enthaltenen Leistungsumfang beschaffen.
- [ ] U-Werte mit Bauteilflächen und Herkunft ergänzen.
- [ ] Zusätzliche Wärmequellen erfragen, ohne deren Existenz vorauszusetzen.

**Vorläufige Bewertung:** Zuerst Datenumfang und Referenzbezug klären. Kleine Änderungen am Nutzungsgrad oder Warmwasserfaktor lösen die große Differenz nicht.

## 4. B-02: Dokumentierte zusätzliche Wärmequellen fehlen

### 4.1 Belegte Angaben

- Baujahr 2005, Fläche 180 m².
- Jahresverbrauch 15.500 kWh Erdgas.
- Drei Personen; Warmwasser über Heizung.
- Überwiegend Fußbodenheizung mit drei abgeglichenen Verteilern; zusätzlich ein Heizkörper.
- Ein Holzofen wird den gesamten Winter genutzt.
- Solarthermie für Warmwasser ist vorhanden.
- Referenzheizlast 9,7 kW; erwartete Ampel Grün.

### 4.2 Zwei getrennte Fehlerquellen in der Energiebilanz

**Holzofen:** Ein Teil der Raumwärme wird nicht vom Gaskessel geliefert und erscheint nicht im Gasverbrauch. Unsere Rechnung erfasst diesen Beitrag nicht.

**Solarthermie:** Ein Teil des Warmwassers kann solar erzeugt werden. Trotzdem ziehen wir die gesamten pauschalen 3.000 kWh vom gasbasierten Nutzwärmeertrag ab. Soweit dieser Bedarf bereits solar gedeckt ist, ist der Abzug aus der Gasbilanz zu groß.

Eine vereinfachte Korrekturstruktur für die Ursachenanalyse wäre:

```text
Gesamter Raumwärmebedarf
≈ bisheriger gasbasierter Raumwärmerest
  + nutzbare Holzofenwärme
  + solar gedeckter Anteil des bisher vom Gas abgezogenen Warmwasserbedarfs
```

Das ist keine bereits implementierte Formel und kein vollständiges Anlagenmodell. Bilanzgrenzen und Verluste müssten vor einer Umsetzung präzisiert werden.

### 4.3 Größenordnung der fehlenden Wärme

Bei unverändert 2.000 Volllaststunden entspricht die Referenz:

```text
9,7 kW × 2.000 h/a = 19.400 kWh/a Raumwärme
Bisher berechneter Raumwärmerest = 10.640 kWh/a
Differenz = 8.760 kWh/a
```

Holzofenbeitrag und Korrektur des Solar-Warmwasserabzugs müssten gemeinsam diese Differenz erklären, wenn alle übrigen Annahmen unverändert bleiben.

**Nur illustrative Aufteilung, keine Messwerte:**

| Solar gedeckter Anteil am bisher angesetzten Warmwasser | Dann verbleibender nutzbarer Holzofenbeitrag zur Erklärung der Differenz |
|---:|---:|
| 0 kWh/a | 8.760 kWh/a |
| 1.500 kWh/a | 7.260 kWh/a |
| 3.000 kWh/a | 5.760 kWh/a |

Die Werte dürfen nicht als nachträglich ermittelte tatsächliche Erträge in das Gebäudeprofil eingetragen werden. Sie zeigen ausschließlich, welche Größenordnung zu prüfen wäre.

Solarthermie allein reicht in diesem vereinfachten Modell nicht aus: Selbst ohne Warmwasserabzug ergäbe die Gasverbrauchsmethode nur 6,82 kW.

### 4.4 Unabhängige Flächenschätzung

```text
180 m² × 40–60 W/m² / 1.000 = 7,2–10,8 kW
```

Die Referenz von 9,7 kW liegt in dieser Spanne. Das beweist sie nicht, unterstützt aber den Verdacht, dass insbesondere die gasbasierte Verbrauchsbilanz unvollständig ist.

### 4.5 Offene Prüfpunkte

- [ ] Holzmenge, Einheit, Zeitraum und möglichst nutzbaren Wärmebeitrag ermitteln.
- [ ] Klären, welche Räume der Holzofen beheizt und ob er künftig weiterbetrieben werden soll.
- [ ] Solarthermieertrag beziehungsweise Deckungsanteil für Warmwasser beschaffen.
- [ ] Tatsächlichen gasgedeckten Warmwasseranteil bestimmen.
- [ ] Referenzumfang klären: vollständiges Gebäude und welche Rolle des Holzofens?
- [ ] Rolle und benötigte Temperatur des einzelnen zusätzlichen Heizkörpers prüfen.

**Vorläufige Bewertung:** Hier liegt die stärkste datensatzgestützte Erklärung vor. Die zusätzlichen Wärmequellen sind belegt; lediglich ihre Größenordnung ist unbekannt.

## 5. B-03: Betriebsannahmen und Verbrauchsumfang prüfen

### 5.1 Belegte Angaben

- Baujahr 1970, Fläche 200 m².
- 40.000 kWh Heizölverbrauch, entsprechend ungefähr 4.000 Litern pro Jahr.
- Zwei Personen; Warmwasser über Heizung.
- Teilweise saniert: Einblasdämmung und gedämmtes Dach.
- Doppelverglasung ohne Low-e-Beschichtung.
- Obergeschoss in den 1990ern ergänzt, derzeit nicht bewohnt.
- 15 Heizkörper; zwölf Ventile müssten ersetzt werden.
- Zweirohrsystem; Vorlauftemperatur unbekannt.
- Referenzheizlast 14,5 kW; erwartete Ampel Gelb.

### 5.2 Sensitivitätsrechnung

Die aktuelle Überschätzung beträgt 2,1 kW beziehungsweise ungefähr 14,5 %.

| Variante, jeweils übrige Annahmen unverändert | Ergebnis |
|---|---:|
| Nutzungsgrad 0,88 und 2.000 h/a | 16,60 kW |
| Nutzungsgrad 0,775 und 2.000 h/a | 14,50 kW |
| Nutzungsgrad 0,88 und 2.300 h/a | 14,43 kW |

Der exakt zur Referenz passende Stundenwert wäre ungefähr 2.290 h/a. **Weder dieser Wert noch 0,775 sind bestätigte Eigenschaften des Gebäudes.** Die Rückwärtsrechnung zeigt nur, dass die Abweichung mit veränderten Betriebsannahmen vereinbar ist.

### 5.3 Mögliche Ursachen

**Jahresnutzungsgrad:** Liefert der tatsächliche Kessel weniger Nutzwärme als pauschal angenommen, überschätzen wir die aus dem Ölverbrauch verfügbare Raumwärme. Angaben zu Kesseltyp, Alter und geeigneten Messdaten fehlen.

**Witterung und Nutzung:** Ein einzelner Verbrauchswert hängt vom Jahr und Heizverhalten ab. Eine Witterungsbereinigung findet aktuell nicht statt. Der BWP beschreibt ausdrücklich die Nutzung von DWD-Klimafaktoren, um Verbrauchsdaten auf ein langjähriges Mittel zu beziehen. [BWP: Klimafaktoren zur Heizlastermittlung](https://www.waermepumpe.de/presse/pressemitteilungen/details/klimafaktoren-des-deutschen-wetterdienstes-zur-heizlastermittlung/)

**Öl-Liefermenge statt Verbrauch:** Die Angabe „ungefähr 4.000 Liter pro Jahr“ ist ohne Tankanfangs- und Endbestand nicht unabhängig überprüfbar. Es ist nicht nachgewiesen, dass hier Liefermenge und Verbrauch verwechselt wurden; es ist ein Prüfpunkt.

**Gebäudeumfang:** Es ist unklar, ob die 200 m² und die Referenz das unbewohnte Obergeschoss vollständig einschließen.

### 5.4 Wichtig: Richtung möglicher Effekte prüfen

Wenn das Obergeschoss im Verbrauchsjahr weniger beheizt wurde, die Referenz aber vollständige Beheizung unterstellt, wäre eher eine **zu niedrige** Verbrauchsschätzung zu erwarten. Beobachtet wird eine **zu hohe** Schätzung. Der Hinweis „unbewohnt“ ist deshalb keine automatische Erklärung für das Vorzeichen unserer Abweichung.

Die Sanierungsmaßnahmen erklären ebenfalls nicht unmittelbar eine zu hohe Verbrauchsschätzung: Ihre Wirkung ist grundsätzlich bereits im tatsächlich gemessenen Verbrauch enthalten. Sie sind besonders für die unabhängige Flächen-/Gebäudeberechnung relevant.

### 5.5 Schwäche der Flächenmethode

Weil `renovation_status=partially` keiner konkreten Klasse zugeordnet wird, verwendet die Anwendung:

```text
200 m² × 40–180 W/m² / 1.000 = 8–36 kW
```

Die dokumentierten Dämmmaßnahmen werden nicht genutzt. Eine derart breite Spanne ist keine belastbare Bestätigung der Referenz von 14,5 kW.

### 5.6 Offene Prüfpunkte

- [ ] Ölverbrauch durch Lieferungen und Tankbestände überprüfen.
- [ ] Verbrauchszeitraum und mehrere Jahre beschaffen.
- [ ] Kesseltyp, Alter und Jahresnutzungsgrad beziehungsweise geeignete Messdaten klären.
- [ ] Beheizte Fläche und Behandlung des Obergeschosses in Verbrauch und Referenz abgleichen.
- [ ] Sanierungsmaßnahmen für die unabhängige Gebäudeschätzung strukturieren.
- [ ] Bedeutung des Ventiltauschs und notwendige Vorlauftemperatur fachlich prüfen.

**Vorläufige Bewertung:** Eine moderate Modell-/Betriebsabweichung ist als Erklärung möglich. Welche Annahme tatsächlich falsch ist, lässt sich aus dem Datensatz allein nicht bestimmen.

## 6. Die Ampelabweichungen haben eigene Ursachen

Heizlastfehler und Ampelfehler müssen getrennt analysiert werden.

| Gebäude | Aktuelle Ampel | Erwartete Ampel | Aktueller Entscheidungsgrund / Lücke |
|---|---|---|---|
| B-01 | Gelb | Grün | Heizlastmethoden widersprechen sich deutlich; Rohrsystem und Vorlauf fehlen. U-Werte und voreingestellte Ventile werden nicht fachlich genutzt. |
| B-02 | Gelb | Grün | Unbekanntes Rohrsystem verhindert Grün. Die abgeglichene Fußbodenheizung wird nicht hinreichend differenziert behandelt. |
| B-03 | Gelb | Gelb | Vorlauf/JAZ fehlt. Der konkret dokumentierte Ventiltausch wird als Entscheidungsgrund nicht verarbeitet. |

B-03 trifft somit die Referenzfarbe, aber noch nicht nachweislich die fachliche Begründung der Referenz. Eine reine Ampeltrefferquote verschleiert diesen Unterschied.

Die tatsächlichen Gründe der nuuEnergy-Referenzampeln sind nicht vollständig dokumentiert. Aus günstigen Indizien darf deshalb nicht rückwirkend eine sichere Erklärung der Referenzentscheidung konstruiert werden.

## 7. Gebäudeübergreifende offene Themen

- [ ] Referenzverfahren, Bilanzgrenzen und Datenstand bei nuuEnergy erfragen.
- [ ] Zusätzliche Wärmequellen strukturiert erfassen, nicht nur als ignorierten Freitext.
- [ ] Fehlende Angaben, widersprüchliche Angaben und bestätigte Hindernisse getrennt behandeln.
- [ ] Baujahrlücken und Teilsanierung im Flächenverfahren nachvollziehbar abbilden.
- [ ] Eine zu breite Ergebnisspanne nicht als erfolgreiche Validierung werten.
- [ ] Heizlastschätzung und Eignungsentscheidung getrennt überprüfen.
- [ ] Ampelgründe mit Fachurteilen vergleichen, nicht nur die Farbe.
- [ ] Faktoren nicht je Gebäude rückwärts an Referenzen anpassen.
- [ ] Vor Evaluierung Regeln und Parameter festlegen; Referenzlabels aus allen Eingaben ausschließen.

## 8. Empfohlene Reihenfolge

1. **Referenzumfang aller Gebäude klären.** Ohne vergleichbare Zielgröße bleibt jede Kalibrierung fragwürdig.
2. **B-01: Originalverbrauch und Nutzung überprüfen.** Größte ungeklärte Diskrepanz.
3. **B-02: Zusatzwärme und Solar-Warmwasserbilanz erfassen.** Konkrete, bereits belegte Modelllücke.
4. **B-03: Ölbilanz, Kessel und Flächenumfang prüfen.** Mehrere plausible, noch unbestätigte Ursachen.
5. **Erst danach Berechnungsverfahren und Validator überarbeiten.** Keine pauschale gemeinsame Korrektur.

## 9. Zugehörige Dokumente

- [Priorisierte Gesamtcheckliste](docs/OFFENE_PUNKTE.md)
- [Formeln und Quellen je Berechnungsmodul](docs/BERECHNUNGEN.md)
- [Testprotokoll und reproduzierbarer dev-Vergleich](docs/TESTPROTOKOLL.md)
- [Architekturkonzept](KONZEPT.md)

Dieses Dokument beschreibt Erkenntnisse und Prüfaufträge. Es behauptet weder eine abschließende Ursachenklärung noch eine fachliche Freigabe der Anwendung.
