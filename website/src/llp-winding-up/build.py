# Builds llp-winding-up/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/llp-winding-up/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/llp-winding-up/"
TITLE = "LLP Winding Up & Closure – Form 24 | Bharat e-Filing"
DESC = "Close your LLP the right way: strike off in Form 24, pending Form 8 and Form 11 catch-up, voluntary liquidation for solvent LLPs, and GST and tax closures."
OG = "https://bharatefiling.com/wp-content/uploads/og/llp-winding-up-1200x630.jpg"
PUB = "2026-10-26"
SLUG = "llp-winding-up"

FAQ = [
 ("How can an LLP be closed?", "There are three main routes: striking off the LLP's name by applying to the Registrar in Form 24 under Section 75 of the LLP Act and Rule 37 of the LLP Rules; voluntary liquidation of a solvent LLP under Section 59 of the Insolvency and Bankruptcy Code, 2016; and winding up by the Tribunal under Section 64 of the LLP Act."),
 ("Who can apply for strike off in Form 24?", "An LLP that has not carried on any business since incorporation, or has stopped carrying on business for at least one year, can apply with the consent of its partners, provided it has no assets or liabilities and has closed its accounts and registrations."),
 ("Do pending Form 8 and Form 11 need to be filed before closure?", "Yes. The LLP must file its pending annual returns and statements of account up to the end of the financial year in which it stopped carrying on business, with the late fee of ₹100 a day for each late form."),
 ("What documents are needed for Form 24?", "The partners' consent, a statement of accounts showing nil assets and liabilities certified by a chartered accountant, an affidavit and indemnity bond from the designated partners, proof of closure of the bank account, and copies of any closure of tax registrations."),
 ("How long does LLP strike off take?", "Usually three to six months after Form 24 is filed. Since 27 August 2024, Form 24 applications are processed centrally, and the Registrar publishes a notice inviting objections before striking off the name."),
 ("What is voluntary liquidation of an LLP?", "A solvent LLP that has assets can be wound up voluntarily under Section 59 of the Insolvency and Bankruptcy Code. The designated partners declare solvency, the partners pass a resolution, an insolvency professional is appointed as liquidator to sell the assets and pay creditors, and the Tribunal passes the dissolution order."),
 ("When does the Tribunal wind up an LLP?", "Under Section 64 of the LLP Act, the Tribunal can wind up an LLP if, for example, it has fewer than two partners for more than six months, it cannot pay its debts, it has defaulted in filing its returns for five consecutive years, or it acted against the interests of India."),
 ("Can an LLP with GST registration be closed?", "Yes, but the GST registration should be cancelled first by applying in REG-16 and filing the final return, and the TAN should be surrendered. Strike off is easier once every registration is closed."),
 ("What happens to the partners' liability after closure?", "Partners and designated partners remain liable for any liability or fraud from the period before closure. Closure does not wipe out past obligations."),
 ("Can a struck-off LLP be restored?", "Yes. An aggrieved person, including a partner or creditor, can apply to the Tribunal to restore the LLP's name, generally within three years of the strike off."),
 ("What are the late fees for pending LLP filings?", "Form 8 and Form 11 each carry a late fee of ₹100 a day from their due dates. An LLP that missed several years should calculate these before deciding on the closure route."),
 ("Does the LLP need to file a final income tax return?", "Yes. The LLP files its income tax return in ITR-5 for the final year under the Income-tax Act, 2025, from tax year 2026-27, and settles any tax due before closure."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-closure p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "LLP Winding Up"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "LLP Winding Up",
  "alternateName": ["LLP closure", "LLP strike off Form 24", "Voluntary liquidation of LLP", "Close LLP online"],
  "serviceType": "Closure of a limited liability partnership by strike off or liquidation",
  "description": "Closure of LLPs by strike off in Form 24 under Section 75 and Rule 37, pending Form 8 and Form 11 catch-up, GST and TAN closure, and voluntary liquidation of solvent LLPs under Section 59 of the Insolvency and Bankruptcy Code.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Limited liability partnerships in India that want to close"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "LLP Closure Plans", "itemListElement": [
    {"@type": "Offer", "name": "Pending Filings Catch-up", "price": "2499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "LLP Strike Off", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Voluntary Liquidation", "price": "49999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to close an LLP by strike off", "totalTime": "P120D",
  "supply": [{"@type": "HowToSupply", "name": "Partners' consent"}, {"@type": "HowToSupply", "name": "CA-certified statement of accounts"},
             {"@type": "HowToSupply", "name": "Affidavit and indemnity bond"}, {"@type": "HowToSupply", "name": "Bank account closure letter"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Stop business", "text": "Stop carrying on business and settle all assets and liabilities."},
   {"@type": "HowToStep", "position": 2, "name": "Catch up filings", "text": "File pending Form 8 and Form 11 up to the year in which business stopped, and the final ITR-5."},
   {"@type": "HowToStep", "position": 3, "name": "Close registrations", "text": "Cancel GST, surrender TAN and close the bank account."},
   {"@type": "HowToStep", "position": 4, "name": "File Form 24", "text": "File Form 24 with the partners' consent, statement of accounts, affidavit and indemnity bond."},
   {"@type": "HowToStep", "position": 5, "name": "Strike off", "text": "The Registrar publishes a notice and, if no objection is upheld, strikes off the LLP's name."}]},
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
    <meta property="og:title" content="LLP Winding Up & Closure – Form 24" />
    <meta property="og:description" content="Close your LLP the right way: strike off in Form 24, pending filings and voluntary liquidation handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – LLP Winding Up" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="LLP Winding Up & Closure – Form 24" />
    <meta name="twitter:description" content="LLP no longer in use? Close it properly and stop the yearly filings." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "llp-winding-up"')
assert 'service: "llp-winding-up"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="llp-winding-up"')
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
