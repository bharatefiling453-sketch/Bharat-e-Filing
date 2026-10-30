# Builds professional-tax-return-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/professional-tax-return-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/professional-tax-return-filing/"
TITLE = "Professional Tax Return Filing | Bharat e-Filing"
DESC = "File professional tax returns on time: PTRC and PTEC in Maharashtra, Karnataka PT and other states, with slabs, due dates and payment, handled by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/professional-tax-return-filing-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "professional-tax-return-filing"

FAQ = [
 ("What is professional tax?", "Professional tax is a tax that states levy on professions, trades, callings and employments under Article 276 of the Constitution. The total professional tax payable by one person to a state cannot exceed ₹2,500 a year."),
 ("Who pays professional tax?", "Salaried employees pay it through their employer, who deducts it from salary and deposits it. Professionals, traders, businesses and companies pay their own professional tax after enrolling with the state."),
 ("Do all states levy professional tax?", "No. States such as Maharashtra, Karnataka, West Bengal, Tamil Nadu, Gujarat, Andhra Pradesh and Telangana levy it, each under its own law, rates and due dates. Some states and union territories, such as Delhi, do not levy it."),
 ("What are PTRC and PTEC in Maharashtra?", "PTRC is the registration certificate an employer needs to deduct and pay professional tax on employees' salaries and file returns. PTEC is the enrolment certificate under which a business, professional or company pays its own professional tax."),
 ("What are the Maharashtra salary slabs?", "For men, nil up to ₹7,500 a month, ₹175 a month from ₹7,501 to ₹10,000, and ₹200 a month above ₹10,000, with ₹300 in February. For women, nil up to ₹25,000 a month and ₹200 a month above that, with ₹300 in February, so the yearly total is ₹2,500."),
 ("What are the Karnataka salary slabs?", "From 1 April 2025, nil for monthly pay below ₹25,000, and ₹200 a month for ₹25,000 or more, with ₹300 in February, for a yearly total of ₹2,500."),
 ("When are Maharashtra PTRC returns due?", "Under the 2026 amendment to the Maharashtra rules, an employer whose tax liability in the previous year was ₹50,000 or more files and pays monthly by the 15th of the following month. Other employers file one annual return by 15 March."),
 ("Is professional tax deductible for income tax?", "A salaried person can deduct professional tax from salary income only under the old tax regime, not under the new regime. A business can claim the professional tax it pays as an expense in the year it is actually paid. From tax year 2026-27 these rules are under the Income-tax Act, 2025."),
 ("What happens if professional tax is paid or filed late?", "State laws charge interest for late payment and penalties or late fees for late returns or not registering. An employer who fails to deduct is liable for the tax as well. The amounts differ from state to state."),
 ("Are any people exempt?", "Each state lists its own exemptions. In Maharashtra, for example, they include people over 65 and people with a disability of 40% or more, subject to the conditions in the law."),
 ("What does an employer have to do?", "Register in each state where it has employees, deduct professional tax from salaries at the state's slab, deposit it by the due date, file returns, and keep salary and payment records for inspection."),
 ("What if a business has employees in more than one state?", "Professional tax follows the state where the employee works. The employer registers in each such state that levies the tax and follows that state's slabs, returns and due dates."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-pt p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Professional Tax Return Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Professional Tax Return Filing",
  "alternateName": ["PT return filing", "PTRC return filing", "PTEC payment", "Professional tax payment", "Karnataka PT return"],
  "serviceType": "Professional tax registration, payment and return filing under state laws",
  "description": "Professional tax compliance for employers and businesses: PTRC and PTEC in Maharashtra, Karnataka and other states, monthly and annual returns, and payment tracking.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Employers, professionals and businesses in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Professional Tax Plans", "itemListElement": [
    {"@type": "Offer", "name": "PT Return", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "PT Annual Compliance", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "PT Registration and Annual Compliance", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file a professional tax return as an employer", "totalTime": "P1D",
  "supply": [{"@type": "HowToSupply", "name": "PT registration number"}, {"@type": "HowToSupply", "name": "Salary register for the period"},
             {"@type": "HowToSupply", "name": "Professional tax deducted per employee"}, {"@type": "HowToSupply", "name": "Payment challans"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check your frequency", "text": "Work out from last year's liability whether you file monthly or annually under your state's rules."},
   {"@type": "HowToStep", "position": 2, "name": "Work out the tax", "text": "Apply the state's salary slabs to each employee's pay for the period."},
   {"@type": "HowToStep", "position": 3, "name": "Pay the tax", "text": "Pay the professional tax deducted online on the state's tax portal."},
   {"@type": "HowToStep", "position": 4, "name": "File the return", "text": "File the return on the state portal by the due date with the payment details."},
   {"@type": "HowToStep", "position": 5, "name": "Keep records", "text": "Keep the return, challans and salary records for inspection."}]},
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
    <meta property="og:title" content="Professional Tax Return Filing" />
    <meta property="og:description" content="PTRC, PTEC and state professional tax returns, slabs and due dates, handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Professional Tax Return Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Professional Tax Return Filing" />
    <meta name="twitter:description" content="Running payroll? File professional tax on time, in every state." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "professional-tax-return-filing"')
assert 'service: "professional-tax-return-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="professional-tax-return-filing"')
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
