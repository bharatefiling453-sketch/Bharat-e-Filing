# Builds section-8-company-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/section-8-company-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/section-8-company-registration/"
TITLE = "Section 8 Company Registration | Bharat e-Filing"
DESC = "Register a Section 8 company for your non-profit: licence and incorporation through SPICe+, DSCs, MoA and AoA, PAN and TAN, handled by CS experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/section-8-company-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "section-8-company-registration"

FAQ = [
 ("What is a Section 8 company?", "A Section 8 company is a company licensed under section 8 of the Companies Act, 2013 to promote objects such as commerce, art, science, sports, education, research, social welfare, religion, charity or protection of the environment. It must apply its profits and income only to these objects and cannot pay dividends to its members."),
 ("How many members and directors are needed?", "A Section 8 company formed as a private company needs at least two members and two directors. One formed as a public company needs at least seven members and three directors. At least one director must have stayed in India for 182 days or more in the financial year."),
 ("Is there a minimum capital requirement?", "No. A Section 8 company has no minimum capital requirement, and it can also be formed without share capital as a company limited by guarantee."),
 ("Does the name need to end with Limited?", "No. The licence allows a Section 8 company to drop the word Limited or Private Limited. Names usually include words such as Foundation, Forum, Association, Federation, Council or Institute."),
 ("How is a Section 8 company incorporated?", "Online on the MCA portal through SPICe+. The licence under section 8 is applied for in the same filing, with the memorandum and articles in the prescribed format and declarations from the subscribers and a professional. The licence is issued along with the certificate of incorporation."),
 ("Can members or directors be paid?", "Members cannot receive dividends or any share of the profits. The company can pay reasonable remuneration to members, directors or others for services actually rendered, within the rules."),
 ("Can a One Person Company be a Section 8 company?", "No. A One Person Company cannot be incorporated as, or converted into, a Section 8 company."),
 ("What are the yearly compliances?", "Board meetings, an annual general meeting, audit of the accounts, financial statements in AOC-4 and the annual return in MGT-7, director KYC, and the income tax return. A Section 8 company needs to hold at least one board meeting in every six calendar months."),
 ("Is a Section 8 company exempt from income tax?", "Not automatically. It must register with the Income Tax Department as a charitable organisation. For FY 2025-26 this is registration under section 12A or 12AB of the Income-tax Act, 1961. From tax year 2026-27 registration is under the Income-tax Act, 2025, as a registered non-profit organisation."),
 ("Can donors get a tax deduction?", "Only if the Section 8 company has approval for donations, known as 80G approval under the 1961 Act, with equivalent approval under the Income-tax Act, 2025. Donors then claim the deduction allowed by law."),
 ("Can a Section 8 company receive CSR or foreign funds?", "To run CSR projects for companies, it registers with the MCA in Form CSR-1. To receive foreign contributions, it needs registration or prior permission under the Foreign Contribution (Regulation) Act, 2010."),
 ("What if the company breaks the Section 8 conditions?", "The Central Government can revoke the licence, and the company and its officers in default can face heavy fines, and officers possible imprisonment. Changing the memorandum or articles, or converting into another kind of company, needs government approval."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-section8 p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Section 8 Company"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Section 8 Company Registration",
  "alternateName": ["Section 8 company incorporation", "NGO company registration", "Non-profit company registration", "Section 8 licence"],
  "serviceType": "Licence and incorporation of a Section 8 company under the Companies Act, 2013",
  "description": "Licence and incorporation of a Section 8 non-profit company through SPICe+, with name approval, DSCs, DINs, MoA and AoA, PAN and TAN, and guidance on income tax registration.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "Audience", "audienceType": "Non-profits, foundations and social enterprises in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Section 8 Company Plans", "itemListElement": [
    {"@type": "Offer", "name": "Section 8 Registration", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Section 8 Complete", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Section 8 with Tax Registration", "price": "24999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register a Section 8 company", "totalTime": "P20D",
  "supply": [{"@type": "HowToSupply", "name": "Directors' and members' PAN and ID"}, {"@type": "HowToSupply", "name": "DSCs of directors"},
             {"@type": "HowToSupply", "name": "Registered office proof"}, {"@type": "HowToSupply", "name": "Objects and planned activities"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Get DSCs", "text": "Get Class 3 digital signatures for the proposed directors."},
   {"@type": "HowToStep", "position": 2, "name": "Reserve the name", "text": "Apply for a name that reflects the non-profit objects through SPICe+."},
   {"@type": "HowToStep", "position": 3, "name": "File SPICe+ with the licence", "text": "File SPICe+ with the memorandum and articles in the Section 8 format, the declarations and the estimated income and expenditure."},
   {"@type": "HowToStep", "position": 4, "name": "Get the licence and certificate", "text": "Receive the Section 8 licence and the certificate of incorporation with the CIN, PAN and TAN."},
   {"@type": "HowToStep", "position": 5, "name": "Register for tax", "text": "Hold the first board meeting, appoint the auditor and apply for income tax registration and donation approval."}]},
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
    <meta property="og:title" content="Section 8 Company Registration" />
    <meta property="og:description" content="Licence and incorporation for your non-profit, plus income tax registration, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Section 8 Company Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Section 8 Company Registration" />
    <meta name="twitter:description" content="Running a non-profit? Register it as a Section 8 company." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "section-8-company-registration"')
assert 'service: "section-8-company-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="section-8-company-registration"')
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
