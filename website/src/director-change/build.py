# Builds director-change/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/director-change/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/director-change/"
TITLE = "Director Change Online – DIR-12 Filing | Bharat e-Filing"
DESC = "Appoint, remove or record the resignation of a company director online: board resolutions, DIR-2 consent, DIR-12 within 30 days, DIR-11, GST and bank updates."
OG = "https://bharatefiling.com/wp-content/uploads/og/director-change-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "director-change"

FAQ = [
 ("How do I add a new director to a private limited company?", "Get the new director's consent in DIR-2 and declaration in DIR-8, make sure they hold an active DIN, and pass a board resolution appointing them as an additional director, or appoint them at a general meeting. The company then files DIR-12 with the Registrar within 30 days of the appointment."),
 ("How long can an additional director hold office?", "Under Section 161(1), an additional director appointed by the board holds office up to the next annual general meeting, or the last date on which it should have been held, whichever is earlier. To continue, the director must be regularised by the shareholders at a general meeting."),
 ("Which form is filed for a change in directors?", "DIR-12 is filed by the company within 30 days of any appointment, resignation, removal or change in designation of a director, with the consent, resolution or resignation letter attached."),
 ("How does a director resign?", "The director gives a written notice of resignation to the company under Section 168. The company notes it at the board meeting and files DIR-12 within 30 days. The resignation takes effect from the date the company receives the notice or the date mentioned in it, whichever is later."),
 ("What is DIR-11?", "DIR-11 is an optional form a resigning director may file with the Registrar within 30 days of resigning, giving the reasons. It is useful when the director wants an independent record of the resignation."),
 ("How can shareholders remove a director?", "Under Section 169, a director can be removed by an ordinary resolution at a general meeting. A special notice of the resolution must be given at least 14 days before the meeting, and the director has the right to be heard. DIR-12 is filed within 30 days of removal."),
 ("How many directors must a company have?", "Under Section 149, a private company needs at least two directors, a public company three and a one person company one, with a maximum of 15 unless more are approved by special resolution. At least one director must have stayed in India for 182 days or more in the financial year."),
 ("What if all the directors resign?", "Under Section 168(3), if all directors vacate office, the promoters, or failing them the Central Government, appoint the required number of directors, who hold office until directors are appointed at a general meeting."),
 ("Does the new director need a DIN?", "Yes. Every director of a company needs an active DIN. If the person does not have one, it is applied for before or along with the appointment, and an existing DIN must not be deactivated for missing KYC."),
 ("What is the penalty for filing DIR-12 late?", "DIR-12 filed after 30 days attracts additional fees that rise with the delay. Not filing at all can also lead to penalties for the company and its officers in default."),
 ("Does a director change need a GST update?", "Yes. Adding or removing a director responsible for the company's affairs is a core amendment in the GST registration, applied for within 15 days of the change and approved by the GST officer."),
 ("How is a designated partner changed in an LLP?", "The partners consent to the change as the LLP agreement requires, and the LLP files Form 4 within 30 days of the appointment or cessation. Form 3 is also filed if the LLP agreement changes."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-director-change p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Director Change"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Director Change",
  "alternateName": ["Appointment of director", "Resignation of director", "Removal of director", "DIR-12 filing"],
  "serviceType": "Change in the directors of a company filed with the Registrar of Companies",
  "description": "Appointment, resignation, removal and change in designation of company directors: consent and declarations, board and shareholder resolutions, special notice, DIR-12, DIR-11, LLP Form 4, and GST and bank updates.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Companies, OPCs and LLPs in India changing their directors or designated partners"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Director Change Plans", "itemListElement": [
    {"@type": "Offer", "name": "Director Resignation", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Director Appointment", "price": "2499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Director Removal", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to appoint a new director in a private limited company", "totalTime": "P7D",
  "supply": [{"@type": "HowToSupply", "name": "DIR-2 consent and DIR-8 declaration"}, {"@type": "HowToSupply", "name": "Active DIN of the new director"},
             {"@type": "HowToSupply", "name": "Board resolution"}, {"@type": "HowToSupply", "name": "Company DSC of a signing director"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check eligibility", "text": "Confirm the person is not disqualified under Section 164, holds an active DIN and that the board stays within the limits of Section 149."},
   {"@type": "HowToStep", "position": 2, "name": "Collect consent", "text": "Collect the consent to act in DIR-2 and the declaration of non-disqualification in DIR-8."},
   {"@type": "HowToStep", "position": 3, "name": "Pass the resolution", "text": "Pass a board resolution appointing an additional director, or a shareholders' resolution at a general meeting."},
   {"@type": "HowToStep", "position": 4, "name": "File DIR-12", "text": "File DIR-12 with the Registrar within 30 days of the appointment."},
   {"@type": "HowToStep", "position": 5, "name": "Update records", "text": "Update the register of directors, the GST registration, bank signatories and the director's disclosure of interest in MBP-1."}]},
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
    <meta property="og:title" content="Director Change – DIR-12 Filing" />
    <meta property="og:description" content="Appoint, remove or record a director's resignation, with resolutions, DIR-12 and GST updates handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Director Change" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Director Change – DIR-12 Filing" />
    <meta name="twitter:description" content="New director or a resignation? DIR-12 filed right, within 30 days." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "director-change"')
assert 'service: "director-change"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="director-change"')
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
