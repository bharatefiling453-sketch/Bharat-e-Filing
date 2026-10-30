# Builds llp-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/llp-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/llp-registration/"
TITLE = "LLP Registration Online | Bharat e-Filing"
DESC = "Register your LLP online: limited liability with partnership flexibility. Name, DSCs, FiLLiP and the LLP agreement in Form 3, handled by CS experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/llp-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "llp-registration"

FAQ = [
 ("What is a Limited Liability Partnership?", "A Limited Liability Partnership (LLP) is a body corporate formed under the Limited Liability Partnership Act, 2008. It is a separate legal entity from its partners, and each partner's liability is generally limited to the contribution agreed in the LLP agreement."),
 ("How many partners does an LLP need?", "At least two partners. There is no maximum number of partners. Partners can be individuals or body corporates."),
 ("What is a designated partner?", "Every LLP must have at least two designated partners who are individuals, and at least one of them must be resident in India. Designated partners are responsible for the LLP's compliance with the Act."),
 ("Who counts as resident in India for an LLP?", "For designated partners, a person resident in India is one who has stayed in India for at least 120 days during the financial year, as amended by the LLP (Amendment) Act, 2021."),
 ("How is an LLP incorporated?", "Online on the MCA portal: reserve the name, then file the incorporation form, FiLLiP, with the partners' details, consent of the designated partners, and registered office proof. The certificate of incorporation is issued with the LLPIN."),
 ("When must the LLP agreement be filed?", "The LLP agreement is filed with the Registrar in Form 3 within 30 days of incorporation, and any later change to it is also filed in Form 3 within 30 days."),
 ("What are the yearly filings for an LLP?", "Form 11, the annual return, by 30 May, and Form 8, the statement of account and solvency, by 30 October, after each financial year. Each carries a late fee of ₹100 a day if filed late."),
 ("Does an LLP need an audit?", "Yes, unless its turnover does not exceed ₹40 lakh in the financial year or its partners' contribution does not exceed ₹25 lakh, under rule 24 of the LLP Rules, 2009. Tax audit rules under the Income-tax Act apply separately."),
 ("How is an LLP taxed?", "An LLP is taxed like a partnership firm, at a flat rate of 30% plus surcharge and cess where applicable. From tax year 2026-27 this is under the Income-tax Act, 2025."),
 ("Can partners be paid remuneration and interest?", "Yes, if the LLP agreement authorises it. Interest on capital up to 12% a year and remuneration to working partners within limits based on book profit are deductible for the LLP, and from 1 April 2025 TDS at 10% applies when payments to a partner exceed ₹20,000 in a year."),
 ("Can a partnership firm or company convert into an LLP?", "Yes. The LLP Act allows a partnership firm, a private company or an unlisted public company to convert into an LLP, subject to the conditions in the Act's schedules."),
 ("LLP or private limited company: which is better?", "An LLP suits professional and family businesses that want limited liability with fewer formalities. A private limited company suits businesses that plan to raise equity from investors, since an LLP cannot issue shares."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-llp p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "LLP Registration"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "LLP Registration",
  "alternateName": ["Limited Liability Partnership registration", "LLP incorporation", "Register LLP online", "FiLLiP filing"],
  "serviceType": "Incorporation of a Limited Liability Partnership under the LLP Act, 2008",
  "description": "Incorporation of a Limited Liability Partnership: name reservation, DSCs, FiLLiP filing, LLP agreement drafted and filed in Form 3, with PAN and TAN and first-year compliance.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Professionals and businesses starting together in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "LLP Plans", "itemListElement": [
    {"@type": "Offer", "name": "LLP Registration", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "LLP Complete", "price": "7999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "LLP with First-Year Compliance", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register an LLP", "totalTime": "P15D",
  "supply": [{"@type": "HowToSupply", "name": "Partners' PAN, ID and address proof"}, {"@type": "HowToSupply", "name": "DSCs of designated partners"},
             {"@type": "HowToSupply", "name": "Registered office proof"}, {"@type": "HowToSupply", "name": "LLP agreement terms"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Get DSCs", "text": "Get Class 3 digital signatures for the designated partners."},
   {"@type": "HowToStep", "position": 2, "name": "Reserve the name", "text": "Apply for the LLP name, ending with LLP, on the MCA portal."},
   {"@type": "HowToStep", "position": 3, "name": "File FiLLiP", "text": "File the incorporation form with partner details, designated partner consent and office proof."},
   {"@type": "HowToStep", "position": 4, "name": "Get the certificate", "text": "Receive the certificate of incorporation with the LLPIN, PAN and TAN."},
   {"@type": "HowToStep", "position": 5, "name": "File the LLP agreement", "text": "File the LLP agreement in Form 3 within 30 days of incorporation."}]},
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
    <meta property="og:title" content="LLP Registration Online" />
    <meta property="og:description" content="Limited liability with partnership flexibility: FiLLiP, DSCs and the LLP agreement, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – LLP Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="LLP Registration Online" />
    <meta name="twitter:description" content="Starting with partners? Get limited liability with an LLP." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "llp-registration"')
assert 'service: "llp-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="llp-registration"')
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
