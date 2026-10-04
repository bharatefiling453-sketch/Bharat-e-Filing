# Page roadmap — one page per phase

Every page is built with `scripts/pagekit.py` (identical header, footer, fonts, design system, pop-up, tracking), fact-checked
against primary law, and must pass `npm run check` (HTML, SEO/schema, WCAG 2.2 AA) before delivery. Each service page includes
the real-reviews section (`<!--REVIEWS-->`, see `REVIEWS-KIT.md`).

| Phase | Page                             | Slug                                     | Status                                |
| ----- | -------------------------------- | ---------------------------------------- | ------------------------------------- |
| —     | GST Registration                 | `/gst-registration/`                     | ✅ Done                               |
| —     | GST Return Filing                | `/gst-return-filing/`                    | ✅ Done (merge ChatGPT fixes pending) |
| 1     | Privacy Policy                   | `/privacy-policy/`                       | ✅ Done                               |
| 2     | Terms & Conditions               | `/terms-and-conditions/`                 | Next                                  |
| 3     | Refund Policy                    | `/refund-policy/`                        |                                       |
| 4     | Confidentiality Policy           | `/confidentiality-policy/`               |                                       |
| 5     | Disclaimer                       | `/disclaimer/`                           |                                       |
| 6     | Contact Us                       | `/contact-us/`                           |                                       |
| 7     | About Us                         | `/about-us/`                             |                                       |
| 8     | Editorial Policy                 | `/editorial-policy/`                     |                                       |
| 9     | Income Tax e-Filing (ITR)        | `/income-tax-e-filing/`                  |                                       |
| 10    | ITR for Salaried                 | `/itr-for-salaried/`                     |                                       |
| 11    | ITR for Self Employed            | `/itr-for-self-employed/`                |                                       |
| 12    | ITR for Sole Proprietorship      | `/itr-for-sole-proprietorship/`          |                                       |
| 13    | ITR for Partnership Firm         | `/itr-for-partnership-firm/`             |                                       |
| 14    | ITR for LLP                      | `/itr-for-llp/`                          |                                       |
| 15    | ITR for Company                  | `/itr-for-company/`                      |                                       |
| 16    | TDS Return Filing                | `/tds-return-filing/`                    |                                       |
| 17    | Income Tax Notice                | `/income-tax-notice/`                    |                                       |
| 18    | GST Annual Return (GSTR-9)       | `/gst-annual-return/`                    |                                       |
| 19    | GST LUT Filing                   | `/gst-lut-filing/`                       |                                       |
| 20    | GST Amendment                    | `/gst-registration-amendment/`           |                                       |
| 21    | GST Revocation                   | `/gst-revocation/`                       |                                       |
| 22    | GST Notice Reply                 | `/gst-notice-reply/`                     |                                       |
| 23    | GST E-Invoicing                  | `/gst-e-invoicing/`                      |                                       |
| 24    | GSTR-10 Final Return             | `/gstr-10-final-return/`                 |                                       |
| 25    | Sole Proprietorship Registration | `/sole-proprietorship-registration/`     |                                       |
| 26    | Partnership Firm Registration    | `/partnership-firm-registration/`        |                                       |
| 27    | One Person Company               | `/one-person-company-registration/`      |                                       |
| 28    | LLP Registration                 | `/llp-registration/`                     |                                       |
| 29    | Private Limited Company          | `/private-limited-company-registration/` |                                       |
| 30    | Startup India                    | `/startup-india-registration/`           |                                       |
| 31    | Section 80-IAC                   | `/section-80-iac-registration/`          |                                       |
| 32    | Udyam (MSME) Registration        | `/udyam-registration/`                   |                                       |
| 33    | FSSAI Registration / Licence     | `/fssai-registration/`                   |                                       |
| 34    | Digital Signature (DSC)          | `/digital-signature-certificate/`        |                                       |
| 35    | Import Export Code (IEC)         | `/import-export-code/`                   |                                       |
| 36    | ICEGATE Registration             | `/icegate-registration/`                 |                                       |
| 37    | Trade License                    | `/trade-license/`                        |                                       |
| 38    | Professional Tax Registration    | `/professional-tax-registration/`        |                                       |
| 39    | Trademark Registration           | `/trademark-registration/`               |                                       |
| 40    | Trademark Objection              | `/trademark-objection/`                  |                                       |
| 41    | Trademark Opposition             | `/trademark-opposition/`                 |                                       |
| 42    | Trademark Rectification          | `/trademark-rectification/`              |                                       |
| 43    | Trademark Renewal                | `/trademark-renewal/`                    |                                       |
| 44    | Design Registration              | `/design-registration/`                  |                                       |
| 45    | Logo Design                      | `/logo-design/`                          |                                       |

New clean slugs replace the mixed `/product/…` and `/services/…` URLs; each old URL must 301-redirect to its new page
(see `LINK-INVENTORY.md`). The list will be updated once the full sitemap can be crawled.
