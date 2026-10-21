# Builds gstr-10-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/gstr-10-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/gstr-10-filing/"
TITLE = "GSTR-10 Final Return Filing Online | Bharat e-Filing"
DESC = "GST registration cancelled? File the GSTR-10 final return within 3 months and avoid a ₹200/day late fee. Stock reversal, dues and notices handled by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/gstr-10-filing-1200x630.jpg"
PUB = "2026-10-21"
SLUG = "gstr-10-filing"

FAQ = [
 ("What is GSTR-10?", "GSTR-10 is the final return that a registered person must file once their GST registration is cancelled. It is required by Section 45 of the CGST Act and Rule 81 of the CGST Rules, and it reports the stock and capital goods held on the day before cancellation and the tax payable on them."),
 ("Who has to file GSTR-10?", "Every normal taxpayer who filed returns under Section 39(1) and whose registration is cancelled, whether they surrendered it voluntarily or the officer cancelled it. Composition taxpayers, input service distributors, non-resident taxable persons and persons deducting or collecting tax at source do not file GSTR-10."),
 ("What is the due date for GSTR-10?", "GSTR-10 must be filed within three months of the date of cancellation or the date of the cancellation order, whichever is later."),
 ("What is the late fee for not filing GSTR-10 on time?", "Under Section 47, the late fee is ₹100 a day under CGST and ₹100 a day under SGST or UTGST, a total of ₹200 a day, capped at ₹5,000 under each Act, so ₹10,000 in all. Interest at 18% a year under Section 50 also applies to any tax paid late."),
 ("What happens if I do not file GSTR-10?", "The officer issues a notice in Form GSTR-3A asking you to file within 15 days. If you still do not file, the officer can assess your liability to the best of their judgement under Section 62 and raise a demand with interest and penalty."),
 ("Can a best judgement assessment order be withdrawn?", "Yes. Under Section 62(2), the assessment order is deemed withdrawn if you file a valid return within 60 days of its service. This can be extended by a further 60 days on payment of an additional late fee of ₹100 a day, but the late fee and interest on the tax remain payable."),
 ("What details are reported in GSTR-10?", "You report the inputs, semi-finished goods, finished goods and capital goods held in stock on the day immediately before the effective date of cancellation, with the tax involved, and pay the resulting liability along with any interest and late fee."),
 ("How is the tax on closing stock calculated?", "Under Section 29(5), you pay the higher of the input tax credit on the inputs, semi-finished and finished goods in stock and the output tax payable on those goods. For capital goods, you pay the higher of the credit reduced by 5 percentage points for every quarter or part of a quarter since the invoice date and the tax on their transaction value."),
 ("I have no stock left. Do I still need to file GSTR-10?", "Yes. GSTR-10 must be filed even if there is no closing stock and no tax to pay. You file it with nil values to close your compliance on the cancelled registration."),
 ("Is GSTR-10 the same as GSTR-9 annual return?", "No. GSTR-9 is the annual return for a financial year, while GSTR-10 is a one-time final return filed after cancellation. You may still need to file GSTR-9 for the year of cancellation if you are otherwise required to."),
 ("What do I need to file GSTR-10?", "You need the cancellation order and its effective date, a stock statement as on the day before cancellation with purchase invoices, the list of capital goods with invoice dates and credit taken, your last filed returns, and GST portal access with DSC or EVC."),
 ("Does the Income-tax Act, 2025 affect GSTR-10?", "No. GSTR-10 is a GST return and is unchanged. From 1 April 2026 the Income-tax Act, 2025 replaces the 1961 Act, so keep the closing stock in your final GST return consistent with the closing stock in your books and income-tax return."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-gstr-10 p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "GST Services", "item": "https://bharatefiling.com/product-category/gst/"},
   {"@type": "ListItem", "position": 3, "name": "GSTR-10 Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "GSTR-10 Filing",
  "alternateName": ["GST final return", "Form GSTR-10", "Final return after GST cancellation"],
  "serviceType": "Filing of the GST final return in Form GSTR-10",
  "description": "CA-reviewed filing of the GSTR-10 final return under Section 45 of the CGST Act and Rule 81, including closing stock and capital goods reversal under Section 29(5), late fee computation and replies to GSTR-3A notices and best judgement assessments.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Businesses whose GST registration has been cancelled"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "GSTR-10 Filing Plans", "itemListElement": [
    {"@type": "Offer", "name": "GSTR-10 Filing", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "GSTR-10 + Stock Reversal", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Notice & Assessment", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file GSTR-10 final return", "totalTime": "P3D",
  "supply": [{"@type": "HowToSupply", "name": "Cancellation order with the effective date"}, {"@type": "HowToSupply", "name": "Stock statement as on the day before cancellation"},
             {"@type": "HowToSupply", "name": "Capital goods list with invoice dates and credit taken"}, {"@type": "HowToSupply", "name": "GST portal login and DSC or EVC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Note the due date", "text": "Check the cancellation order and note the later of the date of cancellation and the date of the order. GSTR-10 is due within three months of it."},
   {"@type": "HowToStep", "position": 2, "name": "Prepare the stock statement", "text": "List inputs, semi-finished goods, finished goods and capital goods held on the day before cancellation, with invoices and the credit taken."},
   {"@type": "HowToStep", "position": 3, "name": "Compute the liability", "text": "Under Section 29(5), take the higher of the credit on stock and the output tax on it, and for capital goods the higher of the reduced credit and the tax on transaction value."},
   {"@type": "HowToStep", "position": 4, "name": "File GSTR-10 and pay", "text": "On the GST portal go to Services, Returns, Final Return, enter the details, pay the tax, interest and late fee, and file with DSC or EVC."},
   {"@type": "HowToStep", "position": 5, "name": "Keep the acknowledgement", "text": "Download the filed return and ARN, and keep the stock workings for any later scrutiny."}]},
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
    <meta property="og:title" content="GSTR-10 Final Return Filing Online" />
    <meta property="og:description" content="File your final return within 3 months of cancellation. Stock reversal, late fee and GSTR-3A notices handled by GST experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – GSTR-10 Filing" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="GSTR-10 Final Return Filing Online" />
    <meta name="twitter:description" content="GST registration cancelled? File GSTR-10 within 3 months and avoid the ₹200 a day late fee." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "gstr-10-filing"')
assert 'service: "gstr-10-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="gstr-10-filing"')
globalnav = cut("    <!-- ================= GLOBAL NAV", "    <!-- ================= LOCAL NAV")
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
