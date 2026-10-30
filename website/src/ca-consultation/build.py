# Builds ca-consultation/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/ca-consultation/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/ca-consultation/"
TITLE = "CA Consultation Online – Talk to a CA | Bharat e-Filing"
DESC = "Talk to a practising CA by phone or video on income tax, capital gains, GST, business set-up or a tax notice, and get a written summary of the advice."
OG = "https://bharatefiling.com/wp-content/uploads/og/ca-consultation-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "ca-consultation"

FAQ = [
 ("What is a CA consultation?", "A one-to-one session with a practising chartered accountant, by phone or video, to get answers on income tax, GST, business set-up, accounts or a tax notice. You get advice on your own facts and a written summary of what to do next."),
 ("What can I ask a CA?", "Anything on income tax returns, capital gains, deductions and tax planning, advance tax, GST registration and returns, starting or structuring a business, company and LLP compliance, tax notices, NRI taxation, and accounts or audit questions."),
 ("How does the consultation work?", "You choose a plan and share your question. We assign a CA who fits your topic, you upload documents if needed, the CA calls or video-calls you at the booked time, and you receive a written summary of the advice within 24 hours."),
 ("How long is a consultation?", "A quick call is 30 minutes and suits one focused question. An expert consultation is 60 minutes on video and suits planning, capital gains, business or notice questions. Ongoing needs are better served by a monthly advisory plan."),
 ("Is my information kept confidential?", "Yes. Chartered accountants are bound by the confidentiality rules of the ICAI Code of Ethics, and we handle your data under the Digital Personal Data Protection Act, 2023. We use your documents only to advise you."),
 ("How do I know the CA is genuine?", "Every consultation is with a practising member of the Institute of Chartered Accountants of India. We share the CA's name and membership number, which you can verify on the ICAI website."),
 ("What should I keep ready for the call?", "Your PAN, the question you want answered, and relevant papers such as Form 16, the annual information statement, bank or capital gains statements, GST returns, or the notice you received. Share them before the call so the CA can prepare."),
 ("Which income tax law applies now?", "The Income-tax Act, 2025 applies from 1 April 2026, and the old previous year and assessment year are replaced by a single tax year, starting with tax year 2026-27. Returns for financial year 2025-26 are still filed under the Income-tax Act, 1961."),
 ("Who needs to pay advance tax?", "Anyone whose tax for the year, after TDS and TCS, is ₹10,000 or more pays advance tax in instalments by 15 June, 15 September, 15 December and 15 March. Resident senior citizens without business income are exempt, and presumptive taxpayers can pay the full amount by 15 March."),
 ("Can a CA help after I receive a tax notice?", "Yes. A CA reads the notice, checks the deadline and the facts, and tells you how to respond. If you want, we can also draft and file the reply as a separate service."),
 ("Can I get a consultation in Hindi?", "Yes. Consultations are available in Hindi and English, by phone or video, and the written summary can be shared in either language."),
 ("Will the CA also file my return or do the work?", "The consultation is advice. If you want us to do the work, such as filing a return, GST compliance or replying to a notice, the CA explains the service and its fee before you decide."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-consult p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Income Tax", "item": "https://bharatefiling.com/income-tax/"},
   {"@type": "ListItem", "position": 3, "name": "CA Consultation"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "CA Consultation",
  "alternateName": ["Talk to a CA online", "Chartered accountant consultation", "Online tax consultation", "CA advice on call"],
  "serviceType": "Consultation with a chartered accountant",
  "description": "One-to-one phone or video consultations with practising chartered accountants on income tax, capital gains, advance tax, GST, business set-up, company compliance and tax notices, with a written summary of the advice.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "Audience", "audienceType": "Individuals, professionals, NRIs and businesses in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "CA Consultation Plans", "itemListElement": [
    {"@type": "Offer", "name": "Quick Call", "price": "499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Expert Consultation", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Advisory Plan", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to book a CA consultation", "totalTime": "P1D",
  "supply": [{"@type": "HowToSupply", "name": "PAN"}, {"@type": "HowToSupply", "name": "Your question"},
             {"@type": "HowToSupply", "name": "Relevant documents"}, {"@type": "HowToSupply", "name": "Phone or video device"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Choose a plan", "text": "Pick a quick call, an expert consultation or a monthly advisory plan."},
   {"@type": "HowToStep", "position": 2, "name": "Share your question", "text": "Tell us the topic and upload any documents the CA should see."},
   {"@type": "HowToStep", "position": 3, "name": "Get matched", "text": "We assign a practising CA who handles your topic and confirm the slot."},
   {"@type": "HowToStep", "position": 4, "name": "Talk to the CA", "text": "Discuss your situation by phone or video and ask follow-up questions."},
   {"@type": "HowToStep", "position": 5, "name": "Get the summary", "text": "Receive a written summary of the advice and next steps within 24 hours."}]},
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
    <meta property="og:title" content="CA Consultation Online – Talk to a CA" />
    <meta property="og:description" content="Talk to a practising CA by phone or video and get a written summary of the advice within 24 hours." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – CA Consultation" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="CA Consultation Online – Talk to a CA" />
    <meta name="twitter:description" content="Tax or business question? Talk to a practising CA in Hindi or English." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "ca-consultation"')
assert 'service: "ca-consultation"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="ca-consultation"')
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
