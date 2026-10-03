# Repositories, plugins & tools for the Bharat eFiling rebuild

Everything the design, development and SEO team needs to build product pages that outrank
IndiaFilings, ClearTax, Vakilsearch, RegisterKaro and the rest.

**Legend** — ✅ already installed in `website/package.json` · ⭐ must-have · ➕ nice-to-have

---

## 1. Platform decision (read first)

The live site is **WordPress + WooCommerce** (`/product-category/gst/`). Two routes:

| Route                                          | When to choose                                               | Stack                                                                                                                           |
| ---------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **A. Stay on WordPress (recommended for now)** | Team edits content daily, WooCommerce checkout already works | GeneratePress or Kadence theme + GenerateBlocks/Kadence Blocks + Rank Math Pro + this design system as a child-theme stylesheet |
| B. Headless / static                           | Later, when speed is the top priority and devs own content   | Next.js or Astro + a headless CMS; WordPress kept only for checkout                                                             |

The reference page in `gst-registration/index.html` is plain HTML + one CSS file + one JS file so it drops
into **either** route without rework.

## 2. WordPress plugins (route A)

| ⭐  | Plugin                                                                                         | Purpose                                                                                                                        |
| --- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| ⭐  | **Rank Math SEO (Pro)**                                                                        | Titles/meta, schema (Service, FAQ, Breadcrumb), XML sitemaps, redirects, 404 monitor, IndexNow                                 |
| ⭐  | **GeneratePress Premium** + **GenerateBlocks Pro** _or_ **Kadence Theme** + **Kadence Blocks** | Lightweight theme and blocks that can reproduce this design system without page-builder bloat (avoid Elementor/Divi for speed) |
| ⭐  | **Google Site Kit** _or_ **GTM4WP** (Duracell Tomi)                                            | Inserts GTM container + WooCommerce dataLayer (purchase, add_to_cart)                                                          |
| ⭐  | **Complianz** _or_ **CookieYes**                                                               | Cookie banner with Google Consent Mode v2 (needed for GA4/Ads in India & EU visitors)                                          |
| ⭐  | **WP Rocket** _or_ **LiteSpeed Cache** (if host is LiteSpeed)                                  | Page cache, critical CSS, delay JS                                                                                             |
| ⭐  | **ShortPixel** _or_ **Imagify**                                                                | WebP/AVIF conversion, compression                                                                                              |
| ⭐  | **Fluent Forms** _or_ **WPForms**                                                              | Lead forms with UTM hidden fields, CRM webhooks                                                                                |
| ⭐  | **Redirection** (or Rank Math redirects)                                                       | 301 old `/product-category/…` and `/product/…` URLs to new clean slugs                                                         |
| ⭐  | **Wordfence** + **UpdraftPlus**                                                                | Security + backups                                                                                                             |
| ➕  | **Perfmatters**                                                                                | Disable unused scripts per page                                                                                                |
| ➕  | **Click to Chat (HoliThemes)**                                                                 | WhatsApp button                                                                                                                |
| ➕  | **WP Google Review Slider / Trustindex**                                                       | Real Google reviews widget (never hand-written testimonials)                                                                   |
| ➕  | **TablePress**                                                                                 | Reusable threshold / due-date tables                                                                                           |
| ➕  | **Polylang / WPML**                                                                            | Hindi pages (`/hi/…`) with hreflang                                                                                            |
| ➕  | **Microsoft Clarity** (official plugin)                                                        | Heatmaps & session recordings (or fire via GTM)                                                                                |

## 3. GitHub repositories — UI / UX & design system

