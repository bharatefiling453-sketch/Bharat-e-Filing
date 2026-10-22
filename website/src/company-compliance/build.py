# Builds company-compliance/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/company-compliance/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/company-compliance/"
TITLE = "Company Annual Compliance Online | Bharat e-Filing"
DESC = "Annual ROC compliance for private limited companies and OPCs: board meetings, AGM, AOC-4, MGT-7, ADT-1, DPT-3, MSME-1 and DIR-3 KYC handled by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/company-compliance-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "company-compliance"

FAQ = [
 ("What is annual compliance for a private limited company?", "Annual compliance is the set of filings and meetings every company must complete each year under the Companies Act, 2013 and tax laws: board meetings, the annual general meeting, financial statements in AOC-4, the annual return in MGT-7 or MGT-7A, auditor appointment, director disclosures, and income tax, TDS and GST returns."),
 ("What are the due dates for AOC-4 and MGT-7?", "The AGM must be held within six months of the end of the financial year, by 30 September. AOC-4 is due within 30 days of the AGM and MGT-7 or MGT-7A within 60 days of the AGM. For an AGM on 30 September 2026, AOC-4 is due by 30 October 2026 and MGT-7 by 29 November 2026."),
 ("What is the penalty for late AOC-4 or MGT-7?", "Each form filed late attracts an additional fee of ₹100 a day with no upper limit, plus penalties on the company and officers in default under Sections 92 and 137. Not filing for two consecutive years can lead to the company being struck off under Section 248."),
 ("How many board meetings must a company hold?", "A company must hold its first board meeting within 30 days of incorporation and at least four board meetings a year, with no more than 120 days between two meetings. One person companies, small companies and dormant companies need at least one meeting in each half of the calendar year, at least 90 days apart."),
 ("Does a one person company need to hold an AGM?", "No. A one person company is exempt from holding an annual general meeting. It must still file its financial statements in AOC-4 within 180 days of the end of the financial year and its annual return in MGT-7A."),
 ("What is DIR-3 KYC and how often is it filed?", "DIR-3 KYC is the KYC of every person holding a Director Identification Number. From 31 March 2026, it is filed once every three financial years by 30 June, instead of every year. Changes in mobile number, email or address must be updated within 30 days."),
 ("What is Form DPT-3?", "DPT-3 is an annual return of deposits and of outstanding money received that is not treated as a deposit, such as loans from directors. Every company other than a government company files it by 30 June for the year ended 31 March."),
 ("What is Form MSME-1?", "MSME-1 is a half-yearly return filed by companies that owe money to micro or small enterprises for more than 45 days. It is due by 30 April for October to March and by 31 October for April to September."),
 ("What is a small company and what relief does it get?", "From 1 December 2025, a private company with paid-up capital up to ₹10 crore and turnover up to ₹100 crore is a small company, unless it is a holding or subsidiary company, a Section 8 company or governed by a special Act. Small companies hold fewer board meetings, file an abridged annual return and face lower penalties."),
 ("When must the first auditor be appointed?", "The board must appoint the first auditor within 30 days of incorporation. At the first AGM, the shareholders appoint an auditor for five years, and the company files Form ADT-1 within 15 days of that appointment."),
 ("What tax compliances does a company have?", "A company files its income tax return in ITR-6, gets a tax audit where required, pays advance tax in four instalments, deducts and deposits TDS and files quarterly TDS returns, and, if registered, files GST returns. For FY 2025-26, ITR-6 is due by 21 November 2026."),
 ("Does the Income-tax Act, 2025 change company compliance?", "ROC compliance under the Companies Act is unchanged. For tax, the Income-tax Act, 2025 applies from tax year 2026-27, so the company's tax filings for that year onwards follow the new Act's section numbers."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-compliance p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Company Compliance"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Company Annual Compliance",
  "alternateName": ["ROC annual filing", "Private limited company compliance", "AOC-4 and MGT-7 filing"],
  "serviceType": "Annual ROC and tax compliance for private limited companies and one person companies",
  "description": "Annual compliance for private limited companies and OPCs under the Companies Act, 2013: board meetings and minutes, AGM, AOC-4, MGT-7 or MGT-7A, ADT-1, DPT-3, MSME-1, DIR-3 KYC and director disclosures, with ITR-6, TDS and GST coordination.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Private limited companies, one person companies and startups in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Company Compliance Plans", "itemListElement": [
    {"@type": "Offer", "name": "OPC & Small Company", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Private Limited Annual Compliance", "price": "19999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Complete Compliance with Accounts & Tax", "price": "39999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to complete annual compliance for a private limited company", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Audited financial statements and auditor's report"}, {"@type": "HowToSupply", "name": "Board's report and notice of AGM"},
             {"@type": "HowToSupply", "name": "Shareholding and director details"}, {"@type": "HowToSupply", "name": "DSC of a director"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Hold board meetings", "text": "Hold at least four board meetings a year, or two for small companies and OPCs, and approve the accounts and board's report."},
   {"@type": "HowToStep", "position": 2, "name": "Complete the audit", "text": "Get the statutory audit done and the financial statements signed."},
   {"@type": "HowToStep", "position": 3, "name": "Hold the AGM", "text": "Hold the AGM by 30 September to adopt the accounts and appoint or ratify the auditor."},
   {"@type": "HowToStep", "position": 4, "name": "File with the ROC", "text": "File AOC-4 within 30 days and MGT-7 or MGT-7A within 60 days of the AGM, and ADT-1 within 15 days where an auditor is appointed."},
   {"@type": "HowToStep", "position": 5, "name": "Complete event and tax filings", "text": "File DPT-3, MSME-1 and DIR-3 KYC when due, and the company's ITR-6, TDS and GST returns."}]},
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
    <meta property="og:title" content="Company Annual Compliance Online" />
    <meta property="og:description" content="AGM, AOC-4, MGT-7, ADT-1, DPT-3, MSME-1 and DIR-3 KYC for your company, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Company Compliance" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Company Annual Compliance Online" />
    <meta name="twitter:description" content="AOC-4 due 30 October, MGT-7 by 29 November. Avoid ₹100 a day: let experts file it." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "company-compliance"')
assert 'service: "company-compliance"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="company-compliance"')
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
