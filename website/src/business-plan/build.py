# Builds business-plan/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/business-plan/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/business-plan/"
TITLE = "Business Plan and Project Report | Bharat e-Filing"
DESC = "Get a bank-ready business plan or project report: market research, 5-year projections, DSCR and break-even, for Mudra, PMEGP, term loans and investors."
OG = "https://bharatefiling.com/wp-content/uploads/og/business-plan-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "business-plan"

FAQ = [
 ("What is a business plan?", "A business plan is a written document that explains what a business will do, who its customers are, how it will operate and compete, who runs it, and how it will make money, with projected financial statements and the funding it needs."),
 ("Is a project report the same as a business plan?", "They overlap. A project report, often called a detailed project report or DPR, is the version banks and government schemes ask for. It focuses on the project cost, means of finance, projected profit and cash flow, and the ability to repay the loan."),
 ("What does a business plan contain?", "An executive summary, the business and its products, market and competition, marketing and sales, operations, the team, the project cost and funding plan, and projected profit and loss, balance sheet and cash flow, with key ratios such as DSCR and break-even."),
 ("Which loans need a business plan or project report?", "Most business loans do, including term loans, working capital loans, loans under PM Mudra Yojana, PMEGP, and collateral-free loans backed by the CGTMSE guarantee. The detail expected grows with the loan size."),
 ("How much can be borrowed under PM Mudra Yojana?", "Shishu covers loans up to ₹50,000, Kishore above ₹50,000 up to ₹5 lakh, and Tarun above ₹5 lakh up to ₹10 lakh. Tarun Plus, from October 2024, covers ₹10 lakh to ₹20 lakh for borrowers who have repaid an earlier Tarun loan."),
 ("What are the PMEGP project limits?", "Under the guidelines for 2021-22 to 2025-26, the maximum project cost for the margin money subsidy is ₹50 lakh for manufacturing and ₹20 lakh for business or service units, with a subsidy of 15% to 35% depending on category and location. Check the KVIC PMEGP portal for the current scheme period."),
 ("What is DSCR and what do banks look for?", "The debt service coverage ratio compares the cash a business earns with the loan repayments and interest it must pay. A DSCR above 1 means earnings cover repayments. Many banks look for an average of around 1.25 to 1.5 or more, but each bank sets its own norms."),
 ("How many years of projections are needed?", "Usually three to five years for a loan, and often the full loan tenure for a term loan. Investors typically expect a three to five year financial model with the assumptions behind it."),
 ("Do projections need to be certified by a CA?", "Banks may ask for projected financials certified by a chartered accountant, often in the CMA data format, especially for larger or working capital loans. Smaller loans may need only the project report."),
 ("Is a business plan useful for investors?", "Yes. Investors expect a business plan or pitch deck with a financial model, the market size, the funding ask and how the money will be used. A DPIIT-recognised startup may also apply to schemes such as the Startup India Seed Fund Scheme through incubators."),
 ("How do taxes affect the projections?", "Projected profits should allow for income tax, which from tax year 2026-27 is under the Income-tax Act, 2025, and for GST where registration is required. The choice of structure, such as proprietorship, LLP or company, changes the tax and compliance costs in the plan."),
 ("Is my business information kept confidential?", "Yes. We use your information only to prepare your plan, protect it under the Digital Personal Data Protection Act, 2023, and can sign a non-disclosure agreement on request."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-bplan p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Start a Business", "item": "https://bharatefiling.com/business-registration/"},
   {"@type": "ListItem", "position": 3, "name": "Business Plan"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Business Plan and Project Report",
  "alternateName": ["Project report for bank loan", "Detailed project report", "DPR for Mudra loan", "PMEGP project report", "Business plan writing"],
  "serviceType": "Preparation of business plans, project reports and financial projections",
  "description": "Business plans and bank-ready project reports with market research, 3 to 5 year financial projections, DSCR and break-even analysis, for loans, government schemes and investors.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Founders and MSMEs in India seeking loans or investment"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Business Plan Plans", "itemListElement": [
    {"@type": "Offer", "name": "Project Report", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Business Plan Complete", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Investor Pitch Pack", "price": "19999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to prepare a business plan for a bank loan", "totalTime": "P7D",
  "supply": [{"@type": "HowToSupply", "name": "Business idea and products"}, {"@type": "HowToSupply", "name": "Quotations for machinery and premises"},
             {"@type": "HowToSupply", "name": "Expected prices, costs and sales"}, {"@type": "HowToSupply", "name": "Promoters' KYC and past financials, if any"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Define the goal", "text": "Decide who the plan is for: a bank, a government scheme or an investor, and how much funding is needed."},
   {"@type": "HowToStep", "position": 2, "name": "Research the market", "text": "Study customers, competitors and pricing to support the sales assumptions."},
   {"@type": "HowToStep", "position": 3, "name": "Work out the project cost", "text": "List the capital costs and working capital, and the means of finance: own funds, loan and any subsidy."},
   {"@type": "HowToStep", "position": 4, "name": "Build the projections", "text": "Prepare 3 to 5 years of projected profit and loss, balance sheet and cash flow, with DSCR and break-even."},
   {"@type": "HowToStep", "position": 5, "name": "Write and review", "text": "Write the plan, review the assumptions, and submit it with the loan application or to investors."}]},
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
    <meta property="og:title" content="Business Plan and Project Report" />
    <meta property="og:description" content="Bank-ready project reports and investor plans with 5-year projections, DSCR and break-even, by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Business Plan and Project Report" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Business Plan and Project Report" />
    <meta name="twitter:description" content="Need a loan or investor? Start with a plan that adds up." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "business-plan"')
assert 'service: "business-plan"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="business-plan"')
globalnav = cut("    <!-- ================= GLOBAL NAV", "    <!-- ================= LOCAL NAV").replace(
    '<a href="https://bharatefiling.com/product-category/gst/" aria-current="page">GST</a>', '<a href="https://bharatefiling.com/product-category/gst/">GST</a>').replace(
    '<a href="https://bharatefiling.com/business-registration/">Start a Business</a>', '<a href="https://bharatefiling.com/business-registration/" aria-current="page">Start a Business</a>')
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
