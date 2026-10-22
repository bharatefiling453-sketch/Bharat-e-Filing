# Builds tds-return-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/tds-return-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/tds-return-filing/"
TITLE = "TDS Return Filing Online – 24Q, 26Q, 27Q | Bharat e-Filing"
DESC = "File quarterly TDS returns 24Q, 26Q, 27Q and TCS 27EQ on time. Form 16 and 16A, TRACES defaults, corrections and late fee checks handled by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/tds-return-filing-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "tds-return-filing"

FAQ = [
 ("What is a TDS return?", "A TDS return is a quarterly statement that a deductor files with the Income Tax Department, showing the tax deducted at source from each payee, the challans used to deposit it and the payees' PANs. It lets payees get credit for the tax in their Form 26AS and AIS."),
 ("Which TDS return form should I file?", "Form 24Q is for TDS on salary, Form 26Q for TDS on other payments to residents, Form 27Q for payments to non-residents, and Form 27EQ for tax collected at source (TCS). A deductor files every form that applies, each quarter."),
 ("What are the due dates for TDS returns?", "TDS returns in Forms 24Q, 26Q and 27Q are due by 31 July for April to June, 31 October for July to September, 31 January for October to December and 31 May for January to March. TCS returns in Form 27EQ are due by 15 July, 15 October, 15 January and 15 May."),
 ("What is the late fee for filing a TDS return late?", "Under Section 234E, a late fee of ₹200 a day applies until the return is filed, capped at the total TDS or TCS amount for the quarter. The fee must be paid before the return is accepted."),
 ("What is the penalty for not filing a TDS return?", "Under Section 271H, a penalty of ₹10,000 to ₹1 lakh can apply for not filing or filing an incorrect TDS return. No penalty applies if the TDS, interest and late fee are paid and the return is filed within one year of the due date."),
 ("When must Form 16 and Form 16A be issued?", "Form 16 for salary is issued once a year by 15 June after the financial year ends. Form 16A for other payments is issued every quarter, within 15 days of the return due date. Both are downloaded from TRACES after the return is processed."),
 ("What happens if I deposit TDS late?", "Interest is charged at 1% a month or part of a month if tax was not deducted, and 1.5% a month or part of a month from the date of deduction to the date of deposit if it was deducted but deposited late. TDS must be deposited by the 7th of the next month, and by 30 April for March."),
 ("What is a TRACES default and how do I fix it?", "After processing, TRACES reports defaults such as short payment, short deduction, late payment interest, late filing fee or invalid PAN. They are cleared by paying the amount due and filing a correction return using the consolidated file downloaded from TRACES."),
 ("Can I revise a TDS return?", "Yes. A correction return can be filed any number of times to fix PAN errors, challan mismatches or missing deductee details. It is prepared on the consolidated file from TRACES, using the original return's token number."),
 ("What if the payee does not give a PAN?", "Under Section 206AA, TDS must be deducted at the higher of twice the normal rate or 20% when the payee does not furnish a valid PAN. Collect PAN before the first payment to avoid this."),
 ("What changed in TDS from April 2025?", "Many TDS thresholds were raised, such as professional fees to ₹50,000, commission to ₹20,000 and rent to ₹50,000 a month, and the higher TDS rate for non-filers under Section 206AB was removed. TDS on payments to partners under Section 194T also began."),
 ("Does the Income-tax Act, 2025 change TDS returns?", "Yes. From 1 April 2026 the Income-tax Act, 2025 governs TDS and TCS for tax year 2026-27, with the TDS provisions consolidated under new section numbers. Quarterly statements continue, but check the current forms on the e-filing portal and TRACES before filing."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-tds-return p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "TDS Return Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "TDS Return Filing",
  "alternateName": ["TDS return filing online", "Form 24Q, 26Q, 27Q and 27EQ filing", "Quarterly TDS statement filing"],
  "serviceType": "Quarterly TDS and TCS return filing in Forms 24Q, 26Q, 27Q and 27EQ",
  "description": "Quarterly TDS and TCS return filing for businesses and employers, including challan reconciliation, PAN validation, Form 16 and 16A issue, TRACES default resolution, correction returns and Section 234E late fee checks.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Businesses, employers and organisations that deduct or collect tax at source in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "TDS Return Filing Plans", "itemListElement": [
    {"@type": "Offer", "name": "Single TDS Return", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Quarterly TDS Plan", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Annual TDS Compliance", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file a TDS return", "totalTime": "P2D",
  "supply": [{"@type": "HowToSupply", "name": "TAN and TRACES login"}, {"@type": "HowToSupply", "name": "Challan details (CIN) for TDS deposited"},
             {"@type": "HowToSupply", "name": "Deductee names, PANs, amounts paid and TDS deducted"}, {"@type": "HowToSupply", "name": "DSC or EVC of the responsible person"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Collect deductee data", "text": "List every payment in the quarter with the payee's PAN, section, amount paid and TDS deducted."},
   {"@type": "HowToStep", "position": 2, "name": "Match challans", "text": "Match each deduction to the challan used to deposit it, and pay any shortfall with interest."},
   {"@type": "HowToStep", "position": 3, "name": "Prepare and validate", "text": "Prepare the return in the Return Preparation Utility and validate it with the File Validation Utility, checking PANs against the database."},
   {"@type": "HowToStep", "position": 4, "name": "File the return", "text": "Upload the validated file on the e-filing portal with DSC or EVC by the quarterly due date."},
   {"@type": "HowToStep", "position": 5, "name": "Issue certificates and clear defaults", "text": "Download and issue Form 16 or 16A from TRACES, and clear any defaults with a correction return."}]},
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
    <meta property="og:title" content="TDS Return Filing Online – 24Q, 26Q, 27Q, 27EQ" />
    <meta property="og:description" content="Quarterly TDS and TCS returns filed on time, with Form 16/16A and TRACES defaults handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – TDS Return Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="TDS Return Filing Online – 24Q, 26Q, 27Q, 27EQ" />
    <meta name="twitter:description" content="Q2 TDS return due 31 October. Avoid ₹200 a day: let experts file it." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "tds-return-filing"')
assert 'service: "tds-return-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="tds-return-filing"')
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
