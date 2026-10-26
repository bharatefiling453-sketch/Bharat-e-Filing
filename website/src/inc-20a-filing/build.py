# Builds inc-20a-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/inc-20a-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/inc-20a-filing/"
TITLE = "INC-20A Filing – Commencement of Business | Bharat e-Filing"
DESC = "File INC-20A, the commencement of business declaration, within 180 days of incorporation. Proof of capital checked, certified and filed by CS and CA experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/inc-20a-filing-1200x630.jpg"
PUB = "2026-10-26"
SLUG = "inc-20a-filing"

FAQ = [
 ("What is Form INC-20A?", "INC-20A is the declaration for commencement of business under Section 10A of the Companies Act, 2013. A director declares that every subscriber to the memorandum has paid the value of the shares agreed to be taken, with proof of the payment attached."),
 ("Which companies must file INC-20A?", "Every company with a share capital incorporated on or after 2 November 2018 must file INC-20A, including private companies, one person companies and public companies. Companies without a share capital, such as many Section 8 companies, do not file it."),
 ("What is the due date for INC-20A?", "INC-20A must be filed within 180 days from the date of incorporation shown on the certificate of incorporation."),
 ("Can a company start business before filing INC-20A?", "No. Under Section 10A, a company with share capital cannot commence any business or exercise any borrowing powers until it files the declaration and has verified its registered office."),
 ("What is the penalty for not filing INC-20A?", "The company is liable to a penalty of ₹50,000, and every officer in default to ₹1,000 for each day of default, up to ₹1,00,000. Small companies, one person companies and startups may get lower penalties under Section 446B."),
 ("Can the company be struck off for not filing INC-20A?", "Yes. If the declaration is not filed within 180 days and the Registrar has reasonable cause to believe the company is not carrying on business, the Registrar may start action to strike off its name under Section 248."),
 ("What documents are needed for INC-20A?", "A bank statement or other proof showing that each subscriber has paid the subscription money into the company's bank account, the director's digital signature, and certification of the form by a practising chartered accountant, company secretary or cost accountant."),
 ("Who signs and certifies INC-20A?", "A director signs the declaration with a digital signature, and a practising professional certifies the form after checking the proof of payment."),
 ("Is the registered office verification part of commencement?", "Yes. Section 10A also requires the company to have verified its registered office. Where the address was given at incorporation in SPICe+, it is already on record; otherwise the company files INC-22 within 30 days of incorporation."),
 ("Can INC-20A be filed after 180 days?", "Yes, with higher additional fees that rise with the delay. The penalties under Section 10A may still apply, and the company or officers can apply for adjudication of the penalty."),
 ("What else is due soon after incorporation?", "The first board meeting within 30 days, appointment of the first auditor by the board within 30 days, and share certificates within two months of incorporation. The company also needs a bank account, PAN and TAN, and GST registration where required."),
 ("How does income tax apply to a new company?", "A new company files its income tax return in ITR-6 under the Income-tax Act, 2025, from tax year 2026-27, even for a short first year, and deducts tax at source where required once it starts business."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-inc20a p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "INC-20A Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "INC-20A Filing",
  "alternateName": ["Commencement of business filing", "Form INC-20A", "Declaration of commencement of business", "Section 10A filing"],
  "serviceType": "Filing of the declaration for commencement of business",
  "description": "Filing of Form INC-20A, the declaration for commencement of business under Section 10A of the Companies Act, 2013, within 180 days of incorporation, with proof of subscription money and professional certification.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Newly incorporated companies with share capital in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "INC-20A Plans", "itemListElement": [
    {"@type": "Offer", "name": "INC-20A Filing", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Commencement Pack", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Late Filing and Penalty", "price": "7999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file INC-20A", "totalTime": "P3D",
  "supply": [{"@type": "HowToSupply", "name": "Bank statement showing subscription money"}, {"@type": "HowToSupply", "name": "Director's digital signature"},
             {"@type": "HowToSupply", "name": "Certificate of incorporation"}, {"@type": "HowToSupply", "name": "Practising professional's certification"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Open the bank account", "text": "Open the company's current account using the certificate of incorporation, PAN and board resolution."},
   {"@type": "HowToStep", "position": 2, "name": "Collect subscription money", "text": "Each subscriber pays the value of the shares agreed in the memorandum into the company's account."},
   {"@type": "HowToStep", "position": 3, "name": "Prepare the proof", "text": "Download the bank statement showing every subscriber's payment."},
   {"@type": "HowToStep", "position": 4, "name": "Sign and certify", "text": "A director signs INC-20A with a digital signature and a practising professional certifies it."},
   {"@type": "HowToStep", "position": 5, "name": "File within 180 days", "text": "File INC-20A on the MCA portal within 180 days of incorporation and keep the SRN."}]},
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
    <meta property="og:title" content="INC-20A Filing – Commencement of Business" />
    <meta property="og:description" content="Declare commencement of business within 180 days. Proof of capital checked, certified and filed by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – INC-20A Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="INC-20A Filing – Commencement of Business" />
    <meta name="twitter:description" content="New company? File INC-20A within 180 days before you start business." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "inc-20a-filing"')
assert 'service: "inc-20a-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="inc-20a-filing"')
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
