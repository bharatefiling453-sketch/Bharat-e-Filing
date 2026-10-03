# GST Return Filing page: competitor ranking (3 Oct 2026)

Same method and weights as `COMPETITOR-RANKING.md`. **This scores page quality, not Google position.** Bharat eFiling's
page is measured (checks + Lighthouse). Competitor sites are blocked from the build environment, so their scores are
**estimates** from search listings (prices cited below). Re-check by opening each page.

## Ranking (out of 100)

| #   | Page                                                 | Score                                              | Price (12 months unless noted)                     | Strongest point                                                                                                              | Biggest gap                                                                                |
| --- | ---------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 1   | **Bharat eFiling, new page** (`/gst-return-filing/`) | **89** once placeholders are filled (**86** today) | ₹7,999 / ₹11,999* / ₹15,999                        | Due-date finder + late fee calculator on the service page; 3-year bar, locked GSTR-3B, IMS flow, Income-tax Act 2025 mapping | Priced above the cheapest rivals; no transaction limits stated; no reviews or named CA yet |
| 2   | ClearTax                                             | ~80                                                | Monthly/quarterly packs                            | Very deep GSTR-1 / 3B / late-fee guides, huge authority                                                                      | Guides and paid plans on separate URLs                                                     |
| 3   | IndiaFilings                                         | ~77                                                | ₹998/month · ₹7,899/year                           | Dedicated charges page, big learning library                                                                                 | Generic layout                                                                             |
| 4   | Vakilsearch / Zolvit                                 | ~75                                                | ₹999 (3 months) · ₹2,999 · ₹4,999                  | Cheapest yearly plan; limits stated (200 txns / ₹10 lakh)                                                                    | Heavy discount-led upsell                                                                  |
| 5   | Corpbiz                                              | ~66                                                | ₹999/month · ₹24,999 (150 txns, 36-month validity) | Clear transaction cap                                                                                                        | Expensive annual pack, thin page                                                           |
| 6   | Ebizfiling                                           | ~64                                                | ₹599 (single nil return) · ₹7,999                  | Low-cost nil-return entry point                                                                                              | Plan limits are complex                                                                    |
| 7   | RegisterKaro                                         | ~60                                                | ₹500–₹15,000/month range                           | Explains cost by business size                                                                                               | No fixed price                                                                             |
| 8   | Bharat eFiling, current product page                 | ~40 (est.)                                         | ₹7,999–₹15,999                                     | Real product page with a price range                                                                                         | WooCommerce product layout; no guide, tools or FAQ schema seen in search                   |

\* ₹11,999 is an estimate awaiting confirmation; ₹7,999 and ₹15,999 match the live site.

## New page: score by criterion

| Criterion (weight)                  | Score       | Why                                                                                                                                                         |
| ----------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Freshness & legal accuracy (20)     | 19          | 3-year bar (GSTN, 29 Oct 2025), GSTR-3B lock, GST 2.0, GSTR-9 relief, Income-tax Act 2025; −1 because IMS mandatory dates are not stated (sources conflict) |
| Direct answer + depth, AEO/GEO (15) | 14          | Quick answer, 13 FAQs = schema, due-date and late-fee tables, two tools; −1 until a Hindi version exists                                                    |
| Structured data (10)                | 10          | `check:seo`: 61 checks pass (Service, Offers, HowTo, FAQPage, Breadcrumb)                                                                                   |
| Proof / E-E-A-T (15)                | 8 (5 today) | Sources and dates present; reviews and named CA missing                                                                                                     |
| Price clarity (10)                  | 8           | Prices beside the form, per-year and +GST stated; transaction or turnover limits per plan not yet stated                                                    |
| UX & design (10)                    | 10          | Same v3 design; tools, rhythm strip, ITC flow, stepper                                                                                                      |
| Speed & accessibility (10)          | 10          | Lighthouse mobile 94 / 100 / 96* / 100; zero axe violations desktop + mobile                                                                                |
| Conversion paths (10)               | 10          | Plan picker in form, pop-up, tools leading to CTAs, WhatsApp, mobile bar                                                                                    |
| **Total**                           | **89**      |                                                                                                                                                             |

\* Best-practices 96 is caused only by the sandbox blocking Google Fonts and the placeholder GTM ID.

## What would move it higher

1. **State the limits per plan** (e.g. up to 100 invoices a month, or turnover up to ₹X). Every price-led competitor does,
   and it answers the buyer's first question. (+2 price clarity)
2. **Consider an entry plan.** Vakilsearch sells 12 months for ₹2,999 and Ebizfiling a nil return for ₹599. A low-cost
   "Nil returns – 12 months" plan would compete for the many small filers without lowering your main prices. Business decision.
3. **Named CA reviewer + real Google reviews** (+3 to +7 proof).
4. **Confirm the IMS mandatory dates** from the latest GSTN advisory and add them to the timeline (+1 freshness).
5. **Hindi version** of the page and tools.

## Evidence about tools

Searches for GST late-fee calculators returned stand-alone tools (Masters India, AI Accountant, TaxAdda and others), not the
service pages of the competitors above. That suggests few rivals put a calculator on the page where you buy, but it does
not prove it.

## Sources

- Vakilsearch: <https://vakilsearch.com/gst-return-filing>
- IndiaFilings: <https://www.indiafilings.com/gst-return-filing>, <https://www.indiafilings.com/gst-return-filing/charges>
- ClearTax: <https://cleartax.in/services/gst-filing-123/p>
- Corpbiz: <https://corpbiz.io/gst-return-filing>
- Ebizfiling: <https://ebizfiling.com/service/gst-returns/>
- RegisterKaro: <https://www.registerkaro.in/post/gst-registration-fees>
- Bharat eFiling live: <https://bharatefiling.com/product/gst-return-filing-gstr-1-gstr-3b/>
- Calculators: <https://www.mastersindia.co/interest-and-late-fee-calculator/>, <https://www.aiaccountant.com/resources/gst-late-fee-calculator>
