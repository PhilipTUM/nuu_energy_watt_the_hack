### nuuEnergy Challenge: **Heat Pump Ready?  Can AI tell you if your home is ready for clean heating?**

Many homeowners are unsure whether a heat pump would work in their home. Getting a reliable answer usually requires an on-site assessment, leaving uncertainty about costs, renovations, and suitability.

!image.png

**Your challenge:** Build an AI-powered tool that provides an honest first assessment in under three minutes using an energy bill, building age, address, and smartphone photos. Estimate heating needs, assess heat pump suitability, and clearly explain what a professional still needs to check.


# Heat Pump Ready? nuuEnergy Challenge

<aside>
⚡

**Track:** Buildings & Everyday Energy · **Challenge partner:** nuuEnergy

Build an AI tool that gives a homeowner an honest first heat-pump-readiness assessment in under three minutes, from data they already have.

</aside>

Most homeowners never get past the very first question *“Would a heat pump even work in my home?”* 

Your job: use the information a homeowner already has (energy bill, building age, heating system, address, a few photos) to give a **transparent first answer** and clearly flag what still needs to be checked by a professional technician.

---

## Quick links

Heat Pump Ready? One-Pager

Your Mission

Technical Guardrails

Data Provided

Deliverables & Bonus

Evaluation Criteria

Prize

## At a glance

| Topic | Summary |
| --- | --- |
| **Goal** | First readiness assessment in < 3 minutes |
| **Inputs** | Energy bill, building age, address, photos |
| **Output** | Green / yellow / red + short reason |
| **Data** | 5 buildings (3 dev, 2 eval) as CSV + JSON |
| **Prototype** | Runs locally in a standard browser |
| **Top criteria** | Technical execution (25) · Problem-solution fit & user value (25) |
| **Prize 🏆** | €1,000 + a table football ⚽️ + a Tech Day with the nuuEnergy product team |

<aside>
💡

Honesty over precision: a tool that says *“I can’t tell from this data, a technician must check X and Y”* beats one that returns a confident wrong number.

</aside>


Heat Pump Ready? One-Pager
Track: Buildings & Everyday Energy · Challenge partner: nuuEnergy
The problem
Millions of homes still heat with gas or oil. Heat pumps are the cleaner alternative and work in far more existing buildings than people think. Yet most homeowners never get past the first question: "Would a heat pump even work in my home?" Today, only a technician's visit answers it.
Your challenge
Build a tool that gives a homeowner an honest first answer in under three minutes, using only what they already have: their energy bill, a few facts about the building and some smartphone photos.
The result must tell the homeowner:
Ready or not? Green / yellow / red, with a reason they understand
What's still open? What the tool can't tell, and what a technician has to check on site
How you get there is up to you.
What you get
5 real example buildings (CSV + JSON): 3 come with nuuEnergy's reference values to build and calibrate on, for 2 the jury keeps the reference values hidden
Fixed assumptions, so all cost comparisons are comparable:
Assumption
Value
Heat-pump electricity
26 ct/kWh
Natural gas
11 ct/kWh
Heating oil
1.70 €/litre (≈ 17 ct/kWh)
Heat-pump efficiency (JAZ)
4.0 underfloor heating · 3.5 radiators up to 55 °C · 2.8 radiators 55–60 °C
Background reading: 🔁Background: Single-pipe vs. two-pipe heating​
What you deliver
A working prototype that runs in the browser
Your results for the 2 evaluation buildings, shown in the pitch
A live demo, not slides
How we judge
Criterion
Points
Technical execution & reliability
25
Problem-solution fit & user value
25
Explainability & handling uncertainty
20
Innovation & smart use of technology
15
Feasibility & scalability
15
A tool that says "I can't tell from this data, a technician must check X and Y" beats one that returns a confident wrong number.
Prize
€1,000 in cash · a soccer table · a Tech Day with the nuuEnergy product team
Key terms


# Background: Single-pipe vs. two-pipe heating

<aside>
💡

One field in the dataset is `pipe_system` (two-pipe / single-pipe / unknown). This page explains what that means, why it matters for heat pumps and why it is often hard to tell from photos.

</aside>

## The difference in one sentence each

- **Two-pipe system (Zweirohrheizung):** every radiator gets hot water from a shared supply pipe and sends the cooled water back through a separate return pipe. All radiators get water at roughly the same temperature.
- **Single-pipe system (Einrohrheizung):** one pipe runs as a loop from radiator to radiator. Each radiator takes some water out of the loop and puts it back into the same pipe. So the water gets cooler from radiator to radiator.

