# Builds llp-winding-up/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/company-winding-up/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/company-winding-up/"
TITLE = "Company Winding Up & Strike Off – STK-2 | Bharat e-Filing"
DESC = "Close your private company the right way: strike off in STK-2, pending AOC-4 and MGT-7 catch-up, voluntary liquidation, and GST and tax closures."
OG = "https://bharatefiling.com/wp-content/uploads/og/company-winding-up-1200x630.jpg"
PUB = "2026-10-26"
SLUG = "company-winding-up"

FAQ = [
 ("How can a company be closed in India?", "There are three main routes: voluntary strike off by applying to the Registrar in Form STK-2 under Section 248(2) of the Companies Act, 2013; voluntary liquidation of a solvent company under Section 59 of the Insolvency and Bankruptcy Code, 2016; and winding up by the Tribunal under Section 271 of the Companies Act."),
 ("Which companies can apply for strike off in STK-2?", "A company that has not commenced business within one year of incorporation, or has not carried on any business or operation for the two immediately preceding financial years, can apply after extinguishing all its liabilities, with a special resolution or the consent of members holding 75% of the paid-up share capital."),
 ("Which companies cannot apply in STK-2?", "Section 249 bars a company from applying if, in the previous three months, it changed its name or registered office state, or disposed of property or rights for value other than in the normal course; or if it is listed, under inspection, investigation or prosecution, holds public deposits, is a Section 8 company, or has a pending scheme of arrangement or winding up."),
 ("Do pending AOC-4 and MGT-7 need to be filed before strike off?", "Yes. The company must file its overdue financial statements and annual returns up to the end of the financial year in which it stopped business, with the additional fee of ₹100 a day for each late form."),
 ("What documents are needed for STK-2?", "The special resolution or members' consent, a statement of accounts in STK-8 certified by a chartered accountant and dated not more than 30 days before filing, an indemnity bond in STK-3 and an affidavit in STK-4 from every director, and proof of closure of the bank account and tax registrations."),
 ("How long does company strike off take?", "Usually four to eight months. Since 1 May 2023, STK-2 applications are processed by the Centre for Processing Accelerated Corporate Exit (C-PACE), which publishes a public notice in STK-6 inviting objections within 30 days before striking off the name."),
 ("What is voluntary liquidation of a company?", "A solvent company with assets can be wound up under Section 59 of the Insolvency and Bankruptcy Code. A majority of directors declare solvency, the members pass a special resolution within four weeks, an insolvency professional is appointed as liquidator to sell the assets and pay creditors, and the Tribunal passes the dissolution order."),
 ("When does the Tribunal wind up a company?", "Under Section 271 of the Companies Act, the Tribunal can wind up a company if, for example, it passed a special resolution to be wound up by the Tribunal, acted against the sovereignty or security of India, conducted its affairs fraudulently, failed to file financial statements or annual returns for five consecutive years, or if it is just and equitable to do so."),
 ("Should GST be cancelled before strike off?", "Yes. Cancel the GST registration by applying in REG-16 and filing the final return, surrender the TAN after the last TDS return, and close the bank account before filing STK-2."),
 ("Are directors still liable after strike off?", "Yes. Under Section 248(7), the liability of every director, officer and member continues and can be enforced as if the company had not been dissolved."),
 ("Can a struck-off company be restored?", "Yes. A company, member, creditor or workman aggrieved by the strike off can apply to the Tribunal under Section 252. An appeal against the Registrar's order lies within three years, and an application by a member, creditor or workman can be made within twenty years."),
 ("Does the company need to file a final income tax return?", "Yes. The company files its income tax return in ITR-6 for the final year under the Income-tax Act, 2025, from tax year 2026-27, and settles any tax due before applying for strike off."),
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
   {"@type": "ListItem", "position": 3, "name": "Company Winding Up"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Company Winding Up",
  "alternateName": ["Company closure", "Company strike off STK-2", "Voluntary liquidation of company", "Close private limited company online"],
  "serviceType": "Closure of a company by strike off or liquidation",
  "description": "Closure of companies by strike off in STK-2 under Section 248(2) of the Companies Act, 2013, pending AOC-4 and MGT-7 catch-up, GST and TAN closure, and voluntary liquidation of solvent companies under Section 59 of the Insolvency and Bankruptcy Code.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Private companies and OPCs in India that want to close"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Company Closure Plans", "itemListElement": [
    {"@type": "Offer", "name": "Pending Filings Catch-up", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Company Strike Off", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Voluntary Liquidation", "price": "74999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to close a company by strike off", "totalTime": "P180D",
  "supply": [{"@type": "HowToSupply", "name": "Special resolution or 75% members' consent"}, {"@type": "HowToSupply", "name": "CA-certified statement of accounts in STK-8"},
             {"@type": "HowToSupply", "name": "Directors' indemnity bond (STK-3) and affidavit (STK-4)"}, {"@type": "HowToSupply", "name": "Bank account closure letter"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Stop business", "text": "Stop carrying on business and extinguish all liabilities."},
   {"@type": "HowToStep", "position": 2, "name": "Catch up filings", "text": "File pending AOC-4 and MGT-7 up to the year in which business stopped, and the final ITR-6."},
   {"@type": "HowToStep", "position": 3, "name": "Close registrations", "text": "Cancel GST, surrender TAN and close the bank account."},
   {"@type": "HowToStep", "position": 4, "name": "File STK-2", "text": "Pass the special resolution and file STK-2 with the STK-8 statement of accounts and the directors' STK-3 and STK-4."},
   {"@type": "HowToStep", "position": 5, "name": "Strike off", "text": "The Registrar publishes a notice in STK-6 and, if no objection is upheld, strikes off the name and publishes STK-7."}]},
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
    <meta property="og:title" content="Company Winding Up & Strike Off – STK-2" />
    <meta property="og:description" content="Close your company the right way: strike off in STK-2, pending filings and voluntary liquidation handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Company Winding Up" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Company Winding Up & Strike Off – STK-2" />
    <meta name="twitter:description" content="Company no longer in use? Close it properly and stop the yearly filings." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "company-winding-up"')
assert 'service: "company-winding-up"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="company-winding-up"')
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
