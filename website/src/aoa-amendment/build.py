# Builds aoa-amendment/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/aoa-amendment/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/aoa-amendment/"
TITLE = "AOA Amendment Online – MGT-14 Filing | Bharat e-Filing"
DESC = "Alter your company's articles of association: special resolution, MGT-14 in 30 days, new Table F articles, investor rights, entrenchment and conversions."
OG = "https://bharatefiling.com/wp-content/uploads/og/aoa-amendment-1200x630.jpg"
PUB = "2026-10-26"
SLUG = "aoa-amendment"

FAQ = [
 ("What are the articles of association?", "The articles of association, or AOA, are the company's internal rulebook. They cover share transfers, board and general meetings, directors' powers, borrowing, dividends and other management matters, within the limits of the Companies Act and the memorandum."),
 ("How do I amend the articles of association?", "Hold a board meeting to approve the draft and call a general meeting, pass a special resolution of the shareholders under Section 14 of the Companies Act, 2013, and file MGT-14 with the Registrar within 30 days, with a copy of the altered articles."),
 ("What is a special resolution?", "A special resolution is passed when the votes cast in favour are at least three times the votes cast against, at a general meeting called with notice stating the intention to propose it as a special resolution."),
 ("Can the board alter the articles?", "No. Only the shareholders can alter the articles, by special resolution. The board approves the draft and calls the general meeting."),
 ("Why do startups amend their articles at funding?", "Investor rights in a shareholders' agreement, such as pre-emption, right of first refusal, tag-along, drag-along, nominee directors and affirmative votes, are best written into the articles so that they bind the company and its shareholders. Courts have refused to enforce some private-company transfer restrictions that were not in the articles."),
 ("What is an entrenchment provision?", "It is a clause in the articles that can be changed only if conditions stricter than a special resolution are met. In a private company it is added with the agreement of all members, and in a public company by special resolution. The Registrar is notified in MGT-14 within 30 days."),
 ("Should old articles be replaced with Table F?", "Companies registered under the 1956 Act often have articles that refer to repealed sections. Adopting a fresh set based on Table F of Schedule I of the Companies Act, 2013, with your own changes, brings them up to date in one resolution."),
 ("Do the articles need to allow an increase in authorised capital?", "Yes. Under Section 61, a company can increase its authorised capital by ordinary resolution only if its articles authorise it. If they do not, the articles are altered first by special resolution."),
 ("How does a private company convert into a public company?", "It alters its articles by special resolution to remove the private company restrictions, increases its directors and members to the public company minimums, and files the resolution and altered documents with the Registrar, including INC-27."),
 ("How does a public company convert into a private company?", "It passes a special resolution to alter its articles and applies to the Regional Director for approval. After the order, it files INC-27 with the Registrar within the prescribed time, and the Registrar issues a fresh certificate."),
 ("Can the articles say anything the company wants?", "No. The articles cannot conflict with the Companies Act or the memorandum. Any clause that goes against the Act is void to that extent."),
 ("Does an AOA change affect income tax or GST?", "Not directly. The PAN, TAN and GSTIN stay the same. But if the change alters who signs or who controls the company, update authorised signatories on the income-tax portal under the Income-tax Act, 2025, the GST portal and the bank."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-aoa p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "AOA Amendment"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "AOA Amendment",
  "alternateName": ["Alteration of articles of association", "Adopt new articles", "Entrenchment provisions", "Private to public conversion"],
  "serviceType": "Alteration of a company's articles of association filed with the Registrar of Companies",
  "description": "Alteration of the articles of association under Section 14: targeted changes, new Table F articles, investor rights from shareholders' agreements, entrenchment provisions, and private-public conversions, with special resolution and MGT-14 filing.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Private and public companies in India changing their articles"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "AOA Amendment Plans", "itemListElement": [
    {"@type": "Offer", "name": "Article Alteration", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "New Articles", "price": "7999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Company Conversion", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to amend the articles of association", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Draft of the altered articles"}, {"@type": "HowToSupply", "name": "Notice of general meeting with explanatory statement"},
             {"@type": "HowToSupply", "name": "Special resolution"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Draft the change", "text": "Draft the altered clauses or a complete new set of articles, checked against the Act and the memorandum."},
   {"@type": "HowToStep", "position": 2, "name": "Board meeting", "text": "Hold a board meeting to approve the draft and call a general meeting."},
   {"@type": "HowToStep", "position": 3, "name": "Special resolution", "text": "Pass a special resolution of the shareholders under Section 14."},
   {"@type": "HowToStep", "position": 4, "name": "File MGT-14", "text": "File MGT-14 with the special resolution and altered articles within 30 days."},
   {"@type": "HowToStep", "position": 5, "name": "Follow through", "text": "Update the company's records and, where the change affects signatories or control, the bank, GST and income-tax portals."}]},
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
    <meta property="og:title" content="AOA Amendment – MGT-14 Filing" />
    <meta property="og:description" content="Update your company's rulebook: new articles, investor rights or conversion, with the special resolution and MGT-14 handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – AOA Amendment" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="AOA Amendment – MGT-14 Filing" />
    <meta name="twitter:description" content="Raising funds or old articles? Amend your AOA the right way." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "aoa-amendment"')
assert 'service: "aoa-amendment"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="aoa-amendment"')
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
