# Builds tan-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/tan-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/tan-registration/"
TITLE = "TAN Registration Online – Apply for TAN | Bharat e-Filing"
DESC = "Apply for TAN online in Form 49B. Find out if you need one, get it allotted fast, and keep TDS deposits and quarterly TDS returns on time with CA help."
OG = "https://bharatefiling.com/wp-content/uploads/og/tan-registration-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "tan-registration"

FAQ = [
 ("What is TAN?", "TAN, the Tax Deduction and Collection Account Number, is a 10-character alphanumeric number issued by the Income Tax Department to every person who deducts or collects tax at source. It must be quoted on TDS and TCS payments, quarterly statements and the certificates given to payees."),
 ("Who needs to apply for TAN?", "Every person responsible for deducting or collecting tax at source must obtain a TAN under Section 203A. This includes companies, firms, LLPs, trusts, government offices, and individuals or HUFs whose accounts are audited, whenever they pay salary, contractor or professional fees, rent, interest, commission or other payments covered by TDS or TCS."),
 ("Do individuals need TAN to deduct TDS on property or rent?", "No. Individuals and HUFs not required to get a tax audit can deduct TDS on buying property (Section 194-IA), rent above ₹50,000 a month (Section 194-IB) and payments to contractors or professionals (Section 194M) using their PAN, through challan-cum-statements in Form 26QB, 26QC or 26QD. They do not need a TAN for these."),
 ("How do I apply for TAN online?", "Apply in Form 49B online through the Protean (NSDL) TIN portal. Fill in the deductor category, name, address and contact details, submit, and sign the acknowledgement with Aadhaar e-sign or DSC, or send the signed acknowledgement as instructed. The TAN is then allotted and communicated by email and post."),
 ("What documents are needed for TAN registration?", "No documents need to be uploaded with an online Form 49B. You need the correct legal name, address of the office that will deduct tax, PAN of the entity where applicable, the deductor category, and the details of the person responsible for deducting tax."),
 ("How long does it take to get a TAN?", "TAN is usually allotted within about a week to ten working days after the signed application is received. You can track the status on the Protean portal using the 14-digit acknowledgement number."),
 ("What is the penalty for not obtaining a TAN?", "Failing to apply for a TAN or to quote it where required can attract a penalty of ₹10,000 under Section 272BB. TDS challans and returns without a valid TAN are also not accepted by the banks and the TDS system."),
 ("Is TAN valid for life?", "Yes. TAN is a lifetime number and does not need renewal. If your name, address or other details change, apply using the form for changes or correction in TAN data. Do not apply for a new TAN for the same deductor, as holding more than one is not allowed."),
 ("Can a company have different TANs for its branches?", "Yes. Branches or divisions of a company or other entity can obtain separate TANs if each branch deducts tax and files its own TDS statements. Each branch then deposits TDS and files returns under its own TAN."),
 ("What do I do after getting a TAN?", "Register the TAN on the income tax e-filing portal and TRACES, deposit TDS by the 7th of the next month (30 April for March), file quarterly TDS statements by 31 July, 31 October, 31 January and 31 May, and issue TDS certificates such as Form 16 and Form 16A to payees."),
 ("What are the penalties for late TDS deposit or returns?", "Interest is charged at 1% a month for not deducting TDS and 1.5% a month for deducting but depositing late. A late TDS statement attracts a fee of ₹200 a day under Section 234E, capped at the TDS amount, and a penalty of ₹10,000 to ₹1 lakh can apply under Section 271H."),
 ("Does the Income-tax Act, 2025 change TAN?", "No. Your existing TAN continues. From 1 April 2026 the Income-tax Act, 2025 governs TDS and TCS for tax year 2026-27, with new section numbers, so check the current challan and statement formats on the e-filing portal and TRACES."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-tan p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "TAN Registration"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "TAN Registration",
  "alternateName": ["Apply for TAN", "Form 49B", "Tax Deduction and Collection Account Number"],
  "serviceType": "Application for Tax Deduction and Collection Account Number (TAN) in Form 49B",
  "description": "Online TAN application in Form 49B for companies, firms, LLPs, trusts, government offices and audited individuals, with e-filing and TRACES registration, monthly TDS deposit reminders and quarterly TDS statements.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Businesses, employers and organisations that deduct or collect tax at source in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "TAN Registration Plans", "itemListElement": [
    {"@type": "Offer", "name": "TAN Application", "price": "999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "TAN + First TDS Return", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "TDS Compliance for a Year", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to apply for TAN online", "totalTime": "P10D",
  "supply": [{"@type": "HowToSupply", "name": "Legal name and address of the deducting office"}, {"@type": "HowToSupply", "name": "PAN of the entity, where applicable"},
             {"@type": "HowToSupply", "name": "Details of the person responsible for deducting tax"}, {"@type": "HowToSupply", "name": "Aadhaar e-sign or DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check if you need TAN", "text": "Confirm you deduct or collect tax at source. Individuals and HUFs without a tax audit deducting on property, rent or contractor payments can use PAN-based challans instead."},
   {"@type": "HowToStep", "position": 2, "name": "Search for an existing TAN", "text": "Use Know Your TAN on the e-filing portal so you do not apply twice for the same deductor."},
   {"@type": "HowToStep", "position": 3, "name": "Fill Form 49B", "text": "Fill Form 49B online on the Protean TIN portal with the deductor category, name, address and responsible person."},
   {"@type": "HowToStep", "position": 4, "name": "Sign and submit", "text": "Sign the acknowledgement with Aadhaar e-sign or DSC and note the 14-digit acknowledgement number."},
   {"@type": "HowToStep", "position": 5, "name": "Receive and register TAN", "text": "Receive the TAN by email, then register it on the e-filing portal and TRACES before your first TDS deposit and return."}]},
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
    <meta property="og:title" content="TAN Registration Online – Apply for TAN" />
    <meta property="og:description" content="Form 49B filed for you, TAN registered on TRACES, and TDS deposits and returns kept on time by CAs." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – TAN Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="TAN Registration Online – Apply for TAN" />
    <meta name="twitter:description" content="Need to deduct TDS? Get your TAN in Form 49B and stay on top of TDS returns." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "tan-registration"')
assert 'service: "tan-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="tan-registration"')
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
