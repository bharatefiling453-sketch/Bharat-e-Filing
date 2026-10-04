# Bharat e-Filing blog standard (v1)

Reference post: `src/blog/tax-audit-due-date-extended-ay-2026-27/page.py` → `/blog/tax-audit-due-date-extended-ay-2026-27/`.
Copy that folder for every new post, then build with `python3 scripts/pagekit.py blog/<slug>` and run `npm run check`.

## Page order (do not change)

1. Reading-progress bar (top, saffron→amber).
2. Hero: breadcrumb (Home › Blog › Category › Post) · chips (category, "Updated <date>", AY, read time) · H1 · dek
   (1–2 sentences) · byline (writer + CA fact-checker) · published date · share (WhatsApp, LinkedIn, X, copy link).
3. **Image 1: featured/cover** 1200×675 (also the og:image and schema image).
4. Two columns on desktop: article (max 760px) + sticky aside (table of contents, CTA card). One column on mobile with a
   collapsible table of contents.
5. Article: quick answer (`.answer`, 35–70 words) → visual summary (e.g. date cards) → key takeaways (4–6 bullets) →
   intro → H2 sections in question form → **image 2** (infographic) mid-article → tables, notes, decision checks →
   mid-article CTA after the "risk/penalty" section → numbered action plan → **image 3** (screenshot/how-to) →
   author/reviewer card → FAQ (8–10, identical to FAQPage schema) → official sources → disclaimer.
6. Related: 3 cards (2 guides + 1 service page).

## SEO / AEO / GEO checklist (enforced by `scripts/seo-check.mjs` where marked ✓)

| Item               | Rule                                                                                                                                                                                                                                    |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Title ✓            | 30–60 chars, primary keyword first, ends with "Bharat e-Filing"                                                                                                                                                                         |
| Meta description ✓ | 120–160 chars, keyword + date + benefit                                                                                                                                                                                                 |
| URL ✓              | `/blog/<keyword-slug>/`, lowercase, hyphens, trailing slash, no dates unless evergreen-proofed                                                                                                                                          |
| H1 ✓               | Exactly one; can be longer than the title (≤110 chars for headline schema)                                                                                                                                                              |
| Headings ✓         | No skipped levels; H2s phrased as questions people search                                                                                                                                                                               |
| Quick answer ✓     | 35–70 words, in `.answer` (speakable + AI-overview friendly)                                                                                                                                                                            |
| Schema ✓           | Organization, WebSite, WebPage (+reviewedBy, primaryImageOfPage), BreadcrumbList, BlogPosting (headline, image, author, dates with time zone, publisher, wordCount, about, mentions, citation, keywords), Person (CA reviewer), FAQPage |
| Open Graph ✓       | og:type=article, article:published_time / modified_time / section / tag, 1200×630 image                                                                                                                                                 |
| Links ✓            | ≥8 internal (service pages + related posts), ≥3 official external (incometax.gov.in, incometaxindia.gov.in, cbic, mca, indiabudget) opened in a new tab with `rel="noopener"`                                                           |
| Length ✓           | ≥1,500 words of useful content; no filler                                                                                                                                                                                               |
| Dates ✓            | Visible published + updated `<time>`; bump `modified` and the "Updated" chip on every factual change                                                                                                                                    |
| E-E-A-T            | Named CA reviewer with ICAI membership number, author box, editorial-policy link, sources list                                                                                                                                          |
| Images             | 3 placeholders, descriptive alt text, WebP, explicit size, lazy-load except the cover                                                                                                                                                   |
| Accessibility ✓    | WCAG 2.2 AA (axe): contrast, table captions, focusable scroll regions, labelled share group                                                                                                                                             |
| Keywords           | 1 primary + 4–6 secondary in title, H1, first 100 words, one H2, image alt, FAQ; no meta keywords tag                                                                                                                                   |

## Fixes made to the supplied draft

- **Brand and design:** "Bharat eFiling" → "Bharat e-Filing". The off-brand palette (cream background, marigold, brick) and the dark-mode colours are replaced with the site design system (navy/saffron/leaf, Inter, white). The page now has the site header, footer, pop-up, mobile action bar and tracking.
- **Title and canonical:** the title was 66 chars and is now 60. The canonical had no trailing slash and now has one. The meta keywords tag is dropped (search engines ignore it).
- **Schema:** before, it was only Article + FAQPage, with no image, no author person and no breadcrumb. It is now a full BlogPosting graph with a CA reviewer and a breadcrumb. Dates now carry the time zone.
- **Facts:**
  - **Section 234A:** the draft only said "silent on 234A". The post now explains why interest may still run from 31 October and says to pay tax by then.
  - **Form 3CEB:** the 31 October 2026 transfer-pricing report date (unchanged) was missing and is now added.
  - **Voluntary audit:** a voluntary audit does not move you into the audit category; this now appears in both the FAQ and the body.
  - **Section 43B(h):** added to the Form 3CD review step (delayed payments to MSME suppliers).
  - **Unverified date:** the claim that the portal news was posted on 29 September is removed.
- **Links:**
  - The "ITR filing service" and "GST return filing" links pointed to the homepage and are corrected.
  - The circular PDF URL could not be verified, so the post links to the portal news page and the CBDT circulars page instead.
  - Internal links: 1 → 12 or more.
- **UX:**
  - Added a table of contents (sticky on desktop, collapsible on mobile), reading progress, read time, share buttons, key takeaways, two in-article CTAs, related cards and 3 image placeholders.
  - The countdown now runs inside the date cards.

## Before publishing a post

- [ ] Replace `REPLACE_CA_NAME` / ICAI number (byline, author card, schema).
- [ ] Upload the 3 images to the paths in the comments; swap each `.img-ph` for `<img width height alt loading>`.
- [ ] Confirm that every internal URL in "Related" is live.
- [ ] Add the post to `/blog/`, the category page, `sitemap.xml` and (for news) `news-sitemap.xml`.
- [ ] Submit the URL in Search Console and Bing Webmaster (IndexNow).
