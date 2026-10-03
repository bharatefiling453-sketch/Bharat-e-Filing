# GST Registration page: competitor ranking & fact-check (re-run 3 Oct 2026, page v3)

## How to read this ranking

- **This scores page quality, not Google position.** Google rank also depends on domain authority, backlinks, reviews and
  site age, where IndiaFilings, ClearTax and Vakilsearch are years ahead. A better page is what lets Bharat eFiling close
  that gap over time; it will not outrank them on day one.
- **Competitor sites could not be opened from the build environment** (network policy blocked them). Prices and claims below
  come from search-engine listings of their pages (cited at the end). Scores for content, design and freshness are
  **estimates** from those listings and the brands' known page formats. Re-score after opening each page yourself using the
  checklist in `PRODUCT-PAGE-STANDARD.md` §11.
- The new Bharat eFiling page is scored **as it will be once the placeholders are filled** (real phone, address, CA name, prices).

## Ranking (page quality, out of 100) — re-run on page v3

| #   | Page                                                   | Score                                                     | Entry price        | Strongest point                                                                                                                     | Biggest gap                                                                           |
| --- | ------------------------------------------------------ | --------------------------------------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 1   | **Bharat eFiling, new page v3** (`/gst-registration/`) | **91** once placeholders are filled (**88** as it stands) | ₹999 (placeholder) | Only page in the set covering the 1 Oct 2026 Multistate Registration and the 8 Sep 2026 biometric order; measured Lighthouse 96–100 | No reviews, no real usage numbers, CA reviewer not yet named, no domain authority yet |
| 2   | ClearTax guide + service                               | ~80                                                       | ₹1,499             | Very deep guide content, huge authority                                                                                             | Guide and paid service on separate URLs                                               |
| 3   | IndiaFilings                                           | ~76                                                       | ₹1,500             | Large "learn" library feeding internal links, brand trust                                                                           | Generic layout; higher entry price                                                    |
| 4   | Vakilsearch / Zolvit                                   | ~74                                                       | ₹399               | Aggressive price, 2026 content, comparison articles                                                                                 | Quotes 7–10 working days; heavy upsell                                                |
| 5   | Corpbiz                                                | ~66                                                       | ₹398               | Lowest price, city-level landing pages                                                                                              | City pages risk thin or duplicate content                                             |
| 6   | RegisterKaro                                           | ~64                                                       | ₹500–₹2,500 range  | Fees explained by entity type                                                                                                       | Price range instead of a clear price                                                  |
| 7   | LegalWiz                                               | ~62                                                       | ₹1,999             | Clean, simple guide                                                                                                                 | Highest entry price in the set                                                        |
| 8   | Bharat eFiling, current (`/product-category/gst/`)     | ~35                                                       | —                  | —                                                                                                                                   | A WooCommerce category listing, not a service page                                    |

### New page v3: score by criterion

| Criterion (weight)                  | v1 (first build) | v3 now          | How it was judged                                                                                         |
| ----------------------------------- | ---------------- | --------------- | --------------------------------------------------------------------------------------------------------- |
| Freshness & legal accuracy (20)     | 17               | **20**          | Multistate (1 Oct 2026), biometric order, REG-01 guidance, REG-32, IMS, GSTR-3B lock; two v1 errors fixed |
| Direct answer + depth, AEO/GEO (15) | 14               | **14**          | Quick-answer card, 13 FAQs = schema, timeline; −1 until a Hindi version exists                            |
| Structured data (10)                | 10               | **10**          | `npm run check:seo`: 63 checks pass                                                                       |
| Proof / E-E-A-T (15)                | 8                | **8** (5 today) | Sources and dates present; reviews and named CA missing                                                   |
| Price clarity (10)                  | 8                | **9**           | Prices beside the form and directly below it                                                              |
| UX & design (10)                    | 7                | **10**          | Lighter hero, all-white theme, timeline, stepper                                                          |
| Speed & accessibility (10)          | 9 (est.)         | **10**          | **Measured** below                                                                                        |
| Conversion paths (10)               | 8                | **10**          | Plan picker in form, pop-up (CTA / exit-intent / timed), WhatsApp, Log in, mobile bar                     |
| **Total**                           | **88 (est.)**    | **91**          |                                                                                                           |

### Measured: Lighthouse on page v3 (local server)