Single-pipe systems were common in German buildings from the 1960s and 1970s, especially in apartment buildings. Most other buildings use two-pipe systems.

## Why it matters for heat pumps

A heat pump works most efficiently at a low flow temperature (see the JAZ values in the One-Pager).

- In a single-pipe loop, the last radiators only get water that has already cooled down. To keep those rooms warm, the system usually needs a **higher flow temperature**, which means a lower JAZ and higher running costs.
- Single-pipe loops are **harder to balance**. Water partly bypasses the radiators, so the return water stays warm, which heat pumps don't like.
- This is **not a deal-breaker**. Heat pumps can work with single-pipe systems, but a technician usually has to check things first: for example larger radiators at the end of the loop, a higher flow temperature or converting parts of the system.

Rule of thumb for your tool: a confirmed single-pipe system is rarely a clean "green" without an on-site check.

## How to spot it in photos

| What you see | What it points to |
| --- | --- |
| Valve at the top, return fitting at the bottom, two separate pipes with no connection between them | Likely two-pipe |
| One pipe running along the wall or skirting from radiator to radiator, often with a short bypass piece between the pipes | Likely single-pipe |
| One single connection at the bottom of the radiator, both pipes coming from the floor into one valve | Often single-pipe, but two-pipe versions of this valve exist |
| Compact valve block under the radiator ("H-block") with two pipes | Often can't tell: these exist for both systems. An extra adjustable port on the side (for the bypass) points to single-pipe |
| Construction year 1960s to 1970s, apartment building | Single-pipe more likely, but not proof |

## Why photos are often not enough

- **Two pipes at a radiator do not mean two-pipe.** Single-pipe radiators also have two connections.
- **The system belongs to the building, not to one radiator.** A brand-new bathroom radiator on an old single-pipe loop is still single-pipe.
- The best evidence is usually not at the radiator: how the pipes run *between* radiators, markings on the valve, or the pipe layout in the boiler room.

Even experienced installers are sometimes unsure from a single photo.

## What we expect from your tool

- If `pipe_system` is given, use it.
- If it is `unknown`, you can estimate it from photos and construction year, but **show how confident you are** and why.
- If you can't tell, say so. For example: *"Heating pipe system unclear from the photos. A technician should check whether this is a single-pipe system, because that can require a higher flow temperature."*

This is exactly what the jury means by **handling uncertainty**.

## Photo examples

<aside>
✅

Real photos from nuuEnergy projects (anonymised), each assessment confirmed by a heating installer.

</aside>

# Your Mission

## The problem

Millions of homes still heat with gas or oil. Heat pumps are the cleaner alternative and work in far more existing buildings than people think. Yet most homeowners never get past the first question: *“Would a heat pump even work in my home?”* Many wrongly assume they need underfloor heating or a full renovation.
Today, only a technician's visit answers it. That costs time and money on both sides – and sometimes the technician finds out on site that a heat pump won't work without major changes.

## Your mission

**Build a tool that gives a homeowner an honest first answer in under three minutes, using only what they already have:** their energy bill, a few facts about the building and some smartphone photos.
The goal is **not** a perfect technical calculation. It is a transparent, understandable first assessment that is honest about what it can and cannot say.

## What the result must tell the homeowner

1. **Ready or not?** Green / yellow / red, with a reason they understand.
2. **What's still open?** What the tool can't tell, and what a technician has to check on site.
**How you get there is up to you.**

## What green, yellow and red mean

- 🟢 **Green:** Likely suitable based on available information.
- 🟡 **Yellow:** Potentially suitable, but important checks remain, less data
- 🔴 **Red:** Insufficient evidence for a positive assessment.

<aside>
⚠️

**Important:** Missing data does not automatically mean a building is unsuitable. Your tool must clearly distinguish between *“there is an obstacle”* and *“we can't tell yet from this data”*.

</aside>

Four rules of thumb to get you started. Rough reference figures, not exact. **Honesty over precision:** if the data doesn't support a claim, say so and flag it.

### 1. Heating load (kW)

Two quick ways to estimate it. If you have both, show both, and show the range if they differ.

**a) Floor area × typical value per m², by building age:**

| Building | Heat load (W/m²) |
| --- | --- |
| Unrenovated, built before 1979 | 120-180 |
| Built in the 1980s-1990s | 80-120 |
| Renovated or built 2002+ | 40-60 |
| Low-energy house / new build | 15-40 |

