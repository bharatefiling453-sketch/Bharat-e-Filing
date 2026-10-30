# Builds trust-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/trust-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/trust-registration/"
TITLE = "Trust Registration | Bharat e-Filing"
DESC = "Register a charitable trust online: trust deed drafting, registration with the Sub-Registrar, PAN, and income tax registration, handled by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/trust-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "trust-registration"

FAQ = [
 ("What is a trust?", "A trust is an arrangement in which a person, called the settlor or author, hands property to trustees to hold and use for the benefit of others or for a purpose. A charitable trust is set up for public purposes such as relief of the poor, education, medical relief, preservation of the environment or advancement of any other object of general public utility."),
 ("Which law governs a trust?", "Private trusts are governed by the Indian Trusts Act, 1882. Public charitable and religious trusts are outside that Act and are governed by general law and, in some states, by a state public trusts law, such as the Maharashtra Public Trusts Act in Maharashtra, under which the trust registers with the Charity Commissioner."),
 ("Does a trust deed have to be registered?", "A trust of immovable property must be created by a registered written instrument under section 5 of the Indian Trusts Act, 1882, read with the Registration Act, 1908. Even where it is not compulsory, registering the deed with the Sub-Registrar is strongly advised, because banks, donors and the Income Tax Department expect a registered deed."),
 ("How many trustees are needed?", "There is no fixed minimum in central law, and a trust can have a single trustee. Most charitable trusts appoint at least two trustees so that decisions and bank operations are not held by one person. Some state laws and the trust deed itself can set their own rules."),
 ("Who can be a settlor or trustee?", "Any person competent to contract can create a trust or act as a trustee, and the settlor can also be a trustee. Trustees must accept the trust, and they must act in the interest of the trust and its objects."),
 ("What should the trust deed contain?", "The name and address of the trust, the settlor and trustees, the objects, the initial property, how trustees are appointed and removed, powers and duties of trustees, how accounts are kept, and what happens to the assets if the trust is dissolved, which for a charitable trust is a transfer to another charity with similar objects."),
 ("Can a charitable trust be revoked?", "A charitable trust deed should be irrevocable. A revocable transfer can lead to the income being taxed in the settlor's hands and can block income tax registration as a charity."),
 ("Is a trust exempt from income tax?", "Not automatically. A charitable trust must register with the Income Tax Department. For FY 2025-26 this is registration under section 12A or 12AB of the Income-tax Act, 1961. From tax year 2026-27 registration is under the Income-tax Act, 2025, as a registered non-profit organisation, with provisional registration for a new trust."),
 ("How much of its income must a trust spend?", "To keep its income exempt, a registered trust generally needs to apply at least 85% of its income to its objects in the year, or accumulate it within the rules. This 85% condition continues under the Income-tax Act, 2025 for registered non-profit organisations."),
 ("Can donors get a tax deduction?", "Only if the trust has approval for donations, known as 80G approval under the 1961 Act, with equivalent approval under the Income-tax Act, 2025. Donors then claim the deduction allowed by law."),
 ("Does a trust need to file returns?", "Yes. A registered trust files its income tax return every year, gets its accounts audited when the law requires it, and files the audit report before the due date. Trusts in states with a public trusts law may also file yearly accounts with the Charity Commissioner."),
 ("Can a trust receive CSR or foreign funds?", "To run CSR projects for companies, it registers with the MCA in Form CSR-1. To receive foreign contributions, it needs registration or prior permission under the Foreign Contribution (Regulation) Act, 2010."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-trust p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Trust Registration"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Trust Registration",
  "alternateName": ["Charitable trust registration", "NGO trust registration", "Trust deed registration", "Public trust registration"],
  "serviceType": "Drafting and registration of a charitable trust deed in India",
  "description": "Drafting of a charitable trust deed, registration with the Sub-Registrar, the trust's PAN, and guidance on income tax registration and donation approval.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "Audience", "audienceType": "Founders of charitable and religious trusts in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Trust Registration Plans", "itemListElement": [
    {"@type": "Offer", "name": "Trust Deed", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Trust Registration Complete", "price": "7999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Trust with Tax Registration", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register a charitable trust", "totalTime": "P15D",
  "supply": [{"@type": "HowToSupply", "name": "Settlor's and trustees' PAN and ID"}, {"@type": "HowToSupply", "name": "Address proof of the trust's office"},
             {"@type": "HowToSupply", "name": "Objects of the trust"}, {"@type": "HowToSupply", "name": "Two witnesses"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Plan the trust", "text": "Fix the name, objects, settlor, trustees and the initial property of the trust."},
   {"@type": "HowToStep", "position": 2, "name": "Draft the deed", "text": "Draft an irrevocable trust deed with clauses on trustees, powers, accounts and dissolution."},
   {"@type": "HowToStep", "position": 3, "name": "Register the deed", "text": "The settlor and witnesses sign the deed before the Sub-Registrar, who registers it."},
   {"@type": "HowToStep", "position": 4, "name": "PAN and bank account", "text": "Apply for the trust's PAN and open a bank account in the trust's name."},
   {"@type": "HowToStep", "position": 5, "name": "Register for tax", "text": "Apply for income tax registration as a charity and for donation approval."}]},
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
    <meta property="og:title" content="Trust Registration" />
    <meta property="og:description" content="Trust deed drafting and registration, PAN, and income tax registration for your charity, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Trust Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Trust Registration" />
    <meta name="twitter:description" content="Starting a charity? Register your trust the right way." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "trust-registration"')
assert 'service: "trust-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="trust-registration"')
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