|         | Performance | Accessibility | Best practices | SEO     | LCP   | Blocking time | CLS |
| ------- | ----------- | ------------- | -------------- | ------- | ----- | ------------- | --- |
| Mobile  | **96**      | **100**       | 96*            | **100** | 2.0 s | 10 ms         | 0   |
| Desktop | **100**     | **100**       | 96*            | **100** | 0.5 s | 0 ms          | 0   |

\* The only best-practices failure is two console errors caused by the build sandbox blocking Google Fonts and the placeholder
GTM ID; both disappear on the live site. Mobile performance was 88 before this run's fix (the page flag that triggers animations
is now set before first paint, the timeline measures after paint, and the costly blur filter was removed), with blocking time
falling from 320 ms to 10 ms. Live scores will depend on your hosting and the tags you add in GTM; re-test with PageSpeed
Insights after launch.

### What changed for competitors

Competitor sites are still blocked from this environment, so their scores are unchanged estimates. Searches for the two newest
changes (Multistate Registration, 1 Oct 2026; biometric order, 8 Sep 2026) returned only news and CA blogs, and none of the
seven competitor service pages. That suggests they had not yet added these updates, but it does not prove it; check their
pages yourself.

### Scoring criteria (weight)

Freshness & legal accuracy (20) · Direct answer + depth for AEO/GEO (15) · Structured data (10) · Proof/E-E-A-T: named
reviewer, sources, reviews (15) · Price clarity (10) · UX & design (10) · Speed & accessibility (10) · Conversion paths (10).

## Why the new page is better

1. **Most current law on the page.** It covers the **8 Sep 2026 Delhi High Court interim order** making biometric Aadhaar
   authentication mandatory for every new GST registration, **Rule 14A** (3-day route, from 1 Nov 2025), GST 2.0 slabs
   (22 Sep 2025) and the GSTR-9 relief up to ₹2 crore. Pages that still promise "Aadhaar OTP in 2 minutes" are now out of date.
2. **Income-tax Act, 2025 ↔ 1961 cross-reference.** It maps s.58 (old 44AD/44ADA/44AE), s.63 (old 44AB) and s.393 (old
   194C/194J/194-O/194Q), with the transition rule for FY 2025-26. This GST × income-tax link is unusual on GST registration pages.
3. **Accurate state thresholds.** It names all 10 states that kept the ₹20 lakh goods limit and the 4 states with the ₹10 lakh
   services limit. Many pages simplify this to "special category states" and get it wrong.
4. **Built for answer engines (AEO/GEO).** A 55-word direct answer at the top, questions as headings, 13 FAQs whose text matches
   the schema word for word, `speakable` markup, `llms.txt`, AI crawlers allowed, and primary-source links on every claim.
5. **Complete structured data.** Organization, WebSite, WebPage (with reviewer and dates), Breadcrumb, Service with prices,
   HowTo and FAQPage, all in one linked graph.
6. **Premium, modern design in your brand colours.** Apple-style sticky local nav, glass lead form, bento "at a glance" grid,
   reading-width guide, dark featured plan, floating mobile action bar. Zero accessibility violations (WCAG 2.2 AA).
7. **Honest conversion design.** Three CTA paths (form, WhatsApp, call) at every scroll position, UTM/click-ID capture on
   leads, and no fake reviews or invented numbers (which can draw a Google manual action or a CCPA complaint).
8. **Rupee-worked examples:** a Pune bakery, a Jaipur freelancer and an Indore trader's penalty exposure.

## What still has to happen to actually reach #1 on Google

1. Fill the placeholders: phone, address, CA reviewer with ICAI number, prices.
2. Launch at `/gst-registration/` with 301s from `/product-category/gst/`, and submit in Search Console and Bing.
3. Embed **real Google reviews** and add real numbers (GSTINs filed, average approval days) once you have them.
4. Build the topic cluster: GST return filing, LUT, amendment, cancellation, notice reply and 10–15 `/learn/` guides, all
   interlinked.
5. Earn links: local business listings, CA association directories, guest posts, and a press note on the biometric change.
6. Re-check the biometric-order status (it was listed for hearing on 22 Sep 2026) and update the page and its date.

## Fact-check log

