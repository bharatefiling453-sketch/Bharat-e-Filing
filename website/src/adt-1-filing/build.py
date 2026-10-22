# Builds adt-1-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/adt-1-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/adt-1-filing/"
TITLE = "ADT-1 Filing Online – Auditor Appointment | Bharat e-Filing"
DESC = "File ADT-1 for your company's auditor within 15 days: first auditor, five-year appointment at the AGM, casual vacancy, consent and eligibility certificate."
OG = "https://bharatefiling.com/wp-content/uploads/og/adt-1-filing-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "adt-1-filing"

FAQ = [
 ("What is ADT-1?", "ADT-1 is the form in which a company informs the Registrar of Companies about the appointment of its statutory auditor. It is filed by the company under Section 139 of the Companies Act, 2013 and Rule 4 of the Companies (Audit and Auditors) Rules, 2014."),
 ("When is ADT-1 due?", "ADT-1 must be filed within 15 days of the meeting at which the auditor is appointed. For an auditor appointed at an AGM held on 30 September, ADT-1 is due by 15 October."),
 ("How long is an auditor appointed for?", "At the first annual general meeting, the company appoints an auditor to hold office from the end of that meeting until the end of the sixth annual general meeting, a term of five years. Annual ratification by shareholders is no longer required since May 2018."),
 ("Who appoints the first auditor of a company?", "The board appoints the first auditor within 30 days of incorporation. If the board does not, it informs the members, who appoint the auditor at an extraordinary general meeting within 90 days. The first auditor holds office until the end of the first annual general meeting."),
 ("Is ADT-1 needed for the first auditor?", "The MCA form provides for reporting the first auditor, and filing it within 15 days of the board meeting is widely followed so the Registrar's record shows the auditor from the start. We recommend filing it."),
 ("What documents are attached to ADT-1?", "The resolution appointing the auditor, the auditor's written consent, the auditor's certificate that the appointment satisfies the conditions of Section 141, and a copy of the company's intimation of appointment to the auditor."),
 ("What is a casual vacancy in the office of auditor?", "A casual vacancy arises when the auditor's office falls vacant mid-term, for example on resignation. The board fills it within 30 days; if the vacancy arose from resignation, the appointment must also be approved by the members within three months. ADT-1 is filed for the new appointment."),
 ("What happens when an auditor resigns?", "The auditor files ADT-3 with the Registrar within 30 days of resigning, stating the reasons. The company then fills the casual vacancy and files ADT-1 for the new auditor."),
 ("Can a company remove its auditor before the term ends?", "Only with a special resolution of the members and prior approval of the Central Government, applied for in ADT-2 within 30 days of the board resolution, after giving the auditor a reasonable opportunity of being heard."),
 ("Which companies must rotate their auditors?", "Listed companies, unlisted public companies with paid-up capital of ₹10 crore or more, private companies with paid-up capital of ₹50 crore or more, and companies with public borrowings of ₹50 crore or more. An individual auditor can serve one term of five years and a firm two terms, followed by a five-year cooling-off period."),
 ("How many companies can one auditor audit?", "Under Section 141(3)(g), an auditor can hold audit appointments in up to 20 companies, not counting one person companies, dormant companies, small companies and private companies with paid-up capital below ₹100 crore."),
 ("Is the statutory auditor the same as the tax auditor?", "Not necessarily. The tax audit under the Income-tax Act, 2025 can be done by the statutory auditor or by another chartered accountant. ADT-1 relates only to the statutory auditor appointed under the Companies Act."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-adt1 p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "ADT-1 Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "ADT-1 Filing",
  "alternateName": ["Auditor appointment filing", "Form ADT-1", "Appointment of statutory auditor", "Casual vacancy of auditor"],
  "serviceType": "Filing of the appointment of a company's statutory auditor with the Registrar of Companies",
  "description": "ADT-1 filing for first auditors, five-year appointments at the AGM, reappointments and casual vacancies, with the auditor's consent and Section 141 certificate, resolutions and rotation checks.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Companies in India appointing or changing their statutory auditor"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "ADT-1 Plans", "itemListElement": [
    {"@type": "Offer", "name": "ADT-1 Filing", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Auditor Appointment Pack", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Auditor Change", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file ADT-1 for a company's auditor", "totalTime": "P15D",
  "supply": [{"@type": "HowToSupply", "name": "Auditor's written consent"}, {"@type": "HowToSupply", "name": "Section 141 eligibility certificate"},
             {"@type": "HowToSupply", "name": "Board or AGM resolution"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Get consent and certificate", "text": "Obtain the auditor's written consent and certificate that the appointment meets the conditions of Section 141."},
   {"@type": "HowToStep", "position": 2, "name": "Pass the resolution", "text": "Appoint the auditor by board resolution for a first auditor or casual vacancy, or by the members at the AGM for a five-year term."},
   {"@type": "HowToStep", "position": 3, "name": "Inform the auditor", "text": "Send the auditor a letter of appointment."},
   {"@type": "HowToStep", "position": 4, "name": "File ADT-1", "text": "File ADT-1 with the Registrar within 15 days of the meeting, with the resolution, consent, certificate and intimation attached."},
   {"@type": "HowToStep", "position": 5, "name": "Diary the term", "text": "Note when the term ends at the sixth AGM, and any rotation limits."}]},
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
    <meta property="og:title" content="ADT-1 Filing – Auditor Appointment" />
    <meta property="og:description" content="Appoint your company's auditor and file ADT-1 within 15 days, with consent, certificate and resolutions handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – ADT-1 Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="ADT-1 Filing – Auditor Appointment" />
    <meta name="twitter:description" content="Auditor appointed? ADT-1 filed right, within 15 days." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "adt-1-filing"')
assert 'service: "adt-1-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="adt-1-filing"')
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
