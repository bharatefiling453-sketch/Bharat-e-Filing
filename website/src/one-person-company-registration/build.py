# Builds one-person-company-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/one-person-company-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/one-person-company-registration/"
TITLE = "One Person Company (OPC) Registration | Bharat e-Filing"
DESC = "Register a One Person Company online: limited liability for a solo founder, open to Indian citizens including NRIs, with SPICe+, nominee and INC-20A handled."
OG = "https://bharatefiling.com/wp-content/uploads/og/one-person-company-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "one-person-company-registration"

FAQ = [
 ("What is a One Person Company?", "A One Person Company (OPC) is a company with only one person as its member, defined in section 2(62) of the Companies Act, 2013. It is a separate legal entity with limited liability, so the owner's personal assets are generally protected from the company's debts."),
 ("Who can form an OPC?", "Only a natural person who is an Indian citizen, whether resident in India or not, can incorporate an OPC or be its nominee. Since 1 April 2021, Indian citizens who are not resident in India, such as NRIs, can also form one."),
 ("What does resident in India mean for an OPC?", "For OPC rules, a person resident in India is one who has stayed in India for at least 120 days during the immediately preceding financial year. This replaced the earlier 182-day test from 1 April 2021."),
 ("Can one person form more than one OPC?", "No. A natural person can incorporate only one OPC, or be a nominee in only one OPC, at a time."),
 ("Why does an OPC need a nominee?", "The sole member must name a nominee who will become the member if the member dies or becomes incapable of contracting. The nominee's written consent is filed with the incorporation application."),
 ("Is there a limit on capital or turnover for an OPC?", "Not any more. The Companies (Incorporation) Second Amendment Rules, 2021 removed the earlier paid-up capital and turnover limits that forced an OPC to convert, and allow an OPC to convert voluntarily into a private or public company at any time."),
 ("How many directors can an OPC have?", "At least one and up to fifteen directors. The sole member can also be the sole director."),
 ("How is an OPC incorporated?", "Online on the MCA portal through the SPICe+ form, with the electronic memorandum and articles of association. The application also covers the company's PAN and TAN, and can include GST, EPFO and ESIC registrations and a bank account through linked forms."),
 ("What compliances does an OPC have after incorporation?", "Filing INC-20A within 180 days of incorporation, appointing the first auditor within 30 days, filing financial statements in AOC-4 within 180 days of the end of the financial year, filing the abridged annual return in MGT-7A, and filing an income tax return every year."),
 ("Does an OPC hold an annual general meeting?", "No. Section 96 of the Companies Act exempts an OPC from holding an annual general meeting."),
 ("How is an OPC taxed?", "An OPC is taxed as a domestic company, not as an individual. It can choose a concessional company tax rate of 22% plus surcharge and cess by giving up certain deductions. From tax year 2026-27 this is under the Income-tax Act, 2025."),
 ("What is the difference between an OPC and a proprietorship?", "A proprietorship is not separate from its owner, so the owner's liability is unlimited. An OPC is a separate company with limited liability and perpetual succession through its nominee, but it has more compliance, including audited accounts and MCA filings."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-opc p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "One Person Company"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "One Person Company Registration",
  "alternateName": ["OPC registration", "One Person Company incorporation", "Register OPC online", "OPC for NRIs"],
  "serviceType": "Incorporation of a One Person Company under the Companies Act, 2013",
  "description": "Incorporation of a One Person Company through SPICe+, with name approval, DSC, nominee consent, e-MoA and e-AoA, PAN and TAN, and post-incorporation compliance including INC-20A.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Solo founders and Indian citizens, including NRIs"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "OPC Plans", "itemListElement": [
    {"@type": "Offer", "name": "OPC Registration", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "OPC Complete", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "OPC with First-Year Compliance", "price": "16999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register a One Person Company", "totalTime": "P15D",
  "supply": [{"@type": "HowToSupply", "name": "Member's and nominee's PAN and ID"}, {"@type": "HowToSupply", "name": "Director's DSC"},
             {"@type": "HowToSupply", "name": "Registered office proof"}, {"@type": "HowToSupply", "name": "Nominee's consent"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Get the DSC", "text": "Get a Class 3 digital signature for the proposed director."},
   {"@type": "HowToStep", "position": 2, "name": "Reserve the name", "text": "Apply for the company name, ending with (OPC) Private Limited, through SPICe+."},
   {"@type": "HowToStep", "position": 3, "name": "File SPICe+", "text": "File SPICe+ with the e-MoA, e-AoA, nominee consent and registered office proof."},
   {"@type": "HowToStep", "position": 4, "name": "Get the certificate", "text": "Receive the certificate of incorporation with the CIN, PAN and TAN."},
   {"@type": "HowToStep", "position": 5, "name": "Start compliance", "text": "Open the bank account, appoint the first auditor within 30 days and file INC-20A within 180 days."}]},
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
    <meta property="og:title" content="One Person Company (OPC) Registration" />
    <meta property="og:description" content="Limited liability for a solo founder: SPICe+, nominee and post-incorporation compliance, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – One Person Company Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="One Person Company (OPC) Registration" />
    <meta name="twitter:description" content="Going solo with limited liability? Register your One Person Company." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "one-person-company-registration"')
assert 'service: "one-person-company-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="one-person-company-registration"')
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