| Claim                                                                               | Status                                                                                                    | Source                                 |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| ₹40L goods / ₹20L services; ₹20L goods in 10 states; ₹10L services in 4 states      | **Corrected** (earlier version listed only 4 states for goods)                                            | Notification 10/2019-CT; Sec 22 CGST   |
| Rule 14A: ≤ ₹2.5L monthly B2B output tax, 3 working days, from 1 Nov 2025           | Verified                                                                                                  | Notification 18/2025-CT                |
| Biometric Aadhaar mandatory for all new registrations (interim, 8 Sep 2026)         | **Added**; previous text said "OTP on your phone"                                                         | Delhi HC interim order; press coverage |
| Rule 9: 7 working days; 30 days with physical verification; deemed approval         | Verified                                                                                                  | Rule 9 CGST Rules                      |
| Penalty for not registering = ₹10,000 or tax evaded, whichever is higher (s.122(1)) | **Corrected** (earlier example wrongly applied the 10% rule of s.122(2), which is for registered persons) | Sec 122 CGST                           |
| Rule 10A bank account: 30 days or before GSTR-1/IFF, else suspension                | Verified, suspension risk added                                                                           | GSTN advisory                          |
| GSTR-9 mandatory only above ₹2 crore                                                | Verified                                                                                                  | Notification 15/2025-CT                |
| E-invoicing at ₹5 crore AATO                                                        | Verified                                                                                                  | Notification 10/2023-CT                |
| E-commerce goods sellers relief from 1 Oct 2023                                     | Verified, notification number added                                                                       | Notification 34/2023-CT                |
| GST 2.0: 5% / 18% / 40% from 22 Sep 2025                                            | Verified                                                                                                  | 56th GST Council; PIB                  |
| Income-tax Act, 2025: assent 21 Aug 2025, in force 1 Apr 2026, "tax year"           | Verified                                                                                                  | PIB / Income Tax Dept press release    |
| s.58 = 44AD/44ADA/44AE; s.63 = 44AB; s.393 = TDS sections                           | Verified                                                                                                  | Income-tax Act, 2025                   |

## Sources

- Multistate Registration: <https://taxguru.in/goods-and-service-tax/gstn-introduces-multistate-gst-registration-facility-multiple-states-uts.html>, <https://www.caclubindia.com/news/gst-portal-launches-multi-state-registration-facility-with-single-master-trn-26830.asp>
- Biometric order detail: <https://taxguru.in/goods-and-service-tax/delhi-hc-directs-biometric-aadhaar-authentication-gst-registration.html>
- IndiaFilings price: <https://www.indiafilings.com/learn/what-is-the-fees-for-gst-registration>
- Vakilsearch: <https://vakilsearch.com/gst-registration>
- ClearTax: <https://cleartax.in/services/gst-registration/p>, <https://cleartax.in/s/gst-registration>
- Corpbiz: <https://corpbiz.io/gst-registration>
- RegisterKaro: <https://www.registerkaro.in/post/gst-registration-fees>
- LegalWiz: <https://www.legalwiz.in/gst-registration-india>
- Thresholds: <https://taxguru.in/goods-and-service-tax/gst-registration-exemption-40-lacs-w-e-f-01-04-19.html>
- Rule 14A: <https://taxguru.in/goods-and-service-tax/rules-gst-registration-3-working-days-1st-november-2025-notified.html>
- Biometric order: <https://www.freepressjournal.in/india/delhi-high-court-orders-nationwide-biometric-aadhaar-verification-for-fresh-gst-registrations>, <https://www.jurishour.in/gst/gst-registration-biometric-aadhar-authentication/>
- Rule 9: <https://www.taxtmi.com/acts?id=26854>
- Section 122: <https://cleartax.in/s/section-122-of-cgst-act-penalties-offences>
- Rule 10A: <https://taxguru.in/goods-and-service-tax/advisory-furnishing-bank-account-details-gst-rule-10a.html>
- GSTR-9 relief: <https://www.taxtmi.com/article/detailed?id=15279>
- Notification 34/2023: <https://www.taxscan.in/central-govt-exempts-suppliers-of-goods-supplies-through-e-commerce-operators-from-gst-registration-subject-to-conditions-w-e-f-october-1st/305561>
- GST 2.0: <https://www.pib.gov.in/PressReleasePage.aspx?PRID=2164586&reg=48&lang=2>
- Income-tax Act, 2025: <https://www.pib.gov.in/PressReleasePage.aspx?PRID=2248005&reg=3&lang=2>
