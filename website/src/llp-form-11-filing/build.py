# Builds llp-form-11-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/llp-form-11-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/llp-form-11-filing/"
TITLE = "LLP Form 11 Filing Online – Annual Return | Bharat e-Filing"
DESC = "File LLP Form 11 by 30 May: partners, contribution and changes reported, CS certification where needed, and late Form 11 caught up before ₹100 a day adds up."
OG = "https://bharatefiling.com/wp-content/uploads/og/llp-form-11-filing-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "llp-form-11-filing"

FAQ = [
 ("What is LLP Form 11?", "Form 11 is the annual return of a limited liability partnership, filed with the Registrar under Section 35 of the LLP Act, 2008 and Rule 25 of the LLP Rules, 2009. It reports the LLP's partners and designated partners, their contribution, and changes during the year."),
 ("What is the due date for Form 11?", "Form 11 is due within 60 days of the end of the financial year, that is by 30 May. For FY 2025-26 it was due by 30 May 2026, and for FY 2026-27 it is due by 30 May 2027."),
 ("What is the late fee for Form 11?", "Form 11 filed after 30 May attracts an additional fee of ₹100 for each day of delay. It keeps adding up until the form is filed, so a year's delay costs over ₹36,000 for one form."),
 ("Is Form 11 required if the LLP had no business?", "Yes. Every LLP must file Form 11 every year, even with no business, income or transactions. Only an LLP that has been struck off is free of the filing."),
 ("Who signs Form 11?", "Form 11 is signed by a designated partner with a digital signature. Where the LLP's contribution exceeds ₹50 lakh or its turnover exceeds ₹5 crore, it must also be certified by a practising company secretary."),
 ("What information is needed for Form 11?", "The LLPIN, details of all partners and designated partners with their DPIN or DIN, each partner's contribution received, details of body corporate partners, changes in partners during the year, and the LLP's turnover and total contribution."),
 ("What is the difference between Form 11 and Form 8?", "Form 11 is the annual return about partners and contribution, due by 30 May. Form 8 is the statement of account and solvency with the financial figures, due by 30 October. Both are filed every year."),
 ("Do partner changes need a separate form?", "Yes. Appointment or cessation of a partner or designated partner is filed in Form 4 within 30 days, and a change in the LLP agreement in Form 3. Form 11 then reflects the position for the year."),
 ("What is a small LLP?", "A small LLP is one whose partners' contribution does not exceed ₹25 lakh and turnover does not exceed ₹40 lakh, within the limits the LLP Act allows the government to prescribe. Small LLPs face lower penalties for many defaults, but must still file Form 11 on time."),
 ("Can I file Form 11 for past years together?", "Yes. Pending Form 11 returns for earlier years can be filed now, each with its own late fee of ₹100 a day. Filing them in order also clears the way for Form 8 and for any closure application."),
 ("Do designated partners need DIN KYC?", "Yes. Designated partners hold a DIN or DPIN, and their KYC must be up to date, or the DIN is deactivated and cannot be used to sign Form 11."),
 ("Is Form 11 linked to the LLP's income tax return?", "They are separate. Form 11 goes to the Registrar under the LLP Act, while the LLP files its income tax return in ITR-5 under the Income-tax Act, 2025 from tax year 2026-27. Contribution and partner details should match across both."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-form11 p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "LLP Form 11 Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "LLP Form 11 Filing",
  "alternateName": ["LLP annual return", "Form 11 filing", "LLP Form 11 late filing"],
  "serviceType": "Annual return of a limited liability partnership filed with the Registrar of Companies",
  "description": "LLP Form 11 annual return filed by 30 May: partner, designated partner and contribution details, body corporate partners, CS certification where required, and catch-up filing of late Form 11 returns.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Limited liability partnerships in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Form 11 Plans", "itemListElement": [
    {"@type": "Offer", "name": "Form 11 Filing", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Form 11 + Form 8", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Late Form 11 Catch-up", "price": "2499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file LLP Form 11", "totalTime": "P2D",
  "supply": [{"@type": "HowToSupply", "name": "LLPIN and partner details"}, {"@type": "HowToSupply", "name": "Contribution received from each partner"},
             {"@type": "HowToSupply", "name": "Turnover for the year"}, {"@type": "HowToSupply", "name": "Designated partner's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Confirm partners", "text": "Confirm the partners and designated partners, and that every partner change during the year was filed in Form 4."},
   {"@type": "HowToStep", "position": 2, "name": "Record contribution", "text": "Record the contribution received from each partner and the LLP's total contribution and turnover."},
   {"@type": "HowToStep", "position": 3, "name": "Check certification", "text": "Get a practising company secretary's certificate if contribution exceeds ₹50 lakh or turnover exceeds ₹5 crore."},
   {"@type": "HowToStep", "position": 4, "name": "Sign and file", "text": "Sign Form 11 with a designated partner's DSC and file it by 30 May."},
   {"@type": "HowToStep", "position": 5, "name": "Plan Form 8", "text": "Diary Form 8, the statement of account and solvency, due by 30 October."}]},
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
    <meta property="og:title" content="LLP Form 11 Filing – Annual Return" />
    <meta property="og:description" content="Your LLP's annual return filed by 30 May, with partners and contribution checked by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – LLP Form 11 Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="LLP Form 11 Filing – Annual Return" />
    <meta name="twitter:description" content="LLP Form 11 due 30 May. Filed right, before ₹100 a day adds up." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "llp-form-11-filing"')
assert 'service: "llp-form-11-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="llp-form-11-filing"')
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
