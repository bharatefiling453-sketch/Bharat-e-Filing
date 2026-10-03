# Bharat eFiling — Product / Service Page Standard v1.0

Use this standard for **every** service page (GST, ITR, company registration, trademark, MSME, TDS, …).
`gst-registration/index.html` is the reference build. Copy it, swap the content, keep the structure.

---

## 1. URL & slug rules

| Rule                                                         | ✅ Good                        | ❌ Bad                                                                   |
| ------------------------------------------------------------ | ------------------------------ | ------------------------------------------------------------------------ |
| Short, root-level, primary keyword only                      | `/gst-registration/`           | `/product-category/gst/`, `/product/gst-registration-online-india-2026/` |
| Lowercase, hyphens, trailing slash                           | `/llp-registration/`           | `/LLP_Registration`                                                      |
| No years, prices or stop-words (so it never needs to change) | `/itr-filing/`                 | `/itr-filing-2026-at-rs-499/`                                            |
| Category hub = plural topic                                  | `/gst/` lists all GST services |                                                                          |
| Guides live under `/learn/`                                  | `/learn/gst-rate-list/`        |                                                                          |

**Migration:** 301-redirect every old WooCommerce URL (`/product/…`, `/product-category/…`) to the new slug
(Rank Math → Redirections). Keep WooCommerce products for checkout, but set them `noindex` so the
service page is the only indexed URL for the keyword (avoids cannibalisation).

## 2. Title & meta formulas

| Element          | Formula                                                                                       | Limit         |
| ---------------- | --------------------------------------------------------------------------------------------- | ------------- |
| `<title>`        | `{Primary keyword} Online – {Key benefit/time} \| Bharat eFiling`                             | 50–60 chars   |
| Meta description | `{Action verb} {keyword} with {differentiator}. {Speed}, {price/fee fact}, {2 proof points}.` | 120–155 chars |
| H1               | Primary keyword + promise (can be longer than title)                                          | 1 per page    |
| OG title         | Title without brand                                                                           | ≤ 70 chars    |
| OG image         | 1200 × 630, brand navy background, service name, one icon                                     | < 200 KB      |

## 3. Page section order (tuned for conversions + answer engines)

1. Announcement ribbon (latest change) → global nav (logo, menu, **Log in**, Get started) → sticky local nav (section links + Apply now)
2. **Hero, kept minimal:** breadcrumb · "New" pill · H1 · one-line promise · 2 buttons · 3 short ticks. Right: **lead form with a
   built-in plan picker** (prices next to the enquiry form).
3. **Live updates ticker** (latest notifications, pauses on hover).
4. **Pricing** (3 plans, middle one featured), directly below the form. Plan buttons open the pop-up with that plan selected.
5. "At a glance" bento tiles.
6. Guide on white: Overview with the **quick answer card (40–60 words)** → Eligibility (+2 worked examples) → **What's new
   timeline** (scroll-animated, newest first) → Types → Documents.
7. **Process stepper** (animated, 5 steps) + statutory-timeline note.
8. Penalties → After registration → Income-tax Act 2025 ↔ 1961 → DIY vs us.
9. Bundles + related services → reviewer box + sources → FAQ → CTA band → footer → mobile action bar.
10. **Lead pop-up:** opens from CTAs, on desktop exit intent, or after 45 s if the visitor has scrolled; at most once per
    session automatically and never after a lead is submitted.

**Messaging rules:** backgrounds stay white (colour comes from cards, callouts and gradients, never grey bands). Do not mention
government fees. Talk about our fee only, shown before the customer starts.

## 4. SEO checklist

- [ ] Primary keyword in slug, title, H1, first 100 words, one H2, image alt, meta description
- [ ] 6–10 secondary keywords/questions as H2/H3s (from Search Console, AlsoAsked, "People also ask")
- [ ] 1,800–3,000 words of genuinely useful content; no fluff paragraphs
- [ ] Canonical (self), `index,follow,max-snippet:-1,max-image-preview:large`, hreflang `en-IN` (+ `hi-IN` when Hindi page exists)
- [ ] Page included in Rank Math sitemap; submitted in Search Console **and** Bing Webmaster Tools; IndexNow ping on update
- [ ] Image files named `gst-registration-process.webp`, with width/height set, lazy-loaded below the fold
- [ ] Core Web Vitals: **LCP < 2.0 s, INP < 200 ms, CLS < 0.05** on 4G mobile; total JS < 100 KB on first load

