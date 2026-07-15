---
name: tuesday_rules_archive_20260604
archived: 2026-06-04
reason: Tuesday classes put on hold to reduce weekly load. Restore when ready.
---

# Archived: Tuesday Rules (pre-hold state)

## From Training_program_Scheduling_Rules.md

### Rule 1 — Weekly Volume Target (original)
> Gym: target 2x (Mon back/legs/arms + Tue chest/shoulder), **minimum 1x**. Primary slots are Mon + Tue — can shift if life intervenes, but at least one gym session must be preserved each week. Rescheduling fallback: Mon+Thu or Tue+Thu if one primary slot is blocked.

> 1x Tue evening (optional light class: improv contemporary, salsa solo, or hiphop — single only, no bundle; see R2b)

### Rule 2 — Tuesday row in Default Week table (original)
| **Tue** | Gym ~15:00 (chest/shoulder) + optional light class | 🔴+🟡 | Evening options (single only): improv contemporary 18:45, salsa solo 19:00, or hiphop 20:30. No bundle — keep Tue moderate after heavy Mon (see R2b) |

### R2b — Tuesday Sequencing Rule (original, full text)
Tuesday pairs a High gym session (chest/shoulder) with an optional light evening class. The evening is always a single class, never a bundle:

- **Default:** Gym ~15:00 (chest/shoulder) → optional light evening (one of: improv contemporary 18:45, salsa solo 19:00, or hiphop 20:30). Pick one only, no doubles.
- **If skipping evening:** Gym is the only activity — Tuesday becomes a single-High day for recovery.

Doubles rule — the Tue/Wed block contains exactly one double evening:
- **Tue = gym + evening class** → Wed = Jazz only (no Hiphop after)
- **Tue = gym only** → Wed = Jazz + optional Hiphop (double on Wed)

Monday gym (back/legs) + Iyengar always counts as a structured day regardless of Tue/Wed pattern. The Tuesday evening class is the flexible element — skip freely when energy is lower.

### Rule 9 — Choreo Cycle — Contemporary (Tue) (original)
ADC Contemporary (Tue 20:15) runs on a 4-week choreography cycle. Default attendance: Weeks 2 and 4.

---

## From Training_program_Class_Pool.md

### Tuesday Class Pool (original)
| Class | Time | Location | Intensity | Priority |
|-------|------|----------|-----------|----------|
| Mysore Ashtanga | 07:00 | Bluebird West | 🔴 High | Backup |
| HJS Ballet | 09:30 | HJS | 🔴 High | Floating |
| HJS Contemporary | 11:15 | HJS | 🔴 High | Floating |
| Ashtanga Led | 16:00 | Yoga Circle | 🔴 High | Backup |
| Ashtanga Led | 18:00 | Breathing Space | 🔴 High | Backup |
| ADC Contemporary | 18:45 | ADC | 🟡 Moderate | Primary (if no Mysore) |
| ADC Contemporary | 20:15 | ADC | 🔴 High | Primary (if no Mysore) |
| ADC Salsa Solo | 19:00 | ADC | 🟡 Moderate | Primary |
| Hiphop | 20:30 | ADC | 🟡 Moderate | Primary |
| Yin Yoga | 20:15 | Rumah Yoga | 🟢 Light | Primary (Deloading) |
| Reformer Pilates | 10:00–17:00 | KC Move / Studio 191 | 🟡 Moderate | Backup (Deloading) |

> ⚠️ **Conflict:** ADC Contemporary 18:45 and Salsa Solo 19:00 overlap — cannot do both.

---

## Restore instructions

To reinstate Tuesday:
1. In **Rule 1**: restore "Gym: target 2x (Mon back/legs/arms + Tue chest/shoulder), minimum 1x" and add back "1x Tue evening (optional light class)"
2. In **Rule 2 table**: restore Tuesday row as above
3. **Restore R2b** in full (replace the on-hold placeholder)
4. In **Class Pool Tuesday section**: remove the on-hold note, restore original table
5. In **calendar_scheduler_v3.py** `propose_week`: restore `schedule("Tuesday", tue, "Gym - Back/Leg/Arm", 15, 0, 120, "Gym", fixed=False)`
6. In **Rule 9**: reinstate Contemporary (Tue 20:15) choreo cycle tracking
