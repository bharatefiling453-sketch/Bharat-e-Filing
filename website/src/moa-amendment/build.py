# Builds moa-amendment/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/moa-amendment/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/moa-amendment/"
TITLE = "MOA Amendment Online – MGT-14, SH-7 | Bharat e-Filing"
DESC = "Amend your company's memorandum online: change the objects clause, increase authorised capital or alter other clauses, with resolutions, MGT-14 and SH-7 filed."
OG = "https://bharatefiling.com/wp-content/uploads/og/moa-amendment-1200x630.jpg"
PUB = "2026-10-26"
SLUG = "moa-amendment"

FAQ = [
 ("What is the memorandum of association?", "The memorandum of association, or MOA, is the company's charter. It sets out its name, registered office state, objects, the liability of members, its authorised capital and the subscribers' details. It is altered under Section 13 of the Companies Act, 2013, and under Section 61 for share capital."),
 ("How do I change the objects clause of a company?", "Hold a board meeting, pass a special resolution of the shareholders approving the altered objects clause, and file it with the Registrar in MGT-14 within 30 days, along with the altered MOA. The change takes effect when the Registrar registers it."),
 ("How do I increase the authorised capital of a company?", "If the articles allow it, the shareholders pass an ordinary resolution under Section 61 to increase the authorised capital, and the company files SH-7 with the Registrar within 30 days, with the altered capital clause of the MOA. If the articles do not allow it, they are altered first by special resolution."),
 ("What is a special resolution?", "A special resolution is passed when the votes cast in favour are at least three times the votes cast against, at a general meeting called with notice stating the intention to propose it as a special resolution."),
 ("Is MGT-14 needed for an increase in authorised capital?", "Only where a special resolution is passed, such as to alter the articles. An increase by ordinary resolution under Section 61 is reported in SH-7."),
 ("When does an MOA alteration take effect?", "An alteration of the memorandum has effect only when it is registered by the Registrar. The Registrar registers the alteration and certifies it within 30 days of the documents being filed."),
 ("Which MOA changes need outside approval?", "A change of name needs Registrar approval, a shift of registered office to another state needs Regional Director approval, and a change of objects by a company with unused money raised from the public by prospectus needs extra steps, including a postal ballot, newspaper notice and an exit offer to dissenting shareholders."),
 ("Can a company carry on a business not in its objects clause?", "It should not. A business outside the objects can be challenged, and banks, licensing authorities and the GST department often check the objects clause. Alter the MOA before starting a new line of business."),
 ("Does the company need to adopt a new format MOA?", "Companies registered under the old Act often have long objects clauses with main, ancillary and other objects. When altering the objects, many companies adopt a fresh MOA in the format of the Companies Act, 2013 at the same time."),
 ("What documents are needed for an MOA amendment?", "The board resolution, the notice of the general meeting with the explanatory statement, the special or ordinary resolution, the altered MOA, and a director's digital signature for filing."),
 ("Should the company name change when the objects change?", "Not necessarily. But if the name describes the old business, for example Textiles or Infra, consider a name change so the name matches the new activity. It is a separate process through RUN and INC-24."),
 ("Does an MOA change affect income tax or GST?", "The PAN and GSTIN stay the same. Update the nature of business in the GST registration and use the right business code in the income tax return under the Income-tax Act, 2025, from tax year 2026-27."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-moa p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "MOA Amendment"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "MOA Amendment",
  "alternateName": ["Alteration of memorandum of association", "Change of objects clause", "Increase in authorised capital", "MGT-14 and SH-7 filing"],
  "serviceType": "Alteration of a company's memorandum of association filed with the Registrar of Companies",
  "description": "Alteration of the memorandum of association under Sections 13 and 61: objects clause changes by special resolution and MGT-14, authorised capital increases by ordinary resolution and SH-7, and adoption of a new-format MOA.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Private and public companies in India changing their memorandum"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "MOA Amendment Plans", "itemListElement": [
    {"@type": "Offer", "name": "Authorised Capital Increase", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Objects Clause Change", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "MOA and AOA Overhaul", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to change the objects clause of a company", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Draft of the altered objects clause"}, {"@type": "HowToSupply", "name": "Notice of general meeting with explanatory statement"},
             {"@type": "HowToSupply", "name": "Special resolution"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Draft the new clause", "text": "Draft the altered objects clause, and decide whether to adopt a new-format MOA."},
   {"@type": "HowToStep", "position": 2, "name": "Board meeting", "text": "Hold a board meeting to approve the draft and call a general meeting."},
   {"@type": "HowToStep", "position": 3, "name": "Special resolution", "text": "Pass a special resolution at the general meeting approving the alteration."},
   {"@type": "HowToStep", "position": 4, "name": "File MGT-14", "text": "File MGT-14 with the special resolution and altered MOA within 30 days."},
   {"@type": "HowToStep", "position": 5, "name": "Registration", "text": "The Registrar registers the alteration; then update GST, bank and licences for the new activity."}]},
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
    <meta property="og:title" content="MOA Amendment – MGT-14, SH-7" />
    <meta property="og:description" content="Change your objects clause or raise authorised capital, with resolutions, MGT-14 and SH-7 handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – MOA Amendment" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="MOA Amendment – MGT-14, SH-7" />
    <meta name="twitter:description" content="New business line or more capital? Amend your MOA the right way." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "moa-amendment"')
assert 'service: "moa-amendment"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="moa-amendment"')
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
