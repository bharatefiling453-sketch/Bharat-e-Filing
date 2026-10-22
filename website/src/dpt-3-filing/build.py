# Builds dpt-3-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/dpt-3-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/dpt-3-filing/"
TITLE = "DPT-3 Filing Online – Return of Deposits | Bharat e-Filing"
DESC = "File DPT-3 by 30 June: report deposits and exempted loans from directors, relatives and companies as on 31 March, with every receipt classified by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/dpt-3-filing-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "dpt-3-filing"

FAQ = [
 ("What is DPT-3?", "DPT-3 is the annual return in which a company reports to the Registrar the deposits it holds and the money it has received that is not treated as a deposit, such as loans from directors or other companies. It is filed under Rule 16 of the Companies (Acceptance of Deposits) Rules, 2014."),
 ("What is the due date for DPT-3?", "DPT-3 is filed every year by 30 June, with figures as on 31 March of that year. For the financial year 2026-27, the return as on 31 March 2027 is due by 30 June 2027."),
 ("Which companies must file DPT-3?", "Every company that has outstanding deposits, or outstanding money received that is not treated as a deposit, as on 31 March must file it. Government companies, banks, NBFCs and housing finance companies are outside these rules."),
 ("Does a company with no loans need to file DPT-3?", "If the company has no deposits and no outstanding receipts that fall within the exempted categories as on 31 March, there is nothing to report and DPT-3 is generally not filed. We confirm this from your balance sheet."),
 ("Are loans from directors deposits?", "No, if the director gives a written declaration at the time of giving the loan that the money is not out of borrowed funds. The amount is then exempted, but it is still reported in DPT-3."),
 ("Are loans from relatives of directors deposits?", "For a private company, money received from a relative of a director is exempted, provided the relative declares that it is not given out of borrowed funds. It is reported in DPT-3."),
 ("When does a customer advance become a deposit?", "An advance for the supply of goods or services is exempted only if it is adjusted against the supply within 365 days. If it is not adjusted within that time, it is treated as a deposit."),
 ("When does share application money become a deposit?", "If shares are not allotted within 60 days of receiving the application money, and the money is not refunded within 15 days after that, the amount is treated as a deposit."),
 ("Does DPT-3 need an auditor's certificate?", "A return of deposits must contain information duly audited by the company's auditor, so an auditor's certificate is attached where the company holds deposits. For exempted transactions alone, practice varies; we coordinate the certificate with your auditor where required."),
 ("Can a private company accept deposits?", "A private company can accept deposits from its members within the limits and conditions of Section 73 of the Companies Act and the Deposit Rules. Deposits from the public are not allowed for private companies."),
 ("What is the penalty for not filing DPT-3?", "Late filing attracts additional fees that rise with the delay. Under Rule 21 of the Deposit Rules, contraventions can also lead to penalties for the company and its officers in default."),
 ("Can loans to a company be taken in cash?", "Under the Income-tax Act, 2025, loans and deposits of ₹20,000 or more should not be taken or repaid in cash; the penalty can equal the amount. Use banking channels for every loan you report in DPT-3."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-dpt3 p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "DPT-3 Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "DPT-3 Filing",
  "alternateName": ["Return of deposits", "Form DPT-3", "Return of money not considered as deposits"],
  "serviceType": "Annual return of deposits and exempted receipts filed with the Registrar of Companies",
  "description": "DPT-3 filing by 30 June with figures as on 31 March: classification of loans from directors, relatives, other companies and banks, customer advances and share application money, director declarations and auditor certificate coordination.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Private and public companies in India with loans, advances or deposits"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "DPT-3 Plans", "itemListElement": [
    {"@type": "Offer", "name": "DPT-3 Filing", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "DPT-3 + Loan Review", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Deposit Return", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file DPT-3", "totalTime": "P7D",
  "supply": [{"@type": "HowToSupply", "name": "Balance sheet as on 31 March"}, {"@type": "HowToSupply", "name": "Lender-wise list of loans and advances"},
             {"@type": "HowToSupply", "name": "Director and relative declarations"}, {"@type": "HowToSupply", "name": "Auditor's certificate, where required"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "List every receipt", "text": "List all loans, advances and other money outstanding on 31 March, lender by lender."},
   {"@type": "HowToStep", "position": 2, "name": "Classify", "text": "Classify each item as a deposit or as an exempted receipt under Rule 2(1)(c), such as loans from directors, relatives, companies or banks."},
   {"@type": "HowToStep", "position": 3, "name": "Collect declarations", "text": "Collect the declarations from directors and relatives that the money is not from borrowed funds."},
   {"@type": "HowToStep", "position": 4, "name": "Auditor's certificate", "text": "Get the auditor's certificate where the company holds deposits."},
   {"@type": "HowToStep", "position": 5, "name": "File by 30 June", "text": "File DPT-3 with the Registrar by 30 June, signed with a director's DSC."}]},
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
    <meta property="og:title" content="DPT-3 Filing – Return of Deposits" />
    <meta property="og:description" content="Report your company's deposits and exempted loans in DPT-3 by 30 June, with every receipt classified by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – DPT-3 Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="DPT-3 Filing – Return of Deposits" />
    <meta name="twitter:description" content="Loans from directors or other companies? DPT-3 filed right, by 30 June." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "dpt-3-filing"')
assert 'service: "dpt-3-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="dpt-3-filing"')
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
