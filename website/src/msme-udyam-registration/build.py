# Builds msme-udyam-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/msme-udyam-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/msme-udyam-registration/"
TITLE = "Udyam Registration (MSME) Online | Bharat e-Filing"
DESC = "Register your MSME on Udyam with the April 2025 limits checked: micro, small or medium. Plus updates and help collecting late payments from buyers."
OG = "https://bharatefiling.com/wp-content/uploads/og/msme-udyam-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "msme-udyam-registration"

FAQ = [
 ("What is Udyam Registration?", "Udyam Registration is the official registration of micro, small and medium enterprises (MSMEs) with the Ministry of MSME. It is done online on the Udyam Registration portal using Aadhaar, and gives the enterprise a permanent Udyam Registration Number and certificate."),
 ("What are the MSME limits from 1 April 2025?", "Under notification S.O. 1364(E) dated 21 March 2025, a micro enterprise has investment in plant and machinery or equipment up to ₹2.5 crore and turnover up to ₹10 crore; a small enterprise up to ₹25 crore and ₹100 crore; and a medium enterprise up to ₹125 crore and ₹500 crore."),
 ("How is the category decided if one limit is crossed?", "Both investment and turnover are considered. If an enterprise crosses either limit for its category, it moves to the next higher category, but it moves down only when it falls below both limits of its current category."),
 ("Is export turnover counted?", "No. Turnover from exports is excluded when calculating turnover for MSME classification."),
 ("What do I need to register?", "The Aadhaar number of the proprietor, managing partner, karta or authorised signatory, the PAN of the enterprise, and GSTIN where the business is required to be registered under GST. Investment and turnover details are linked to income tax and GST records."),
 ("Do I need to upload documents?", "No. Udyam Registration is based on self-declaration, and no documents or certificates need to be uploaded. The details are checked against government databases such as PAN and GST."),
 ("Do I need to renew Udyam Registration?", "No. The registration is permanent, but the details should be kept updated. Investment and turnover are updated using income tax and GST data, and the category can change each year."),
 ("Can traders register on Udyam?", "Yes. Retail and wholesale traders can register on Udyam, but their registration is for priority sector lending benefits only."),
 ("Within how many days must buyers pay MSE suppliers?", "Under Section 15 of the MSMED Act, 2006, a buyer must pay a micro or small enterprise within the period agreed in writing, which cannot exceed 45 days from acceptance, or within 15 days if there is no written agreement."),
 ("What if a buyer pays a micro or small enterprise late?", "The buyer must pay compound interest with monthly rests at three times the bank rate notified by the RBI under Section 16 of the MSMED Act. The supplier can also apply to the MSE Facilitation Council through the MSME Samadhaan portal."),
 ("How does late payment affect the buyer's income tax?", "Under section 43B(h) of the Income-tax Act, 1961, and section 37(2)(g) of the Income-tax Act, 2025 from tax year 2026-27, a buyer can deduct an amount owed to a micro or small enterprise only in the year it is actually paid, if it is not paid within the time allowed under the MSMED Act."),
 ("What is MSME Form 1?", "Companies that owe micro or small enterprises for more than 45 days must file MSME Form 1 with the MCA every half-year, disclosing the amounts and reasons for delay: by 30 April for October to March, and by 31 October for April to September."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-udyam p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Udyam Registration"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Udyam Registration",
  "alternateName": ["MSME registration", "Udyam certificate", "Udyam Aadhaar registration", "MSME Udyam update"],
  "serviceType": "MSME registration on the Udyam Registration portal",
  "description": "Udyam Registration for micro, small and medium enterprises, with classification checked against the limits in force from 1 April 2025, plus Udyam updates and help with delayed MSE payments.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Micro, small and medium enterprises in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Udyam Plans", "itemListElement": [
    {"@type": "Offer", "name": "Udyam Registration", "price": "499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Udyam Plus", "price": "999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "MSME Payment Recovery", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register on Udyam", "totalTime": "P1D",
  "supply": [{"@type": "HowToSupply", "name": "Aadhaar of the proprietor, partner or director"}, {"@type": "HowToSupply", "name": "PAN of the enterprise"},
             {"@type": "HowToSupply", "name": "GSTIN, if registered"}, {"@type": "HowToSupply", "name": "Bank account and business details"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Verify Aadhaar", "text": "Enter the Aadhaar number of the proprietor, managing partner, karta or authorised signatory and verify it by OTP."},
   {"@type": "HowToStep", "position": 2, "name": "Validate PAN", "text": "Enter the enterprise's PAN, which is validated and used to fetch income tax and GST details."},
   {"@type": "HowToStep", "position": 3, "name": "Fill business details", "text": "Add the enterprise name, address, activity, NIC codes, bank details and employment."},
   {"@type": "HowToStep", "position": 4, "name": "Declare and submit", "text": "Declare investment and turnover and submit the self-declaration with OTP."},
   {"@type": "HowToStep", "position": 5, "name": "Get the certificate", "text": "Receive the Udyam Registration Number and download the certificate."}]},
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
    <meta property="og:title" content="Udyam Registration (MSME) Online" />
    <meta property="og:description" content="Register your MSME on Udyam with the April 2025 limits checked, plus help collecting late payments." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Udyam Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Udyam Registration (MSME) Online" />
    <meta name="twitter:description" content="Running a small business? Get your Udyam certificate, with expert help." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "msme-udyam-registration"')
assert 'service: "msme-udyam-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="msme-udyam-registration"')
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
