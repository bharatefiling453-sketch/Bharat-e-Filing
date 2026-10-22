# Builds company-itr-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/company-itr-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/company-itr-filing/"
TITLE = "Company ITR Filing (ITR-6) Online | Bharat e-Filing"
DESC = "File ITR-6 for your private limited company. Section 115BAA vs normal tax, MAT, losses, Form 10-IC and ROC filings AOC-4 and MGT-7 handled by CAs."
OG = "https://bharatefiling.com/wp-content/uploads/og/company-itr-filing-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "company-itr-filing"

FAQ = [
 ("Which ITR form does a company file?", "Every company files ITR-6, except a company claiming exemption under Section 11 for income from property held for charitable or religious purposes, which files ITR-7. ITR-6 must be filed with the digital signature (DSC) of a director or authorised signatory."),
 ("Is it mandatory for a company to file an income tax return?", "Yes. Every company must file its return every year under Section 139(1), whatever its income, even if it made a loss or had no business during the year."),
 ("What is the due date for company ITR filing for FY 2025-26?", "Companies are audited under the Companies Act, so they file by the audit-case due date. For FY 2025-26 it is 21 November 2026, extended from 31 October by CBDT Circular 7/2026. Companies with international or specified domestic transactions that need a transfer pricing report file by 30 November 2026."),
 ("What is the income tax rate for a company?", "A domestic company can opt for Section 115BAA and pay 22% plus a 10% surcharge and 4% cess, about 25.17%, without most exemptions and without MAT. Otherwise it pays 25% if its turnover in FY 2023-24 did not exceed ₹400 crore, or 30%, plus a surcharge of 7% above ₹1 crore and 12% above ₹10 crore, and 4% cess."),
 ("Should my company opt for Section 115BAA?", "It usually saves tax when the company has few deductions or incentives to claim. Companies claiming large deductions, such as Section 80-IAC for startups, or holding unused MAT credit may pay less under the normal regime. Once chosen, the 115BAA option cannot be withdrawn, so compare both before deciding."),
 ("How do I opt for Section 115BAA?", "File Form 10-IC on the income tax portal on or before the due date for filing the return for the first year you choose the option, then file ITR-6 under the new rate. A late Form 10-IC can lead to the option being denied."),
 ("What is MAT and when does it apply?", "Minimum Alternate Tax under Section 115JB applies to companies under the normal regime when tax on book profit at 15%, plus surcharge and cess, is higher than tax on normal income. MAT paid can be carried forward as a credit for 15 years. Companies under Section 115BAA do not pay MAT."),
 ("Can a company carry forward its losses?", "Yes. Business losses can be carried forward for eight years if the return is filed by the due date. For a closely held company, losses lapse if more than 49% of the shareholding changes, except for eligible startups where all original shareholders continue."),
 ("What is the tax holiday for startups?", "An eligible startup recognised by DPIIT and incorporated before 1 April 2030 can claim a 100% deduction of profits under Section 80-IAC for any three consecutive years out of its first ten, after obtaining the Inter-Ministerial Board certificate."),
 ("What ROC filings does a company have every year?", "After the annual general meeting, which must be held by 30 September, a company files financial statements in AOC-4 within 30 days, its annual return in MGT-7 or MGT-7A within 60 days, and the auditor appointment in ADT-1 within 15 days where applicable. Late AOC-4 and MGT-7 filings attract an additional fee of ₹100 a day each."),
 ("What happens if a company files its ITR late?", "A late fee of up to ₹5,000 under Section 234F, interest under Section 234A on unpaid tax, the loss of the right to carry forward losses, and in serious cases prosecution under Section 276CC. A belated return can be filed until 31 December 2026."),
 ("Does the Income-tax Act, 2025 change company ITR filing for FY 2025-26?", "Returns for FY 2025-26 are filed under the Income-tax Act, 1961. The Income-tax Act, 2025 applies to income from tax year 2026-27 and renumbers provisions such as the concessional company tax regime and MAT, so plan next year's computation with the new references."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-company-itr p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "Company ITR Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Company ITR Filing",
  "alternateName": ["ITR-6 filing", "Private limited company income tax return", "Corporate tax return filing"],
  "serviceType": "Income tax return filing in ITR-6 for private limited and other companies",
  "description": "CA-led ITR-6 filing for companies, including Section 115BAA versus normal regime comparison, MAT under Section 115JB, Form 10-IC, loss carry-forward, startup deductions under Section 80-IAC and annual ROC filings AOC-4 and MGT-7.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Private limited companies, one person companies and startups in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Company ITR Filing Plans", "itemListElement": [
    {"@type": "Offer", "name": "Small or Dormant Company", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Company ITR-6", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Company Annual Compliance", "price": "19999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file ITR-6 for a company", "totalTime": "P3D",
  "supply": [{"@type": "HowToSupply", "name": "Audited financial statements and auditor's report"}, {"@type": "HowToSupply", "name": "Tax audit report (Form 3CA-3CD) if applicable"},
             {"@type": "HowToSupply", "name": "AIS, Form 26AS and TDS details"}, {"@type": "HowToSupply", "name": "DSC of a director or authorised signatory"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Finalise audited accounts", "text": "Complete the statutory audit under the Companies Act and the tax audit under Section 44AB where it applies."},
   {"@type": "HowToStep", "position": 2, "name": "Choose the tax regime", "text": "Compare tax under Section 115BAA with the normal regime and MAT, and file Form 10-IC by the due date if opting for 115BAA."},
   {"@type": "HowToStep", "position": 3, "name": "Compute total income", "text": "Adjust book profit for disallowances, depreciation under the Income-tax Act, deductions and brought-forward losses."},
   {"@type": "HowToStep", "position": 4, "name": "Pay the balance tax", "text": "Pay any tax and interest remaining after advance tax and TDS by challan."},
   {"@type": "HowToStep", "position": 5, "name": "File ITR-6 with DSC", "text": "File ITR-6 on incometax.gov.in by the due date with the digital signature of a director, then file AOC-4 and MGT-7 with the ROC after the AGM."}]},
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
    <meta property="og:title" content="Company ITR Filing (ITR-6) Online" />
    <meta property="og:description" content="ITR-6 filed by CAs. Section 115BAA vs normal tax, MAT, losses and ROC filings handled." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Company ITR Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Company ITR Filing (ITR-6) Online" />
    <meta name="twitter:description" content="ITR-6 due 21 November 2026. 115BAA, MAT and AOC-4/MGT-7 handled by Chartered Accountants." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "company-itr-filing"')
assert 'service: "company-itr-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="company-itr-filing"')
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
