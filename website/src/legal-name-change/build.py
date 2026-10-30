# Builds legal-name-change/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/legal-name-change/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/legal-name-change/"
TITLE = "Legal Name Change – Gazette & Affidavit | Bharat e-Filing"
DESC = "Change your name legally in India: affidavit, two newspaper ads and Gazette publication, plus help updating PAN, Aadhaar, passport and bank records."
OG = "https://bharatefiling.com/wp-content/uploads/og/legal-name-change-1200x630.jpg"
PUB = "2026-10-30"
SLUG = "legal-name-change"

FAQ = [
 ("How do I change my name legally in India?", "The usual process has three steps: swear an affidavit declaring your old and new names, publish the change in two newspapers, commonly one in English and one in the local language, and apply to have it published in the Gazette of India or your State Gazette. The Gazette notification is the strongest official proof of the change."),
 ("Is a Gazette notification compulsory?", "Not in every case, but it is the most widely accepted proof. Some agencies accept other documents for certain changes, such as a marriage certificate after marriage, while others ask for the Gazette notification, especially for a complete change of name."),
 ("Where is a name change published?", "Changes of name by individuals are published in the Gazette of India by the Department of Publication, and applications can be made online. Many states also publish name changes in the State Gazette."),
 ("What documents are needed for a name change?", "An affidavit stating the old and new names and the reason, the original newspaper advertisements, identity and address proof, recent photographs, and the application in the prescribed format, signed by you and a witness."),
 ("How long does the name change take?", "The affidavit and newspaper advertisements can usually be done within a few days. Gazette publication takes longer and depends on the publishing office, so plan for several weeks before your new name appears."),
 ("Can I change my name after marriage without the Gazette?", "Often, yes. A marriage certificate is commonly accepted to change a surname in documents such as the passport and PAN. A Gazette notification is still useful if you want one consistent proof for every record."),
 ("How many times can I change my name in Aadhaar?", "UIDAI allows the name in Aadhaar to be updated twice in a lifetime, including spelling corrections. Beyond that, a further change needs special approval from UIDAI, supported by documents such as a Gazette notification or court order."),
 ("How do I update my PAN after a name change?", "Apply for a change in PAN data online and attach proof of the new name, such as the Gazette notification or marriage certificate. Keep the PAN and Aadhaar names consistent, because mismatches can cause problems with linking and tax filings."),
 ("Can I change my name in my passport?", "Yes. Passport Seva accepts a Gazette notification, central or state, as proof of a change of name, and also lists newspaper clippings with the required documents as an option for some applicants."),
 ("Can a minor's name be changed?", "Yes. The parent or guardian makes the application and affidavit on behalf of the minor child, with the child's birth certificate and the parent's identity proof."),
 ("Which records should I update after changing my name?", "Aadhaar and PAN first, then bank accounts, passport, voter ID, driving licence, insurance and investments, property records, and educational and employment records."),
 ("Does a name change affect my income tax return?", "Your return is filed under your PAN, so update the PAN name and keep it matching Aadhaar. Returns for tax year 2026-27 onwards are filed under the Income-tax Act, 2025; earlier years follow the Income-tax Act, 1961."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-namechange p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Legal Name Change"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Legal Name Change",
  "alternateName": ["Name change gazette", "Change name legally in India", "Name change affidavit and newspaper ad", "Gazette notification for name change"],
  "serviceType": "Legal change of name of an individual",
  "description": "Legal change of name for individuals: affidavit drafting, newspaper advertisements, Gazette publication application, and help updating PAN, Aadhaar, passport and bank records.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "Audience", "audienceType": "Individuals in India who want to change their name"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Name Change Plans", "itemListElement": [
    {"@type": "Offer", "name": "Affidavit and Newspaper", "price": "1499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Complete Name Change", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Name Change and Records Update", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to change your name legally in India", "totalTime": "P45D",
  "supply": [{"@type": "HowToSupply", "name": "Affidavit"}, {"@type": "HowToSupply", "name": "Two newspaper advertisements"},
             {"@type": "HowToSupply", "name": "Identity and address proof"}, {"@type": "HowToSupply", "name": "Photographs"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Swear the affidavit", "text": "Swear an affidavit stating your old name, new name and the reason for the change."},
   {"@type": "HowToStep", "position": 2, "name": "Publish in newspapers", "text": "Publish the change in two newspapers, commonly one in English and one in the local language."},
   {"@type": "HowToStep", "position": 3, "name": "Apply to the Gazette", "text": "Apply for publication in the Gazette of India or your State Gazette with the affidavit, advertisements and documents."},
   {"@type": "HowToStep", "position": 4, "name": "Get the notification", "text": "Download the Gazette notification once your name change is published."},
   {"@type": "HowToStep", "position": 5, "name": "Update your records", "text": "Update Aadhaar and PAN first, then your bank, passport and other records."}]},
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
    <meta property="og:title" content="Legal Name Change – Gazette & Affidavit" />
    <meta property="og:description" content="Affidavit, newspaper ads and Gazette publication, plus help updating PAN, Aadhaar and passport." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Legal Name Change" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Legal Name Change – Gazette & Affidavit" />
    <meta name="twitter:description" content="Changing your name? Do it properly, once, with expert help." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "legal-name-change"')
assert 'service: "legal-name-change"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="legal-name-change"')
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
