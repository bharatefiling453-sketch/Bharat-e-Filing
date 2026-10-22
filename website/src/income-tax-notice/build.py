# Builds income-tax-notice/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/income-tax-notice/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/income-tax-notice/"
TITLE = "Income Tax Notice Reply Online | Bharat e-Filing"
DESC = "Got an income tax notice under 143(1)(a), 139(9), 143(2), 148A or 156? Understand it, meet the deadline and reply on the e-filing portal with CA help."
OG = "https://bharatefiling.com/wp-content/uploads/og/income-tax-notice-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "income-tax-notice"

FAQ = [
 ("Why did I get an income tax notice?", "Most notices are raised automatically when the return does not match the department's data, such as AIS, Form 26AS or TDS returns, when a return is defective or incomplete, when a demand is outstanding, or when a case is picked for scrutiny or reassessment. The section number on the notice tells you what it is about."),
 ("How do I check if an income tax notice is genuine?", "Every genuine notice carries a Document Identification Number (DIN) and appears on the e-filing portal under Pending Actions, e-Proceedings. You can verify any notice using the Authenticate Notice or Order service on incometax.gov.in."),
 ("What is a notice under Section 143(1)(a)?", "It is a proposed adjustment to your return, sent before processing, for reasons such as an arithmetical error, an incorrect claim or income shown in Form 26AS or AIS but missing from the return. You can agree or disagree online within 30 days; if you do not respond, the adjustment is made."),
 ("What is a defective return notice under Section 139(9)?", "It means the return is incomplete or has inconsistencies, such as tax paid but not claimed, or business income without a balance sheet. You must correct the defect within 15 days by filing a corrected return in response, otherwise the return is treated as invalid."),
 ("What is a scrutiny notice under Section 143(2)?", "It means your return has been selected for detailed assessment. It must be served within three months from the end of the financial year in which the return was filed. Assessment is faceless: you upload replies and documents on the e-filing portal, and can ask for a video hearing."),
 ("What is a Section 148A notice?", "It is a show cause notice asking why income should not be treated as having escaped assessment, before a reassessment notice under Section 148 is issued. After the 2024 amendment, it can be issued within three years from the end of the assessment year, or five years if escaped income is ₹50 lakh or more. Reply with evidence within the time stated."),
 ("What should I do with a demand notice under Section 156?", "Check whether the demand is correct. If it is, pay within 30 days to avoid interest of 1% a month under Section 220(2). If it is wrong, submit a response on the portal disagreeing with the demand, file a rectification under Section 154, or appeal."),
 ("What is a Section 245 notice?", "It is an intimation that the department proposes to adjust your refund against an outstanding demand. You can agree, disagree or partly agree on the portal within 30 days."),
 ("What happens if I ignore an income tax notice?", "The department can complete the assessment on the information it has, raise a demand with interest, and levy penalties, such as ₹10,000 for not complying with a notice and 50% or 200% of the tax on under-reported or misreported income under Section 270A."),
 ("How do I reply to an income tax notice online?", "Log in to incometax.gov.in, go to Pending Actions and then e-Proceedings or the Compliance portal, open the notice, and submit your response with supporting documents before the due date. Keep the acknowledgement."),
 ("Can I appeal against an assessment order?", "Yes. You can appeal to the Commissioner (Appeals) in Form 35 within 30 days of receiving the order, and further to the Income Tax Appellate Tribunal. For mistakes apparent from the record, you can file a rectification request under Section 154."),
 ("Does the Income-tax Act, 2025 change income tax notices?", "Notices for tax years up to FY 2025-26 continue under the Income-tax Act, 1961 provisions. The Income-tax Act, 2025 applies from tax year 2026-27 and renumbers sections, so notices for later years will cite new section numbers for the same kinds of proceedings."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-notice p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "Income Tax Notice"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Income Tax Notice Reply",
  "alternateName": ["Income tax notice response", "Reply to Section 143(1)(a) notice", "Scrutiny and reassessment notice reply"],
  "serviceType": "Drafting and filing replies to income tax notices on the e-filing portal",
  "description": "CA-led replies to income tax notices, including Section 143(1)(a) adjustments, 139(9) defective returns, 143(2) scrutiny, 148A reassessment, 156 demands and 245 refund adjustments, with rectification and appeals where needed.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "PeopleAudience", "audienceType": "Individuals and businesses in India who have received an income tax notice"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Income Tax Notice Plans", "itemListElement": [
    {"@type": "Offer", "name": "Notice Reply", "price": "2499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Scrutiny Assessment", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Reassessment & Appeal", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to reply to an income tax notice", "totalTime": "P7D",
  "supply": [{"@type": "HowToSupply", "name": "The notice with its DIN"}, {"@type": "HowToSupply", "name": "The ITR, computation, AIS and Form 26AS for that year"},
             {"@type": "HowToSupply", "name": "Evidence: bank statements, invoices, Form 16, deduction proofs"}, {"@type": "HowToSupply", "name": "E-filing portal login"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Verify the notice", "text": "Check the DIN and confirm the notice appears on the e-filing portal under Pending Actions."},
   {"@type": "HowToStep", "position": 2, "name": "Identify the section and deadline", "text": "Read the section, assessment year, issue raised and the date by which a reply is due."},
   {"@type": "HowToStep", "position": 3, "name": "Compare with your records", "text": "Match the issue against your return, AIS, Form 26AS and books to see whether it is correct."},
   {"@type": "HowToStep", "position": 4, "name": "Draft the reply", "text": "Prepare a point-by-point reply with documents, or agree and pay if the department is right."},
   {"@type": "HowToStep", "position": 5, "name": "Submit and follow up", "text": "Submit the reply on the portal before the due date, save the acknowledgement and track the order."}]},
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
    <meta property="og:title" content="Income Tax Notice Reply Online" />
    <meta property="og:description" content="Understand your notice, meet the deadline and reply on the portal with a Chartered Accountant." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Income Tax Notice" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Income Tax Notice Reply Online" />
    <meta name="twitter:description" content="Got a 143(1)(a), 139(9), 143(2) or 148A notice? Reply on time with a CA." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "income-tax-notice"')
assert 'service: "income-tax-notice"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="income-tax-notice"')
globalnav = cut("    <!-- ================= GLOBAL NAV", "    <!-- ================= LOCAL NAV").replace(
    '<a href="https://bharatefiling.com/product-category/gst/" aria-current="page">GST</a>', '<a href="https://bharatefiling.com/product-category/gst/">GST</a>').replace(
    '<a href="https://bharatefiling.com/income-tax/">Income Tax</a>', '<a href="https://bharatefiling.com/income-tax/" aria-current="page">Income Tax</a>')
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
