# 2026-09 Upsell Sync Notes

> Prepared 2026-09-01 for sync with J.
> Source: `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3` (2-year master table).
> Scope: 1-Meta, tagged (`is_lowest_price IS NOT NULL`), economy-only, international.

## 1. LCC vs FSC gap — claim reversed

The claim "LCC improving, FSC stagnant, gap widening" is **not supported** over the last 12
months. The reverse is true.

| Month | FSC | LCC | Gap (LCC−FSC) |
|---|---|---|---|
| 2025-09 | 30.1% | 35.8% | +5.7pp |
| 2026-04 | 32.3% | 35.1% | +2.8pp |
| 2026-08 | 32.4% | 36.4% | +4.0pp |

- **FSC improved** 30.1 → 32.4 (+2.3pp, step-up around Apr 2026) — not stagnant.
- **LCC roughly flat** 35.8 → 36.4 (+0.6pp, oscillating 35.1–37.2).
- **Gap narrowed** 5.7 → 4.0 — not widened.

The FSC catch-up is concentrated in a few FSC airlines (CZ +7.4, TG +5.1, HX +7.1), not
broad-based. ⚠️ Verify/correct before syncing a "gap widening" narrative.

## 2. OW vs pure RT — confirmed

OW-single is consistently ~8–10pp higher than RT-pure (structural, stable over 12 months).

| Month | OW-single | RT-pure | Gap |
|---|---|---|---|
| 2025-09 | 37.6% | 27.7% | 9.9pp |
| 2026-08 | 38.4% | 29.6% | 8.8pp |

## 3. Airline movers + deep-dive proposal (Jun → Aug)

Proposed deep-dives (needle movers: high volume × large delta, potentially replicable):

| Airline | Type | Δ | Aug vol | Why deep-dive |
|---|---|---|---|---|
| **CZ** | FSC | **+7.4pp** | 72k | Amadeus distribution shift → replicable pattern (check who else is migrating GDS/NDC) |
| **TG** | FSC | **+5.1pp** | 79k | Biggest FSC improver, unexplained (supply / fare family / ranking?) |
| **VJ** | LCC | **+5.8pp** | 65k | Biggest LCC improver — what's the LCC lever? |
| **AK** | LCC | **−4.0pp** | 90k | Biggest LCC decliner (AirAsia — ties to existing VPL/VP work) |

**EY** (−9.8pp, FSC, 25k) — excluded from deep-dive: the drop is war/geopolitically driven
(Middle East conflict affecting Etihad's traffic mix), exogenous, not a Trip-side lever.