**b) From consumption:**

1. Convert to kWh if needed: 1 litre of heating oil ≈ 10 kWh, 1 m³ of gas ≈ 10 kWh.
2. Useful heat ≈ consumption × 0.88 (the old boiler loses about 12 %).
3. Subtract hot water (the bill includes showers etc.): ~1,000 kWh per person per year.
4. ÷ ~2,000 full-load hours ≈ heat load in kW.

Above ~75 W/m², better windows or insulation may be worth it — a useful hint for the result.

### 2. Radiators

The key question: which flow temperature do the existing radiators need to keep the house warm? Heat pumps run efficiently up to about 55 °C; 55–60 °C still works, but with higher electricity consumption.

**How you turn this into green / yellow / red is up to you** – just make your logic transparent.

**Why higher temperatures cost more:** the hotter the water has to be, the harder the heat pump works. It needs more electricity to deliver the same amount of heat, so efficiency drops and operating costs go up. Many modern heat pumps can technically reach 60 °C or more, but it is the expensive way to run them. Your cost estimate should reflect this.

**Radiator output drops at lower temperatures:** at 55 °C a radiator delivers only about **half** of its rated output (usually stated for 75 °C). From the photo, estimate type and size — Type 11 / 22 / 33 = number of panels and fins — and check roughly whether the radiators can still cover the heat load.

Typical signals:

- **Underfloor heating** → good fit
- **Large or newer panel radiators** → usually fine at ≤ 55 °C
- **Small, old radiators or a single-pipe system (Einrohrheizung)** → flag as "needs checking"

### 3. Operating costs

**Heat pump:** useful heat ÷ efficiency × heat-pump electricity price

**Today:** annual consumption × current fuel price

**Efficiency (JAZ, Jahresarbeitszahl):** how many kWh of heat the heat pump makes from 1 kWh of electricity. You don't need to calculate it — **use these fixed values**, depending on the flow temperature from your radiator check:

| Heating system / flow temperature | JAZ to use |
| --- | --- |
| Underfloor heating (~35 °C) | 4.0 |
| Radiators up to 55 °C | 3.5 |
| Radiators 55–60 °C | 2.8 |

Please also use these fixed prices so all teams are comparable:

| Energy | Price for the challenge |
| --- | --- |
| ♨️ Heat-pump electricity | 26 ct/kWh |
| 🔥 Natural gas | 11 ct/kWh |
| 🛢️ Heating oil | 1.70 €/litre (≈ 17 ct/kWh) |

Show your assumptions openly in the result.

### 4. Always checked by a technician

Exact heat load, electrical capacity, and where the outdoor unit can go.

---

What does a gas bill look like? Here is a public sample bill from Stadtwerke München, the annual consumption in kWh is on the first page: SWM sample bill (PDF)

---

### Most common no-go decissions

1. Common technical no-gos

## Key terms

- **Heating load (Heizlast):** how much heating power (kW) the house needs on the coldest day of the year. Determines how big the heat pump must be.
- **Flow temperature (Vorlauftemperatur):** temperature of the water going into the radiators. The lower, the more efficient the heat pump.
- **JAZ (Jahresarbeitszahl):** how many kWh of heat a heat pump delivers per kWh of electricity over a year. JAZ 3.5 = 1 kWh electricity becomes 3.5 kWh heat.
- **Full-load hours (Volllaststunden):** how many hours the heating would run at full power to deliver one year's heat. In Germany ~2,000 h. Annual heat ÷ full-load hours = heating load.
- **Boiler efficiency (Nutzungsgrad):** share of the gas or oil that actually ends up as heat. Older boilers: ~0.88.
- **Single-pipe vs. two-pipe system (Einrohr / Zweirohr):** in a two-pipe system each radiator has its own supply and return pipe — standard and fine. In a single-pipe system the radiators are connected in series, so the water cools down from one to the next — critical for a heat pump.
- **Radiator type (Typ 11 / 22 / 33):** first digit = number of panels, second digit = number of fin layers behind them. More panels and fins = more heat output. In a photo, look at the radiator from the side or top and count the panels.
- **Underfloor heating (Fußbodenheizung, FBH):** heating pipes in the floor. Works with very low flow temperatures (~35 °C) — ideal for heat pumps, but not required.
- More detail
    - **Ideal flow temperature:** ≤ 45 °C is ideal; up to ~55 °C is efficient; 55–60 °C works with higher electricity use.
    - **Full-load hours:** realistic range is ~1,800–2,100 hours per year.
    - **Myth-busting:** underfloor heating is **not** required; a full renovation is **not** required.
    - **Full technician checklist:** exact heat load (DIN EN 12831), room-by-room radiator sizing, electrical capacity & meter cabinet, hydraulics, outdoor-unit placement, sound and permits.



    Data Provided
