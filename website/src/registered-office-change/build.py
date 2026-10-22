# Builds registered-office-change/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/registered-office-change/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/registered-office-change/"
TITLE = "Registered Office Change Online – INC-22 | Bharat e-Filing"
DESC = "Shift your company or LLP registered office: same city, same state or another state. Resolutions, INC-22, MGT-14, INC-23, LLP Form 15 and GST updates."
OG = "https://bharatefiling.com/wp-content/uploads/og/registered-office-change-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "registered-office-change"

FAQ = [
 ("How do I change the registered office of a company within the same city?", "If the new address is within the local limits of the same city, town or village, the board passes a resolution approving the new address and the company files INC-22 with the Registrar within 30 days of the change, with proof of the new office."),
 ("What if the registered office moves to another city in the same state?", "A move outside the local limits of the city needs a special resolution of the shareholders, filed in MGT-14 within 30 days, and INC-22 within 30 days of the change. If the new place falls under a different Registrar of Companies in the same state, the change must also be confirmed by the Regional Director on an application in INC-23."),
 ("How do I shift a registered office from one state to another?", "Pass a special resolution to alter the memorandum, advertise the proposal in Form INC-26 in an English and a vernacular newspaper, notify creditors, debenture holders and the State Government, and apply to the Regional Director in INC-23. After the order, file it with the Registrar in INC-28 within 30 days, and file INC-22 for the new address."),
 ("How long does a state-to-state shift take?", "It usually takes two to three months. The newspaper notice, objections from creditors or others, and the Regional Director's review set the pace. Under Section 13(4), the Central Government is to decide the application within 60 days."),
 ("Which form is filed for a change of registered office?", "INC-22 is filed for every change of registered office address, within 30 days of the change. MGT-14 is filed for the special resolution where one is needed, INC-23 for Regional Director approval, and INC-28 to file the Regional Director's order."),
 ("What documents are needed for INC-22?", "Proof of the new address, such as a registered title document or a notarised rent agreement with a recent rent receipt, a no-objection certificate from the owner, and a utility bill not older than two months, along with the board or special resolution."),
 ("What is the penalty for not filing INC-22 on time?", "Under Section 12(8) of the Companies Act, the company and every officer in default can face a penalty of ₹1,000 for each day the default continues, up to ₹1 lakh, in addition to additional fees for late filing."),
 ("When can a company not shift its registered office to another state?", "Under Rule 30, the shift is not allowed if an inquiry, inspection or investigation has been started against the company, or a prosecution under the Companies Act is pending against it. Objections from creditors or employees must also be settled."),
 ("How does an LLP change its registered office?", "With the consent of the partners as required by the LLP agreement, the LLP files Form 15 with the Registrar within 30 days. For a move to another state, the LLP first publishes a notice in newspapers and obtains the consent of its secured creditors. Form 3 is filed if the LLP agreement changes."),
 ("Does a registered office change affect GST?", "Within the same state, the GSTIN stays the same and the principal place of business is updated through a core amendment within 15 days of the change. GST registration is state-wise, so moving to another state needs a new GST registration in that state."),
 ("Does the PAN or CIN change when the registered office moves?", "The PAN stays the same; only the address on record is updated. The CIN includes a state code, so after a state-to-state shift the company gets a new CIN reflecting the new state, while remaining the same company."),
 ("Must the new address be displayed?", "Yes. Under Section 12, the company must paint or affix its name and registered office address outside every office, and print the registered office address, CIN, phone, email and website on its letterheads, invoices and official documents."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-office-change p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Registered Office Change"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Registered Office Change",
  "alternateName": ["Change of registered office address", "INC-22 filing", "Shifting registered office to another state", "LLP Form 15"],
  "serviceType": "Change of registered office of a company or LLP with the Registrar of Companies",
  "description": "End-to-end change of registered office for private limited companies, OPCs and LLPs: within the same city, within the same state, or from one state to another, with resolutions, INC-22, MGT-14, INC-23, INC-26, INC-28 or LLP Form 15, and PAN and GST updates.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Companies, OPCs and LLPs in India moving their registered office"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Registered Office Change Plans", "itemListElement": [
    {"@type": "Offer", "name": "Same City Shift", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Same State Shift", "price": "7999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "State to State Shift", "price": "24999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to change the registered office of a company", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Rent agreement or title document"}, {"@type": "HowToSupply", "name": "No-objection certificate from the owner"},
             {"@type": "HowToSupply", "name": "Utility bill not older than two months"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Find the route", "text": "Check whether the move is within the same city, to another city in the same state, to another Registrar's area, or to another state."},
   {"@type": "HowToStep", "position": 2, "name": "Board approval", "text": "Hold a board meeting to approve the new address, and call a general meeting if a special resolution is needed."},
   {"@type": "HowToStep", "position": 3, "name": "Special resolution and approvals", "text": "For moves outside the city, pass a special resolution and file MGT-14 within 30 days; get Regional Director approval in INC-23 where required."},
   {"@type": "HowToStep", "position": 4, "name": "File INC-22", "text": "File INC-22 with proof of the new office within 30 days of the change, and INC-28 for a Regional Director order."},
   {"@type": "HowToStep", "position": 5, "name": "Update records", "text": "Update the GST registration, PAN address, bank, licences, signboard and stationery with the new address."}]},
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
    <meta property="og:title" content="Registered Office Change – INC-22" />
    <meta property="og:description" content="Moving office? Shift your company or LLP registered office within the city, state or to another state, with every filing handled." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Registered Office Change" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Registered Office Change – INC-22" />
    <meta name="twitter:description" content="Moving office? Shift your registered office the right way, with INC-22 and GST updated." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "registered-office-change"')
assert 'service: "registered-office-change"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="registered-office-change"')
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
