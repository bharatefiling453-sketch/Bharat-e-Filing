# Builds proprietorship-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/proprietorship-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/proprietorship-registration/"
TITLE = "Proprietorship Registration Online | Bharat e-Filing"
DESC = "Start your sole proprietorship the right way: GST, Udyam and Shop Act in your business name, current account documents, and tax set up under the 2025 Act."
OG = "https://bharatefiling.com/wp-content/uploads/og/proprietorship-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "proprietorship-registration"

FAQ = [
 ("What is a sole proprietorship?", "A sole proprietorship is a business owned and run by one individual. It is not a separate legal entity from its owner, so the proprietor owns all the profits and is personally responsible for all the business's debts."),
 ("Is there a registration for a proprietorship itself?", "No single law registers a proprietorship. It is set up through registrations in the business name, such as GST, Udyam, Shop Act and a current bank account, using the proprietor's own PAN."),
 ("Does a proprietorship need its own PAN?", "No. A proprietorship uses the proprietor's personal PAN, and its income is taxed as the proprietor's income."),
 ("When is GST registration needed?", "When aggregate turnover crosses ₹40 lakh for suppliers of goods or ₹20 lakh for suppliers of services, with lower limits in some special category states. Registration is compulsory regardless of turnover in some cases, such as interstate supply of goods."),
 ("How do I open a current account for my proprietorship?", "Banks follow the RBI's KYC rules, which ask a proprietary concern for two documents as proof of business, such as a Udyam certificate, Shop Act certificate, GST certificate or the proprietor's income tax return showing business income. Banks can accept one in limited cases after verifying the business."),
 ("Should a proprietorship register on Udyam?", "Yes, if it qualifies as a micro, small or medium enterprise. Udyam Registration gives access to MSME benefits, including the 45-day payment protection for micro and small enterprises, and serves as business proof."),
 ("Is Shop Act registration needed?", "Shops, offices and other commercial establishments generally need to register or file an intimation under their state's Shops and Establishments Act, or under the OSH Code where the state accepts it. The rule depends on the state and number of workers."),
 ("How is a proprietorship taxed?", "Business income is added to the proprietor's other income and taxed at the rates that apply to individuals. From tax year 2026-27 this is under the Income-tax Act, 2025; earlier years follow the Income-tax Act, 1961."),
 ("What is presumptive taxation?", "Under section 58 of the Income-tax Act, 2025, which replaces sections 44AD and 44ADA, eligible small businesses can declare profit at 8% of turnover, or 6% of digital receipts, and eligible professionals at 50% of receipts, without maintaining detailed books."),
 ("Who can use presumptive taxation?", "Resident individuals with business turnover up to ₹2 crore, or ₹3 crore if cash receipts are within 5%, and professionals with receipts up to ₹50 lakh, or ₹75 lakh if cash receipts are within 5%."),
 ("When does a proprietorship need a tax audit?", "Under section 63 of the Income-tax Act, 2025, which replaces section 44AB, a business needs a tax audit if turnover exceeds ₹1 crore, or ₹10 crore if cash transactions are within 5%, and a profession if receipts exceed ₹50 lakh. Other conditions can also trigger an audit, so check with a CA."),
 ("Can a proprietorship be converted into a company later?", "Yes. A growing proprietorship can move its business into a private limited company or an LLP, and transfer its assets and liabilities, usually with professional help to manage the tax and registrations."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-proprietorship p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Proprietorship"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Proprietorship Registration",
  "alternateName": ["Sole proprietorship registration", "Start a proprietorship", "Proprietorship firm registration", "Proprietorship GST and Udyam"],
  "serviceType": "Setting up a sole proprietorship through business registrations",
  "description": "Setting up a sole proprietorship in India through GST, Udyam and Shop Act registrations and the documents banks need for a current account, with tax and compliance guidance under the Income-tax Act, 2025.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Individuals starting a business in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Proprietorship Plans", "itemListElement": [
    {"@type": "Offer", "name": "Proprietorship Starter", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Proprietorship Complete", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Proprietorship with First-Year Compliance", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to start a sole proprietorship in India", "totalTime": "P7D",
  "supply": [{"@type": "HowToSupply", "name": "Proprietor's PAN and Aadhaar"}, {"@type": "HowToSupply", "name": "Business address proof"},
             {"@type": "HowToSupply", "name": "Business name"}, {"@type": "HowToSupply", "name": "Photograph"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Choose a name", "text": "Pick a business name that doesn't infringe a registered trademark."},
   {"@type": "HowToStep", "position": 2, "name": "Get registrations", "text": "Register on Udyam and, where needed, under GST and your state's Shop Act, in the business name."},
   {"@type": "HowToStep", "position": 3, "name": "Open a current account", "text": "Give the bank two proofs of business, such as the Udyam, Shop Act or GST certificate."},
   {"@type": "HowToStep", "position": 4, "name": "Set up books", "text": "Keep accounts, or plan to use presumptive taxation if eligible."},
   {"@type": "HowToStep", "position": 5, "name": "Stay compliant", "text": "File GST returns if registered, pay advance tax and file the income tax return each year."}]},
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
    <meta property="og:title" content="Proprietorship Registration Online" />
    <meta property="og:description" content="GST, Udyam and Shop Act in your business name, current account documents and tax set-up, by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Proprietorship Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Proprietorship Registration Online" />
    <meta name="twitter:description" content="Starting on your own? Set up your proprietorship the right way." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "proprietorship-registration"')
assert 'service: "proprietorship-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="proprietorship-registration"')
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
