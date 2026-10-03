# Bharat eFiling — Website Rebuild Kit

Design system, reference service page and QA toolchain for rebuilding every Bharat eFiling product page.
**Start with `gst-registration/index.html`** — it is the template for all other services.

```
website/
├── gst-registration/index.html     ← reference service page (copy for every product)
├── gst-return-filing/index.html    ← GST Return Filing page (with due-date finder + late fee calculator)
├── assets/css/bef-design-system.css ← colours, fonts, spacing, all components
├── assets/js/bef-page.js           ← nav, TOC, FAQ, form validation, dataLayer events
├── docs/PRODUCT-PAGE-STANDARD.md   ← the rules: slug, SEO, AEO, GEO, schema, linking, design, launch checklist
├── docs/RESOURCES.md               ← repos, WordPress plugins & tools to use
├── docs/TRACKING.md                ← GTM / GA4 / Ads / Meta / Clarity / UET setup
├── robots.txt · llms.txt · sitemap-services.xml
└── scripts/                        ← automated SEO + accessibility checks
```

## For developers (Discord hand-off)

```bash
cd website
npm install            # installs html-validate, stylelint, prettier, lighthouse, playwright, axe, linkinator
npm run serve          # http://localhost:8080/gst-registration/
npm run check          # HTML + CSS lint, SEO/schema check, WCAG 2.2 AA check (+ screenshots in reports/)
```

`check:a11y` uses Chromium via Playwright. If no browser is installed run `npx playwright install chromium`,
or set `CHROME_PATH` to an existing Chrome/Chromium binary.

### Making a new service page

1. Copy `gst-registration/` to `/{new-slug}/` and follow the section order in `docs/PRODUCT-PAGE-STANDARD.md §3`.
2. Update `<title>`, meta, canonical, OG tags, JSON-LD (`Service`, `FAQPage`, `BreadcrumbList`, `HowTo`), `data-service` on `<body>`.
3. Keep FAQ text identical in HTML and JSON-LD; run `npm run check:seo`.
4. Get CA sign-off on facts, then run the launch checklist (§12).

### Using on WordPress

Load `bef-design-system.css` and `bef-page.js` from the child theme; build each section as a reusable
GenerateBlocks/Kadence pattern using the same class names; let Rank Math output the schema graph (paste the
FAQ/Service/HowTo JSON from this page into Rank Math's custom schema) — do not output schema twice.

## Sharing the page as one file (Discord, email, WhatsApp)

```bash
npm run build:single   # → dist/bharat-efiling-gst-registration.html and dist/bharat-efiling-gst-return-filing.html
```

The output embeds everything (styles, scripts, logo, favicon and the Inter + Noto Sans Devanagari fonts), so it looks
identical on any computer, even offline. Re-run it after every edit. Recipients download the file from Discord and open it
in Chrome, Edge, Safari or Firefox (Discord shows `.html` attachments as a download, not a rendered page).

## Before launch — placeholders to replace

| Placeholder                                                  | Meaning                                                        |
| ------------------------------------------------------------ | -------------------------------------------------------------- |
| `+91 00000 00000`, `tel:+910000000000`, `wa.me/910000000000` | Real phone & WhatsApp numbers                                  |
| `care@bharatefiling.com`                                     | Confirm the real support email                                 |
| `REPLACE_STREET/CITY/STATE`, `000000`                        | Registered office address (must match Google Business Profile) |
| `REPLACE_CA_NAME`, ICAI no., `/team/REPLACE_CA_SLUG/`        | Reviewing Chartered Accountant                                 |
| `REPLACE+`, `REPLACE ★`                                      | Real GSTIN count and real Google rating — or delete            |
| ₹999 / ₹1,999 / ₹4,999                                       | **Example prices** — confirm with management (HTML + JSON-LD)  |
| Social URLs (`/bharatefiling`)                               | Confirm actual handles                                         |
| `GTM-XXXXXXX`, verification tokens                           | See `docs/TRACKING.md`                                         |
| OG image, logo, checklist PDF URLs                           | Create and upload the assets                                   |

`npm run check:seo` lists any placeholder still present.
