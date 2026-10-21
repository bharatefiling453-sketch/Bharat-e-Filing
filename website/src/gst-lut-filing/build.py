# Builds gst-lut-filing/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/gst-lut-filing/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/gst-lut-filing/"
TITLE = "GST LUT Filing Online (Form RFD-11) | Bharat e-Filing"
DESC = "File your GST LUT in Form RFD-11 online and export goods or services without paying IGST. CA-reviewed filing, ARN in 24 hours, renewals and refund help."
OG = "https://bharatefiling.com/wp-content/uploads/og/gst-lut-filing-1200x630.jpg"
PUB = "2026-10-21"

FAQ = [
 ("What is LUT in GST?", "A Letter of Undertaking (LUT) is a declaration filed in Form GST RFD-11 under Rule 96A of the CGST Rules. It lets a registered exporter make zero-rated supplies, meaning exports of goods or services and supplies to SEZ units or developers, without paying IGST, and then claim a refund of unutilised input tax credit."),
 ("Who can file an LUT under GST?", "Any GST-registered person making zero-rated supplies can file an LUT, except a person who has been prosecuted for tax evasion of ₹2.5 crore or more under the CGST Act, the IGST Act or any earlier indirect tax law (Notification 37/2017-Central Tax). Those persons must export under a bond instead."),
 ("What is the validity of an LUT?", "An LUT is valid for one financial year, from 1 April to 31 March. A fresh LUT has to be filed for every financial year, so the LUT for FY 2026-27 expires on 31 March 2027."),
 ("What is the last date to file the LUT for FY 2026-27?", "File it before your first export of the financial year, ideally by 31 March of the previous year. If you missed it, file as soon as possible: CBIC Circular 37/11/2018-GST allows a delay in furnishing the LUT to be condoned on an ex post facto basis depending on the facts, so take advice for exports made before filing."),
 ("What documents are needed to file an LUT?", "You need your GSTIN and GST portal login, the authorised signatory’s details and DSC or EVC, the names, addresses and occupations of two independent witnesses, and, for exports of goods, your Import Export Code (IEC). If you filed an LUT last year, keep its ARN handy."),
 ("Who signs the LUT?", "The LUT is signed by the proprietor, a working partner, the managing director, the company secretary or a person authorised by the working partner or board of directors, using a digital signature certificate (DSC) or an electronic verification code (EVC)."),
 ("Is the LUT approved by an officer?", "No separate approval is needed. Under CBIC Circular 8/8/2017-GST, the LUT is deemed accepted as soon as the acknowledgement (ARN) is generated on the GST portal."),
 ("What happens if goods are not exported within 3 months or payment is not received within 1 year?", "Under Rule 96A, if goods are not exported within 3 months of the invoice date, or payment for exported services is not received within 1 year, or any longer period allowed by the Commissioner, you must pay the IGST with 18% interest within 15 days. Otherwise the LUT facility can be withdrawn until the amount is paid."),
 ("Can I export without an LUT?", "Yes, by furnishing a bond, usually with a bank guarantee, or by paying IGST and claiming it back. Since 1 October 2023, Section 16 of the IGST Act limits the IGST-paid route to notified goods and persons, so for most exporters the LUT or bond is now the standard route."),
 ("Do supplies to an SEZ need an LUT?", "Yes. Supplies to an SEZ unit or developer for authorised operations are zero-rated under Section 16 of the IGST Act. With an LUT you can invoice them without IGST, with the endorsement Rule 46 requires on the invoice."),
 ("Do freelancers exporting services need an LUT?", "If you are GST-registered and bill foreign clients, yes. Filing an LUT lets you invoice without IGST, provided the supply meets the export of services conditions in Section 2(6) of the IGST Act, including payment in convertible foreign exchange or in Indian rupees where RBI permits."),
 ("How do I get a refund after exporting under LUT?", "File Form GST RFD-01 for refund of unutilised input tax credit under Rule 89(4) within 2 years of the relevant date (Section 54). For zero-rated supplies, 90% of the claim can be granted provisionally, usually within 7 days of the acknowledgement (Section 54(6) and Rule 91)."),
 ("Does the Income-tax Act, 2025 change anything for exporters under LUT?", "The LUT itself is a GST procedure and is unchanged. From 1 April 2026 the Income-tax Act, 2025 replaces the 1961 Act for your export income; ‘previous year’ becomes ‘tax year’ and tax audit under section 44AB moves to section 63. Your GST export turnover should reconcile with the turnover in your income-tax return."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-lut p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "GST Services", "item": "https://bharatefiling.com/product-category/gst/"},
   {"@type": "ListItem", "position": 3, "name": "GST LUT Filing"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "GST LUT Filing",
  "alternateName": ["Letter of Undertaking under GST", "Form GST RFD-11", "LUT for export without IGST"],
  "serviceType": "Filing of Letter of Undertaking (LUT) in Form GST RFD-11",
  "description": "CA-reviewed filing of the Letter of Undertaking in Form GST RFD-11 under Rule 96A of the CGST Rules, so exporters and SEZ suppliers can make zero-rated supplies without paying IGST, with renewal reminders and refund support.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Exporters of goods and services, freelancers with foreign clients and suppliers to SEZ units"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "GST LUT Filing Plans", "itemListElement": [
    {"@type": "Offer", "name": "LUT Filing", "price": "999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Exporter", "price": "2499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Refund Pro", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to file a GST LUT (Form RFD-11) online", "totalTime": "PT1H",
  "supply": [{"@type": "HowToSupply", "name": "GSTIN and GST portal login"}, {"@type": "HowToSupply", "name": "Authorised signatory with DSC or EVC"},
             {"@type": "HowToSupply", "name": "Name, address and occupation of two independent witnesses"}, {"@type": "HowToSupply", "name": "Import Export Code (for exports of goods)"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Open the LUT form", "text": "Log in to the GST portal and go to Services, User Services, Furnish Letter of Undertaking (LUT)."},
   {"@type": "HowToStep", "position": 2, "name": "Choose the financial year", "text": "Select the financial year for which the LUT is being furnished and upload last year’s LUT if required."},
   {"@type": "HowToStep", "position": 3, "name": "Tick the declarations", "text": "Accept the three self-declarations covering export within the allowed time, compliance with GST law and payment of tax with interest on failure."},
   {"@type": "HowToStep", "position": 4, "name": "Add witnesses and signatory", "text": "Enter the name, address and occupation of two independent witnesses, and the place and date of filing."},
   {"@type": "HowToStep", "position": 5, "name": "Sign and download the acknowledgement", "text": "Sign with DSC or EVC. The ARN is generated at once and the LUT is deemed accepted; download it and quote it on export invoices."}]},
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
    <meta property="og:title" content="GST LUT Filing Online – Export Without Paying IGST" />
    <meta property="og:description" content="File Form GST RFD-11 with a CA-reviewed application. ARN in 24 hours, renewal reminders and refund help for exporters." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – GST LUT Filing Online" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="GST LUT Filing Online – Export Without Paying IGST" />
    <meta name="twitter:description" content="Form GST RFD-11 filed by experts, checked by a CA. For exporters, freelancers and SEZ suppliers." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "gst-lut-filing"')
assert 'service: "gst-lut-filing"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="gst-lut-filing"')
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
os.makedirs("gst-lut-filing", exist_ok=True)
open("gst-lut-filing/index.html", "w").write(out)
print("built gst-lut-filing/index.html", len(out))
