# Builds gst-registration-amendment/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/gst-registration-amendment/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/gst-registration-amendment/"
TITLE = "GST Registration Amendment Online | Bharat e-Filing"
DESC = "Change your GST address, business name, partners, directors, email, mobile or bank details online. Core and non-core amendments filed by experts, CA-reviewed."
OG = "https://bharatefiling.com/wp-content/uploads/og/gst-registration-amendment-1200x630.jpg"
PUB = "2026-10-21"
SLUG = "gst-registration-amendment"

FAQ = [
 ("What is GST registration amendment?", "GST registration amendment is the process of updating the details you gave at registration, such as business address, name, partners or directors, contact details or bank account, under Section 28 of the CGST Act and Rule 19 of the CGST Rules. It is filed online on the GST portal in Form GST REG-14."),
 ("What are core and non-core fields in GST registration?", "Core fields are the name of the business, the principal place of business, additional places of business and the details of partners, directors, karta or managing committee members. Changing them needs the officer’s approval. All other details, such as email, mobile number, bank account, goods and services (HSN/SAC) and authorised signatories, are non-core and are updated without approval."),
 ("What is the time limit to apply for GST amendment?", "Under Rule 19(1) you must apply within 15 days of the change. For core fields, the proper officer has 15 working days from the application to approve it in Form REG-15 or raise a query; if the officer does not act in time, the amendment is treated as approved."),
 ("How long does GST amendment approval take?", "Non-core amendments take effect as soon as you file them. Core amendments are decided by the officer within 15 working days of the application. If the officer raises a query in Form REG-03, you reply in REG-04 within 7 working days and the officer then decides."),
 ("How do I change my business address in GST?", "Changing the principal or an additional place of business within the same state is a core amendment. You file REG-14 with proof of the new address, such as an electricity bill, property tax receipt or rent agreement, and a consent letter if the premises belong to someone else. Moving to another state needs a fresh registration in that state."),
 ("Can I change the business name in GST registration?", "Yes. A change in the name of the business, without a change in PAN, is a core amendment approved by the officer. Update the name with the Income Tax Department or the Registrar first, then file REG-14 with the supporting certificate or deed so the GST certificate shows the new name."),
 ("How do I add or remove a partner or director in GST?", "Adding or removing a partner, director, karta or managing committee member is a core amendment. You file REG-14 with the person’s PAN, Aadhaar and photograph and proof of appointment or exit, such as the amended partnership deed or the company’s filing with the Registrar."),
 ("How do I change the mobile number or email in GST registration?", "Mobile number and email of the authorised signatory are non-core fields. You update them through REG-14 and verify the new details with OTPs. If you no longer have access to the registered mobile or email, the change can be made through the jurisdictional officer."),
 ("When is a new GST registration needed instead of an amendment?", "A fresh registration is needed when the PAN changes, for example when a proprietorship becomes a partnership or a partnership becomes an LLP or company, and when the business moves to or starts operating from another state. An amendment cannot be used in these cases."),
 ("Will I get a new GST certificate after amendment?", "Yes, after a core amendment is approved, the updated registration certificate in Form REG-06 can be downloaded from the GST portal with the new details. Non-core changes update your profile on the portal without a new certificate."),
 ("What happens if I do not update my GST registration?", "Not updating your registration within the time limit is a contravention that can attract a general penalty of up to ₹25,000 each under the CGST and SGST Acts (Section 125). If the officer cannot find you at the registered address during verification, your registration can also be suspended or cancelled."),
 ("Does the Income-tax Act, 2025 affect GST amendments?", "No. GST amendments are unaffected. From 1 April 2026 the Income-tax Act, 2025 replaces the 1961 Act, so keep your name, address and PAN details consistent across the income-tax portal and the GST portal, because GST registration is linked to your PAN."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-amendment p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "GST Services", "item": "https://bharatefiling.com/product-category/gst/"},
   {"@type": "ListItem", "position": 3, "name": "GST Registration Amendment"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "GST Registration Amendment",
  "alternateName": ["GST amendment", "Change of address in GST", "Form GST REG-14", "Add partner or director in GST"],
  "serviceType": "Amendment of GST registration particulars in Form GST REG-14",
  "description": "CA-reviewed amendment of GST registration under Section 28 of the CGST Act and Rule 19, covering core fields (name, places of business, partners and directors) and non-core fields (contact details, bank, HSN/SAC), with replies to officer queries.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "GST-registered proprietors, partnerships, LLPs and companies whose details have changed"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "GST Amendment Plans", "itemListElement": [
    {"@type": "Offer", "name": "Non-core", "price": "999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Core", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Multiple changes", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to amend GST registration online", "totalTime": "P15D",
  "supply": [{"@type": "HowToSupply", "name": "Proof of the change (address proof, deed, appointment or name-change certificate)"}, {"@type": "HowToSupply", "name": "PAN, Aadhaar and photograph of any new partner or director"},
             {"@type": "HowToSupply", "name": "GST portal login"}, {"@type": "HowToSupply", "name": "DSC or EVC of the authorised signatory"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Open the amendment form", "text": "Log in to the GST portal and go to Services, Registration, Amendment of Registration Core Fields or Non-Core Fields."},
   {"@type": "HowToStep", "position": 2, "name": "Edit the changed fields", "text": "Open the relevant tab, edit the details, and enter the date of change and the reason for the amendment."},
   {"@type": "HowToStep", "position": 3, "name": "Upload supporting documents", "text": "Upload proof of the change, such as address proof, the amended deed, appointment documents or the new name certificate."},
   {"@type": "HowToStep", "position": 4, "name": "Verify and submit REG-14", "text": "Sign the application with DSC or EVC within 15 days of the change and note the Application Reference Number."},
   {"@type": "HowToStep", "position": 5, "name": "Track approval", "text": "Non-core changes apply at once. For core changes, answer any REG-03 query in REG-04 within 7 working days and download the amended certificate after approval in REG-15."}]},
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
    <title>{TITLE}</title>
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
    <meta property="og:title" content="GST Registration Amendment Online – Address, Name, Partners" />
    <meta property="og:description" content="Update your GST registration within 15 days of a change. Core and non-core amendments filed by experts, checked by a CA." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – GST Registration Amendment" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="GST Registration Amendment Online" />
    <meta name="twitter:description" content="Change address, name, partners, directors, email or bank in GST. Filed by experts, CA-reviewed." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "gst-registration-amendment"')
assert 'service: "gst-registration-amendment"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="gst-registration-amendment"')
globalnav = cut("    <!-- ================= GLOBAL NAV", "    <!-- ================= LOCAL NAV")
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
