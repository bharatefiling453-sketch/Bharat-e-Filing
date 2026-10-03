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

## 3. Page section order (do not reorder — it is tuned for conversions + answer engines)

1. Top bar (phone, email, hours) → sticky header (logo, 6 nav items, one CTA)
2. **Hero**: breadcrumb · "Updated {date}" badge · H1 · **AEO answer box (40–60 words)** · 4 benefit bullets · 2 CTAs (primary + WhatsApp) · trust numbers · **lead form card** on the right
3. Highlights strip (4 cards: time, fee, quality, language)
4. Main content with sticky **"On this page"** table of contents:
   1. What is {service}? (definition + law reference + **illustration**)
   2. Who needs it? (eligibility table + **2 worked examples** with Indian names/cities)
   3. What changed recently? (dated, cites notification numbers)
   4. Types / options (table)
   5. Documents required (table by entity type + downloadable PDF)
   6. Step-by-step process (numbered timeline with day estimates + statutory timeline callout)
   7. Fees & plans (3 tiers, middle one featured; govt fee stated separately)
   8. Penalties / risks (with a worked rupee example)
   9. After you get it (compliance calendar)
   10. Income-tax angle — **Income-tax Act, 2025 section + the earlier 1961 Act section side by side**
   11. Why us (DIY vs us table) + **real** Google reviews widget
   12. Bundles (2) + related services (6 cards)
   13. Reviewer box (CA name, ICAI no., last fact-checked date) + official sources list
5. FAQ (10–15 questions, accordion, first one open)
6. CTA band (start · WhatsApp · call)
7. Footer (brand + address, 4 link columns, social, disclaimer, legal links)
8. Mobile sticky bar (WhatsApp + primary CTA)

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

## 10. Design system (`assets/css/bef-design-system.css`)

| Token               | Value                                                                                                 | Use                                                |
| ------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Navy 900 / 800      | `#0a1f44` / `#0f2b5b`                                                                                 | Headings, footer, primary buttons — trust          |
| Saffron 500         | `#f47c20`                                                                                             | Primary CTA fill (with navy text, 6.0:1 contrast)  |
| Saffron 600         | `#b04e08`                                                                                             | Eyebrow labels, small accent text on white (≥ 5:1) |
| India Green 600     | `#128a3c`                                                                                             | Success ticks, "Updated" badge                     |
| Ink 900 / 700 / 500 | `#111827` / `#374151` / `#6b7280`                                                                     | Body, secondary, muted text                        |
| Fonts               | Plus Jakarta Sans 700/800 (headings), Inter 400–700 (body), Noto Sans Devanagari (Hindi)              |                                                    |
| Type scale          | Fluid, major-third: H1 30→48 px, H2 24→34 px, body 16→17 px, line-height 1.65, max 68 characters/line |                                                    |
| Spacing             | 4 px grid: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80; sections 48→88 px fluid                          |                                                    |
| Radius              | 6 / 10 / 16 px; pills 999 px                                                                          |                                                    |
| Buttons             | Min 48 px tall (WCAG 2.2 target size), 1 primary CTA style per screen                                 |                                                    |

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
