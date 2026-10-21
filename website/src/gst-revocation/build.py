# Builds gst-revocation/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/gst-revocation/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/gst-revocation/"
TITLE = "GST Revocation of Cancellation Online | Bharat e-Filing"
DESC = "GST registration cancelled by the officer? Apply for revocation in REG-21 within 90 days. Pending returns, dues, officer replies and appeals handled by experts."
OG = "https://bharatefiling.com/wp-content/uploads/og/gst-revocation-1200x630.jpg"
PUB = "2026-10-21"
SLUG = "gst-revocation"

FAQ = [
 ("What is revocation of GST registration cancellation?", "Revocation is the process of restoring a GST registration that the proper officer cancelled on their own motion, for example for not filing returns. It is governed by Section 30 of the CGST Act and Rule 23 of the CGST Rules, and you apply on the GST portal in Form GST REG-21."),
 ("What is the time limit to apply for GST revocation?", "You must apply in Form REG-21 within 90 days of the date of service of the cancellation order. On sufficient cause, the Commissioner or an authorised officer not below the rank of Joint or Additional Commissioner can extend this by up to 180 more days."),
 ("Can I apply for revocation if I cancelled my registration voluntarily?", "No. Revocation under Section 30 applies only when the officer cancelled the registration on their own motion. If you surrendered it yourself, you need to apply for a fresh registration."),
 ("Do I need to file pending returns before applying for revocation?", "Yes. If your registration was cancelled for not filing returns, you must file all pending returns and pay the tax, interest, late fee and any penalty before applying. The application is not entertained while those returns are outstanding."),
 ("How long does the officer take to decide a revocation application?", "If satisfied, the officer revokes the cancellation in Form REG-22 within 30 days of receiving the application. If the officer plans to reject it, they first issue a show cause notice in REG-23, you reply in REG-24 within 7 working days, and the officer decides within 30 days of your reply."),
 ("What do I do after my registration is restored?", "Under Rule 23, file all returns for the period from the date of cancellation to the date of the revocation order within 30 days of the revocation order. Then resume your regular GSTR-1 and GSTR-3B filing."),
 ("What if the 90-day revocation period has passed?", "Within the next 180 days, you can ask the Commissioner to extend the time for sufficient cause. After that, the options are an appeal against the cancellation order in APL-01 within 3 months of the order (extendable by 1 month), a writ petition before the High Court in suitable cases, or a fresh registration."),
 ("Can old pending returns block revocation?", "They can. Since the 3-year time limit was enforced on the GST portal, a return cannot be filed more than three years after its due date. If a pending return is already time-barred, the usual condition of filing all returns cannot be met, so expert advice is needed on appeal or other remedies."),
 ("Can I appeal against cancellation instead of applying for revocation?", "Yes. You can appeal against the cancellation order before the appellate authority in Form APL-01 within 3 months of the order under Section 107, extendable by 1 month for sufficient cause. Revocation is usually faster when the reason for cancellation, such as non-filing, can be cured."),
 ("What happens to my business while the registration is cancelled?", "You cannot collect GST, issue tax invoices or generate e-way bills, your buyers cannot claim input tax credit on your supplies, and continuing to make taxable supplies without registration can attract tax, interest and penalty. Restoring the registration quickly limits this damage."),
 ("What documents are needed for GST revocation?", "You need the cancellation order (REG-19) and show cause notice (REG-17), proof that pending returns are filed and dues paid, the reason for the default with supporting evidence, and GST portal access with DSC or EVC. Where cancellation was for not operating from the declared address, you also need current address proof."),
 ("Does the Income-tax Act, 2025 affect GST revocation?", "No. Revocation is a GST process and is unchanged. From 1 April 2026 the Income-tax Act, 2025 replaces the 1961 Act, so keep your turnover consistent across GST returns filed for the gap period and your income-tax return."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-revocation p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "GST Services", "item": "https://bharatefiling.com/product-category/gst/"},
   {"@type": "ListItem", "position": 3, "name": "GST Revocation"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "GST Revocation",
  "alternateName": ["Revocation of GST cancellation", "Form GST REG-21", "Restore cancelled GST registration"],
  "serviceType": "Revocation of cancellation of GST registration in Form GST REG-21",
  "description": "CA-reviewed revocation of cancelled GST registration under Section 30 of the CGST Act and Rule 23, including filing of pending returns, payment of dues, replies to REG-23 notices, extension requests and appeals.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Businesses whose GST registration was cancelled by the GST officer"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "GST Revocation Plans", "itemListElement": [
    {"@type": "Offer", "name": "Revocation", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Revocation + Returns", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Complex Cases", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to apply for revocation of GST cancellation", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Cancellation order (REG-19) and show cause notice (REG-17)"}, {"@type": "HowToSupply", "name": "All pending returns filed and dues paid"},
             {"@type": "HowToSupply", "name": "Reason for the default with supporting evidence"}, {"@type": "HowToSupply", "name": "GST portal login and DSC or EVC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check the cancellation order", "text": "Download the cancellation order and note the date of service, the reason and the effective date of cancellation."},
   {"@type": "HowToStep", "position": 2, "name": "File pending returns and pay dues", "text": "File every pending return up to the date of cancellation and pay tax, interest, late fee and any penalty."},
   {"@type": "HowToStep", "position": 3, "name": "Apply in REG-21", "text": "On the GST portal go to Services, Registration, Application for Revocation of Cancelled Registration, give the reasons, attach documents and sign with DSC or EVC within 90 days."},
   {"@type": "HowToStep", "position": 4, "name": "Reply to any REG-23 notice", "text": "If the officer issues a show cause notice in REG-23, reply in REG-24 within 7 working days."},
   {"@type": "HowToStep", "position": 5, "name": "File returns after revocation", "text": "Once revoked in REG-22, file the returns for the period between cancellation and revocation within 30 days and resume regular filing."}]},
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
    <meta property="og:title" content="GST Revocation Online – Restore Your Cancelled GSTIN" />
    <meta property="og:description" content="Apply in REG-21 within 90 days. Pending returns, dues, officer replies and appeals handled by GST experts, checked by a CA." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – GST Revocation" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="GST Revocation of Cancellation Online" />
    <meta name="twitter:description" content="GSTIN cancelled? Restore it in REG-21 within 90 days, with pending returns filed by experts." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "gst-revocation"')
assert 'service: "gst-revocation"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="gst-revocation"')
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
