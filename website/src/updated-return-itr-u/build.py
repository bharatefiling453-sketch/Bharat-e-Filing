# Builds updated-return-itr-u/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/updated-return-itr-u/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/updated-return-itr-u/"
TITLE = "Revised & Updated Return (ITR-U) Filing | Bharat e-Filing"
DESC = "Missed income or made a mistake in your ITR? File a revised return, or an updated return (ITR-U) within 48 months. Additional tax worked out by CAs."
OG = "https://bharatefiling.com/wp-content/uploads/og/updated-return-itr-u-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "updated-return-itr-u"

FAQ = [
 ("What is the difference between a revised return and an updated return (ITR-U)?", "A revised return under Section 139(5) corrects any mistake in a return already filed, including claims that reduce tax, but only within a limited time. An updated return under Section 139(8A), filed as ITR-U, can be filed much later, up to 48 months from the end of the assessment year, but only to report extra income or pay more tax, with additional tax."),
 ("Until when can I revise my ITR for FY 2025-26?", "A revised return for FY 2025-26 (AY 2026-27) can be filed until 31 March 2027, before the assessment is completed. A fee applies if you revise after 31 December 2026. You can revise more than once within this time."),
 ("What is the time limit to file ITR-U?", "After the Finance Act, 2025, an updated return can be filed within 48 months from the end of the relevant assessment year, up from 24 months earlier."),
 ("How much additional tax is payable on ITR-U?", "You pay additional tax on the aggregate of tax and interest due on the updated return: 25% if filed within 12 months from the end of the assessment year, 50% within 24 months, 60% within 36 months and 70% within 48 months."),
 ("Can I file ITR-U if I never filed the original return?", "Yes. An updated return can be filed even if no original or belated return was filed for that year, as long as it results in tax payable and the other conditions are met."),
 ("When can an updated return not be filed?", "ITR-U cannot be filed to show a loss, reduce tax, increase a refund, or where a search or survey has begun, an assessment or reassessment is pending or completed for that year, or prosecution proceedings have started. After 36 months, it can be filed only if no reassessment show cause notice was issued, or the officer has decided it is not a fit case."),
 ("How many times can I file an updated return?", "Only one updated return can be filed for each assessment year. Make sure every missed item is included before filing."),
 ("Do I need to pay tax before filing ITR-U?", "Yes. Under Section 140B, the tax, interest, late fee and additional tax must be paid before the updated return is filed, and the challan details are reported in the return."),
 ("Can I claim a refund through ITR-U?", "No. An updated return cannot be used to claim or increase a refund or reduce your tax liability. For mistakes apparent from the record you can seek rectification under Section 154, and in genuine hardship cases, condonation of delay under Section 119(2)(b)."),
 ("What mistakes can a revised return fix?", "A revised return can fix almost anything in the original return: missed income, wrong deductions, wrong ITR form, wrong bank account, or the regime choice where the law allows. It replaces the original return completely."),
 ("Does filing ITR-U stop penalties?", "Voluntarily disclosing missed income through ITR-U, with the tax and additional tax paid, generally protects you from penalty for under-reporting that income, because you corrected it before the department found it."),
 ("Does the Income-tax Act, 2025 change ITR-U?", "Revised and updated returns for years up to FY 2025-26 follow the Income-tax Act, 1961. The Income-tax Act, 2025 applies from tax year 2026-27 and keeps both facilities with new section numbers, so check the current utility on the e-filing portal."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-itr-u p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "Revised & Updated Return (ITR-U)"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Revised & Updated Return (ITR-U) Filing",
  "alternateName": ["ITR-U filing", "Updated income tax return", "Revised ITR filing"],
  "serviceType": "Filing of revised returns under Section 139(5) and updated returns under Section 139(8A)",
  "description": "CA-led filing of revised income tax returns and updated returns (ITR-U), including eligibility checks, computation of tax, interest and additional tax under Section 140B, and the choice between revision, ITR-U, rectification and condonation.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "PeopleAudience", "audienceType": "Individuals and businesses in India who need to correct or update an income tax return"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Revised & Updated Return Plans", "itemListElement": [
    {"@type": "Offer", "name": "Revised Return", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Updated Return (ITR-U)", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "ITR-U for Business or Multiple Years", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file an updated return (ITR-U)", "totalTime": "P2D",
  "supply": [{"@type": "HowToSupply", "name": "Original return and computation, if filed"}, {"@type": "HowToSupply", "name": "AIS and Form 26AS for the year"},
             {"@type": "HowToSupply", "name": "Proof of the missed income"}, {"@type": "HowToSupply", "name": "Net banking for the tax payment"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check eligibility", "text": "Confirm the year is within 48 months, the update increases tax, and no search, survey, assessment or reassessment bars it."},
   {"@type": "HowToStep", "position": 2, "name": "Compute tax and additional tax", "text": "Compute tax and interest on the updated income, then add 25%, 50%, 60% or 70% additional tax depending on the time elapsed."},
   {"@type": "HowToStep", "position": 3, "name": "Pay before filing", "text": "Pay the full amount by challan under Section 140B before filing."},
   {"@type": "HowToStep", "position": 4, "name": "File ITR-U", "text": "Select the assessment year and Section 139(8A) in the return, give the reason for updating, and report the challan."},
   {"@type": "HowToStep", "position": 5, "name": "Verify within 30 days", "text": "E-verify the updated return with Aadhaar OTP, net banking or DSC within 30 days of filing."}]},
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
    <meta property="og:title" content="Revised &amp; Updated Return (ITR-U) Filing" />
    <meta property="og:description" content="Fix a mistake or report missed income: revised return or ITR-U within 48 months, worked out by CAs." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Revised &amp; Updated Return" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Revised &amp; Updated Return (ITR-U) Filing" />
    <meta name="twitter:description" content="Missed income in an old ITR? Update it with ITR-U before the additional tax goes up." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "updated-return-itr-u"')
assert 'service: "updated-return-itr-u"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="updated-return-itr-u"')
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