## 5. AEO (Answer Engine Optimisation — featured snippets, AI Overviews, voice)

- **Answer box** directly under H1: defines the thing + the 3 numbers people search (limit, fee, time) in 40–60 words.
- Each H2 is phrased as the **question** users type; the first sentence below it answers it fully.
- Use **tables** for comparisons/limits/dates and **ordered lists** for processes — snippet-friendly.
- FAQ answers are 40–80 words, self-contained (no "as mentioned above").
- `speakable` schema points to the answer box.

## 6. GEO (Generative Engine Optimisation — ChatGPT, Perplexity, Gemini, Claude)

- Cite **specific, verifiable facts**: section/rule numbers, notification numbers, effective dates, ₹ amounts.
- Link 4–6 **official sources** (gst.gov.in, CBIC, GST Council, incometaxindia.gov.in) — LLMs trust pages that cite primary sources.
- Visible **reviewer with credentials** + "last fact-checked" date (E-E-A-T).
- Consistent entity data everywhere (name, address, phone identical on site, Google Business Profile, JustDial, LinkedIn, Crunchbase).
- `llms.txt` at site root listing key service URLs; `robots.txt` allows OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, Google-Extended.
- Original elements LLMs can't find elsewhere: worked rupee examples, checklists, your own anonymised data ("median approval time for our clients in 2026: X days").

## 7. Structured data (one `@graph` per page)

Required: `Organization` (+ `ProfessionalService`), `WebSite`, `WebPage` (with `dateModified`, `reviewedBy`),
`BreadcrumbList`, `Service` (with `OfferCatalog` prices), `FAQPage`. Optional: `HowTo` (process pages), `VideoObject` (if a video is embedded).

- FAQ schema text must equal the visible FAQ text **word for word** (`npm run check:seo` enforces this).
- **Never** add `AggregateRating`/`Review` schema for your own business on your own site — Google ignores it and it risks a manual action.
- Validate with Rich Results Test + validator.schema.org before publishing.

## 8. Linking

**Internal (≥ 8 per page):** breadcrumb → category hub; 2 bundles; 6 related services; 1–2 links to income-tax pages;
1–2 links to `/learn/` guides; footer columns. Hub page (`/gst/`) links to every GST service. Use descriptive anchors ("GST return filing"), never "click here".

**External (≥ 3):** government/regulator sources only, `target="_blank" rel="noopener"`. Do not link to competitors.

## 9. Content quality & legal accuracy

- Every number on the page carries a law reference (Act + section/rule or notification).
- Income-tax references show **both** the Income-tax Act, 2025 section and the earlier Income-tax Act, 1961 section (e.g. tax audit: s.63 / old s.44AB; presumptive: s.58 / old ss.44AD-44AE; TDS: s.393 / old ss.194C, 194J, 194-O, 194Q). Note that FY 2025-26 is still under the 1961 Act.
- Each page reviewed by a CA before publishing and re-checked after every GST Council meeting / Budget; update the "Updated" badge and `dateModified` together.
- **Reviews and statistics must be real.** No invented customer counts, ratings or testimonials (Consumer Protection (E-Commerce) Rules & ASCI guidelines; Google spam policies).
- Disclaimer in footer: not affiliated with GSTN/CBIC/ITD.

## 10. Design system v2 (`assets/css/bef-design-system.css`)

Visual language: calm, premium and editorial, in the style of Apple, Google and Stripe product pages. Lots of whitespace,
one type family, big confident headlines, a neutral canvas, and brand colour used only where it carries meaning.

