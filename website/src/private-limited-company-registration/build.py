# Builds private-limited-company-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/private-limited-company-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/private-limited-company-registration/"
TITLE = "Private Limited Company Registration | Bharat e-Filing"
DESC = "Register a private limited company online: SPICe+, DSCs, DINs, e-MoA and e-AoA, PAN and TAN, plus first-year compliance, handled by CS experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/private-limited-company-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "private-limited-company-registration"

FAQ = [
 ("What is a private limited company?", "A private limited company is a company defined in section 2(68) of the Companies Act, 2013. Its articles restrict the transfer of shares, limit members to 200, and bar inviting the public to subscribe to its securities. It is a separate legal entity, and its shareholders' liability is limited to the unpaid amount on their shares."),
 ("How many members and directors are needed?", "At least two members and at least two directors. A private company can have up to 200 members and up to 15 directors, and more directors by special resolution. The same two people can be both members and directors."),
 ("Does a private company need a resident director?", "Yes. Under section 149(3), every company must have at least one director who has stayed in India for a total of at least 182 days during the financial year."),
 ("Is there a minimum capital requirement?", "No. The minimum paid-up capital requirement was removed in 2015, so a private company can start with any amount of capital its founders choose."),
 ("How is a private company incorporated?", "Online on the MCA portal through the SPICe+ form, with the electronic memorandum and articles of association. SPICe+ also covers DINs for directors, the company's PAN and TAN, and, through linked forms, registrations such as GST, EPFO and ESIC and a bank account."),
 ("What happens after incorporation?", "The board holds its first meeting within 30 days, appoints the first auditor within 30 days, issues share certificates within two months, and files INC-20A, the commencement of business declaration, within 180 days of incorporation."),
 ("What are the yearly compliances?", "Holding board meetings and an annual general meeting, getting the accounts audited, filing financial statements in AOC-4 and the annual return in MGT-7 or MGT-7A, director KYC, and the company's income tax return."),
 ("How many board meetings must be held?", "At least four a year, with no more than 120 days between two meetings. A small company needs at least one meeting in each half of the calendar year, at least 90 days apart."),
 ("Must a private company's shares be in demat form?", "Private companies other than small companies must issue securities only in demat form and help existing shareholders dematerialise their shares, under rule 9B of the Companies (Prospectus and Allotment of Securities) Rules, 2014."),
 ("How is a private company taxed?", "As a domestic company. It can opt for a concessional rate of 22% plus surcharge and cess by giving up certain deductions. From tax year 2026-27 this is under the Income-tax Act, 2025."),
 ("Can a private company raise investment?", "Yes. It can issue shares to investors through private placement or a rights issue, which is the main reason founders who plan to raise funding choose a private limited company over an LLP."),
 ("Can a startup get tax benefits?", "A private company recognised by DPIIT as a startup can access Startup India benefits, and eligible startups can apply for a tax holiday on profits for three consecutive years out of their first ten, subject to the conditions in the Income-tax Act."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-pvtltd p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Private Limited Company"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Private Limited Company Registration",
  "alternateName": ["Pvt Ltd registration", "Private company incorporation", "Register a company online", "SPICe+ company registration"],
  "serviceType": "Incorporation of a private limited company under the Companies Act, 2013",
  "description": "Incorporation of a private limited company through SPICe+, with name approval, DSCs, DINs, e-MoA and e-AoA, PAN and TAN, and post-incorporation compliance including INC-20A.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Founders and startups in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Private Limited Company Plans", "itemListElement": [
    {"@type": "Offer", "name": "Company Registration", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Company Complete", "price": "8999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Company with First-Year Compliance", "price": "24999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register a private limited company", "totalTime": "P15D",
  "supply": [{"@type": "HowToSupply", "name": "Directors' and shareholders' PAN and ID"}, {"@type": "HowToSupply", "name": "DSCs of directors"},
             {"@type": "HowToSupply", "name": "Registered office proof"}, {"@type": "HowToSupply", "name": "Proposed names and capital"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Get DSCs", "text": "Get Class 3 digital signatures for the proposed directors."},
   {"@type": "HowToStep", "position": 2, "name": "Reserve the name", "text": "Apply for the company name, ending with Private Limited, through SPICe+."},
   {"@type": "HowToStep", "position": 3, "name": "File SPICe+", "text": "File SPICe+ with the e-MoA, e-AoA, director consents and registered office proof."},
   {"@type": "HowToStep", "position": 4, "name": "Get the certificate", "text": "Receive the certificate of incorporation with the CIN, PAN and TAN."},
   {"@type": "HowToStep", "position": 5, "name": "Start compliance", "text": "Hold the first board meeting and appoint the auditor within 30 days, issue share certificates and file INC-20A within 180 days."}]},
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
    <meta property="og:title" content="Private Limited Company Registration" />
    <meta property="og:description" content="SPICe+, DSCs, DINs, e-MoA and e-AoA, PAN and TAN, and first-year compliance, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Private Limited Company Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Private Limited Company Registration" />
    <meta name="twitter:description" content="Building to raise funds? Register your private limited company." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "private-limited-company-registration"')
assert 'service: "private-limited-company-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="private-limited-company-registration"')
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
