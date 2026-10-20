# Service page design v2 ("new adopted design")

Status: **draft, waiting for approval.** Reference build: `gst-return-filing/index.html`.
Once it's approved, "create the new adopted design for <service>" means: build that service page in this layout, with no extra questions.
Everything in `PRODUCT-PAGE-STANDARD.md` still applies (SEO, AEO, GEO, schema, fact-checking, Income-tax Act 2025 references, no government-fee mentions, "Bharat e-Filing" spelling), except for the section order below.

## Section order

1. **Ribbon:** one line on the latest change. Then the global nav, then the sticky local nav. Add "Live dates" and "Reviews" to the local nav.
2. **Clean hero (`.hero--clean`):** centred, with **no form** and **under 25 words in total**. It holds:
   - breadcrumb;
   - H1, which is the primary keyword plus a short promise in gradient text;
   - a one-line sub;
   - 2 buttons: "Start" (goes to `#get-started`) and a secondary one (goes to `#live`);
   - one live chip, for example "Next GSTR-3B due in 17 hrs 9 min".
3. **Live widgets (`#live`):** 4 `.live-card`s in a row (2 on tablet, 1 on mobile), then a count-up `.stat-strip` of 4 numbers.
   - The cards are: countdowns (`.cd`, with days/hrs/min/sec and a filing-window meter), a running cost meter (`.live-card--warn`), and an annual deadline card (`.live-card--navy`).
   - **Every number must come from today's date or from the law.** Never use invented business stats (clients served, returns filed, ratings) until they are real and verifiable.
4. **Ticker:** latest updates.
5. **Lead split (`#get-started`, `.lead-split`):**
   - left: kicker, H2, one line, 3 "what happens next" steps (`.next-steps`) and ticks;
   - right: the form card with the plan picker.
6. Pricing, then at a glance, then calculators.
7. **Guide plus related blogs column (`.guide-split`):**
   - The article sits at reading width. The sticky `.reads` aside on the right holds 5–6 related blog links (`.reads__list`) and a navy CTA box. On mobile it stacks below the article.
   - Only link to blog posts that are published.
8. Process, then the rest of the guide.
9. **Testimonials (`#reviews`):** a scroll-snap carousel (`.t-track`) with prev/next buttons and a Google reviews badge.
   - Use **real Google reviews only**, word for word, with the client's permission.
   - The `data-sample` cards are layout placeholders and show a "Sample" tag.
   - Add Review/AggregateRating schema only once every card is real.
10. Related services, then reviewer and sources, then FAQ, then the CTA band, then the footer, then the mobile action bar. The lead pop-up behaves as before.

## Building blocks

- **CSS:** `assets/css/bef-design-system.css`, section 19 "SERVICE PAGE v2".
- **Shared JS (`assets/js/bef-page.js`):**
  - `[data-count-to]` count-up. The HTML already holds the final value, so the page is safe without JS and for SEO.
  - `[data-t-scroll]` carousel buttons.
- **Page JS:** the live clock (the countdown, meter and deadline logic for that service) sits in the page's inline script. Reuse the `nextDue` / `lastMissed` / `endOf` helpers from the GST page.

## Live widget ideas by service

| Service                | Countdown cards                                  | Running meter                                 | Deadline card                      |
| ---------------------- | ------------------------------------------------ | --------------------------------------------- | ---------------------------------- |
| ITR filing             | ITR due 31 Jul; belated/revised due 31 Dec       | 234F fee plus 234A interest per day late      | Days left to file a belated return |
| TDS returns            | 24Q/26Q quarterly due dates                      | 234E ₹200/day fee                             | Next Form 16 issue date            |
| GST registration       | Time to GSTIN (3–7 working days)                 | —                                             | Threshold tracker (₹20/40 lakh)    |
| ROC / company filing   | AOC-4 / MGT-7 due dates                          | ₹100/day additional fee                       | AGM deadline                       |
| Trademark              | Objection reply window (30 days)                 | —                                             | Renewal date (10 years)            |
