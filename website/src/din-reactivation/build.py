# Builds din-reactivation/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/din-reactivation/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/din-reactivation/"
TITLE = "DIN Reactivation Online – Deactivated DIN | Bharat e-Filing"
DESC = "Reactivate a deactivated DIN online: DIR-3 KYC Web with the ₹5,000 late fee, PAN and DSC checks, plus help with Section 164(2) disqualified DINs."
OG = "https://bharatefiling.com/wp-content/uploads/og/din-reactivation-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "din-reactivation"

FAQ = [
 ("Why was my DIN deactivated?", "The most common reason is not filing DIR-3 KYC by its due date. The MCA record then shows the DIN as deactivated due to non-filing of DIR-3 KYC, and it stays that way until the KYC is filed."),
 ("How do I reactivate a deactivated DIN?", "File DIR-3 KYC Web on the MCA portal with the late fee of ₹5,000. The form needs your PAN and Aadhaar details, a personal mobile number and email verified by OTP, and your digital signature. Once it is approved, the DIN status returns to approved."),
 ("Is the ₹5,000 late fee charged per day?", "No. It is a flat late fee of ₹5,000 for each DIN, however long the DIN has been deactivated."),
 ("How long does DIN reactivation take?", "We file within 24 hours of receiving complete details. The status usually changes once the form is processed on the MCA portal, typically within a few working days. Mismatches with the PAN record are the most common cause of delay."),
 ("What can't I do while my DIN is deactivated?", "You cannot be appointed as a director, and MCA forms that need your DIN or signature, such as DIR-12, AOC-4 and MGT-7, cannot be filed with it until the DIN is reactivated."),
 ("Is a deactivated DIN the same as a disqualified director?", "No. Deactivation is caused by missing KYC and is fixed by filing it. Disqualification under Section 164(2) happens when a company where you are a director fails to file its financial statements or annual returns for three continuous financial years, or defaults on deposits, debentures or dividends for a year."),
 ("How long does a Section 164(2) disqualification last?", "The director cannot be appointed or reappointed in that company or any other company for five years from the date on which the company failed to file or pay. The director's office in other companies is also vacated under Section 167."),
 ("Can a Section 164(2) disqualification be removed earlier?", "It cannot be removed simply by filing KYC. Depending on the facts, options include reviving a struck-off company through the Tribunal under Section 252, correcting the record where a director was wrongly marked, or legal remedies. A professional should review each case."),
 ("Can a surrendered or cancelled DIN be reactivated?", "Generally no. A DIN surrendered through DIR-5 or cancelled under Rule 11, for example as a duplicate, is not reactivated; a fresh DIN is applied for if the person is appointed as a director again."),
 ("My mobile number or email has changed. Can I still reactivate?", "Yes. Use your current personal mobile number and email in the reactivation KYC; both are verified by OTP while filing. They must not be shared with another director."),
 ("What documents are needed to reactivate a DIN?", "PAN, Aadhaar, current residential address, a personal mobile number and email, and a valid digital signature certificate. Foreign nationals use their passport in place of PAN and Aadhaar."),
 ("When is the next KYC due after reactivation?", "After reactivation, the DIN follows the three-year KYC cycle, due by 30 June, under the rules in force from 31 March 2026. Any change in mobile, email or address must be updated within 30 days."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-reactivation p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "DIN Reactivation"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "DIN Reactivation",
  "alternateName": ["Deactivated DIN reactivation", "DIN reactivation through DIR-3 KYC", "Disqualified director DIN review"],
  "serviceType": "Reactivation of a Director Identification Number deactivated for non-filing of KYC",
  "description": "Reactivation of DINs deactivated for missed DIR-3 KYC, with PAN, Aadhaar and DSC checks, DIR-3 KYC Web filed with the late fee, and review of DINs disqualified under Section 164(2).",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Directors and designated partners with a deactivated or disqualified DIN"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "DIN Reactivation Plans", "itemListElement": [
    {"@type": "Offer", "name": "DIN Reactivation", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Reactivation + DSC", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Disqualification Review", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to reactivate a deactivated DIN", "totalTime": "P3D",
  "supply": [{"@type": "HowToSupply", "name": "PAN and Aadhaar"}, {"@type": "HowToSupply", "name": "Personal mobile number and email"},
             {"@type": "HowToSupply", "name": "Current residential address"}, {"@type": "HowToSupply", "name": "Valid DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check the DIN status", "text": "Confirm on the MCA portal whether the DIN is deactivated for non-filing of KYC, or flagged as disqualified."},
   {"@type": "HowToStep", "position": 2, "name": "Match details", "text": "Make sure the name and date of birth match the PAN record, the PAN is linked with Aadhaar and the DSC is valid."},
   {"@type": "HowToStep", "position": 3, "name": "Verify by OTP", "text": "Verify a personal mobile number and email with one-time passwords."},
   {"@type": "HowToStep", "position": 4, "name": "File with the late fee", "text": "Sign DIR-3 KYC Web with the DSC and pay the ₹5,000 late fee."},
   {"@type": "HowToStep", "position": 5, "name": "Confirm reactivation", "text": "Check that the DIN status shows approved, then diary the next KYC date."}]},
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
    <meta property="og:title" content="DIN Reactivation – Deactivated DIN" />
    <meta property="og:description" content="Deactivated DIN? Reactivate it with DIR-3 KYC Web, with PAN and DSC checked first by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – DIN Reactivation" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="DIN Reactivation – Deactivated DIN" />
    <meta name="twitter:description" content="DIN deactivated? Get it active again and unblock your MCA filings." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "din-reactivation"')
assert 'service: "din-reactivation"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="din-reactivation"')
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
