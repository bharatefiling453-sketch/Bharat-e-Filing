# Builds partnership-firm-registration/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/partnership-firm-registration/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/partnership-firm-registration/"
TITLE = "Partnership Firm Registration Online | Bharat e-Filing"
DESC = "Start a partnership firm the right way: deed drafted, firm PAN, registration with the Registrar of Firms, and tax set up under the Income-tax Act, 2025."
OG = "https://bharatefiling.com/wp-content/uploads/og/partnership-firm-registration-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "partnership-firm-registration"

FAQ = [
 ("What is a partnership firm?", "Under section 4 of the Indian Partnership Act, 1932, a partnership is the relation between persons who have agreed to share the profits of a business carried on by all or any of them acting for all. The persons are partners, and together they are the firm."),
 ("How many partners can a firm have?", "At least two. The maximum is 50, under section 464 of the Companies Act, 2013 read with rule 10 of the Companies (Miscellaneous) Rules, 2014."),
 ("Is registration of a partnership firm compulsory?", "Under the Indian Partnership Act, registration is optional in most states and can be done at any time, though some states have amended the Act for their firms. Registering is strongly advised because of the disabilities an unregistered firm faces under section 69."),
 ("What happens if a firm isn't registered?", "Under section 69, an unregistered firm cannot sue a third party to enforce a right arising from a contract, and a partner cannot sue the firm or other partners to enforce rights under the partnership. The firm can still be sued by others."),
 ("How is a firm registered?", "The partners file a statement under section 58 with the Registrar of Firms of the state where the firm's place of business is, with the partnership deed, address proof and prescribed details, signed by all partners. Once the Registrar is satisfied, the firm is entered in the Register of Firms."),
 ("What should a partnership deed contain?", "The firm name and business, partners' names and addresses, capital contributions, profit-sharing ratio, interest on capital, remuneration to working partners, duties, admission and retirement of partners, and how disputes and dissolution are handled."),
 ("Does a partnership firm need its own PAN?", "Yes. A firm is a separate taxpayer for income tax and needs its own PAN, which is also used for its bank account and GST registration."),
 ("How is a partnership firm taxed?", "A firm is taxed on its own income at a flat rate, currently 30%, plus surcharge and cess where applicable. From tax year 2026-27 this is under the Income-tax Act, 2025; earlier years follow the Income-tax Act, 1961."),
 ("Can partners be paid interest and salary?", "Yes, if the deed authorises it. Interest on capital up to 12% simple a year and remuneration to working partners within limits based on book profit are deductible for the firm, and taxable for the partner as business income."),
 ("Is TDS deducted on payments to partners?", "Yes. From 1 April 2025, a firm deducts tax at 10% on salary, remuneration, commission, bonus or interest paid to a partner when the total exceeds ₹20,000 in the year. The rule was section 194T of the 1961 Act and is carried into the Income-tax Act, 2025."),
 ("Is a partner's share of profit taxed again?", "No. A partner's share in the firm's profit, which has already been taxed in the firm's hands, is not taxed again in the partner's hands."),
 ("What are the partners' liabilities?", "Partners are jointly and severally liable for the firm's debts, so each partner's personal assets can be used to pay them. Partners who want limited liability often choose an LLP instead."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-partnership p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Partnership Firm"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Partnership Firm Registration",
  "alternateName": ["Partnership registration", "Partnership deed drafting", "Registrar of Firms registration", "Start a partnership firm"],
  "serviceType": "Partnership deed and registration of a firm under the Indian Partnership Act, 1932",
  "description": "Drafting of the partnership deed, firm PAN and registration with the Registrar of Firms under section 58 of the Indian Partnership Act, 1932, with tax set-up under the Income-tax Act, 2025.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "People starting a business together in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Partnership Plans", "itemListElement": [
    {"@type": "Offer", "name": "Partnership Deed", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Partnership Registration", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Registration with First-Year Compliance", "price": "11999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to register a partnership firm", "totalTime": "P21D",
  "supply": [{"@type": "HowToSupply", "name": "Partnership deed"}, {"@type": "HowToSupply", "name": "Partners' PAN and ID"},
             {"@type": "HowToSupply", "name": "Proof of the firm's place of business"}, {"@type": "HowToSupply", "name": "Statement in the state's prescribed form"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Agree the terms", "text": "Agree the firm name, capital, profit-sharing ratio, interest, remuneration and exit terms."},
   {"@type": "HowToStep", "position": 2, "name": "Execute the deed", "text": "Draft the partnership deed, sign it and get it stamped as your state requires."},
   {"@type": "HowToStep", "position": 3, "name": "Get the firm PAN", "text": "Apply for the firm's PAN using the deed."},
   {"@type": "HowToStep", "position": 4, "name": "Register with the Registrar of Firms", "text": "File the section 58 statement with the deed and documents, signed by all partners."},
   {"@type": "HowToStep", "position": 5, "name": "Bank, GST and compliance", "text": "Open the firm's current account, register for GST if needed, and set up books and tax."}]},
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
    <meta property="og:title" content="Partnership Firm Registration Online" />
    <meta property="og:description" content="Partnership deed, firm PAN and Registrar of Firms registration, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Partnership Firm Registration" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Partnership Firm Registration Online" />
    <meta name="twitter:description" content="Starting a business together? Set up your partnership firm properly." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "partnership-firm-registration"')
assert 'service: "partnership-firm-registration"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="partnership-firm-registration"')
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
