# Field Confirmation: Benefit Fingerprint Logic (v4)

**To:** Oliver Tang  
**From:** Michael Zhang  
**Date:** 2026-06-30  
**Purpose:** Confirm that the field definitions used in `MZ_202606_quantification_v4` are correct before running production queries

---

## Background

In the previous clarification (2026-06-29), I found that `carrier_amount = 0` for all EY cancellable rows — meaning `paid_cancel` was always zero under the original logic. Details below.

### Observed conflict (EY, 2026 YTD, Economy)

Filter: `condition_start_minute = -1`, `isactivated = 1`, `is_allowed_all_un_use_show_up = 'H'`

| Fee pattern | Row count | carrier_amount | consolidator_amount |
|---|---|---|---|
| Both zero / NULL | 14,413 | 0 | 0 |
| consolidator_amount > 0 only | 14,801 | 0 | ~317–400 TWD |
| carrier_amount > 0 | 0 | — | — |

### What the frontend shows

EY Comfort fare shows cancellation with a penalty fee broken into three components: airline fee / consolidator fee / Trip.com service fee. The airline fee component is non-zero on both Trip.com's fare detail page and EY's official website — directly contradicting `carrier_amount = 0` in the data.

### Fix applied in v4

Switched from `carrier_amount` to `all_un_use_show_up_amount` as the cancel fee signal. I would like to confirm this is the correct field before relying on it for the airline-level ranking.

---

## Current Logic in v4

### Cancel policy (`e_customer_cancellation`)

Filter: `condition_start_minute = -1`, `isactivated = 1`

```sql
CASE
  WHEN is_allowed_all_un_use_show_up = 'H' AND COALESCE(all_un_use_show_up_amount, 0) = 0
    THEN '3.free_cancel'
  WHEN is_allowed_all_un_use_show_up = 'H' AND all_un_use_show_up_amount > 0
    THEN '2.paid_cancel'
  WHEN is_allowed_all_un_use_show_up = 'T'
    THEN '1.no_cancel'
  ELSE NULL  -- token absent
END AS cancel_policy_class
```

### Change policy (`c_customer_change`)

Filter: `no_show_strict_condition_start_minute = -1`, `isactivated = 1`

```sql
CASE
  WHEN is_allowed_out_all_un_use_show_up_strict = 'H' AND COALESCE(out_all_un_use_show_up_strict_amount, 0) = 0
    THEN '3.free_change'
  WHEN is_allowed_out_all_un_use_show_up_strict = 'H' AND out_all_un_use_show_up_strict_amount > 0
    THEN '2.paid_change'
  WHEN is_allowed_out_all_un_use_show_up_strict = 'T'
    THEN '1.no_change'
  ELSE NULL  -- token absent
END AS change_policy_class
```

---

## Questions for Oliver

**Q1 — `all_un_use_show_up_amount`:** Does this field represent the total penalty amount the customer pays (airline + consolidator combined), or is it airline-only? My assumption is that it solves the `carrier_amount = 0` issue seen in EY — can you confirm?

**Q2 — Change policy filter:** I'm using `no_show_strict_condition_start_minute = -1` to get the current active window, mirroring `condition_start_minute = -1` in the cancel table. Is this the correct sentinel for change policy?

**Q3 — `is_allowed` value set:** The SQL comments note `H = allowed, T = not allowed`. Are there other values (e.g. `N`, `F`) I should handle, or is it always H / T / NULL?

**Q4 — NULL token rows:** If a token has no row in `e_customer_cancellation` or `c_customer_change`, I classify it as NULL (no record). Is NULL the right interpretation — i.e., policy data was never loaded — or does it indicate something else (e.g. non-GDS booking)?

---

## Why This Matters

The cancel/change classification is the core of the benefit fingerprint. An error here would misclassify Brand Fare tiers (e.g. EY Comfort as `free_cancel` instead of `paid_cancel`), which would understate the misleading label exposure and make the airline-level ranking unreliable.
