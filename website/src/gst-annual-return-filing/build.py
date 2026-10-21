# Builds gst-annual-return-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/gst-annual-return-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/gst-annual-return-filing/"
TITLE = "GSTR-9 Annual Return Filing Online | Bharat e-Filing"
DESC = "File GSTR-9 and GSTR-9C for FY 2025-26 before 31 December 2026. Full-year reconciliation, missed ITC check, late fee help and CA-reviewed annual return filing."
OG = "https://bharatefiling.com/wp-content/uploads/og/gst-annual-return-filing-1200x630.jpg"
PUB = "2026-10-21"
SLUG = "gst-annual-return-filing"

FAQ = [
 ("What is GSTR-9?", "GSTR-9 is the annual return under Section 44 of the CGST Act and Rule 80 of the CGST Rules. It consolidates a regular taxpayer’s outward supplies, inward supplies, input tax credit, tax paid, HSN summary and amendments for a financial year, as reported in GSTR-1 and GSTR-3B, with corrections."),
 ("What is the due date for GSTR-9 for FY 2025-26?", "The due date is 31 December 2026, that is 31 December following the end of the financial year, unless the government extends it by notification."),
 ("Is GSTR-9 mandatory for turnover below ₹2 crore?", "No. Registered persons with aggregate turnover up to ₹2 crore in the financial year are exempt from filing GSTR-9 for FY 2024-25 onwards (Notification 15/2025-Central Tax), though they may still file it voluntarily. Above ₹2 crore it is mandatory."),
 ("Who must file GSTR-9C?", "GSTR-9C, a self-certified reconciliation statement between your audited financial statements and GSTR-9, must be filed by taxpayers whose aggregate turnover exceeds ₹5 crore in the financial year. CBIC Circular 246/03/2025-GST clarifies that the annual return is complete only when GSTR-9C is also filed where it is required."),
 ("Who does not need to file GSTR-9?", "Composition taxpayers (who file GSTR-4 instead), casual taxable persons, non-resident taxable persons, Input Service Distributors, persons deducting TDS or collecting TCS under GST and suppliers of online information and database access services from outside India do not file GSTR-9."),
 ("What is the late fee for GSTR-9?", "Under Notification 7/2023-Central Tax, the late fee is ₹50 a day (₹25 CGST + ₹25 SGST) for aggregate turnover up to ₹5 crore and ₹100 a day for ₹5 crore to ₹20 crore, both capped at 0.04% of turnover in the state. Above ₹20 crore it is ₹200 a day, capped at 0.5% of turnover in the state, under Section 47(2)."),
 ("Can GSTR-9 be revised after filing?", "No. GSTR-9 cannot be revised once filed, so it should be reconciled carefully before submission. Any additional tax found while preparing it can be paid through Form DRC-03 with interest."),
 ("Until when can I claim missed ITC for FY 2025-26?", "Under Section 16(4), input tax credit for FY 2025-26 can be claimed in a return up to 30 November 2026 or the date of filing the annual return, whichever is earlier. ITC not claimed in GSTR-3B by then cannot be added through GSTR-9."),
 ("Is there a time limit to file old GSTR-9 returns?", "Yes. Under Section 44(2), an annual return cannot be filed after 3 years from its due date. For example, GSTR-9 for FY 2022-23, due on 31 December 2023, cannot be filed after 31 December 2026."),
 ("What documents are needed to file GSTR-9?", "You need GSTR-1, GSTR-1A, GSTR-3B and GSTR-2B for all months of the year, sales and purchase registers, books of accounts, the HSN-wise summary of supplies, details of ITC reversals and reclaims, and any DRC-03 payments. For GSTR-9C you also need the audited financial statements."),
 ("How does the 22 September 2025 rate change affect GSTR-9 for FY 2025-26?", "GST 2.0 rates applied from 22 September 2025, which falls inside FY 2025-26. Your GSTR-9 should reconcile taxable values and tax at the old rates up to 21 September 2025 and at the new rates from 22 September 2025, including the HSN summary."),
 ("Does the Income-tax Act, 2025 change anything for GSTR-9?", "GSTR-9 is unchanged. From 1 April 2026 the Income-tax Act, 2025 replaces the 1961 Act, ‘previous year’ becomes ‘tax year’ and tax audit under section 44AB moves to section 63. Turnover in GSTR-9 and GSTR-9C is compared with your income-tax return and tax audit report, so the two should reconcile."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-gstr-9 p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "GST Services", "item": "https://bharatefiling.com/product-category/gst/"},
   {"@type": "ListItem", "position": 3, "name": "GST Annual Return Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "GST Annual Return Filing",
  "alternateName": ["GSTR-9 filing", "GSTR-9C reconciliation statement", "GST annual return"],
  "serviceType": "Preparation and filing of the GST annual return (GSTR-9) and reconciliation statement (GSTR-9C)",
  "description": "CA-reviewed preparation and filing of GSTR-9 under Section 44 of the CGST Act and GSTR-9C for turnover above ₹5 crore, with full-year reconciliation of GSTR-1, GSTR-3B, GSTR-2B and books.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Regular GST taxpayers, proprietors, partnerships, LLPs and companies"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "GST Annual Return Plans", "itemListElement": [
    {"@type": "Offer", "name": "GSTR-9", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "GSTR-9 + 9C", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Clean-up", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file GSTR-9 online", "totalTime": "P3D",
  "supply": [{"@type": "HowToSupply", "name": "GSTR-1, GSTR-3B and GSTR-2B for all 12 months"}, {"@type": "HowToSupply", "name": "Sales and purchase registers and books of accounts"},
             {"@type": "HowToSupply", "name": "HSN-wise summary and ITC reversal details"}, {"@type": "HowToSupply", "name": "GST portal login and DSC or EVC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Open the annual return", "text": "Log in to the GST portal and go to Services, Returns, Annual Return, then select the financial year and GSTR-9."},
   {"@type": "HowToStep", "position": 2, "name": "Download the system-computed summary", "text": "Download the GSTR-9 system-computed PDF and the GSTR-1 and GSTR-3B summaries to compare with your books."},
   {"@type": "HowToStep", "position": 3, "name": "Reconcile and fill the tables", "text": "Reconcile outward supplies, ITC (including Table 8A from GSTR-2B), tax paid, amendments and HSN details, and edit the auto-filled tables where needed."},
   {"@type": "HowToStep", "position": 4, "name": "Pay any additional liability", "text": "Pay any extra tax found during reconciliation through DRC-03 with interest, and compute any late fee."},
   {"@type": "HowToStep", "position": 5, "name": "Preview, sign and file", "text": "Preview the draft GSTR-9, file it with DSC or EVC and, if turnover exceeds ₹5 crore, file the self-certified GSTR-9C."}]},
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
    <title>{TITLE}</title>
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
    <meta property="og:title" content="GSTR-9 Annual Return Filing – File Before 31 December 2026" />
    <meta property="og:description" content="GSTR-9 and GSTR-9C for FY 2025-26 with full-year reconciliation, missed-ITC check and CA review." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – GSTR-9 Annual Return Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="GSTR-9 Annual Return Filing Online" />
    <meta name="twitter:description" content="File GSTR-9 and GSTR-9C before 31 December 2026, reconciled and checked by a CA." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "gst-annual-return-filing"')
assert 'service: "gst-annual-return-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="gst-annual-return-filing"')
globalnav = cut("    <!-- ================= GLOBAL NAV", "    <!-- ================= LOCAL NAV")
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
