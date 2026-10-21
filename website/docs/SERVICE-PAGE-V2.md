# Service page design v2 ("new adopted design")

Status: **draft, waiting for approval.** Reference builds: `gst-return-filing/index.html` and `gst-registration/index.html` (rebuilt in v2 on 21 Oct 2026, with an eligibility checker and a registration date planner).
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

## Photos, ad slider and motion (added 20 Oct 2026)

Section order: clean hero, then live widgets, then the **promo slider** (3 ad banners, autoplay every 5.5 s, dots, swipe, pauses on hover), then the ticker and the lead form. After that come pricing (with **benefit chips** that have a shine sweep), the **"Why us" animated bento**, at a glance, and so on. A **sticky promo bar** shows on desktop after the first screen.

Always-running motion:
- slider autoplay and its progress bar;
- floating "app" cards that bob over the photos;
- the call timer counting up;
- the "Fetching → Auto-filled" loop;
- the pulsing "Approve & file" button;
- the 24-hour track filling;
- the expert card stack fanning out;
- the shine sweep on buttons and chips;
- the live clock.

All motion stops for visitors who turn on reduced motion.

### Product mockups (default visuals)

Each ad panel has a code-drawn, animated mockup under the photo slot: a WhatsApp-style filing chat (`.mock-phone` + `.chat`), a reconciliation window (`.mock-window` + `.recon`), and a CA call card (`.mock-call`). These work with no image files. A real photo, if added, covers the mockup.

### Image specs

Photos live in `assets/img/<service-slug>/`. Each `<img>` carries `data-optional`, so a missing file hides itself and the gradient panel still looks finished.

| File                          | Size (px)        | Ratio | Where it shows                               |
| ----------------------------- | ---------------- | ----- | -------------------------------------------- |
| `slide-*.webp` × 3            | 1680 × 944       | 16:9  | Promo slider, right half (left edge fades)   |
| `expert-portrait.webp`        | 800 × 1000       | 4:5   | "Your own expert" card                       |
| `<audience>-owner.webp`       | 1200 × 1200      | 1:1   | "Built for Bharat" photo card                |

- Export as WebP, quality 80, under 180 KB each.
- Keep the subject on one side, so the text side and the floating cards have room.
- No text, logos or watermarks in the photo. Phone screens should be plain white, because the floating cards supply the "app" content.

### Prompt template (Canva "generate image")

> Photorealistic advertising photo, wide banner. A smiling Indian **{persona, age, clothing}** in **{setting}**, holding up a smartphone toward the camera / at a desk with a laptop, confident and happy. Soft natural daylight, shallow depth of field, **{props}** blurred behind. **{Left/right} third of frame empty for text overlay.** Premium Indian fintech ad campaign style. No text, no logos, no watermarks, phone screen plain white.

GST Return Filing prompts used:
1. **Slider 1:** a textile shop owner (woman, 35, mustard kurta) holding up a phone.
2. **Slider 2:** an e-commerce seller (man, 30, navy shirt) in a warehouse office with a tablet.
3. **Slider 3:** a female CA (40, navy blazer, headset) reviewing on a laptop, with the left third empty.
4. **Expert portrait:** a man, 35, light blue shirt, on a mint studio background, 4:5.
5. **Kirana owner:** a man, 45, white shirt, at the shop counter holding a phone, 1:1.

Floating-card figures (for example ₹1,24,560 ITC) are app illustrations, not client data, and the HTML comment says so. Business claims on the page (for example "24hrs Guaranteed") must be ones the business actually honours. The pricing note defines "24hrs Guaranteed" as 24 hours from receiving complete data.