The dataset contains 5 real buildings from nuuEnergy projects, provided as CSV + JSON. They are anonymised: no names or addresses, PLZ reduced to area level, floor area and consumption slightly rounded.
3 development cases (buildings_dev) carry nuuEnergy's reference heating-load value (kW) and the expected readiness verdict (green / yellow / red), so teams can build and calibrate their method.
The input fields describe what a homeowner would realistically know. Empty values mean the information was not documented, just like in real life. Some cases are deliberately contradictory.
Download
buildings_dev.csv
buildings_dev.json
buildings_eval.csv
buildings_eval.json
The 5 buildings at a glance
ID
Set
Year
Area
Distribution
Pipe system
Carrier
Consumption
Location
B-01
dev
2001
195 m²
radiators
unknown
gas (LPG)
10,000 kWh
Munich area (82xxx)
B-02
dev
2005
180 m²
underfloor
unknown
gas
15,500 kWh
Munich area (82xxx)
B-03
dev
1970
200 m²
radiators
two-pipe
oil
40,000 kWh
Hamburg area (21xxx)
B-04
eval
1987
160 m²
radiators
single-pipe
oil
25,000 kWh
Munich area (85xxx)
B-05
eval
2006
125 m²
mixed
unknown
gas
27,000 kWh
Munich area (85xxx)
Reference values for the dev cases:
ID
Reference heating load
Expected verdict
B-01
9.6 kW
green
B-02
9.7 kW
green
B-03
14.5 kW
yellow
Fields
Field
Type
Example
building_id
string
B-01
construction_year
integer
1970
floor_area_m2
integer
200
renovation_status
enum (optional, often empty)
unrenovated / partially / fully
heat_distribution
enum
radiators / underfloor / mixed
annual_consumption_kwh
integer
24500
energy_carrier
enum
gas / oil / district / electric
energy_carrier_detail
string
natural gas / LPG / heating oil, approx. 2,500 litres per year
radiator_info
string
15 radiators, 12 valves need replacement
pipe_system
enum (what is this?)
two-pipe / single-pipe / unknown
flow_temperature_c
integer (optional, often empty)
55
persons_in_household
integer
3
hot_water_via_heating
boolean
yes / no
rooms
integer (optional)
11
building_notes
string
insulation, extra heat sources (e.g. wood stove), solar thermal
location
string (area-level)
Munich area (82xxx)
reference_heating_load_kw
number (dev cases only)
9.6
expected_verdict
enum (dev cases only)
green / yellow / red


# Deliverables & Bonus

## What you deliver

1. A **working prototype** that runs in the browser.
2. Your results for the 3 **evaluation buildings** (`buildings_eval`), shown in the pitch. 
3. A **live demo**, not slides.

## Bonus Challenges (optional, if time permits)

- **Read an uploaded energy bill** automatically (consumption, energy carrier, costs).
- **Installation-risk detection**: flag spatial constraints from photos (e.g. where the outdoor unit could realistically go).

# Evaluation Criteria

## Evaluation Criteria (100 points)

| Criterion | Points | What we evaluate |
| --- | --- | --- |
| 1. Technical Execution & Reliability | 25 | Does the prototype work? Are calculations technically plausible? Does it handle different building cases? |
| 2. Problem-Solution Fit & User Value | 25 | Does it solve the homeowner's actual problem? Is the assessment understandable, useful and actionable? |
| 3. Explainability & Handling Uncertainty | 20 | Are assumptions transparent? Does the tool identify missing information and avoid misleading conclusions? |
| 4. Innovation & Smart Use of Technology | 15 | Is the approach creative? Is AI used meaningfully rather than just added as a gimmick? |
| 5. Feasibility & Scalability | 15 | Could this become a real product? Can the solution work across many different homes without excessive manual effort? |
| **Total** | **100** |  |

<aside>
💡

A tool that says *“I can't tell from this data, a technician must check X and Y”* beats one that returns a confident wrong number.

</aside>