| Token                  | Value                                                                        | Use                                                                           |
| ---------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Navy (logo)            | `#102161`, deep `#0a1640`, ink `#0b1433`                                     | Headings, primary buttons, featured plan, dark tiles                          |
| Saffron → Amber (logo) | `#ff8813` → `#fcc224` gradient                                               | Main CTA ("Apply now"), "Most popular" badge, highlight tile, headline accent |
| Saffron text           | `#b45309`                                                                    | Small accent labels on white (≥ 5:1)                                          |
| Leaf green (logo)      | `#3c8c31` / `#4eb03f`, text `#2f6f27`                                        | Ticks, "fact-checked" dot, success states                                     |
| Neutrals               | ink `#1d1d1f`, `#424245`, `#6e6e73`; canvas `#fff` / `#f5f5f7`               | Body text, secondary text, alternating section backgrounds                    |
| Font                   | Inter (variable, optical sizing) + Noto Sans Devanagari                      | One family everywhere; tight tracking (−0.035em) on headlines                 |
| Type scale             | H1 38→64 px, H2 30→48 px, body 17 px, line-height 1.6, reading column 760 px |                                                                               |
| Spacing                | 4 px grid; sections 72→140 px fluid                                          |                                                                               |
| Radius                 | 10 / 14 / 22 / 30 px; pill buttons                                           |                                                                               |
| Depth                  | Soft navy-tinted shadows, frosted-glass sticky bars (`backdrop-filter`)      |                                                                               |
| Motion                 | Fade-up on scroll, 0.8 s ease-out; switched off for `prefers-reduced-motion` |                                                                               |

**Page furniture:** announcement ribbon → frosted global nav (logo, centred menu, Call + Get started) → sticky local nav
(page title, section links with scroll-spy, "Apply now") → hero with glass lead-form card → bento "at a glance" grid →
guide in a reading column on a grey canvas → full-width pricing → FAQ → gradient CTA → light Apple-style footer →
floating mobile action bar.

Logo files: `assets/img/bef-logo.webp` (+ `@2x`), `bef-logo.png`, and `bef-mark.svg` (vector icon / favicon).

Accessibility gate: **WCAG 2.2 AA with zero axe violations** on desktop and mobile (`npm run check:a11y`).

## 11. Competitor benchmark — what to beat

Score every new page 0–2 on each row against the top 3 ranking pages for its keyword (IndiaFilings,
ClearTax, Vakilsearch, RegisterKaro, Corpbiz, LegalWiz, Ebizfiling…). Publish only when Bharat eFiling scores
highest overall.

| Criterion         | Question to ask                                                                      |
| ----------------- | ------------------------------------------------------------------------------------ |
| Freshness         | Does the page show a visible updated date and the latest law change (e.g. Rule 14A)? |
| Direct answer     | Is the core question answered in the first screen in ≤ 60 words?                     |
| Depth             | Tables for limits/documents/dates? Worked rupee examples?                            |
| Proof             | Named, credentialed reviewer? Official sources linked?                               |
| Price clarity     | Govt fee vs professional fee vs GST shown separately?                                |
| Speed             | Mobile LCP under 2.5 s?                                                              |
| Friction          | Can a user enquire in < 20 seconds (form, WhatsApp, call) from any scroll position?  |
| Language          | Hindi option?                                                                        |
| Cross-law insight | Does it connect GST with income tax (Income-tax Act, 2025)?                          |

## 12. Launch checklist

- [ ] All `REPLACE…` / `GTM-XXXXXXX` / `00000 00000` placeholders replaced (`npm run check:seo` warns until done)
- [ ] Prices confirmed and identical in visible plans **and** JSON-LD offers
- [ ] `npm run check` passes (HTML, CSS, SEO, accessibility)
- [ ] Lighthouse mobile ≥ 90 performance, 100 accessibility, 100 SEO, 100 best practices
- [ ] Rich Results Test: FAQ, Breadcrumb, Organization detected, no errors
- [ ] GTM preview: all events fire (see `TRACKING.md`)
- [ ] 301s from old URLs live; old URL returns 301 → new URL returns 200
- [ ] URL inspected and "Request indexing" in Search Console; submitted in Bing Webmaster Tools