| ⭐  | Repository                                                              | Why                                                                                                        |
| --- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| ⭐  | [tailwindlabs/tailwindcss](https://github.com/tailwindlabs/tailwindcss) | Utility CSS if you move to a headless build; tokens in `bef-design-system.css` map 1:1 to a Tailwind theme |
| ⭐  | [shadcn-ui/ui](https://github.com/shadcn-ui/ui)                         | Accessible, copy-paste React components (accordion, tabs, dialog) for Next.js route                        |
| ⭐  | [radix-ui/primitives](https://github.com/radix-ui/primitives)           | Unstyled accessible primitives behind shadcn                                                               |
| ➕  | [saadeghi/daisyui](https://github.com/saadeghi/daisyui)                 | Tailwind component classes if the team prefers HTML over React                                             |
| ➕  | [argyleink/open-props](https://github.com/argyleink/open-props)         | Ready CSS custom-property scales (spacing, shadows, easing) — reference for our tokens                     |
| ⭐  | [lucide-icons/lucide](https://github.com/lucide-icons/lucide)           | Consistent 24px stroke icons (matches the icons used on the page)                                          |
| ➕  | [tabler/tabler-icons](https://github.com/tabler/tabler-icons)           | 5,000+ icons incl. finance/legal glyphs                                                                    |
| ➕  | [tailwindlabs/heroicons](https://github.com/tailwindlabs/heroicons)     | Alternate icon set                                                                                         |
| ⭐  | [rsms/inter](https://github.com/rsms/inter)                             | The single brand font (v2): variable weights + optical sizing, excellent ₹ and tabular figures             |
| ⭐  | [notofonts/devanagari](https://github.com/notofonts/devanagari)         | Noto Sans Devanagari for Hindi pages                                                                       |
| ⭐  | [fontsource/fontsource](https://github.com/fontsource/fontsource)       | Self-host fonts (faster + no third-party request; DPDP-friendly)                                           |
| ➕  | [airbnb/lottie-web](https://github.com/airbnb/lottie-web)               | Lightweight animated illustrations (process steps, success state)                                          |
| ➕  | [penpot/penpot](https://github.com/penpot/penpot)                       | Open-source Figma alternative if the design team needs one                                                 |
| ➕  | [storybookjs/storybook](https://github.com/storybookjs/storybook)       | Component catalogue so every page uses the same blocks                                                     |
| ➕  | [alpinejs/alpine](https://github.com/alpinejs/alpine)                   | Tiny JS for tabs, calculators, toggles on WordPress pages                                                  |
| ⭐  | [anthropics/skills](https://github.com/anthropics/skills)               | Claude "frontend-design" skill used to generate distinctive, non-generic UI                                |

**Illustrations (websites, free commercial licences):** unDraw (undraw.co — set brand colour `#0f2b5b`),
Storyset by Freepik (attribution), Blush, Humaaans. Commission 5–6 custom India-specific scenes
(Kirana shop, home bakery, freelancer, e-commerce seller, CA desk) for a unique brand look.

## 4. GitHub repositories — SEO, AEO & GEO

| ⭐   | Repository                                                                  | Why                                                                             |
| ---- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| ⭐   | [schemaorg/schemaorg](https://github.com/schemaorg/schemaorg)               | Source of truth for Service, FAQPage, HowTo, Organization vocab                 |
| ✅⭐ | [google/schema-dts](https://github.com/google/schema-dts)                   | TypeScript types to build valid JSON-LD                                         |
| ⭐   | [Yoast/wordpress-seo](https://github.com/Yoast/wordpress-seo)               | Read their schema graph implementation (we mirror the `@graph` + `@id` pattern) |
| ⭐   | [AnswerDotAI/llms-txt](https://github.com/AnswerDotAI/llms-txt)             | `llms.txt` spec — helps ChatGPT/Perplexity/Claude understand the site (GEO)     |
| ⭐   | [GoogleChrome/lighthouse](https://github.com/GoogleChrome/lighthouse) ✅    | Performance / SEO / a11y audits                                                 |
| ⭐   | [GoogleChrome/lighthouse-ci](https://github.com/GoogleChrome/lighthouse-ci) | Fail a deploy if scores drop                                                    |
| ⭐   | [GoogleChrome/web-vitals](https://github.com/GoogleChrome/web-vitals)       | Send real-user LCP/INP/CLS to GA4                                               |
| ➕   | [harlan-zw/unlighthouse](https://github.com/harlan-zw/unlighthouse)         | Lighthouse for every URL of the site in one run                                 |
| ✅   | [JustinBeckwith/linkinator](https://github.com/JustinBeckwith/linkinator)   | Broken internal/external link checker                                           |
| ➕   | [ekalinin/sitemap.js](https://github.com/ekalinin/sitemap.js)               | Sitemap generation for a headless build                                         |
| ➕   | [garmeeh/next-seo](https://github.com/garmeeh/next-seo)                     | Meta + JSON-LD helpers if you choose Next.js                                    |

**SaaS tools (not repos):** Google Search Console, Bing Webmaster Tools (also feeds ChatGPT search),
Rich Results Test, Schema Markup Validator, PageSpeed Insights, Screaming Frog SEO Spider,
Ahrefs or Semrush (keyword gaps vs competitors), AlsoAsked / AnswerThePublic (FAQ discovery),
Google Trends (Hindi vs English query volume).

## 5. Tracking & marketing

| ⭐  | Item                                                                  | Notes                                                                                               |
| --- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| ⭐  | Google Tag Manager (web container)                                    | Only snippet on the page; everything else fires inside it — see `TRACKING.md`                       |
| ⭐  | GA4                                                                   | Key events: `generate_lead`, `click_call`, `click_whatsapp`, `purchase`                             |
| ⭐  | Google Ads conversion + Enhanced Conversions                          | Hashed email/phone from lead form                                                                   |
| ⭐  | Meta Pixel + Conversions API                                          | CAPI via WooCommerce plugin or server GTM                                                           |
| ⭐  | Microsoft Clarity                                                     | Free heatmaps; [microsoft/clarity](https://github.com/microsoft/clarity) is the open-source library |
| ⭐  | Microsoft Advertising UET tag                                         | Bing ads + consent mode                                                                             |
| ⭐  | [orestbida/cookieconsent](https://github.com/orestbida/cookieconsent) | Free consent banner if not using Complianz/CookieYes                                                |
| ➕  | [QwikDev/partytown](https://github.com/QwikDev/partytown)             | Move third-party tags off the main thread (headless route)                                          |

## 6. Quality & performance (✅ installed in `website/`)

| Tool                                                           | Command                                   | Checks                                                                                                                               |
| -------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| ✅ html-validate                                               | `npm run lint:html`                       | Valid, accessible HTML                                                                                                               |
| ✅ stylelint + config-standard                                 | `npm run lint:css`                        | CSS consistency                                                                                                                      |
| ✅ prettier                                                    | `npm run format`                          | Formatting                                                                                                                           |
| ✅ cheerio (custom script)                                     | `npm run check:seo`                       | Title/meta lengths, 1×H1, heading order, schema present, FAQ text = FAQ schema, ≥8 internal links, ≥3 external sources, placeholders |
| ✅ playwright + @axe-core/playwright                           | `npm run check:a11y`                      | WCAG 2.2 AA on desktop + mobile, horizontal scroll, screenshots in `reports/`                                                        |
| ✅ lighthouse                                                  | `npm run serve` then `npm run lighthouse` | Core Web Vitals lab scores                                                                                                           |
| ✅ linkinator                                                  | `npm run lint:links`                      | Broken links                                                                                                                         |
| ➕ [lovell/sharp](https://github.com/lovell/sharp)             | —                                         | Batch convert illustrations to AVIF/WebP                                                                                             |
| ➕ [danielroe/beasties](https://github.com/danielroe/beasties) | —                                         | Inline critical CSS (successor of Critters)                                                                                          |

## 7. Official sources for fact-checking (link these on every page)

- GST Portal — <https://www.gst.gov.in/> and user manuals <https://tutorial.gst.gov.in/>
- CBIC GST Acts, Rules & Notifications — <https://cbic-gst.gov.in/> / <https://taxinformation.cbic.gov.in/>
- GST Council meeting recommendations — <https://gstcouncil.gov.in/>
- Income Tax Department — Income-tax Act, 2025 and 1961 — <https://www.incometaxindia.gov.in/>
- MCA (company/LLP pages) — <https://www.mca.gov.in/>
- Udyam (MSME pages) — <https://udyamregistration.gov.in/>
- IP India (trademark pages) — <https://ipindia.gov.in/>
