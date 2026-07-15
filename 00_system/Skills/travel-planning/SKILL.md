---
name: "travel-planning"
description: "Travel planning assistant — loads preferences, asks targeted clarifying questions if info is missing, then produces a structured trip plan with hotel, itinerary, culture, nightlife, and dance recommendations."
---

# Travel Planning Skill

Produce a structured, preference-aware travel plan for a new destination. Load the user's travel preferences first, ask clarifying questions for anything missing, then generate a full plan.

---

## Step 1: Load Context

Read these files before doing anything else:

1. `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Travel/travel_preference.md` — core preferences, decision-making process, aesthetic profile, hard requirements
2. `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/02_wiki/CreativityCuriosity/Aesthetic-Intelligence.md` — full aesthetic taste profile for sightseeing and performance filtering
3. Check `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Travel/` for any existing trip folder relevant to this destination — do not repeat planning already done

---

## Step 2: Assess What You Know

From the user's message and loaded context, determine what is already known vs. missing. The required inputs are:

**Required to proceed:**
- [ ] Destination city/country
- [ ] Travel dates (or approximate duration)
- [ ] Primary purpose / anchor event (or confirm there isn't one)

**Important but can be inferred or asked:**
- [ ] Solo or with others? (default: solo, per preference doc)
- [ ] Any people joining mid-trip? (e.g., family dinner)
- [ ] Budget range for hotels (default: €100–130/night per preference doc)
- [ ] Cities/landmarks already visited (to avoid retreading)
- [ ] Any specific interests for this trip (event, performance, exhibition)
- [ ] Flight return date fixed or flexible?

**If any required input is missing, ask before proceeding.** Do not generate a plan with unknown destination or dates. Ask all missing required questions in a single message — do not ask one at a time.

---

## Step 3: Ask Clarifying Questions (if needed)

If information is incomplete, ask in this format — concise, grouped, no more than 5 questions at once:

```
Before I build the plan, a few things I need:

1. [Question]
2. [Question]
...

Everything else I'll pull from your travel preferences.
```

If all required info is present, skip this step entirely and move directly to Step 4.

---

## Step 4: Research

Use web search to fill gaps the preference doc cannot answer. Always research:

1. **Anchor event** — confirm dates, key schedule moments (parade time, opening/closing ceremonies)
2. **Hotel options** — search for quiet hotels in non-epicenter neighborhoods; filter by preference doc criteria (€100–130, high floor available, non-smoking, well-connected by Metro)
3. **National ballet / contemporary dance** — what's running at the national company venue during travel dates; any world premieres
4. **Professional ballet drop-in classes** — Vaganova-method studios, intermediate/advanced adult level, comparable to Henry Jurrien (Amsterdam) / Maemero (Berlin)
5. **LGBTQ+ infrastructure** — gay neighborhood, top saunas, key bars/drag shows if first visit
6. **Day trip options** — high-speed rail destinations 30–90 min away; filter for architectural/cultural depth per aesthetic profile
7. **Museum programme** — check if any special exhibitions running that intersect the aesthetic profile; confirm permanent collection highlights

---

## Step 5: Generate the Plan

Structure the output as follows. Adapt sections to what's relevant — omit sections that don't apply.

---

### [City] Trip Plan — [Dates]

**Anchor:** [Primary event/purpose]
**Duration:** [N nights]
**Travelling:** Solo / [with X on dates Y]

---

#### Open Questions

List any decisions still pending before the trip. Place this first so it's visible on every read. Keep it short — 2–4 items max. Remove items as they're resolved.

---

#### Hotel Recommendations

Shortlist of 3–5 options. For each: neighborhood, price, key reason it fits the preference doc, any booking notes (room type to request, etc.).

Flag: which to book first (usually sells out fastest during events).

---

#### Heat / Climate Protocol

If destination is hot (30°C+): state the daily protocol explicitly.
- Morning window (outdoor)
- Afternoon window (indoor — museums, class, hotel)
- Evening window (outdoor)

---

#### Day-by-Day Itinerary

One section per day. Each day has:
- AM / PM / Evening structure
- Specific venues with addresses where useful
- Booking requirements flagged inline
- Note if day is high-energy (event, nightlife) vs. recovery

Apply the aesthetic profile filter: for museums, name the specific rooms/works worth prioritising, not just the institution.

---

#### Dance & Performance

- **Main performance:** What's running at the national company / main contemporary venue. Include dates, venue, what makes it worth seeing (connect to aesthetic profile).
- **Drop-in class:** Best studio option, method, schedule, how to book.
- **Other:** Any fringe or festival dance programming worth checking.

---

#### LGBTQ+ Infrastructure

*(Include if destination has a gay scene or if LGBTQ+ events are part of the trip)*

- **Neighborhood:** Name and what it's known for
- **Saunas:** Top 2–3, with crowd profile and best timing
- **Bars / drag:** Key venues, especially for a first visit
- **Event-specific notes:** If Pride or circuit event is running, timing guidance for saunas and nightlife (packed vs. relaxed windows)

---

#### Day Trips

For each option:
- Destination, travel time, transport
- What makes it relevant to the aesthetic profile
- Recommended depth (half day / full day / overnight)
- Ranked recommendation if multiple options

---

#### Food & Dining Notes

- Local rhythm (meal times)
- Neighbourhood for tapas/bar-hopping
- Restaurant recommendation for any group/family dinner — with booking note
- Market or casual lunch option

---

#### Booking Checklist

Ordered by urgency:

| Item | Timing | Notes |
|------|--------|-------|
| Hotel | Now | [specific booking note] |
| [Dinner reservation] | Now | [reason: fills up] |
| [Museum tickets] | Soon | [online, skip queue] |
| [Train / day trip] | ~1 week before | [via which app/site] |
| [Class] | On arrival | [check schedule] |

---

#### Open Questions (bottom duplicate — remove when closing out a plan)

*Mirrored at top of document. Update the top section; remove this one once all questions are resolved.*

---

## Key Rules

- Always load `travel_preference.md` first — never plan from scratch without it
- Never repeat tourist-circuit content the user has already done (check the "Trips Already Done" section)
- Apply the aesthetic profile filter to every museum and performance recommendation — generic "must-see" lists are not useful
- Flag heat protocol explicitly for summer/hot destinations
- Family dinner logistics get their own note when family is joining
- Keep the itinerary realistic: one museum per afternoon, recovery days after high-stimulus nights
- If the anchor event is a Pride festival: treat it as a full scheduling constraint, not just one item among many
- Use [[wiki-link]] format when referencing KMS pages
- End every plan with a booking checklist ordered by urgency
