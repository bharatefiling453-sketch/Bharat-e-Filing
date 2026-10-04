# Link inventory — bharatefiling.com + the two new pages (4 Oct 2026)

> **How this list was built.** bharatefiling.com is blocked by this environment's network policy, so the live site could not
> be crawled directly. Part 1 lists every URL that search engines return for the domain (28 confirmed). It is **not yet the
> complete site**: allow `bharatefiling.com` in the environment's network settings and the sitemap can be crawled for a full list.
> Part 2 is complete: every link in the two new pages, extracted from the source files.

---

## Part 1 — Live website (bharatefiling.com)

### 1A. Confirmed URLs (28)

| #   | Section       | Page                             | URL                                                                  |
| --- | ------------- | -------------------------------- | -------------------------------------------------------------------- |
| 1   | Core          | Home                             | https://bharatefiling.com/                                           |
| 2   | Core          | About us                         | https://bharatefiling.com/about-us/                                  |
| 3   | GST           | GST category                     | https://bharatefiling.com/product-category/gst/                      |
| 4   | GST           | GST Return Filing (GSTR-1 & 3B)  | https://bharatefiling.com/product/gst-return-filing-gstr-1-gstr-3b/  |
| 5   | GST           | GST Annual Return (GSTR-9)       | https://bharatefiling.com/product/gst-annual-return-filing-gstr-9/   |
| 6   | GST           | GST Registration Amendment       | https://bharatefiling.com/product/gst-registration-amendment/        |
| 7   | GST           | GST Revocation                   | https://bharatefiling.com/product/gst-revocation-registration/       |
| 8   | GST           | GST Notice (product)             | https://bharatefiling.com/product/gst-notice                         |
| 9   | GST           | GST Notice (service)             | https://bharatefiling.com/services/gst-notice-online/                |
| 10  | GST           | GST Registration in Pune         | https://bharatefiling.com/gst-registration-in-pune-2/                |
| 11  | Income tax    | Income Tax e-Filing              | https://bharatefiling.com/product/income-tax-e-filing/               |
| 12  | Income tax    | ITR for Salaried                 | https://bharatefiling.com/product/itr-for-salaried-guide/            |
| 13  | Income tax    | ITR for Sole Proprietorship      | https://bharatefiling.com/product/itr-for-sole-proprietorship/       |
| 14  | Income tax    | ITR for LLP                      | https://bharatefiling.com/services/itr-for-llp/                      |
| 15  | Income tax    | TDS Return Filing                | https://bharatefiling.com/services/tds-return-filing/                |
| 16  | Business      | Sole Proprietorship Registration | https://bharatefiling.com/sole-proprietorship-registration-in-india/ |
| 17  | Business      | Startup India                    | https://bharatefiling.com/product/startup-india/                     |
| 18  | Business      | Section 80-IAC Registration      | https://bharatefiling.com/section-80-iac-registration/               |
| 19  | Registrations | Udyam Registration (product)     | https://bharatefiling.com/product/udyam-registration/                |
| 20  | Registrations | Udyam Registration (service)     | https://bharatefiling.com/services/udyam-registration/               |
| 21  | Registrations | Professional Tax Registration    | https://bharatefiling.com/product/professional-tax-registration/     |
| 22  | Registrations | ICEGATE Registration             | https://bharatefiling.com/product/icegate-registration/              |
| 23  | Registrations | Import Export Code (IEC)         | https://bharatefiling.com/product/import-export-code/                |
| 24  | Trademark     | Trademark Registration (product) | https://bharatefiling.com/product/trademark-registration             |
| 25  | Trademark     | Trademark Registration (service) | https://bharatefiling.com/services/trademark-registration/           |
| 26  | Trademark     | Trademark Objection              | https://bharatefiling.com/product/trademark-objection/               |
| 27  | Trademark     | Trademark Opposition             | https://bharatefiling.com/product/trademark-opposition/              |
| 28  | Trademark     | Trademark Rectification          | https://bharatefiling.com/product/trademark-rectification/           |

### 1B. Indexed on the demo subdomain (should not be public)

| URL                                                           | Note                                                                          |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| https://demo.bharatefiling.com/product/trademark-opposition/  | Duplicate of #27                                                              |
| https://demo.bharatefiling.com/product/itr-for-self-employed/ | Suggests a live `/product/itr-for-self-employed/` page exists (not confirmed) |

### 1C. Services named on the site whose URL was not found (19)

