# Builds dormant-status-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/dormant-status-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/dormant-status-filing/"
TITLE = "Dormant Company Status – MSC-1 Filing | Bharat e-Filing"
DESC = "Apply for dormant company status under Section 455: eligibility check, special resolution, MSC-1, yearly MSC-3 return and MSC-4 to become active again."
OG = "https://bharatefiling.com/wp-content/uploads/og/dormant-status-filing-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "dormant-status-filing"

FAQ = [
 ("What is a dormant company?", "Under Section 455 of the Companies Act, 2013, a dormant company is one formed for a future project or to hold an asset or intellectual property with no significant accounting transaction, or an inactive company, that has obtained dormant status from the Registrar of Companies."),
 ("What is an inactive company?", "An inactive company is one that has not carried on any business or operation, or has made no significant accounting transaction, during the last two financial years, or has not filed its financial statements and annual returns during the last two financial years."),
 ("What is a significant accounting transaction?", "Any transaction other than payments to the Registrar, payments to fulfil the requirements of the Act or other laws, allotment of shares to fulfil legal requirements, and payments for maintaining the company's office and records."),
 ("How does a company apply for dormant status?", "It passes a special resolution, or obtains the consent of at least three-fourths of its shareholders in value, and files Form MSC-1 with the Registrar along with the supporting documents. The Registrar issues a certificate of dormant status in Form MSC-2."),
 ("Which companies cannot apply for dormant status?", "A company cannot apply if an inspection, inquiry or investigation has been ordered or is pending, if a prosecution is pending against it, if it has public deposits outstanding or is in default on them, if it has outstanding statutory dues or workmen's dues, if there is a dispute in management or ownership, or if its securities are listed. A company with an unsecured loan can apply with the lender's concurrence."),
 ("What must a dormant company file every year?", "A dormant company files a return of dormant company in Form MSC-3 within 30 days from the end of each financial year, that is by 30 April, along with the documents the rules require, and keeps the minimum number of directors."),
 ("How many board meetings must a dormant company hold?", "Under Section 173(5), a dormant company must hold at least one board meeting in each half of a calendar year, with a gap of at least 90 days between the two meetings."),
 ("How long can a company stay dormant?", "The Registrar can strike off the name of a company that remains dormant for five consecutive financial years. Before that, the company should decide whether to become active again or to close."),
 ("How does a dormant company become active again?", "It files Form MSC-4 with a return in Form MSC-3 for the relevant period, and the Registrar issues a certificate of active status in Form MSC-5. If the company does anything inconsistent with its dormant status, its directors must apply within seven days."),
 ("What are the benefits of dormant status?", "A dormant company has lighter compliance than an active company: fewer board meetings, a short annual return in MSC-3, and no cash flow statement, while keeping its name, CIN and assets intact for future use."),
 ("Is dormant status better than closing the company?", "Dormant status suits a company that may be used later, for a future project or to hold an asset. If there is no plan to use it, closing it through strike-off may cost less over time. We advise on the better route for your case."),
 ("Does a dormant company still file income tax returns?", "Yes. A dormant company keeps its PAN and must file its income tax return in ITR-6 every year under the Income-tax Act, 2025 from tax year 2026-27, even if it has no income."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-dormant p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Dormant Status Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Dormant Status Filing",
  "alternateName": ["Dormant company application", "Form MSC-1", "Return of dormant company MSC-3", "Dormant company reactivation"],
  "serviceType": "Application for dormant company status and its yearly compliance with the Registrar of Companies",
  "description": "Dormant status under Section 455: eligibility check, special resolution, Form MSC-1 and MSC-2 certificate, yearly MSC-3 return and board meetings, and MSC-4 application to regain active status.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Inactive companies and companies holding assets or future projects in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Dormant Status Plans", "itemListElement": [
    {"@type": "Offer", "name": "Dormant Annual Upkeep", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Dormant Status Application", "price": "7999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Reactivation", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to apply for dormant company status", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Special resolution or shareholders' consent"}, {"@type": "HowToSupply", "name": "Statement of affairs"},
             {"@type": "HowToSupply", "name": "Lender concurrence for any unsecured loan"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check eligibility", "text": "Confirm the company is inactive or holds an asset or future project, and that none of the conditions that bar an application apply."},
   {"@type": "HowToStep", "position": 2, "name": "Approve the move", "text": "Pass a special resolution, or obtain the consent of three-fourths of the shareholders in value."},
   {"@type": "HowToStep", "position": 3, "name": "File MSC-1", "text": "File Form MSC-1 with the Registrar with the statement of affairs and supporting documents."},
   {"@type": "HowToStep", "position": 4, "name": "Receive MSC-2", "text": "The Registrar issues a certificate of dormant status in Form MSC-2."},
   {"@type": "HowToStep", "position": 5, "name": "Keep up yearly compliance", "text": "File MSC-3 within 30 days of each year end, hold two board meetings a year and keep the minimum directors."}]},
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
    <meta property="og:title" content="Dormant Company Status – MSC-1" />
    <meta property="og:description" content="Park an inactive company the right way: eligibility, MSC-1, yearly MSC-3 and reactivation handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Dormant Status Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Dormant Company Status – MSC-1" />
    <meta name="twitter:description" content="Company not in use? Get dormant status and keep compliance light." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "dormant-status-filing"')
assert 'service: "dormant-status-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="dormant-status-filing"')
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
