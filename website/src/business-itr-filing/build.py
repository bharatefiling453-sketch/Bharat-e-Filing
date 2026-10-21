# Builds business-itr-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/business-itr-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/business-itr-filing/"
TITLE = "Business ITR Filing Online for AY 2026-27 | Bharat e-Filing"
DESC = "File ITR-3, ITR-4, ITR-5 or ITR-6 for your proprietorship, firm, LLP or company. Presumptive income, tax audit, losses and advance tax handled by CAs."
OG = "https://bharatefiling.com/wp-content/uploads/og/business-itr-filing-1200x630.jpg"
PUB = "2026-10-21"
SLUG = "business-itr-filing"

FAQ = [
 ("Which ITR form should a business file?", "A proprietor files ITR-3, or ITR-4 if they opt for presumptive taxation and total income is up to ₹50 lakh. A partnership firm files ITR-5, or ITR-4 if it opts for presumptive taxation. An LLP always files ITR-5, and a company files ITR-6."),
 ("What is the due date for business ITR filing for FY 2025-26?", "The due date is 31 August 2026 for business and professional cases that do not need a tax audit, and 21 November 2026 for tax-audit cases, extended from 31 October by CBDT Circular 7/2026. Companies file by the audit due date. Transfer-pricing cases file by 30 November 2026."),
 ("What is presumptive taxation under Section 44AD?", "Eligible resident individuals, HUFs and partnership firms (not LLPs) with business turnover up to ₹2 crore, or ₹3 crore if cash receipts are no more than 5%, can declare profit at 8% of turnover, or 6% of receipts received digitally. They need not maintain detailed books or get a tax audit for that income."),
 ("What is Section 44ADA for professionals?", "Resident professionals such as doctors, lawyers, architects, engineers and consultants with gross receipts up to ₹50 lakh, or ₹75 lakh if cash receipts are no more than 5%, can declare 50% of receipts as profit and file ITR-4."),
 ("When is a tax audit required for a business?", "A tax audit under Section 44AB applies when business turnover exceeds ₹1 crore, or ₹10 crore if cash receipts and cash payments are each no more than 5%, and when professional receipts exceed ₹50 lakh. It can also apply if you declare profit below the presumptive rate, or opted out of Section 44AD within five years, and your income exceeds the basic exemption limit."),
 ("What is the penalty for not getting a tax audit done?", "Under Section 271B, the penalty is 0.5% of turnover or gross receipts, up to ₹1.5 lakh, unless there was a reasonable cause. The audit report in Form 3CA or 3CB with 3CD must be filed before the ITR."),
 ("How are partnership firms and LLPs taxed?", "Firms and LLPs pay tax at 30% plus a 12% surcharge where income exceeds ₹1 crore and 4% cess. Remuneration and interest to partners are deductible within the limits of Section 40(b), and the partner's share of profit is exempt in their hands under Section 10(2A)."),
 ("What is the limit on partner remuneration?", "Under Section 40(b), on the first ₹6 lakh of book profit or in case of a loss, the deduction is the higher of ₹3 lakh or 90% of book profit. On the balance it is 60% of book profit. Interest on partners' capital is allowed up to 12% a year if authorised by the partnership deed."),
 ("Do firms need to deduct TDS on payments to partners?", "Yes. From 1 April 2025, Section 194T requires a firm to deduct TDS at 10% on salary, remuneration, commission, bonus or interest paid or credited to a partner when the total for the year exceeds ₹20,000."),
 ("What is the tax rate for a company?", "A domestic company can opt for Section 115BAA and pay 22% plus a 10% surcharge and 4% cess, an effective rate of about 25.17%, without most exemptions. Otherwise it pays 25% if turnover in the relevant earlier year was up to ₹400 crore, or 30%, plus surcharge and cess."),
 ("What happens if a business files its ITR late?", "A late fee of up to ₹5,000 under Section 234F and interest under Section 234A apply. A business loss cannot be carried forward from a return filed after the due date, so filing on time protects losses that can otherwise be set off for eight years."),
 ("Does the Income-tax Act, 2025 change business ITR filing for FY 2025-26?", "Returns for FY 2025-26 are filed under the Income-tax Act, 1961. The Income-tax Act, 2025 applies to income from tax year 2026-27, and renumbers key provisions: presumptive taxation becomes Section 58 and tax audit becomes Section 63."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-business-itr p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "Business ITR Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Business ITR Filing",
  "alternateName": ["Business income tax return filing", "ITR-3, ITR-4, ITR-5 and ITR-6 filing", "Firm, LLP and company ITR filing"],
  "serviceType": "Income tax return filing for proprietorships, partnership firms, LLPs and companies",
  "description": "CA-led income tax return filing for businesses and professionals, including presumptive taxation under Sections 44AD, 44ADA and 44AE, tax audit under Section 44AB, partner remuneration and Section 194T TDS, loss carry-forward and advance tax.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Proprietors, professionals, partnership firms, LLPs and private limited companies in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Business ITR Filing Plans", "itemListElement": [
    {"@type": "Offer", "name": "Proprietor & Professional", "price": "3499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Partnership Firm & LLP", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Private Limited Company", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file an income tax return for a business", "totalTime": "P3D",
  "supply": [{"@type": "HowToSupply", "name": "Books of account or bank statements and sales records"}, {"@type": "HowToSupply", "name": "GST returns and Form 26AS / AIS"},
             {"@type": "HowToSupply", "name": "Partnership deed or incorporation documents"}, {"@type": "HowToSupply", "name": "DSC for audit cases, LLPs and companies"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Pick the form and method", "text": "Choose ITR-3, ITR-4, ITR-5 or ITR-6 by entity, and decide between presumptive taxation and regular books."},
   {"@type": "HowToStep", "position": 2, "name": "Finalise the books", "text": "Close the profit and loss account and balance sheet, and match turnover with GST returns and AIS."},
   {"@type": "HowToStep", "position": 3, "name": "Complete the tax audit if needed", "text": "If Section 44AB applies, the auditor files Form 3CA or 3CB with 3CD before the return."},
   {"@type": "HowToStep", "position": 4, "name": "Compute and pay tax", "text": "Compute tax with depreciation, partner remuneration and loss set-off, and pay any balance by challan."},
   {"@type": "HowToStep", "position": 5, "name": "File and verify", "text": "File the return on incometax.gov.in by the due date and verify it with DSC or EVC."}]},
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
    <meta property="og:title" content="Business ITR Filing Online – Firms, LLPs & Companies" />
    <meta property="og:description" content="ITR-3, ITR-4, ITR-5 and ITR-6 filed by CAs. Presumptive income, tax audit, partner TDS and losses handled." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Business ITR Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Business ITR Filing Online – Firms, LLPs & Companies" />
    <meta name="twitter:description" content="Tax-audit case? Your business ITR is due by 21 November 2026. CAs file it for you." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "business-itr-filing"')
assert 'service: "business-itr-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="business-itr-filing"')
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
