# Builds icegate-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/icegate-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/icegate-registration/"
TITLE = "ICEGATE Registration Online | Bharat e-Filing"
DESC = "Register on ICEGATE, the customs portal, with IEC and DSC checks, plus bank account and AD code registration so your IGST export refunds aren't held up."
OG = "https://bharatefiling.com/wp-content/uploads/og/icegate-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "icegate-registration"

FAQ = [
 ("What is ICEGATE?", "ICEGATE, the Indian Customs Electronic Gateway, is the online portal of the Central Board of Indirect Taxes and Customs (CBIC). Importers, exporters, customs brokers and carriers use it to file and track customs documents, pay duty online, upload supporting documents through e-Sanchit, and track IGST refunds and drawback."),
 ("Who needs ICEGATE registration?", "Importers and exporters who want to file or track their own customs documents, pay duty online or manage export refunds, as well as customs brokers, shipping lines, airlines and other trade users. Exporters claiming IGST refunds also need their bank account registered with Customs."),
 ("What do I need for ICEGATE registration?", "An active Import Export Code (IEC), PAN, an email address and mobile number that match the records with DGFT and GSTN, GSTIN where registered, and a Class 3 digital signature certificate of the authorised signatory for DSC-based registration."),
 ("Is a digital signature needed for ICEGATE?", "Full, DSC-based registration is signed with a Class 3 digital signature certificate of the authorised signatory. ICEGATE has also offered a simplified registration for some services; we check which type your work needs before applying."),
 ("How long does ICEGATE registration take?", "The application itself can be completed in a day once the IEC, DSC and contact details are in order. Approval by ICEGATE usually follows within a few working days."),
 ("How do exporters get IGST refunds?", "For goods exported on payment of IGST, the shipping bill is treated as the refund application under Rule 96 of the CGST Rules, 2017. The export invoice must be reported correctly in GSTR-1, GSTR-3B must be filed, the carrier must file the export manifest, and the bank account must be registered with Customs and validated by PFMS."),
 ("Why does PFMS bank validation matter?", "IGST refunds are paid through the Public Financial Management System (PFMS). If the exporter's bank account registered with Customs is not validated by PFMS, or has been closed, a sanctioned refund may not be credited."),
 ("What is AD code registration?", "Exporters register the authorised dealer (AD) code of their bank with Customs at the ports they export from. It links export proceeds and refunds to the right bank account."),
 ("What is e-Sanchit?", "e-Sanchit is the ICEGATE facility to upload supporting documents, such as invoices, packing lists and licences, electronically with the bill of entry or shipping bill, instead of submitting paper copies."),
 ("Does the IEC need to be updated every year?", "Yes. IEC holders must update or confirm their IEC details online with DGFT every year between April and June, even if nothing has changed. An IEC that isn't updated can be deactivated."),
 ("Do I need a LUT to export without paying IGST?", "Exporters who want to export goods or services without paying IGST furnish a Letter of Undertaking (LUT) on the GST portal for each financial year, before making such exports."),
 ("How does income tax apply to an exporter?", "Export income is taxed like other business income. From tax year 2026-27, returns are filed under the Income-tax Act, 2025; returns for financial year 2025-26 and earlier are filed under the Income-tax Act, 1961."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-icegate p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "ICEGATE Registration"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "ICEGATE Registration",
  "alternateName": ["ICEGATE login registration", "Customs ICEGATE registration", "ICEGATE DSC registration", "ICEGATE bank account registration"],
  "serviceType": "Registration on the Indian Customs Electronic Gateway",
  "description": "Registration of importers and exporters on ICEGATE, the CBIC customs portal, with Class 3 DSC, IEC and contact-detail checks, and help with bank account and AD code registration for IGST refunds and drawback.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Importers and exporters in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "ICEGATE Plans", "itemListElement": [
    {"@type": "Offer", "name": "ICEGATE Registration", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "ICEGATE with DSC", "price": "3499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Exporter Pack", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register on ICEGATE", "totalTime": "P5D",
  "supply": [{"@type": "HowToSupply", "name": "Import Export Code (IEC)"}, {"@type": "HowToSupply", "name": "Class 3 digital signature certificate"},
             {"@type": "HowToSupply", "name": "PAN and GSTIN"}, {"@type": "HowToSupply", "name": "Email and mobile matching DGFT records"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check prerequisites", "text": "Confirm the IEC is active and updated, and that the email and mobile match DGFT and GSTN records."},
   {"@type": "HowToStep", "position": 2, "name": "Arrange the DSC", "text": "Get a Class 3 digital signature certificate for the authorised signatory if you don't have one."},
   {"@type": "HowToStep", "position": 3, "name": "Apply on ICEGATE", "text": "Choose the user type, enter the IEC and organisation details, and verify by OTP."},
   {"@type": "HowToStep", "position": 4, "name": "Sign and submit", "text": "Sign the application with the DSC and submit it for approval."},
   {"@type": "HowToStep", "position": 5, "name": "Register bank and AD code", "text": "After approval, register the bank account and AD code so refunds can be credited."}]},
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
    <meta property="og:title" content="ICEGATE Registration Online" />
    <meta property="og:description" content="Register on the customs portal with IEC and DSC checks, plus bank and AD code registration for refunds." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – ICEGATE Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="ICEGATE Registration Online" />
    <meta name="twitter:description" content="Importing or exporting? Get on ICEGATE without the back-and-forth." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "icegate-registration"')
assert 'service: "icegate-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="icegate-registration"')
globalnav = cut("    <!-- ================= GLOBAL NAV", "    <!-- ================= LOCAL NAV").replace(
    '<a href="https://bharatefiling.com/product-category/gst/" aria-current="page">GST</a>', '<a href="https://bharatefiling.com/product-category/gst/">GST</a>').replace(
    '<a href="https://bharatefiling.com/business-registration/">Start a Business</a>', '<a href="https://bharatefiling.com/business-registration/" aria-current="page">Start a Business</a>')
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
