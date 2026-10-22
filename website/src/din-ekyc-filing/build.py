# Builds din-ekyc-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/din-ekyc-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/din-ekyc-filing/"
TITLE = "DIN eKYC Filing Online – DIR-3 KYC | Bharat e-Filing"
DESC = "File DIR-3 KYC for your DIN online: the new three-year cycle due by 30 June, 30-day updates for mobile, email or address, and deactivated DIN reactivation."
OG = "https://bharatefiling.com/wp-content/uploads/og/din-ekyc-filing-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "din-ekyc-filing"

FAQ = [
 ("What is DIN eKYC?", "DIN eKYC is the KYC of a person who holds a Director Identification Number, filed with the Ministry of Corporate Affairs in Form DIR-3 KYC Web. It confirms the director's PAN, Aadhaar, address, personal mobile number and email, verified by OTP and signed with the director's digital signature."),
 ("Do directors still need to file DIR-3 KYC every year?", "No. The Companies (Appointment and Qualification of Directors) Amendment Rules, 2025, effective from 31 March 2026, replaced the annual KYC with a filing once every three financial years, due by 30 June. The earlier 30 September annual deadline no longer applies."),
 ("When is my next DIR-3 KYC due?", "It depends on when you last filed. For directors whose KYC was up to date in 2025, the next routine filing is generally due by 30 June 2028, though some experts read the rule as 30 June 2029. We confirm your exact window from your DIN record."),
 ("What if my mobile number, email or address changes?", "Under the amended rules, a change in your personal mobile number, email address or residential address must be updated through DIR-3 KYC Web within 30 days of the change. An update does not reset the three-year cycle."),
 ("What happens if DIR-3 KYC is not filed?", "The DIN is marked as deactivated due to non-filing of DIR-3 KYC. The person cannot be appointed as a director, and company filings that need that DIN are blocked until the KYC is filed."),
 ("How do I reactivate a deactivated DIN?", "File DIR-3 KYC Web with the late fee of ₹5,000. Once the form is approved, the DIN status returns to approved and the director can sign and be named in MCA filings again."),
 ("Is there a late fee for DIR-3 KYC?", "Yes. Filing after the due date, including to reactivate a deactivated DIN, attracts a late fee of ₹5,000."),
 ("What documents are needed for DIR-3 KYC?", "The director's PAN, Aadhaar, a personal mobile number and email for OTP verification, current residential address, and a valid digital signature certificate. Foreign nationals use their passport in place of PAN and Aadhaar."),
 ("Can the same mobile number or email be used by two directors?", "No. Each director must give a personal mobile number and email address that are not shared with another director, and both are verified by OTP while filing."),
 ("Is DIR-3 KYC needed if I am not a director in any company now?", "Yes. KYC applies to every person who holds a DIN, whether or not they are currently on a board, because the DIN remains allotted to them until it is surrendered."),
 ("How do I change my name or other DIN particulars?", "Changes to particulars such as name, father's name or nationality are made through Form DIR-6 with supporting proof. Changes to mobile number, email or address go through DIR-3 KYC Web within 30 days."),
 ("Does DIN KYC need my PAN to match the income-tax records?", "Yes. The name and date of birth must match the PAN database of the Income Tax Department, and the PAN should be valid and linked with Aadhaar. Mismatches are a common reason for failed KYC."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-din-kyc p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "DIN eKYC Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "DIN eKYC Filing",
  "alternateName": ["DIR-3 KYC filing", "Director KYC", "DIN KYC", "DIN reactivation"],
  "serviceType": "KYC of Director Identification Number holders with the Ministry of Corporate Affairs",
  "description": "DIR-3 KYC Web filing for DIN holders under the three-year cycle, 30-day updates of mobile, email and address, and reactivation of DINs deactivated for non-filing.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Directors and DIN holders of Indian companies and LLPs"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "DIN eKYC Plans", "itemListElement": [
    {"@type": "Offer", "name": "Single Director KYC", "price": "999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Board KYC Pack", "price": "2499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "DIN Reactivation", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file DIR-3 KYC for a DIN", "totalTime": "P1D",
  "supply": [{"@type": "HowToSupply", "name": "PAN and Aadhaar"}, {"@type": "HowToSupply", "name": "Personal mobile number and email"},
             {"@type": "HowToSupply", "name": "Current residential address"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check DIN status", "text": "Check whether the DIN is approved or deactivated, and when KYC was last filed."},
   {"@type": "HowToStep", "position": 2, "name": "Match PAN details", "text": "Make sure the name and date of birth match the PAN database, and the PAN is linked with Aadhaar."},
   {"@type": "HowToStep", "position": 3, "name": "Verify by OTP", "text": "Verify the personal mobile number and email with one-time passwords on the MCA portal."},
   {"@type": "HowToStep", "position": 4, "name": "Sign and submit", "text": "Sign DIR-3 KYC Web with the director's DSC and submit, with the late fee if the DIN is deactivated."},
   {"@type": "HowToStep", "position": 5, "name": "Diary the next date", "text": "Note the next three-yearly due date, and update any change in mobile, email or address within 30 days."}]},
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
    <meta property="og:title" content="DIN eKYC Filing – DIR-3 KYC" />
    <meta property="og:description" content="DIR-3 KYC for directors under the new three-year cycle, 30-day updates and DIN reactivation, filed by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – DIN eKYC Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="DIN eKYC Filing – DIR-3 KYC" />
    <meta name="twitter:description" content="Keep your DIN active. DIR-3 KYC filed right, every three years." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "din-ekyc-filing"')
assert 'service: "din-ekyc-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="din-ekyc-filing"')
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
