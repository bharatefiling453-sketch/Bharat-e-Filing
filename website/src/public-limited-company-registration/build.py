# Builds public-limited-company-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/public-limited-company-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/public-limited-company-registration/"
TITLE = "Public Limited Company Registration | Bharat e-Filing"
DESC = "Register a public limited company online: SPICe+, DSCs, DINs, MoA and AoA, PAN and TAN, demat set-up and board compliance, handled by CS experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/public-limited-company-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "public-limited-company-registration"

FAQ = [
 ("What is a public limited company?", "A public company is a company that is not a private company, as defined in section 2(71) of the Companies Act, 2013. Its shares are freely transferable and it can raise money from the public. A private company that is a subsidiary of a public company is also treated as a public company."),
 ("How many members and directors are needed?", "At least seven members, with no upper limit, and at least three directors. A public company can have up to 15 directors, and more by special resolution. At least one director must have stayed in India for 182 days or more in the financial year."),
 ("Is there a minimum capital requirement?", "No. The minimum paid-up capital requirement was removed in 2015, so a public company can start with any amount of capital."),
 ("What name does a public company use?", "The name must end with the word Limited, and it must not be identical or too similar to an existing company or a registered trademark."),
 ("How is a public company incorporated?", "Online on the MCA portal through the SPICe+ form, with the memorandum and articles of association. SPICe+ also covers DINs for directors, the company's PAN and TAN, and, through linked forms, registrations such as GST, EPFO and ESIC and a bank account."),
 ("How is it different from a private limited company?", "A public company needs more members and directors, its shares can be transferred freely, and it can invite the public to subscribe to its securities, subject to SEBI rules if it lists. In return it has stricter rules on board composition, related party transactions, managerial remuneration and demat of shares."),
 ("When does a public company need independent directors?", "A listed public company needs at least one-third of its board as independent directors. An unlisted public company needs at least two independent directors if its paid-up capital is ₹10 crore or more, turnover is ₹100 crore or more, or outstanding loans, debentures and deposits exceed ₹50 crore. Wholly owned subsidiaries, joint ventures and dormant companies are exempt."),
 ("When is a woman director required?", "Every listed company, and every other public company with paid-up capital of ₹100 crore or more or turnover of ₹300 crore or more, must have at least one woman director."),
 ("Must a public company's shares be in demat form?", "Yes. Under rule 9A of the Companies (Prospectus and Allotment of Securities) Rules, 2014, an unlisted public company must issue securities only in demat form and help existing holders dematerialise them. It also files a half-yearly reconciliation of share capital audit report in Form PAS-6. Nidhi companies, government companies and wholly owned subsidiaries are exempt."),
 ("What are the yearly compliances?", "At least four board meetings a year with no more than 120 days between two meetings, an annual general meeting, audit of the accounts, financial statements in AOC-4 and the annual return in MGT-7, director KYC, and the company's income tax return. A public company cannot be a small company, so it files MGT-7, not MGT-7A."),
 ("What happens after incorporation?", "The board holds its first meeting within 30 days, appoints the first auditor within 30 days, issues share certificates within two months, and files INC-20A, the commencement of business declaration, within 180 days of incorporation."),
 ("How is a public company taxed?", "As a domestic company. It can opt for a concessional rate of 22% plus surcharge and cess by giving up certain deductions. From tax year 2026-27 this is under the Income-tax Act, 2025."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-publtd p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Public Limited Company"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Public Limited Company Registration",
  "alternateName": ["Public company registration", "Public limited company incorporation", "Ltd company registration", "SPICe+ public company"],
  "serviceType": "Incorporation of a public limited company under the Companies Act, 2013",
  "description": "Incorporation of a public limited company through SPICe+, with name approval, DSCs, DINs, MoA and AoA, PAN and TAN, demat set-up and post-incorporation compliance including INC-20A.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Promoters and growing businesses in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Public Limited Company Plans", "itemListElement": [
    {"@type": "Offer", "name": "Public Company Registration", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Public Company Complete", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Public Company with First-Year Compliance", "price": "34999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register a public limited company", "totalTime": "P20D",
  "supply": [{"@type": "HowToSupply", "name": "PAN and ID of directors and seven subscribers"}, {"@type": "HowToSupply", "name": "DSCs of directors"},
             {"@type": "HowToSupply", "name": "Registered office proof"}, {"@type": "HowToSupply", "name": "Proposed names and capital"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Get DSCs", "text": "Get Class 3 digital signatures for the three or more proposed directors."},
   {"@type": "HowToStep", "position": 2, "name": "Reserve the name", "text": "Apply for the company name, ending with Limited, through SPICe+."},
   {"@type": "HowToStep", "position": 3, "name": "File SPICe+", "text": "File SPICe+ with the MoA, AoA, director consents, the seven subscribers' details and registered office proof."},
   {"@type": "HowToStep", "position": 4, "name": "Get the certificate", "text": "Receive the certificate of incorporation with the CIN, PAN and TAN."},
   {"@type": "HowToStep", "position": 5, "name": "Start compliance", "text": "Hold the first board meeting and appoint the auditor within 30 days, get an ISIN and issue shares in demat form, and file INC-20A within 180 days."}]},
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
    <meta property="og:title" content="Public Limited Company Registration" />
    <meta property="og:description" content="SPICe+, DSCs, DINs, PAN and TAN, demat set-up and board compliance, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Public Limited Company Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Public Limited Company Registration" />
    <meta name="twitter:description" content="Planning to scale? Register your public limited company." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "public-limited-company-registration"')
assert 'service: "public-limited-company-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="public-limited-company-registration"')
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
