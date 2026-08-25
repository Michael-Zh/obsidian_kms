# Data Clarification: Cancellation Fee Fields in `o_customer_cancellation`

**To:** Oliver Tang  
**From:** Michael Zhang  
**Date:** 2026-06-29  
**Purpose:** Confirm the correct interpretation of `carrier_amount`, `consolidator_amount`, and `ctrip_amount` for cancel policy classification

---

## Context

I am building a benefit fingerprint analysis using `o_customer_cancellation` to classify orders into `free_cancel`, `paid_cancel`, or `no_cancel` based on the airline's own penalty amount. The classification logic uses `carrier_amount` as the fee signal for the airline tier.

---

## Observed Conflict

### What the data shows (EY, 2026 YTD, Economy)

Filtering to `condition_start_minute = -1` (current active window), `isactivated = 1`, `is_allowed_all_un_use_show_up = 'H'` (cancellation permitted):

| Fee pattern | Row count | carrier_amount | consolidator_amount |
|---|---|---|---|
| Both zero / NULL | 14,413 | 0 | 0 |
| consolidator_amount > 0 only | 14,801 | 0 | ~317–400 TWD |
| carrier_amount > 0 | 0 | — | — |

**Result:** `carrier_amount` is 0 or NULL for all EY cancellable rows. `paid_cancel` = 0 under current logic.

### What the frontend and airline website show

- EY **Comfort** fare: cancellation is permitted but carries a penalty fee. The fee is displayed as three components: airline fee / consolidator fee / Trip.com service fee.
- The airline fee component is non-zero on both Trip.com's fare detail page and EY's official website.
- This directly contradicts `carrier_amount = 0` in the data.

---

## Questions for Oliver

1. **Field ownership:** Does `carrier_amount` represent the airline's own penalty, or is the airline's fee sometimes recorded under `consolidator_amount`? The EY sample rows show `carrier_amount = 0` and `consolidator_amount ≈ 317–400 TWD` — is this expected?

2. **Correct "paid cancel" signal:** To classify an order as having a real cancellation penalty (i.e., not free to cancel), should we use:
   - `carrier_amount > 0` only, or
   - `carrier_amount + consolidator_amount > 0` (combined), or
   - something else entirely?

3. **`consolidator_amount` definition:** Does this field represent a consolidator's markup/handling fee, or does it sometimes carry the airline-filed ATPCO penalty that is routed through a consolidator agreement?

---

## Why This Matters

The goal is to infer Brand Fare tier (e.g., Economy Light vs. Comfort vs. Flex) from cancellation policy without relying on ATPCO brand name mapping. If `carrier_amount = 0` for all EY paid-cancel fares, the classification will incorrectly label Comfort-tier orders as `free_cancel` rather than `paid_cancel`, understating the paid-cancel segment.

Happy to share the sample token IDs or the full diagnostic query if helpful.
