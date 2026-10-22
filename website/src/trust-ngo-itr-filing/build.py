# Builds trust-ngo-itr-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/trust-ngo-itr-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/trust-ngo-itr-filing/"
TITLE = "Trust & NGO ITR-7 Filing Online | Bharat e-Filing"
DESC = "File ITR-7 for your trust, society or Section 8 company. 85% application, Form 10B/10BB audit, 80G Form 10BD and 12AB renewal handled by CAs."
OG = "https://bharatefiling.com/wp-content/uploads/og/trust-ngo-itr-filing-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "trust-ngo-itr-filing"

FAQ = [
 ("Which ITR form does a trust or NGO file?", "Trusts, societies and Section 8 companies registered under Section 12AB or approved under Section 10(23C) that claim exemption file ITR-7. Political parties, research associations, universities and similar institutions also file ITR-7. A trust that is not registered and does not claim exemption files ITR-5 as an association of persons."),
 ("Is it mandatory for a registered trust or NGO to file an income tax return?", "Yes. Under Section 139(4A), a trust or institution must file its return if its total income, before claiming the exemption under Sections 11 and 12, exceeds the basic exemption limit. Filing on time is also a condition for keeping the exemption."),
 ("What is the due date for ITR-7 for FY 2025-26?", "Trusts whose accounts must be audited file by the audit-case due date, which for FY 2025-26 is 21 November 2026, extended from 31 October by CBDT Circular 7/2026. Trusts that do not need an audit file by the general due date."),
 ("How much of its income must a trust spend?", "A charitable or religious trust must apply at least 85% of its income to its objects during the year. Up to 15% can be set aside without conditions. Any further shortfall can be accumulated for up to five years by filing Form 10, provided the money is invested in the modes allowed by Section 11(5)."),
 ("What happens if a trust does not apply 85% of its income?", "The unspent amount that is neither within the 15% allowance nor accumulated through Form 10 or deemed applied through Form 9A becomes taxable at the maximum marginal rate. Accumulated amounts not used within five years also become taxable."),
 ("Which audit report does a trust need, Form 10B or Form 10BB?", "Form 10B applies if total income before exemption exceeds ₹5 crore, the trust received foreign contribution, or applied income outside India. Other trusts that need an audit use Form 10BB. The audit report must be filed before the return, at least one month before the ITR due date."),
 ("Are corpus donations taxable for a trust?", "Voluntary contributions made with a specific direction that they will form part of the corpus are exempt and are not counted as income for the 85% rule, but they must be invested in the modes allowed by Section 11(5). Spending from the corpus is not treated as application of income until it is reinvested."),
 ("How are anonymous donations taxed?", "Under Section 115BBC, anonymous donations above the higher of ₹1 lakh or 5% of total donations are taxed at 30%. Wholly religious trusts are excluded, and partly religious trusts are excluded except for donations made for an educational or medical institution they run."),
 ("What is Form 10BD and Form 10BE?", "A trust approved under Section 80G or 35 files Form 10BD, a statement of donations received, by 31 May after the year ends, and issues Form 10BE certificates to donors by the same date. Late filing attracts a fee of ₹200 a day under Section 234G and a penalty under Section 271K."),
 ("How long is 12AB registration valid?", "Regular registration under Section 12AB is valid for five years. From 1 April 2025, it is granted for ten years where the trust's total income, before the exemption, did not exceed ₹5 crore in each of the two years before the application. Renewal must be applied for in Form 10AB at least six months before expiry."),
 ("Does an NGO with foreign contribution have extra filings?", "Yes. An NGO registered under the Foreign Contribution (Regulation) Act files its annual return in Form FC-4 by 31 December, and its income tax audit must be in Form 10B, whatever its income."),
 ("Does the Income-tax Act, 2025 change ITR filing for trusts for FY 2025-26?", "Returns for FY 2025-26 are filed under the Income-tax Act, 1961. The Income-tax Act, 2025 applies from tax year 2026-27 and brings the rules for charitable trusts and institutions together in a single chapter for registered non-profit organisations, so plan next year's compliance with the new references."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-trust-itr p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "Trust & NGO Tax Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Trust & NGO Tax Filing",
  "alternateName": ["ITR-7 filing", "NGO income tax return", "Charitable trust tax filing"],
  "serviceType": "Income tax return filing in ITR-7 for trusts, societies and Section 8 companies",
  "description": "CA-led ITR-7 filing for charitable and religious trusts, societies and Section 8 companies, including the 85% application test, Form 10 and 9A, audit reports in Form 10B or 10BB, 80G donation statements in Form 10BD and 10BE, 12AB renewal and FCRA returns.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "Audience", "audienceType": "Charitable and religious trusts, societies, Section 8 companies and NGOs in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Trust & NGO Tax Filing Plans", "itemListElement": [
    {"@type": "Offer", "name": "Small Trust", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Trust & NGO ITR-7", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "NGO Complete Compliance", "price": "17999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file ITR-7 for a trust or NGO", "totalTime": "P5D",
  "supply": [{"@type": "HowToSupply", "name": "Trust deed or society registration and 12AB / 80G orders"}, {"@type": "HowToSupply", "name": "Audited income and expenditure account and balance sheet"},
             {"@type": "HowToSupply", "name": "Donation register, corpus and anonymous donation details"}, {"@type": "HowToSupply", "name": "DSC of the authorised trustee"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Finalise the accounts", "text": "Close the income and expenditure account and balance sheet, separating corpus donations, voluntary contributions and application of income."},
   {"@type": "HowToStep", "position": 2, "name": "Check the 85% application", "text": "Compare income with the amount applied to objects, and file Form 10 to accumulate or Form 9A for deemed application if needed."},
   {"@type": "HowToStep", "position": 3, "name": "Get the audit report", "text": "The auditor files Form 10B or Form 10BB on the portal, at least one month before the ITR due date."},
   {"@type": "HowToStep", "position": 4, "name": "File ITR-7", "text": "File ITR-7 on incometax.gov.in by the due date with the trustee's DSC or EVC, reporting registration details, donations and application."},
   {"@type": "HowToStep", "position": 5, "name": "Complete donor and FCRA filings", "text": "File Form 10BD and issue Form 10BE to donors by 31 May, and for FCRA-registered NGOs file Form FC-4 by 31 December."}]},
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
    <meta property="og:title" content="Trust &amp; NGO Tax Filing (ITR-7) Online" />
    <meta property="og:description" content="ITR-7 filed by CAs. 85% application, Form 10B/10BB audit, 80G Form 10BD and 12AB renewal handled." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Trust &amp; NGO Tax Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Trust &amp; NGO Tax Filing (ITR-7) Online" />
    <meta name="twitter:description" content="ITR-7 for trusts, societies and Section 8 companies, with 80G and FCRA filings, handled by CAs." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "trust-ngo-itr-filing"')
assert 'service: "trust-ngo-itr-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="trust-ngo-itr-filing"')
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
