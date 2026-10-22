# Builds llp-compliance/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/llp-compliance/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/llp-compliance/"
TITLE = "LLP Annual Compliance Online – Form 8 & 11 | Bharat e-Filing"
DESC = "Annual LLP compliance made simple: Form 11, Form 8, ITR-5, audit checks, partner changes and DIR-3 KYC filed on time by experts, with no ₹100 a day late fees."
OG = "https://bharatefiling.com/wp-content/uploads/og/llp-compliance-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "llp-compliance"

FAQ = [
 ("What is annual compliance for an LLP?", "Every limited liability partnership must file its annual return in Form 11 and its statement of account and solvency in Form 8 with the Registrar every year, file its income tax return in ITR-5, keep proper books of account, and get an audit where the limits are crossed. Event-based changes, such as new partners, are filed separately."),
 ("What are the due dates for LLP Form 11 and Form 8?", "Form 11 is due by 30 May, within 60 days of the end of the financial year. Form 8 is due by 30 October, within 30 days of the end of six months from the year end. For FY 2025-26, Form 11 was due by 30 May 2026 and Form 8 is due by 30 October 2026."),
 ("What is the late fee for LLP forms?", "Each form filed late attracts an additional fee of ₹100 a day, with no upper limit. A Form 8 filed a year late costs over ₹36,000 in additional fees alone, so filing on time matters."),
 ("Do LLPs need to file even if there is no business?", "Yes. Form 11, Form 8 and the income tax return must be filed every year, even if the LLP had no business or income. An inactive LLP can apply to be struck off, but must first be up to date with its filings."),
 ("When does an LLP need an audit?", "Under the LLP Act, an LLP's accounts must be audited if its turnover exceeds ₹40 lakh or its partners' contribution exceeds ₹25 lakh in the year. Separately, a tax audit under Section 44AB of the Income-tax Act applies when turnover exceeds ₹1 crore, or ₹10 crore if cash transactions are within 5%."),
 ("Who signs and certifies Form 8 and Form 11?", "Both forms are signed by designated partners with their DSCs. Form 8 is certified by a practising chartered accountant, company secretary or cost accountant. Form 11 must be certified by a practising company secretary when contribution exceeds ₹50 lakh or turnover exceeds ₹5 crore."),
 ("What is a small LLP?", "A small LLP is one whose partners' contribution does not exceed ₹25 lakh and turnover does not exceed ₹40 lakh, within the limits the LLP Act allows the government to prescribe. Small LLPs face lower penalties for many defaults."),
 ("What is the due date for an LLP's income tax return?", "An LLP files ITR-5. For FY 2025-26 the due date is 31 August 2026 if no tax audit is required, and 21 November 2026 for tax-audit cases, extended by CBDT Circular 7/2026. An LLP must file with the digital signature of a designated partner."),
 ("How do I add or remove a partner in an LLP?", "Report the change in Form 4 within 30 days, with the consent of the new partner, and file the change in the LLP agreement in Form 3 within 30 days of the change. Late filing attracts the same ₹100 a day additional fee."),
 ("Do designated partners need DIR-3 KYC?", "Yes. Designated partners hold a DIN, so they file DIR-3 KYC. From 31 March 2026, it is filed once every three financial years by 30 June, and any change in mobile number, email or address is updated within 30 days."),
 ("What happens if an LLP does not file for years?", "Fees of ₹100 a day keep running for each form, penalties apply to the LLP and designated partners, and the Registrar can strike off an LLP that is not carrying on business. Designated partners can also face disqualification. Clearing pending years in order is the way out."),
 ("Does the Income-tax Act, 2025 change LLP compliance?", "MCA compliance under the LLP Act is unchanged. For income tax, the Income-tax Act, 2025 applies from tax year 2026-27, so the LLP's tax filings for that year onwards follow the new section numbers."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-llp-compliance p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "LLP Compliance"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "LLP Annual Compliance",
  "alternateName": ["LLP annual filing", "LLP Form 8 and Form 11 filing", "LLP ROC compliance"],
  "serviceType": "Annual MCA and income tax compliance for limited liability partnerships",
  "description": "Annual compliance for LLPs under the LLP Act, 2008: Form 11 annual return, Form 8 statement of account and solvency, audit checks, partner and agreement changes in Forms 3 and 4, DIR-3 KYC for designated partners, and ITR-5 with Section 194T partner TDS.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Limited liability partnerships in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "LLP Compliance Plans", "itemListElement": [
    {"@type": "Offer", "name": "Small LLP", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "LLP Annual Compliance", "price": "11999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "LLP Complete with Accounts & Tax", "price": "24999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to complete annual compliance for an LLP", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "LLP agreement and partner details"}, {"@type": "HowToSupply", "name": "Books of account and, if required, audited accounts"},
             {"@type": "HowToSupply", "name": "Contribution and turnover figures"}, {"@type": "HowToSupply", "name": "DSCs of two designated partners"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "File Form 11", "text": "File the annual return in Form 11 with partner and contribution details by 30 May."},
   {"@type": "HowToStep", "position": 2, "name": "Close and audit the accounts", "text": "Finalise the books and get the accounts audited if turnover exceeds ₹40 lakh or contribution exceeds ₹25 lakh."},
   {"@type": "HowToStep", "position": 3, "name": "File the income tax return", "text": "File ITR-5 with the designated partner's DSC by the due date, after any tax audit."},
   {"@type": "HowToStep", "position": 4, "name": "File Form 8", "text": "File the statement of account and solvency in Form 8 by 30 October, signed by designated partners and certified by a practising professional."},
   {"@type": "HowToStep", "position": 5, "name": "Report changes during the year", "text": "File Form 4 for partner changes and Form 3 for agreement changes within 30 days, and keep DIR-3 KYC current."}]},
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
    <meta property="og:title" content="LLP Annual Compliance Online – Form 8 &amp; 11" />
    <meta property="og:description" content="Form 11, Form 8, ITR-5, audit checks and partner changes for your LLP, filed on time by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – LLP Compliance" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="LLP Annual Compliance Online – Form 8 &amp; 11" />
    <meta name="twitter:description" content="LLP Form 8 is due 30 October. Avoid ₹100 a day: let experts file it." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "llp-compliance"')
assert 'service: "llp-compliance"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="llp-compliance"')
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
