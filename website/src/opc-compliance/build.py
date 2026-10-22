# Builds opc-compliance/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/opc-compliance/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/opc-compliance/"
TITLE = "OPC Annual Compliance Online | Bharat e-Filing"
DESC = "Annual compliance for One Person Companies: AOC-4 in 180 days, MGT-7A, audit, ITR-6, nominee changes and DIR-3 KYC filed on time by experts. No AGM needed."
OG = "https://bharatefiling.com/wp-content/uploads/og/opc-compliance-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "opc-compliance"

FAQ = [
 ("What is annual compliance for a One Person Company?", "A One Person Company must get its accounts audited, file its financial statements in AOC-4, file its annual return in MGT-7A, file its income tax return in ITR-6, and keep its director KYC, deposits and MSME returns up to date. It does not need to hold an annual general meeting."),
 ("What is the due date for AOC-4 for an OPC?", "An OPC files AOC-4 within 180 days of the end of the financial year. For FY 2025-26, that is 27 September 2026. A late AOC-4 attracts an additional fee of ₹100 a day with no upper limit."),
 ("What is the due date for MGT-7A for an OPC?", "An OPC files its annual return in MGT-7A within 60 days of the date on which its AGM would have been due, that is by 29 November 2026 for FY 2025-26. Late filing costs ₹100 a day."),
 ("Does an OPC need to hold an AGM?", "No. Under Section 96 of the Companies Act, a One Person Company is exempt from holding an annual general meeting. Resolutions that would be passed at a meeting are recorded in the minute book and signed by the member."),
 ("How many board meetings must an OPC hold?", "An OPC must hold at least one board meeting in each half of the calendar year, with at least 90 days between them. If the OPC has only one director, no board meeting is required; decisions are recorded in the minute book instead."),
 ("Is an audit compulsory for an OPC?", "Yes. Every company, including an OPC, must have its accounts audited by a chartered accountant. The first auditor is appointed by the board within 30 days of incorporation, and Form ADT-1 is filed within 15 days of an appointment."),
 ("What is the nominee in an OPC and how is it changed?", "Every OPC names a nominee who becomes the member if the sole member dies or is incapacitated. To change the nominee, the member gives notice and the company files Form INC-4 within 30 days, along with the new nominee's consent in Form INC-3."),
 ("Can an OPC convert into a private limited company?", "Yes. Since 1 April 2021, an OPC can convert into a private or public company at any time by filing Form INC-6, as there is no longer a capital or turnover limit forcing conversion. It must then have at least two members and two directors."),
 ("Who can form an OPC?", "Any natural person who is an Indian citizen, whether resident or non-resident in India, can form an OPC and act as its nominee. A resident is someone who has stayed in India for at least 120 days in the previous financial year."),
 ("Are penalties lower for OPCs?", "Yes. Under Section 446B, an OPC or small company that defaults on certain provisions pays half the normal penalty, up to ₹2 lakh for the company and ₹1 lakh for each officer in default. Late filing fees of ₹100 a day still apply in full."),
 ("What tax compliance does an OPC have?", "An OPC is taxed as a company. It files ITR-6, pays advance tax, deducts and deposits TDS, and files GST returns if registered. For FY 2025-26, ITR-6 is due by 21 November 2026 under CBDT Circular 7/2026."),
 ("Does the Income-tax Act, 2025 change OPC compliance?", "ROC compliance under the Companies Act is unchanged. For income tax, the Income-tax Act, 2025 applies from tax year 2026-27, so the OPC's tax filings for that year onwards follow the new section numbers."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-opc-compliance p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "OPC Compliance"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "OPC Annual Compliance",
  "alternateName": ["One Person Company compliance", "OPC annual filing", "AOC-4 and MGT-7A for OPC"],
  "serviceType": "Annual ROC and tax compliance for One Person Companies",
  "description": "Annual compliance for One Person Companies under the Companies Act, 2013: AOC-4 within 180 days, MGT-7A, audit and ADT-1, minutes, nominee changes in INC-3 and INC-4, DPT-3, MSME-1 and DIR-3 KYC, with ITR-6, TDS and GST coordination.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "One Person Companies and solo founders in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "OPC Compliance Plans", "itemListElement": [
    {"@type": "Offer", "name": "OPC ROC Compliance", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "OPC Annual Compliance with ITR-6", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "OPC Complete with Accounts & Tax", "price": "29999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to complete annual compliance for a One Person Company", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Books of account and bank statements"}, {"@type": "HowToSupply", "name": "Audited financial statements"},
             {"@type": "HowToSupply", "name": "Member, nominee and director details"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Close the books and audit", "text": "Finalise the accounts and get them audited by the appointed chartered accountant."},
   {"@type": "HowToStep", "position": 2, "name": "Approve the accounts", "text": "Approve the financial statements at a board meeting, or by recording the decision in the minute book if there is only one director."},
   {"@type": "HowToStep", "position": 3, "name": "File AOC-4", "text": "File the financial statements in AOC-4 within 180 days of the year end, signed by the director."},
   {"@type": "HowToStep", "position": 4, "name": "File ITR-6 and MGT-7A", "text": "File the income tax return in ITR-6 by the due date and the annual return in MGT-7A by 29 November."},
   {"@type": "HowToStep", "position": 5, "name": "Keep event filings current", "text": "File DPT-3, MSME-1 and DIR-3 KYC when due, and INC-4 within 30 days of any nominee change."}]},
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
    <meta property="og:title" content="OPC Annual Compliance Online" />
    <meta property="og:description" content="AOC-4, MGT-7A, audit, ITR-6 and nominee changes for your One Person Company, filed on time by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – OPC Compliance" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="OPC Annual Compliance Online" />
    <meta name="twitter:description" content="OPC MGT-7A due 29 November. Avoid ₹100 a day: let experts file it." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "opc-compliance"')
assert 'service: "opc-compliance"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="opc-compliance"')
globalnav = cut("    <!-- ================= GLOBAL NAV", "    <!-- ================= LOCAL NAV").replace(
    '<a href="https://bharatefiling.com/product-category/gst/" aria-current="page">GST</a>', '<a href="https://bharatefiling.com/product-category/gst/">GST</a>').replace(
    '<a href="https://bharatefiling.com/compliance/">Compliance</a>', '<a href="https://bharatefiling.com/compliance/" aria-current="page">Compliance</a>')
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
