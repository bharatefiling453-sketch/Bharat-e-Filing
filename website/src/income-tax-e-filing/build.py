# Builds income-tax-e-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/income-tax-e-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/income-tax-e-filing/"
TITLE = "Income Tax e-Filing Online for AY 2026-27 | Bharat e-Filing"
DESC = "File your income tax return online, free or with a CA. AIS and Form 26AS import, regime comparison, e-verification and refund tracking handled by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/income-tax-e-filing-1200x630.jpg"
PUB = "2026-10-21"
SLUG = "income-tax-e-filing"

FAQ = [
 ("What is income tax e-filing?", "Income tax e-filing is filing your income tax return (ITR) online on the Income Tax Department's e-filing portal, incometax.gov.in, instead of on paper. You report your income, deductions and taxes paid for the year, upload the return and then e-verify it."),
 ("Who must file an income tax return?", "You must file if your total income before deductions is above the basic exemption limit, which is ₹4 lakh under the new regime for FY 2025-26. You must also file if, for example, you deposited ₹1 crore or more in current accounts or ₹50 lakh or more in savings accounts, spent over ₹2 lakh on foreign travel or over ₹1 lakh on electricity, had TDS and TCS of ₹25,000 or more (₹50,000 for senior citizens), or hold foreign assets."),
 ("What is the last date to file ITR for FY 2025-26 (AY 2026-27)?", "The due date was 31 July 2026 for individuals filing ITR-1 or ITR-2 and 31 August 2026 for non-audit business cases. For tax-audit cases it is 21 November 2026, extended from 31 October by CBDT Circular 7/2026. A belated return can be filed until 31 December 2026."),
 ("Can I still file my ITR after the due date?", "Yes. You can file a belated return until 31 December 2026 with a late fee of ₹5,000, or ₹1,000 if total income is up to ₹5 lakh, under Section 234F. Interest under Section 234A applies on any unpaid tax. After that, an updated return (ITR-U) can be filed within 48 months on payment of additional tax."),
 ("Which ITR form should I file?", "ITR-1 is for resident individuals with income up to ₹50 lakh from salary, one house property and other sources. ITR-2 is for individuals with capital gains, more than one house property or foreign income but no business income. ITR-3 is for business or professional income, including F&O trading. ITR-4 is for presumptive business or professional income up to ₹50 lakh."),
 ("Is income up to ₹12 lakh tax-free?", "Under the new regime for FY 2025-26, the Section 87A rebate of up to ₹60,000 makes tax nil on total income up to ₹12 lakh, or ₹12.75 lakh for salaried individuals after the ₹75,000 standard deduction. The rebate does not cover income taxed at special rates, such as capital gains."),
 ("Should I choose the new or the old tax regime?", "The new regime is the default and has lower rates with fewer deductions. The old regime allows deductions such as 80C, 80D, HRA and home-loan interest. Salaried individuals can choose the better one each year when filing; compare both before you file."),
 ("What documents do I need for income tax e-filing?", "You need your PAN linked with Aadhaar, Form 16 from your employer, the Annual Information Statement (AIS) and Form 26AS, bank interest certificates, capital gains statements if you sold shares or property, and proofs of deductions if you choose the old regime. Keep a pre-validated bank account for the refund."),
 ("Why do I need to e-verify my return?", "A return is complete only after it is verified. You must e-verify within 30 days of uploading, using Aadhaar OTP, net banking or a bank or demat account. If you verify later, the date of verification is treated as the date of filing, and an unverified return is treated as not filed."),
 ("How long does it take to get an income tax refund?", "Refunds are processed after the return is e-verified and processed under Section 143(1), usually within a few weeks. The refund is credited to your pre-validated bank account, and interest under Section 244A is paid on eligible refunds."),
 ("Can I correct a mistake after filing my ITR?", "Yes. You can file a revised return for FY 2025-26 until 31 March 2027, before assessment is completed. A fee applies if you revise after 31 December 2026. If the time limit has passed, an updated return may be possible, but not to reduce tax or claim a higher refund."),
 ("Does the Income-tax Act, 2025 change how I file for FY 2025-26?", "Returns for FY 2025-26 (AY 2026-27) are filed under the Income-tax Act, 1961. The Income-tax Act, 2025 applies from 1 April 2026, so it governs income from tax year 2026-27 onwards, whose returns are filed in 2027. It replaces terms like assessment year with tax year and renumbers sections."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-efiling p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "Income Tax e-Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Income Tax e-Filing",
  "alternateName": ["ITR e-filing", "Online income tax return filing", "File ITR online"],
  "serviceType": "Online filing of income tax returns (ITR-1 to ITR-4) on the Income Tax e-filing portal",
  "description": "Self e-filing and CA-assisted filing of income tax returns for individuals, HUFs and small businesses, including AIS and Form 26AS reconciliation, regime comparison, e-verification, refund tracking and replies to intimations.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "PeopleAudience", "audienceType": "Salaried individuals, pensioners, investors, freelancers and small businesses in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Income Tax e-Filing Plans", "itemListElement": [
    {"@type": "Offer", "name": "Self e-File", "price": "0", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "CA-Assisted Filing", "price": "2499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Capital Gains & Business", "price": "3499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to e-file your income tax return", "totalTime": "PT1H",
  "supply": [{"@type": "HowToSupply", "name": "PAN linked with Aadhaar"}, {"@type": "HowToSupply", "name": "Form 16, AIS and Form 26AS"},
             {"@type": "HowToSupply", "name": "Bank, capital gains and deduction statements"}, {"@type": "HowToSupply", "name": "Pre-validated bank account for the refund"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Collect your documents", "text": "Download Form 16 from your employer and the AIS and Form 26AS from the e-filing portal, and gather bank and capital gains statements."},
   {"@type": "HowToStep", "position": 2, "name": "Choose the ITR form", "text": "Pick ITR-1, ITR-2, ITR-3 or ITR-4 based on your income sources, residential status and total income."},
   {"@type": "HowToStep", "position": 3, "name": "Compare the tax regimes", "text": "Compute tax under the new and the old regime and choose the lower one where you are allowed to."},
   {"@type": "HowToStep", "position": 4, "name": "Pay tax and file", "text": "Pay any balance tax by challan, fill in the return on incometax.gov.in and submit it."},
   {"@type": "HowToStep", "position": 5, "name": "E-verify within 30 days", "text": "E-verify with Aadhaar OTP, net banking or a bank or demat account within 30 days of uploading, then track the refund."}]},
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
    <meta property="og:title" content="Income Tax e-Filing Online – File Your ITR" />
    <meta property="og:description" content="File free yourself or with a CA. AIS import, regime comparison, e-verification and refund tracking included." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Income Tax e-Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Income Tax e-Filing Online – File Your ITR" />
    <meta name="twitter:description" content="File your ITR online, free or with a CA. Belated returns open till 31 December 2026." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "income-tax-e-filing"')
assert 'service: "income-tax-e-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="income-tax-e-filing"')
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