GST Registration (main page) · GST Invoicing & E-Invoicing · GST LUT Form · GSTR-10 (Final Return) · ITR for Self Employed ·
ITR for Partnership Firms · ITR for Company · Income Tax Notice · Partnership Firm Registration · One Person Company ·
LLP Registration · Private Limited Company · FSSAI Registration / Renewal · Digital Signature · Trade License ·
Trademark Renewal · Logo Designing · Design Registration · Contact Us, Privacy Policy, Terms & Conditions, Refund Policy,
Confidentiality Policy, Disclaimer Policy (policy pages exist; URLs not returned)

### 1D. Issues spotted

| Issue                                                       | Example                                                                   | Why it matters                                                                              |
| ----------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Demo site indexed by Google**                             | `demo.bharatefiling.com/...`                                              | Duplicate content competes with the real pages. Add `noindex` or password-protect the demo. |
| **Same service on two URLs** (`/product/` and `/services/`) | Trademark Registration (#24, #25); Udyam (#19, #20); GST Notice (#8, #9)  | Splits ranking signals. Keep one and 301-redirect the other.                                |
| **Mixed URL patterns**                                      | `/product/…`, `/services/…`, root-level (`/section-80-iac-registration/`) | Harder for users and search engines; pick one pattern going forward.                        |
| **Missing trailing slash**                                  | `/product/trademark-registration`, `/product/gst-notice`                  | Can create duplicate URLs if both forms resolve.                                            |
| **"-2" slug**                                               | `/gst-registration-in-pune-2/`                                            | Sign of a duplicate/older page with the same slug.                                          |
| **Year in slugs / titles**                                  | "…Guide 2025" titles                                                      | Dates age pages; update titles yearly or remove the year.                                   |

---

## Part 2 — Links in the two new pages (59 unique)

Legend: **Reg** = GST Registration page · **Returns** = GST Return Filing page

### 2A. Live, confirmed (14) — OK

| URL                                                                 | Used on      |
| ------------------------------------------------------------------- | ------------ |
| https://bharatefiling.com/                                          | Reg, Returns |
| https://bharatefiling.com/about-us/                                 | Reg, Returns |
| https://bharatefiling.com/product-category/gst/                     | Reg, Returns |
| https://bharatefiling.com/product/gst-return-filing-gstr-1-gstr-3b/ | Reg, Returns |
| https://bharatefiling.com/product/gst-annual-return-filing-gstr-9/  | Reg, Returns |
| https://bharatefiling.com/product/gst-registration-amendment/       | Reg, Returns |
| https://bharatefiling.com/product/gst-revocation-registration/      | Reg, Returns |
| https://bharatefiling.com/services/gst-notice-online/               | Returns      |
| https://bharatefiling.com/product/icegate-registration/             | Reg, Returns |
| https://bharatefiling.com/product/professional-tax-registration/    | Reg, Returns |
| https://bharatefiling.com/product/startup-india/                    | Reg, Returns |
| https://bharatefiling.com/product/itr-for-sole-proprietorship/      | Reg, Returns |
| https://bharatefiling.com/product/trademark-objection/              | Reg, Returns |
| https://bharatefiling.com/product/trademark-opposition/             | Reg, Returns |

### 2B. New pages proposed by us (2) — go live together

| URL                                          | Used on                  |
| -------------------------------------------- | ------------------------ |
| https://bharatefiling.com/gst-registration/  | Reg (canonical), Returns |
| https://bharatefiling.com/gst-return-filing/ | Returns (canonical)      |

### 2C. Guessed URLs — not confirmed (21)

| URL in our pages                                                        | Used on                      | Suggested fix                                                                       |
| ----------------------------------------------------------------------- | ---------------------------- | ----------------------------------------------------------------------------------- |
| https://bharatefiling.com/tds-return-filing/                            | Reg, Returns                 | → **https://bharatefiling.com/services/tds-return-filing/** (confirmed)             |
| https://bharatefiling.com/msme-udyam-registration/                      | Reg, Returns                 | → **https://bharatefiling.com/product/udyam-registration/** (confirmed)             |
| https://bharatefiling.com/income-tax/                                   | Reg, Returns (main menu)     | → **https://bharatefiling.com/product/income-tax-e-filing/** or real category URL   |
| https://bharatefiling.com/trademark/                                    | Reg, Returns (main menu)     | → **https://bharatefiling.com/product/trademark-registration** or real category URL |
| https://bharatefiling.com/business-registration/                        | Reg, Returns (main menu)     | Real category URL needed                                                            |
| https://bharatefiling.com/compliance/                                   | Reg, Returns (main menu)     | Real category URL needed                                                            |
| https://bharatefiling.com/learn/                                        | Reg, Returns (menu + footer) | Real blog/guides URL needed                                                         |
| https://bharatefiling.com/learn/income-tax-act-2025-changes/            | Reg                          | Article to be written                                                               |
| https://bharatefiling.com/tax-audit/                                    | Reg, Returns (footer)        | Real URL needed                                                                     |
| https://bharatefiling.com/income-tax-notice/                            | Reg, Returns (footer)        | Real URL needed                                                                     |
| https://bharatefiling.com/my-account/                                   | Reg, Returns (Log in)        | Confirm WooCommerce account URL                                                     |
| https://bharatefiling.com/contact-us/                                   | Reg, Returns                 | Confirm                                                                             |
| https://bharatefiling.com/privacy-policy/                               | Reg, Returns                 | Confirm                                                                             |
| https://bharatefiling.com/terms-and-conditions/                         | Reg, Returns                 | Confirm                                                                             |
| https://bharatefiling.com/refund-policy/                                | Reg, Returns                 | Confirm                                                                             |
| https://bharatefiling.com/editorial-policy/                             | Reg, Returns                 | Page to be created                                                                  |
| https://bharatefiling.com/sitemap_index.xml                             | Reg, Returns                 | Confirm (Rank Math/Yoast default)                                                   |
| https://bharatefiling.com/downloads/gst-registration-checklist.pdf      | Reg                          | PDF to be created                                                                   |
| https://bharatefiling.com/bundles/gst-registration-msme-udyam/          | Reg                          | Bundle page to be created                                                           |
| https://bharatefiling.com/bundles/gst-registration-12-months-filing/    | Reg                          | Bundle page to be created                                                           |
| https://bharatefiling.com/hi/gst-registration/ · /hi/gst-return-filing/ | In HTML comments only        | Future Hindi pages                                                                  |

### 2D. Placeholders (6)

| Link                                                      | Used on               | Needs                  |
| --------------------------------------------------------- | --------------------- | ---------------------- |
| tel:+910000000000                                         | Reg, Returns          | Real phone             |
| https://wa.me/910000000000?text=… (2 versions)            | Reg / Returns         | Real WhatsApp number   |
| mailto:care@bharatefiling.com                             | Reg, Returns          | Confirm email          |
| https://bharatefiling.com/team/REPLACE_CA_SLUG/           | Reg, Returns (schema) | Reviewer CA page       |
| (no link) REPLACE_GOOGLE_TOKEN / BING / META, GTM-XXXXXXX | Reg, Returns          | Verification & tag IDs |

### 2E. Social profiles — handles guessed (5)

| Our link                                       | Used on      | ChatGPT's version (unconfirmed)                  |
| ---------------------------------------------- | ------------ | ------------------------------------------------ |
| https://www.facebook.com/bharatefiling         | Reg, Returns | —                                                |
| https://www.instagram.com/bharatefiling        | Reg, Returns | https://www.instagram.com/bharat_efiling/        |
| https://www.linkedin.com/company/bharatefiling | Reg, Returns | https://www.linkedin.com/company/bharate-filing/ |
| https://www.youtube.com/@bharatefiling         | Reg, Returns | —                                                |
| https://x.com/bharatefiling                    | Reg, Returns | https://x.com/Bharat_efiling                     |

### 2F. Image assets referenced (3) — to upload

| URL                                                                            | Used on                      |
| ------------------------------------------------------------------------------ | ---------------------------- |
| https://bharatefiling.com/wp-content/uploads/og/gst-registration-1200x630.jpg  | Reg (social share image)     |
| https://bharatefiling.com/wp-content/uploads/og/gst-return-filing-1200x630.jpg | Returns (social share image) |
| https://bharatefiling.com/wp-content/uploads/bef-logo.png                      | Reg, Returns (schema logo)   |

### 2G. External official sources (8) — OK

| URL                                                                        | Used on      |
| -------------------------------------------------------------------------- | ------------ |
| https://www.gst.gov.in/                                                    | Reg, Returns |
| https://cbic-gst.gov.in/                                                   | Reg, Returns |
| https://taxinformation.cbic.gov.in/                                        | Reg, Returns |
| https://gstcouncil.gov.in/                                                 | Reg, Returns |
| https://www.incometaxindia.gov.in/                                         | Reg, Returns |
| https://delhihighcourt.nic.in/                                             | Reg          |
| https://tutorial.gst.gov.in/userguide/registration/                        | Reg          |
| https://tutorial.gst.gov.in/userguide/returns/Create_and_Submit_GSTR3B.htm | Returns      |

Not counted as links: in-page anchors (`#pricing`, `#faqs` …), schema IDs (`/#organization`, `/#website`), Google Fonts and
Google Tag Manager script URLs.
