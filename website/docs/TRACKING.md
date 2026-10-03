# Tracking setup — GTM, GA4, Google Ads, Meta, Microsoft Clarity & UET

**Rule: the page contains only two things — the Consent Mode v2 default block and the GTM snippet.**
Every other tag is configured inside one GTM container. This keeps pages fast, lets marketing add or
change tags without developer releases, and keeps consent handled in one place.

## 1. IDs to collect (replace placeholders)

| Placeholder in HTML      | Where to get it                                                                                       |
| ------------------------ | ----------------------------------------------------------------------------------------------------- |
| `GTM-XXXXXXX` (2 places) | tagmanager.google.com → new Web container for bharatefiling.com                                       |
| `REPLACE_GOOGLE_TOKEN`   | Search Console → Settings → Ownership verification → HTML tag (or verify via DNS and delete the meta) |
| `REPLACE_BING_TOKEN`     | Bing Webmaster Tools → import from Search Console (then delete the meta)                              |
| `REPLACE_META_TOKEN`     | Meta Business Suite → Brand safety → Domains                                                          |

## 2. dataLayer events the page already sends (`assets/js/bef-page.js`)

| Event            | Fired when                          | Extra keys                                 |
| ---------------- | ----------------------------------- | ------------------------------------------ |
| `page_meta`      | Page load (before GTM)              | `page_type`, `service`, `service_category` |
| `cta_click`      | Any "Start / Talk to expert" button | `cta_location`, `cta_text`                 |
| `select_plan`    | Pricing plan button                 | `cta_location` (basic/standard/business)   |
| `click_call`     | `tel:` link                         | `cta_location`                             |
| `click_whatsapp` | WhatsApp link                       | `cta_location`                             |
| `file_download`  | Checklist PDF                       | `cta_location`                             |
| `bundle_click`   | Bundle cards                        | `cta_location`                             |
| `faq_open`       | FAQ expanded                        | `faq_question`                             |
| `scroll_depth`   | 25/50/75/100 %                      | `percent`                                  |
| `form_start`     | First keystroke in the lead form    | `form_id`                                  |
| `generate_lead`  | Valid form submit                   | `form_id`, `value`, `currency`             |

Also sent: `popup_open` (key `trigger`: `exit_intent`, `timer` or the button's location), `login_click`, and `plan`
(basic / standard / business) on every `generate_lead`, whose `value` is the chosen plan's price.

Hidden form fields capture `utm_*`, `gclid`, `fbclid`, `msclkid` so every lead in the CRM has its source.

## 3. GTM container — tags to create

| Tag                                                | Trigger                                                                                                                                                                          | Notes                                                                                                                              |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Google tag (GA4 config)                            | Initialization – All Pages                                                                                                                                                       | Measurement ID `G-…`                                                                                                               |
| GA4 event — `{{Event}}`                            | Custom event regex `cta_click\|select_plan\|popup_open\|login_click\|click_call\|click_whatsapp\|file_download\|bundle_click\|faq_open\|scroll_depth\|form_start\|generate_lead` | Pass the extra keys as event parameters; mark `generate_lead`, `click_call`, `click_whatsapp`, `purchase` as **key events** in GA4 |
| Google Ads Conversion – Lead                       | `generate_lead`                                                                                                                                                                  | Turn on **Enhanced Conversions** (hashed email/phone)                                                                              |
| Google Ads Remarketing                             | All Pages                                                                                                                                                                        |                                                                                                                                    |
| Meta Pixel base + `Lead` / `Contact`               | All Pages / `generate_lead` / `click_whatsapp`                                                                                                                                   | Add Conversions API through WooCommerce Meta plugin or server-side GTM, deduplicated by `event_id`                                 |
| Microsoft Clarity                                  | All Pages (Initialization)                                                                                                                                                       | Use the Clarity community template; enable Clarity consent API                                                                     |
| Microsoft UET                                      | All Pages + custom event `generate_lead`                                                                                                                                         | Enable UET Consent Mode                                                                                                            |
| Consent banner (Complianz/CookieYes/CookieConsent) | Consent Initialization                                                                                                                                                           | Calls `gtag('consent','update',…)` on accept                                                                                       |

## 4. WooCommerce purchase tracking

Install **GTM4WP** → enable WooCommerce integration → GA4 ecommerce events (`view_item`, `add_to_cart`,
`begin_checkout`, `purchase`) are pushed automatically. Map `purchase` to Google Ads, Meta `Purchase` and UET.

## 5. Verify before launch

1. GTM **Preview** — every event in the table fires once with the right `cta_location`.
2. GA4 **DebugView** — parameters arrive; key events marked.
3. Meta **Events Manager → Test events**; Clarity dashboard shows a recording; UET Tag Helper green.
4. With consent **denied**, no `_ga` / `_fbp` cookies are set.
