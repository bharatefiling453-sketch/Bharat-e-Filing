# Builds fdi-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/fdi-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/fdi-filing/"
TITLE = "FDI Filing with RBI | Bharat e-Filing"
DESC = "FDI filing with the RBI on FIRMS: Entity Master, FC-GPR within 30 days, FC-TRS, LLP-I and the FLA return, with valuation and CS certificate support."
OG = "https://bharatefiling.com/wp-content/uploads/og/fdi-filing-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "fdi-filing"

FAQ = [
 ("What is FDI filing?", "FDI filing is the reporting of foreign investment received by an Indian company or LLP to the Reserve Bank of India under FEMA. Reports are filed online on the RBI's FIRMS portal through the Single Master Form and are reviewed by the company's authorised dealer bank."),
 ("Which laws govern FDI reporting?", "The Foreign Exchange Management Act, 1999, the FEMA (Non-debt Instruments) Rules, 2019, the FEMA (Mode of Payment and Reporting of Non-Debt Instruments) Regulations, 2019, and the RBI Master Direction on Foreign Investment in India."),
 ("What is the Entity Master on FIRMS?", "Before filing any form, the Indian company or LLP registers a business user on the FIRMS portal and creates its Entity Master, which records its existing foreign investment. Forms such as FC-GPR are then filed under the Single Master Form."),
 ("When is Form FC-GPR due?", "Within 30 days of issuing equity shares, compulsorily convertible preference shares or debentures, or other capital instruments to a person resident outside India."),
 ("How soon must shares be issued after money is received?", "The company must issue the capital instruments within 60 days of receiving the money. If it cannot, it must refund the money to the investor within 15 days after those 60 days end."),
 ("When is Form FC-TRS due?", "Within 60 days of the transfer of capital instruments between a resident and a non-resident, or of the receipt or remittance of funds, whichever is earlier. The resident transferor or transferee files it."),
 ("What is the FLA return?", "The Annual Return on Foreign Liabilities and Assets. Indian companies and LLPs that have received foreign direct investment or made overseas investment file it on the RBI's FLAIR portal by 15 July each year, for the position as on 31 March."),
 ("What forms does an LLP file?", "Form LLP-I within 30 days of receiving foreign capital contribution or acquiring profit shares, and Form LLP-II within 60 days of a disinvestment or transfer between a resident and a non-resident."),
 ("At what price can shares be issued to a foreign investor?", "For an unlisted company, not below the fair value worked out under an internationally accepted pricing method and certified by a chartered accountant, a SEBI-registered merchant banker or a practising cost accountant."),
 ("Does every investment come under the automatic route?", "No. Most sectors allow FDI under the automatic route up to a cap, but some need government approval, and a few are prohibited. Investment from an entity of a country that shares a land border with India, or where the beneficial owner is from such a country, needs government approval."),
 ("What if an FDI form is filed late?", "A delay can usually be regularised within three years of the due date by filing the form and paying the late submission fee worked out by the RBI, which grows with the amount and the delay. Beyond that, or for other contraventions, the matter goes to compounding."),
 ("How is foreign investment taxed?", "Dividends and gains of foreign investors are taxed in India, with tax deducted at source, and relief may be available under a tax treaty. From tax year 2026-27 this is under the Income-tax Act, 2025. The angel tax on share premium was removed from FY 2024-25."),
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
  "reviewedBy": {"@type": "Person", "name": "REPLACE_CS_NAME", "jobTitle": "Company Secretary", "url": "https://bharatefiling.com/team/REPLACE_CS_SLUG/"},
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-fdi p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "FDI Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "FDI Filing with RBI",
  "alternateName": ["FC-GPR filing", "FC-TRS filing", "FIRMS portal filing", "FLA return filing", "Foreign direct investment reporting"],
  "serviceType": "Reporting of foreign direct investment to the Reserve Bank of India under FEMA",
  "description": "FDI reporting on the RBI FIRMS portal: Entity Master, FC-GPR, FC-TRS, LLP-I and LLP-II, and the annual FLA return, with valuation and certificate coordination.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Indian companies and LLPs receiving foreign investment"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "FDI Filing Plans", "itemListElement": [
    {"@type": "Offer", "name": "FC-GPR Filing", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "FDI Complete", "price": "11999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "FDI Annual Compliance", "price": "24999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file FC-GPR for foreign investment", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "FIRC and KYC of the foreign investor from the bank"}, {"@type": "HowToSupply", "name": "Valuation certificate"},
             {"@type": "HowToSupply", "name": "Board resolution and allotment details"}, {"@type": "HowToSupply", "name": "Company secretary certificate"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Receive the money", "text": "Receive the investment through banking channels and get the FIRC and investor KYC from the authorised dealer bank."},
   {"@type": "HowToStep", "position": 2, "name": "Value the shares", "text": "Get a valuation certificate showing the issue price is not below fair value."},
   {"@type": "HowToStep", "position": 3, "name": "Allot within 60 days", "text": "Allot the shares within 60 days of receiving the money and file the allotment with the ROC."},
   {"@type": "HowToStep", "position": 4, "name": "File FC-GPR", "text": "File FC-GPR on the FIRMS portal within 30 days of allotment, with the valuation and company secretary certificates."},
   {"@type": "HowToStep", "position": 5, "name": "Bank approval", "text": "Respond to any queries from the authorised dealer bank until the form is approved, then file the FLA return each year."}]},
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
    <meta property="og:title" content="FDI Filing with RBI" />
    <meta property="og:description" content="FC-GPR, FC-TRS, LLP-I and the FLA return on the RBI FIRMS portal, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – FDI Filing with RBI" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="FDI Filing with RBI" />
    <meta name="twitter:description" content="Received foreign investment? Report it to the RBI on time." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "fdi-filing"')
assert 'service: "fdi-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="fdi-filing"')
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
