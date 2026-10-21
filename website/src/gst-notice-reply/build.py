# Builds gst-notice-reply/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/gst-notice-reply/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/gst-notice-reply/"
TITLE = "GST Notice Reply Online: CA-Reviewed | Bharat e-Filing"
DESC = "Got a GST notice? Reply to ASMT-10, DRC-01, DRC-01B/01C, GSTR-3A or REG-17 with CA-reviewed drafting, reconciliations, hearing support and appeals."
OG = "https://bharatefiling.com/wp-content/uploads/og/gst-notice-reply-1200x630.jpg"
PUB = "2026-10-21"
SLUG = "gst-notice-reply"

FAQ = [
 ("What is a GST notice?", "A GST notice is a written communication from a GST officer, issued on the GST portal, asking you to explain a mismatch, file a pending return, pay a tax shortfall or show cause why a demand, penalty or cancellation should not be made. Each notice names its form, the section of law and the date by which you must reply."),
 ("How do I check if a GST notice is genuine?", "Every genuine notice appears on the GST portal under Services, User Services, View Notices and Orders, or in the Additional Notices and Orders tab. Communications from CBIC officers also carry a Document Identification Number (DIN) that you can verify on the CBIC website. Never pay through a link in an email or SMS."),
 ("What is the time limit to reply to a GST notice?", "It depends on the form: 30 days for scrutiny notice ASMT-10, 7 days for DRC-01B and DRC-01C mismatch intimations, 7 working days for REG-17 and REG-03, 15 days to file the return after GSTR-3A, and the period stated in a show cause notice in DRC-01, usually 30 days. Officers can allow more time on request."),
 ("What happens if I do not reply to a GST notice?", "The officer can pass an order ex parte on the information available, raising a demand with interest and penalty. Unanswered DRC-01B or DRC-01C intimations block your next GSTR-1, an unanswered REG-17 can lead to cancellation of registration, and unpaid demands can be recovered under Section 79, including by attaching bank accounts."),
 ("What is an ASMT-10 notice?", "ASMT-10 is issued after scrutiny of your returns under Section 61 and Rule 99 when the officer finds discrepancies, for example between GSTR-1, GSTR-3B and GSTR-2B. You reply in Form ASMT-11 within 30 days, either explaining the difference or paying any tax due with interest. If the explanation is accepted, the matter closes; otherwise proceedings under Section 73, 74 or 74A can follow."),
 ("What is a DRC-01 show cause notice?", "DRC-01 is the summary of a show cause notice proposing a tax demand with interest and penalty under Section 73, 74 or 74A. You reply in Form DRC-06 with your submissions and documents, and you can ask for a personal hearing, which Section 75(4) requires when an adverse decision is contemplated."),
 ("What is Section 74A of the CGST Act?", "Section 74A, inserted by the Finance (No. 2) Act, 2024, replaces Sections 73 and 74 for demands relating to FY 2024-25 onwards. A show cause notice can be issued within 42 months of the due date of the annual return, and the order is due within 12 months of the notice, extendable by up to 6 months. In non-fraud cases, paying the tax with interest within 60 days of the notice means no penalty."),
 ("What are DRC-01B and DRC-01C notices?", "DRC-01B (Rule 88C) flags tax shown in GSTR-1 that is higher than tax paid in GSTR-3B, and DRC-01C (Rule 88D) flags input tax credit claimed in GSTR-3B that is higher than GSTR-2B. Within 7 days you must pay the difference through DRC-03 or explain it in Part B, otherwise your next GSTR-1 is blocked."),
 ("What is a REG-17 notice?", "REG-17 is a show cause notice proposing cancellation of your GST registration, for example for not filing returns or not operating from the declared address. You reply in Form REG-18 within 7 working days. If cancellation is ordered, you can apply for revocation within the time allowed by Section 30."),
 ("Can I appeal against a GST order?", "Yes. You can file a first appeal in Form APL-01 within 3 months of the order under Section 107, extendable by 1 month for sufficient cause, after paying the admitted tax and a pre-deposit of 10% of the disputed tax. Further appeals lie to the GST Appellate Tribunal (GSTAT), which is now hearing appeals."),
 ("Can I avoid penalty by paying before the order?", "Often, yes. In non-fraud cases, paying the tax and interest within 30 days of a Section 73 notice, or within 60 days of a Section 74A notice, closes the proceedings without penalty. In fraud cases, early payment reduces the penalty to 15% before the notice and 25% within 60 days of it."),
 ("Do GST notices affect my income-tax return?", "They can. GST turnover is compared with the turnover in your income-tax return, AIS and tax audit report, so a mismatch can trigger questions under both laws. From 1 April 2026 the Income-tax Act, 2025 applies; tax audit under section 44AB moves to section 63."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-gst-notice p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "GST Services", "item": "https://bharatefiling.com/product-category/gst/"},
   {"@type": "ListItem", "position": 3, "name": "GST Notice Reply"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "GST Notice Reply",
  "alternateName": ["Reply to GST notice", "GST show cause notice reply", "ASMT-10 reply", "DRC-01 reply"],
  "serviceType": "Drafting and filing replies to GST notices, show cause notices and appeals",
  "description": "CA-reviewed replies to GST notices including ASMT-10, DRC-01A, DRC-01, DRC-01B, DRC-01C, GSTR-3A and REG-17, with reconciliations, personal hearing support and first appeals under Section 107.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "GST-registered businesses, proprietors, companies and e-commerce sellers who received a GST notice"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "GST Notice Reply Plans", "itemListElement": [
    {"@type": "Offer", "name": "Intimation Reply", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Show Cause Defence", "price": "7999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Appeal", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to reply to a GST notice online", "totalTime": "P7D",
  "supply": [{"@type": "HowToSupply", "name": "Copy of the notice and its reference number"}, {"@type": "HowToSupply", "name": "GST returns for the period (GSTR-1, GSTR-3B, GSTR-9)"},
             {"@type": "HowToSupply", "name": "Books of accounts, invoices and reconciliations"}, {"@type": "HowToSupply", "name": "GST portal login and DSC or EVC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Find the notice on the portal", "text": "Log in to the GST portal and open Services, User Services, View Notices and Orders, or the Additional Notices and Orders tab, to confirm the notice is genuine."},
   {"@type": "HowToStep", "position": 2, "name": "Identify the form and deadline", "text": "Note the form (for example ASMT-10, DRC-01 or REG-17), the section invoked, the amount proposed and the reply due date."},
   {"@type": "HowToStep", "position": 3, "name": "Reconcile and gather evidence", "text": "Reconcile returns, books, GSTR-2B and e-way bills for the period and collect invoices and documents that explain each difference."},
   {"@type": "HowToStep", "position": 4, "name": "Draft and file the reply", "text": "Draft a point-wise reply citing the law, attach documents and file it in the prescribed form (ASMT-11, DRC-06, REG-18 or Part B of DRC-01B/01C) signed with DSC or EVC."},
   {"@type": "HowToStep", "position": 5, "name": "Attend the hearing and track the order", "text": "Attend any personal hearing, track the order and, if it goes against you, file an appeal in APL-01 within 3 months."}]},
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
    <meta property="og:title" content="GST Notice Reply Online – Expert Replies, Hearings and Appeals" />
    <meta property="og:description" content="Reply to any GST notice with CA-reviewed drafting: ASMT-10, DRC-01, DRC-01B/01C, GSTR-3A, REG-17 and appeals." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – GST Notice Reply" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="GST Notice Reply Online – CA-Reviewed Replies" />
    <meta name="twitter:description" content="Scrutiny, show cause, mismatch and cancellation notices answered by GST experts, checked by a CA." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "gst-notice-reply"')
assert 'service: "gst-notice-reply"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="gst-notice-reply"')
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
