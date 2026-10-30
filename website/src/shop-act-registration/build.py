# Builds shop-act-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/shop-act-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/shop-act-registration/"
TITLE = "Shop Act Registration Online | Bharat e-Filing"
DESC = "Register your shop or office under your state's Shops and Establishments Act, or the OSH Code where accepted, with documents checked and filed by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/shop-act-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "shop-act-registration"

FAQ = [
 ("What is Shop Act registration?", "Shop Act registration is the registration of a shop, office or commercial establishment under the Shops and Establishments Act of the state where it operates. Each state has its own Act and rules, which govern registration, working hours, holidays and employment conditions."),
 ("Is there one Shop Act for all of India?", "No. Shops and establishments are regulated by state laws, so the forms, thresholds, deadlines and validity differ from state to state. A business with premises in several states follows each state's law."),
 ("How do the new Labour Codes affect Shop Act registration?", "The four Labour Codes came into force on 21 November 2025. The Occupational Safety, Health and Working Conditions Code, 2020 provides for registration of establishments with 10 or more workers, while state Shops and Establishments Acts continue to apply unless a state changes them."),
 ("Do I still need a separate Shop Act registration?", "It depends on your state. Some states have moved to accept registration under the OSH Code in place of separate Shop Act registration; for example, Maharashtra reportedly notified this in April 2026. Others still require registration under their own Shops and Establishments Act. We check your state's current rules before applying."),
 ("What did Maharashtra's 2017 Act require?", "Under the Maharashtra Shops and Establishments (Regulation of Employment and Conditions of Service) Act, 2017, establishments with 10 or more workers registered in Form A, and those with fewer than 10 workers filed a one-time intimation in Form F, within 60 days of starting business."),
 ("Who needs Shop Act registration?", "Most shops, offices, commercial establishments, restaurants, hotels and similar businesses, including those run from small premises, need to register or file an intimation as their state's law requires. Factories are generally covered by other laws."),
 ("What documents are needed?", "Typically the owner's identity and address proof and PAN, a photograph, proof of the business premises such as a rent agreement or electricity bill, the number of workers, and entity documents such as a partnership deed, LLP agreement or certificate of incorporation."),
 ("Why is the Shop Act certificate useful?", "It is official proof that your business exists at the premises. Banks commonly accept it for opening a current account, and it can serve as business proof for other registrations."),
 ("Does the registration need renewal?", "It depends on the state. Some states issue registrations valid for life, others for a fixed period that must be renewed. We confirm the validity for your state and remind you before any renewal is due."),
 ("What if my business details change?", "Changes such as a new address, owner, business name or number of workers usually have to be reported to the authority within the time set by your state's rules."),
 ("What are the penalties for not registering?", "Each state's Act sets its own penalties for running an establishment without the required registration or intimation. Registering on time avoids penalties and inspections."),
 ("How does income tax apply to my shop?", "Business income from the shop is taxed under your PAN. From tax year 2026-27, returns are filed under the Income-tax Act, 2025; returns for financial year 2025-26 and earlier are filed under the Income-tax Act, 1961."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-shopact p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Shop Act Registration"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Shop Act Registration",
  "alternateName": ["Shops and Establishments registration", "Gumasta licence", "Shop licence", "Shop Act licence online"],
  "serviceType": "Registration of shops and establishments under state law",
  "description": "Registration or intimation of shops, offices and commercial establishments under the state Shops and Establishments Act, or under the OSH Code where the state accepts it, with documents checked and the application filed.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Shops, offices and commercial establishments in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Shop Act Plans", "itemListElement": [
    {"@type": "Offer", "name": "Intimation", "price": "699", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Shop Act Registration", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Business Starter Pack", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to get Shop Act registration", "totalTime": "P7D",
  "supply": [{"@type": "HowToSupply", "name": "Owner's ID, address proof and PAN"}, {"@type": "HowToSupply", "name": "Proof of business premises"},
             {"@type": "HowToSupply", "name": "Photograph"}, {"@type": "HowToSupply", "name": "Number of workers"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check your state's rule", "text": "Find out whether your state needs Shop Act registration, an intimation or OSH Code registration, based on your number of workers."},
   {"@type": "HowToStep", "position": 2, "name": "Gather documents", "text": "Collect the owner's identity, address and PAN, premises proof, a photograph and entity documents."},
   {"@type": "HowToStep", "position": 3, "name": "Apply online", "text": "File the application or intimation on the state labour department portal."},
   {"@type": "HowToStep", "position": 4, "name": "Answer queries", "text": "Reply to any query from the authority."},
   {"@type": "HowToStep", "position": 5, "name": "Display the certificate", "text": "Download the certificate or acknowledgement and display it at the premises."}]},
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
    <meta property="og:title" content="Shop Act Registration Online" />
    <meta property="og:description" content="Shop or office? Register under your state's Shops and Establishments Act, with expert help." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Shop Act Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Shop Act Registration Online" />
    <meta name="twitter:description" content="Opening a shop or office? Get your Shop Act registration sorted." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "shop-act-registration"')
assert 'service: "shop-act-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="shop-act-registration"')
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
