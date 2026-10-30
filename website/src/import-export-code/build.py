# Builds import-export-code/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/import-export-code/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/import-export-code/"
TITLE = "Import Export Code (IEC) Registration | Bharat e-Filing"
DESC = "Get your Import Export Code from DGFT online, with PAN, address and bank details checked, plus annual IEC updates so your code never gets deactivated."
OG = "https://bharatefiling.com/wp-content/uploads/og/import-export-code-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "import-export-code"

FAQ = [
 ("What is an Import Export Code (IEC)?", "An IEC is a 10-character code issued by the Directorate General of Foreign Trade (DGFT). Under Section 7 of the Foreign Trade (Development and Regulation) Act, 1992, no person can import or export except under an IEC, unless specifically exempted."),
 ("Who needs an IEC?", "Any business or individual importing or exporting goods for trade, including proprietors, partnerships, LLPs and companies. Exporters of services generally need an IEC to claim benefits under the Foreign Trade Policy."),
 ("Is the IEC linked to PAN?", "Yes. The IEC is based on the applicant's PAN, and one PAN can hold only one IEC. The business name and details in the application should match the PAN records."),
 ("What documents are needed for an IEC?", "PAN of the business or individual, proof of the business address, and bank proof such as a cancelled cheque with the applicant's name pre-printed or a bank certificate. Companies, LLPs and firms also provide details of their directors or partners."),
 ("How is the IEC application signed?", "The online application on the DGFT portal is signed with a digital signature certificate or with Aadhaar-based e-sign. For Aadhaar e-sign, the Aadhaar should be linked to the applicant's PAN and mobile number."),
 ("How long does it take to get an IEC?", "Once the application is complete and signed, the IEC is usually generated online quickly, often the same day. We submit your application within 24 hours of receiving complete details."),
 ("Does an IEC expire?", "An IEC has no expiry date, but it must be updated or confirmed on the DGFT portal every year between 1 April and 30 June, even if nothing has changed."),
 ("What happens if I miss the annual IEC update?", "An IEC that is not updated in the April to June window is deactivated. It can be reactivated by completing the update on the DGFT portal, but shipments and benefits linked to it can be held up until then."),
 ("Can I change details in my IEC?", "Yes. Changes such as address, bank account, partners or directors are made online through an IEC modification on the DGFT portal."),
 ("Is an IEC needed for imports for personal use?", "Goods imported or exported for personal use that are not connected with trade, manufacture or agriculture are exempt from the IEC requirement. Some government bodies and notified cases are also exempt."),
 ("What do I need after getting the IEC?", "Exporters usually register on ICEGATE, register their bank account and AD code with Customs, and furnish a GST Letter of Undertaking if they want to export without paying IGST."),
 ("How is income from exports taxed?", "Export income is taxed as business income. From tax year 2026-27, income tax returns are filed under the Income-tax Act, 2025; returns for financial year 2025-26 and earlier are filed under the Income-tax Act, 1961."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-iec p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Import Export Code"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Import Export Code (IEC) Registration",
  "alternateName": ["IEC registration", "IEC code online", "DGFT import export code", "IEC annual update"],
  "serviceType": "Application for an Import Export Code with DGFT",
  "description": "Import Export Code registration with the Directorate General of Foreign Trade, plus annual IEC updates and modifications, with PAN, address and bank details checked and the application signed by DSC or Aadhaar e-sign.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Importers and exporters in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "IEC Plans", "itemListElement": [
    {"@type": "Offer", "name": "IEC Update or Modification", "price": "999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "IEC Registration", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Exporter Starter Pack", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to apply for an IEC", "totalTime": "P1D",
  "supply": [{"@type": "HowToSupply", "name": "PAN"}, {"@type": "HowToSupply", "name": "Business address proof"},
             {"@type": "HowToSupply", "name": "Cancelled cheque or bank certificate"}, {"@type": "HowToSupply", "name": "DSC or Aadhaar e-sign"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Register on DGFT", "text": "Create a user account on the DGFT portal with the applicant's email and mobile number."},
   {"@type": "HowToStep", "position": 2, "name": "Fill the IEC application", "text": "Enter PAN, entity, address, bank and director or partner details."},
   {"@type": "HowToStep", "position": 3, "name": "Upload documents", "text": "Upload address proof and the cancelled cheque or bank certificate."},
   {"@type": "HowToStep", "position": 4, "name": "Sign and submit", "text": "Sign the application with a DSC or Aadhaar e-sign and submit it."},
   {"@type": "HowToStep", "position": 5, "name": "Download the IEC", "text": "Download the IEC certificate once it is generated, and diarise the annual update."}]},
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
    <meta property="og:title" content="Import Export Code (IEC) Registration" />
    <meta property="og:description" content="Get your IEC from DGFT online, plus annual updates so it never gets deactivated." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Import Export Code" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Import Export Code (IEC) Registration" />
    <meta name="twitter:description" content="Starting to import or export? Get your IEC online, with expert help." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "import-export-code"')
assert 'service: "import-export-code"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="import-export-code"')
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
