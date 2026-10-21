# Builds partnership-llp-itr-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/partnership-llp-itr-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/partnership-llp-itr-filing/"
TITLE = "Partnership Firm & LLP ITR Filing (ITR-5) | Bharat e-Filing"
DESC = "File ITR-5 for your partnership firm or LLP. Partner remuneration, Section 194T TDS, tax audit and LLP Form 8 and Form 11 handled by Chartered Accountants."
OG = "https://bharatefiling.com/wp-content/uploads/og/partnership-llp-itr-filing-1200x630.jpg"
PUB = "2026-10-21"
SLUG = "partnership-llp-itr-filing"

FAQ = [
 ("Which ITR form does a partnership firm or LLP file?", "Both file ITR-5. A partnership firm (other than an LLP) that opts for presumptive taxation under Section 44AD or 44ADA can file ITR-4 instead. An LLP always files ITR-5."),
 ("Is it mandatory for a firm or LLP to file an income tax return?", "Yes. Every partnership firm and LLP must file its return every year under Section 139(1), whatever its income, even if it made a loss or had no business during the year."),
 ("What is the due date for ITR-5 for FY 2025-26?", "The due date is 31 August 2026 for firms and LLPs that do not need a tax audit, and 21 November 2026 for tax-audit cases, extended from 31 October by CBDT Circular 7/2026. Transfer-pricing cases file by 30 November 2026."),
 ("What is the income tax rate for a partnership firm or LLP?", "Firms and LLPs pay a flat 30% on taxable income, plus a 12% surcharge if income exceeds ₹1 crore, and 4% health and education cess. That is an effective rate of 31.2%, or 34.944% above ₹1 crore. There is no basic exemption limit."),
 ("How much remuneration can a firm pay its partners?", "Under Section 40(b), remuneration to working partners is deductible only if the partnership deed authorises it. On the first ₹6 lakh of book profit, or in case of a loss, the limit is the higher of ₹3 lakh or 90% of book profit. On the balance, it is 60% of book profit."),
 ("How much interest on capital can partners get?", "Interest on partners' capital is deductible up to 12% simple interest a year, if the partnership deed authorises it. Any interest above 12% is disallowed in the firm's hands."),
 ("Does a firm have to deduct TDS on partner remuneration?", "Yes. From 1 April 2025, Section 194T requires a firm or LLP to deduct TDS at 10% on salary, remuneration, commission, bonus or interest paid or credited to a partner when the total exceeds ₹20,000 in the financial year."),
 ("How are partners taxed on income from the firm?", "A partner's share of the firm's profit is exempt under Section 10(2A), because the firm has already paid tax on it. Remuneration and interest received from the firm, to the extent allowed to the firm, are taxed in the partner's hands as business income, usually in ITR-3."),
 ("When does a firm or LLP need a tax audit?", "A tax audit under Section 44AB applies when turnover exceeds ₹1 crore, or ₹10 crore if cash receipts and payments are each no more than 5%, and when professional receipts exceed ₹50 lakh. Separately, an LLP needs a statutory audit under the LLP Act if its turnover exceeds ₹40 lakh or contribution exceeds ₹25 lakh."),
 ("What annual filings does an LLP have with the MCA?", "An LLP files Form 11, its annual return, by 30 May, and Form 8, its statement of account and solvency, by 30 October each year. Each form carries an additional fee of ₹100 a day if filed late, so these are separate from the income tax return."),
 ("Is a digital signature required to file ITR-5?", "An LLP must file ITR-5 with the digital signature (DSC) of a designated partner. A firm that needs a tax audit must also use a DSC. A firm without an audit can verify the return electronically with EVC."),
 ("Does the Income-tax Act, 2025 change ITR filing for firms and LLPs for FY 2025-26?", "Returns for FY 2025-26 are filed under the Income-tax Act, 1961. The Income-tax Act, 2025 applies to income from tax year 2026-27, and renumbers the provisions on presumptive taxation, tax audit and partner payments, so plan next year's books with the new references."),
]
schema = {"@context": "https://schema.org", "@graph": [
  {"@id": "https://bharatefiling.com/#organization"},  # placeholder replaced below
]}
org = json.loads(cut('          {\n            "@type": ["Organization", "ProfessionalService"]', '          {\n            "@type": "WebSite"').rstrip().rstrip(','))
site = json.loads(cut('          {\n            "@type": "WebSite"', '          {\n            "@type": "WebPage"').rstrip().rstrip(','))
org["image"] = OG
graph = [org, site,
 {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "inLanguage": "en-IN",
  "isPartOf": {"@id": "https://bharatefiling.com/#website"}, "about": {"@id": URL + "#service"}, "breadcrumb": {"@id": URL + "#breadcrumb"},
  "datePublished": PUB, "dateModified": PUB, "author": {"@id": "https://bharatefiling.com/#organization"},
  "reviewedBy": {"@type": "Person", "name": "REPLACE_CA_NAME", "jobTitle": "Chartered Accountant", "url": "https://bharatefiling.com/team/REPLACE_CA_SLUG/"},
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-itr5 p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "Partnership Firm & LLP ITR"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Partnership Firm & LLP ITR Filing",
  "alternateName": ["ITR-5 filing", "Partnership firm income tax return", "LLP income tax return filing"],
  "serviceType": "Income tax return filing in ITR-5 for partnership firms and limited liability partnerships",
  "description": "CA-led ITR-5 filing for partnership firms and LLPs, including partner remuneration and interest under Section 40(b), Section 194T TDS, tax audit under Section 44AB, presumptive taxation for firms and LLP Form 8 and Form 11 filings.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Partnership firms and limited liability partnerships in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Partnership Firm & LLP ITR Plans", "itemListElement": [
    {"@type": "Offer", "name": "Presumptive Firm", "price": "4499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Firm or LLP ITR-5", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "LLP Complete Compliance", "price": "11999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file ITR-5 for a partnership firm or LLP", "totalTime": "P3D",
  "supply": [{"@type": "HowToSupply", "name": "Partnership deed or LLP agreement"}, {"@type": "HowToSupply", "name": "Books of account, bank statements and GST returns"},
             {"@type": "HowToSupply", "name": "Partner capital, interest and remuneration details"}, {"@type": "HowToSupply", "name": "DSC of a designated or authorised partner"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Finalise the books", "text": "Close the profit and loss account, balance sheet and partners' capital accounts, and match turnover with GST and AIS."},
   {"@type": "HowToStep", "position": 2, "name": "Work out partner payments", "text": "Allow interest on capital up to 12% and remuneration within the Section 40(b) limits, as authorised by the deed, and check Section 194T TDS."},
   {"@type": "HowToStep", "position": 3, "name": "Complete the audits", "text": "Get the tax audit under Section 44AB if it applies, and for an LLP the statutory audit under the LLP Act if turnover exceeds ₹40 lakh or contribution exceeds ₹25 lakh."},
   {"@type": "HowToStep", "position": 4, "name": "Compute tax and pay", "text": "Compute tax at 30% plus surcharge and cess, set off losses and pay any balance by challan."},
   {"@type": "HowToStep", "position": 5, "name": "File ITR-5 and ROC forms", "text": "File ITR-5 by the due date with DSC or EVC, and for an LLP file Form 8 by 30 October and Form 11 by 30 May."}]},
 {"@type": "FAQPage", "@id": URL + "#faq", "mainEntity": [
   {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
schema_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
schema_json = "\n".join("      " + l for l in schema_json.splitlines())

# ---------------- HEAD
head_top = cut("<!DOCTYPE html>", "    <!-- ===== SEARCH ENGINE VERIFICATION")
seo = f'''<!DOCTYPE html>
<html lang="en-IN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />

    <!-- ===== PRIMARY SEO ===== -->
    <title>{html.escape(TITLE, quote=False)}</title>
    <meta
      name="description"
      content="{DESC}"
    />
    <link rel="canonical" href="{URL}" />
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
    <link rel="alternate" hreflang="en-IN" href="{URL}" />
    <link rel="alternate" hreflang="x-default" href="{URL}" />
    <meta name="author" content="Bharat e-Filing Tax Desk" />
    <meta name="theme-color" content="#ffffff" />
    <meta name="format-detection" content="telephone=no" />

    <!-- ===== OPEN GRAPH / SOCIAL ===== -->
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="en_IN" />
    <meta property="og:site_name" content="Bharat e-Filing" />
    <meta property="og:title" content="Partnership Firm &amp; LLP ITR Filing (ITR-5)" />
    <meta property="og:description" content="ITR-5 filed by CAs. Partner remuneration, Section 194T TDS, tax audit and LLP Form 8 and Form 11 handled." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Partnership Firm &amp; LLP ITR" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Partnership Firm &amp; LLP ITR Filing (ITR-5)" />
    <meta name="twitter:description" content="ITR-5 for firms and LLPs, partner TDS and LLP Form 8 handled by Chartered Accountants." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "partnership-llp-itr-filing"')
assert 'service: "partnership-llp-itr-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="partnership-llp-itr-filing"')
globalnav = cut("    <!-- ================= GLOBAL NAV", "    <!-- ================= LOCAL NAV").replace(
    '<a href="https://bharatefiling.com/product-category/gst/" aria-current="page">GST</a>', '<a href="https://bharatefiling.com/product-category/gst/">GST</a>').replace(
    '<a href="https://bharatefiling.com/income-tax/">Income Tax</a>', '<a href="https://bharatefiling.com/income-tax/" aria-current="page">Income Tax</a>')
footer = cut("    <!-- ================= FOOTER", "    <!-- ================= LEAD POP-UP")

body = open(os.path.join(os.path.dirname(__file__), "main.html")).read()
faq_html = "\n".join(
    f'''            <details{" open" if i == 0 else ""}>
              <summary>{html.escape(q, quote=False)}</summary>
              <div class="faq__a"><p>{html.escape(a, quote=False)}</p></div>
            </details>''' for i, (q, a) in enumerate(FAQ))
body = body.replace("<!--FAQ-ITEMS-->", faq_html)
script = open(os.path.join(os.path.dirname(__file__), "page.js")).read()

out = (seo + boiler + "    <!-- ===== STRUCTURED DATA (one @graph) ===== -->\n    <script type=\"application/ld+json\">\n" + schema_json +
       "\n    </script>\n  </head>\n\n" + sprite + body.replace("<!--GLOBALNAV-->", globalnav.rstrip() + "\n").replace("<!--FOOTER-->", footer.rstrip() + "\n")
       .replace("<!--PAGE-SCRIPT-->", script.rstrip()))
os.makedirs(SLUG, exist_ok=True)
open(SLUG + "/index.html", "w").write(out)
print("built " + SLUG + "/index.html", len(out))
