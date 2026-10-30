# Builds legal-consultation/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/legal-consultation/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/legal-consultation/"
TITLE = "Legal Consultation – Talk to a Lawyer | Bharat e-Filing"
DESC = "Talk to an independent advocate by phone or video on contracts, legal notices, cheque bounce, consumer or property matters, with a written note of the advice."
OG = "https://bharatefiling.com/wp-content/uploads/og/legal-consultation-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "legal-consultation"

FAQ = [
 ("What is a legal consultation?", "A one-to-one session, by phone or video, with an independent advocate enrolled with a State Bar Council. You explain your situation, the advocate tells you where you stand under the law and what your options are, and you receive a short written note of the advice."),
 ("What can I ask a lawyer?", "Business contracts and agreements, legal notices you have received or want to send, cheque bounce, recovery of money, consumer complaints, property and rent issues, employment disputes, startup and founder matters, trademarks, and family matters."),
 ("Who gives the advice?", "Independent advocates enrolled with a State Bar Council and bound by the Bar Council of India's rules on professional conduct. We share the advocate's name and enrolment number before the call. Bharat e-Filing arranges the consultation and is not a law firm."),
 ("Is the consultation confidential?", "Yes. Communications with an advocate for legal advice are protected under the Bharatiya Sakshya Adhiniyam, 2023, and we process your personal data under the Digital Personal Data Protection Act, 2023, only to arrange the consultation."),
 ("How much time do I have to act on a bounced cheque?", "Under Section 138 of the Negotiable Instruments Act, 1881, the payee must send a written demand notice within 30 days of receiving the bank's return memo. The drawer then has 15 days to pay, and if they don't, a complaint can be filed within one month after that period ends."),
 ("Where do I file a consumer complaint?", "With the District Commission if the value paid for the goods or services is up to ₹50 lakh, the State Commission if it is above ₹50 lakh and up to ₹2 crore, and the National Commission if it is above ₹2 crore. A complaint should generally be filed within two years of the cause of action."),
 ("How long do I have to file a case to recover money?", "Most suits to recover money must be filed within three years under the Limitation Act, 1963, usually counted from the date the payment fell due. The exact starting point depends on the facts, so check with an advocate early."),
 ("Can the advocate send a legal notice for me?", "Yes. After the consultation, the advocate can draft and send a legal notice on their letterhead as a separate service, with the fee explained before you decide."),
 ("What should I keep ready for the consultation?", "A short summary of what happened with dates, and copies of the documents involved, such as agreements, invoices, notices, emails or messages, the cheque and bank memo, or property papers."),
 ("Do the new criminal laws apply to my matter?", "The Bharatiya Nyaya Sanhita, 2023, the Bharatiya Nagarik Suraksha Sanhita, 2023 and the Bharatiya Sakshya Adhiniyam, 2023 replaced the Indian Penal Code, the Code of Criminal Procedure and the Indian Evidence Act from 1 July 2024. Matters arising before that date may still follow the old laws, so an advocate checks which applies."),
 ("Can you help with tax notices too?", "Income tax matters under the Income-tax Act, 2025, GST and company law filings are handled by our chartered accountants and company secretaries. If your matter involves both, we bring in the right expert."),
 ("Is the consultation available in Hindi?", "Yes. Consultations are available in Hindi and English, by phone or video, and the written note can be shared in either language."),
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
  "reviewedBy": {"@type": "Person", "name": "REPLACE_ADVOCATE_NAME", "jobTitle": "Advocate", "url": "https://bharatefiling.com/team/REPLACE_ADVOCATE_SLUG/"},
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-legal p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Legal Consultation"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Legal Consultation",
  "alternateName": ["Talk to a lawyer online", "Online legal advice", "Advocate consultation", "Legal advice on call"],
  "serviceType": "Arranging consultations with independent advocates",
  "description": "One-to-one phone or video consultations with independent advocates on contracts, legal notices, cheque bounce, recovery, consumer complaints, property, employment and startup matters, with a written note of the advice.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "Audience", "audienceType": "Individuals and businesses in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Legal Consultation Plans", "itemListElement": [
    {"@type": "Offer", "name": "Quick Call", "price": "699", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Expert Consultation", "price": "1999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Legal Notice", "price": "2999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to book a legal consultation", "totalTime": "P1D",
  "supply": [{"@type": "HowToSupply", "name": "Summary of what happened"}, {"@type": "HowToSupply", "name": "Relevant documents"},
             {"@type": "HowToSupply", "name": "Key dates"}, {"@type": "HowToSupply", "name": "Phone or video device"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Choose a plan", "text": "Pick a quick call, an expert consultation or a legal notice."},
   {"@type": "HowToStep", "position": 2, "name": "Share your matter", "text": "Tell us what happened, the key dates, and upload the documents involved."},
   {"@type": "HowToStep", "position": 3, "name": "Get matched", "text": "We arrange an independent advocate who handles your type of matter and confirm the slot."},
   {"@type": "HowToStep", "position": 4, "name": "Talk to the advocate", "text": "Discuss your options by phone or video and ask follow-up questions."},
   {"@type": "HowToStep", "position": 5, "name": "Get the note", "text": "Receive a written note of the advice and next steps within 24 hours."}]},
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
    <meta property="og:title" content="Legal Consultation – Talk to a Lawyer" />
    <meta property="og:description" content="Talk to an independent advocate by phone or video and get a written note of the advice within 24 hours." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Legal Consultation" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Legal Consultation – Talk to a Lawyer" />
    <meta name="twitter:description" content="Legal question? Talk to an advocate in Hindi or English." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "legal-consultation"')
assert 'service: "legal-consultation"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="legal-consultation"')
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
