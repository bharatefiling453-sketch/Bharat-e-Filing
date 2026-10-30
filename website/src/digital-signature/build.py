# Builds digital-signature/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/digital-signature/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/digital-signature/"
TITLE = "Digital Signature (Class 3 DSC) Online | Bharat e-Filing"
DESC = "Get a Class 3 digital signature certificate online for MCA, income tax, GST and e-tenders, with eKYC, video verification and a USB token, guided by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/digital-signature-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "digital-signature"

FAQ = [
 ("What is a digital signature certificate (DSC)?", "A DSC is an electronic certificate issued by a licensed Certifying Authority under the Information Technology Act, 2000. It proves your identity online and lets you sign electronic documents and forms, such as MCA filings, income tax returns and GST returns, with the same legal effect as a handwritten signature."),
 ("Which class of DSC should I buy?", "Class 3. The Controller of Certifying Authorities directed Certifying Authorities to stop issuing Class 2 certificates from 1 January 2021, so Class 3 is the class issued now for individuals and organisations."),
 ("Who issues a DSC in India?", "Only Certifying Authorities licensed by the Controller of Certifying Authorities under the Information Technology Act, 2000 can issue a DSC. We apply on your behalf through a licensed Certifying Authority."),
 ("How is my identity verified?", "Through one of the methods allowed by the Controller of Certifying Authorities, such as Aadhaar eKYC with OTP and video verification, Aadhaar biometric eKYC, or document-based verification. The Certifying Authority confirms your mobile number and email during the process."),
 ("Do I need a DSC for MCA filings?", "Yes. Company and LLP e-forms on the MCA portal are signed with the DSC of an authorised director, designated partner or professional, and directors also use it for DIR-3 KYC. The DSC must be registered on the MCA portal before use."),
 ("Do I need a DSC to file my income tax return?", "Companies must verify their income tax return with a DSC. Most other taxpayers can e-verify with Aadhaar OTP or an electronic verification code, though a registered DSC can also be used."),
 ("Do I need a DSC for GST?", "Companies must sign their GST registration application and returns with a DSC under Rule 26 of the CGST Rules, 2017. Other registered persons can usually use an electronic verification code instead."),
 ("What are signature, encryption and combo DSCs?", "A signature DSC is used to sign documents and filings. An encryption DSC is used to encrypt documents, mainly for e-tendering. A combo DSC has both, and is often needed for government e-tenders."),
 ("How long is a DSC valid?", "A DSC is valid for the period shown on the certificate, usually one or two years from issue. After that it must be renewed by applying for a fresh certificate."),
 ("What is a USB token?", "The DSC is stored on a secure USB crypto token protected by a PIN. You plug in the token to sign. Keep it safe and never share the PIN, because anyone with both can sign as you."),
 ("Can I use one DSC on several portals?", "Yes. The same personal DSC can be registered and used on the MCA, income tax and GST portals, as long as the name and PAN details match each portal's records."),
 ("How does the new Income-tax Act affect DSC use?", "The Income-tax Act, 2025 applies from tax year 2026-27. Returns for financial year 2025-26 and earlier are still filed under the Income-tax Act, 1961. Companies continue to sign their returns with a DSC on the e-filing portal."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-dsc p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Digital Signature"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Digital Signature Certificate",
  "alternateName": ["Class 3 DSC", "DSC online", "Digital signature for MCA, GST and income tax", "DSC renewal"],
  "serviceType": "Application for a Class 3 digital signature certificate",
  "description": "Class 3 digital signature certificates for individuals, directors and organisations, applied through a licensed Certifying Authority with online identity verification, on a secure USB token, for MCA, income tax, GST and e-tender use.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "Audience", "audienceType": "Individuals, directors, professionals and organisations in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "DSC Plans", "itemListElement": [
    {"@type": "Offer", "name": "Class 3 Signature – 1 year", "price": "999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Class 3 Signature – 2 years", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Class 3 Combo or Organisation – 2 years", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to get a Class 3 DSC online", "totalTime": "P1D",
  "supply": [{"@type": "HowToSupply", "name": "PAN"}, {"@type": "HowToSupply", "name": "Aadhaar linked to your mobile"},
             {"@type": "HowToSupply", "name": "Email address"}, {"@type": "HowToSupply", "name": "Phone or laptop with a camera"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Choose the DSC", "text": "Pick the class, type and validity, and whether it is for an individual or an organisation."},
   {"@type": "HowToStep", "position": 2, "name": "Share your details", "text": "Provide your PAN, Aadhaar-linked mobile number and email address."},
   {"@type": "HowToStep", "position": 3, "name": "Verify your identity", "text": "Complete eKYC and video verification as required by the Certifying Authority."},
   {"@type": "HowToStep", "position": 4, "name": "Certificate issued", "text": "The Certifying Authority approves the application and issues the certificate."},
   {"@type": "HowToStep", "position": 5, "name": "Download to the token", "text": "Download the certificate to your USB token and register it on the portals you use."}]},
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
    <meta property="og:title" content="Digital Signature Certificate – Class 3 DSC" />
    <meta property="og:description" content="Class 3 DSC for MCA, income tax, GST and e-tenders, with online verification and a USB token." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Digital Signature Certificate" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Digital Signature Certificate – Class 3 DSC" />
    <meta name="twitter:description" content="Need a DSC? Get a Class 3 certificate online, with expert help." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "digital-signature"')
assert 'service: "digital-signature"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="digital-signature"')
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
