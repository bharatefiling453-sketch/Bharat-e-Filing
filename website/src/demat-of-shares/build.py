# Builds demat-of-shares/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/demat-of-shares/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/demat-of-shares/"
TITLE = "Demat of Shares – ISIN & Rule 9B | Bharat e-Filing"
DESC = "Dematerialise your company's shares: Rule 9B check, ISIN with NSDL and CDSL, RTA and tripartite agreements, shareholder demat requests and half-yearly PAS-6."
OG = "https://bharatefiling.com/wp-content/uploads/og/demat-of-shares-1200x630.jpg"
PUB = "2026-10-26"
SLUG = "demat-of-shares"

FAQ = [
 ("Is demat of shares mandatory for private companies?", "Yes, for private companies other than small companies and Government companies. Under Rule 9B of the Companies (Prospectus and Allotment of Securities) Rules, 2014, they must issue securities only in demat form and help shareholders dematerialise existing holdings. The compliance date for companies that were not small on 31 March 2023 was extended to 30 June 2025."),
 ("Which companies are exempt from Rule 9B?", "Small companies and Government companies are exempt. Producer companies have until 31 March 2028. From 1 December 2025, a private company with paid-up capital up to ₹10 crore and turnover up to ₹100 crore is a small company, unless it is a holding or subsidiary company or falls in another excluded class."),
 ("What if my company stops being a small company later?", "A private company that ceases to be a small company gets 18 months from the end of the financial year in which it ceased to be small to comply with the demat requirements."),
 ("Are unlisted public companies also covered?", "Yes. Unlisted public companies have been required to issue securities only in demat form and facilitate dematerialisation since 2 October 2018, under Rule 9A."),
 ("What is an ISIN?", "An International Securities Identification Number is a unique code given to each class of a company's securities. A company obtains it by entering tripartite agreements with a registrar and share transfer agent and each depository, NSDL and CDSL."),
 ("What is the process to dematerialise company shares?", "The company appoints a registrar and share transfer agent, signs tripartite agreements with NSDL and CDSL, and obtains an ISIN. Each shareholder opens a demat account with a depository participant and submits a demat request with the physical certificate, which the registrar verifies before the shares are credited."),
 ("What is Form PAS-6?", "PAS-6 is the half-yearly reconciliation of share capital audit report, filed within 60 days from the end of each half-year. It reconciles the issued capital with the shares held in NSDL, CDSL and physical form, and is certified by a practising CA or company secretary."),
 ("Can shareholders transfer physical shares after the deadline?", "No. In a company covered by Rule 9B, a shareholder must get existing shares dematerialised before transferring them or subscribing to further securities."),
 ("Do shareholders need their own demat accounts?", "Yes. Each shareholder opens a demat account with a depository participant, such as a bank or broker, in the same name and order as on the share certificate, with PAN."),
 ("What happens to the old share certificates?", "Physical certificates are surrendered with the demat request. After the registrar confirms, they are cancelled and the shares are credited to the shareholder's demat account."),
 ("Does the company need to keep paying the depositories?", "Yes. A company covered by the demat rules must pay the depository and registrar charges on time and maintain the security deposit the rules require. Our professional fee is separate from these charges."),
 ("Is dematerialisation a taxable transfer?", "No. Converting physical shares into demat form does not change ownership, so there is no capital gains tax. The original cost and holding period continue, and a later sale is taxed under the Income-tax Act, 2025 as before."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-demat p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Demat of Shares"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Demat of Shares",
  "alternateName": ["Dematerialisation of shares", "ISIN for private company", "Rule 9B compliance", "PAS-6 filing"],
  "serviceType": "Dematerialisation of a company's securities under Rules 9A and 9B",
  "description": "Demat of company shares: Rule 9B applicability check, registrar appointment, tripartite agreements and ISIN with NSDL and CDSL, shareholder demat requests, and half-yearly PAS-6 reconciliation.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Private and unlisted public companies in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Demat Plans", "itemListElement": [
    {"@type": "Offer", "name": "PAS-6 Filing", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Company Demat Setup", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Shareholder Demat Help", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to dematerialise a private company's shares", "totalTime": "P45D",
  "supply": [{"@type": "HowToSupply", "name": "Board resolution"}, {"@type": "HowToSupply", "name": "MOA, AOA and incorporation certificate"},
             {"@type": "HowToSupply", "name": "Register of members"}, {"@type": "HowToSupply", "name": "Shareholders' demat account details"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check applicability", "text": "Confirm whether Rule 9B applies and the compliance date for your company."},
   {"@type": "HowToStep", "position": 2, "name": "Appoint a registrar", "text": "Appoint a registrar and share transfer agent by board resolution."},
   {"@type": "HowToStep", "position": 3, "name": "Get the ISIN", "text": "Sign tripartite agreements with the registrar and NSDL and CDSL, and obtain the ISIN."},
   {"@type": "HowToStep", "position": 4, "name": "Demat requests", "text": "Shareholders open demat accounts and submit demat requests with their certificates; the registrar verifies and confirms."},
   {"@type": "HowToStep", "position": 5, "name": "Reconcile", "text": "File PAS-6 within 60 days of each half-year end, and issue all new securities in demat form."}]},
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
    <meta property="og:title" content="Demat of Shares – ISIN & Rule 9B" />
    <meta property="og:description" content="Dematerialise your company's shares: Rule 9B check, ISIN with NSDL and CDSL, shareholder demat and PAS-6 by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Demat of Shares" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Demat of Shares – ISIN & Rule 9B" />
    <meta name="twitter:description" content="Private company shares still on paper? Get the ISIN and go demat." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "demat-of-shares"')
assert 'service: "demat-of-shares"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="demat-of-shares"')
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
