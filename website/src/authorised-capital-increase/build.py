# Builds authorised-capital-increase/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/authorised-capital-increase/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/authorised-capital-increase/"
TITLE = "Increase Authorised Capital Online – SH-7 | Bharat e-Filing"
DESC = "Increase your company's authorised capital: articles check, ordinary resolution, altered MOA and SH-7 within 30 days, ready for your next share allotment."
OG = "https://bharatefiling.com/wp-content/uploads/og/authorised-capital-increase-1200x630.jpg"
PUB = "2026-10-26"
SLUG = "authorised-capital-increase"

FAQ = [
 ("What is authorised capital?", "Authorised capital is the maximum share capital a company can issue, as stated in the capital clause of its memorandum. Paid-up capital is the part actually issued and paid for. A company cannot allot shares beyond its authorised capital."),
 ("How do I increase the authorised capital of a company?", "Check that the articles allow it, hold a board meeting to approve and call a general meeting, pass an ordinary resolution under Section 61 of the Companies Act, 2013 altering the capital clause, and file SH-7 with the Registrar within 30 days with the altered memorandum."),
 ("Is a special resolution needed to increase authorised capital?", "No, an ordinary resolution is enough if the articles authorise the increase. If they do not, the articles are first altered by special resolution, which is also filed in MGT-14."),
 ("What is the due date for SH-7?", "SH-7 must be filed within 30 days of the resolution altering the share capital, under Section 64 of the Companies Act."),
 ("When do companies need to increase authorised capital?", "Before issuing new shares beyond the current limit, such as for a funding round, a rights issue, a bonus issue, an employee stock option pool, or converting loans into equity."),
 ("Does increasing authorised capital mean issuing shares?", "No. It only raises the ceiling. Shares are issued separately, by allotment through a rights issue, private placement, bonus issue or other route, with PAS-3 filed within 15 days of allotment."),
 ("What documents are needed for SH-7?", "The notice of the general meeting, the ordinary resolution, the altered memorandum, and the altered articles if they were changed, signed with a director's digital signature."),
 ("Can a one person company increase its authorised capital?", "Yes. In a one person company, the resolution is passed by the sole member and entered in the minute book, and SH-7 is filed within 30 days."),
 ("What other changes to share capital use SH-7?", "Consolidating shares into larger amounts, sub-dividing shares into smaller amounts, converting fully paid shares into stock and back, and cancelling shares that have not been taken up are all altered under Section 61 and reported in SH-7."),
 ("How much should I increase the authorised capital by?", "Enough to cover the paid-up capital after the planned issue, with some headroom for the next round or an ESOP pool, so that you do not need to repeat the process soon. Our calculator suggests a figure."),
 ("Can authorised capital be reduced?", "Unissued shares can be cancelled under Section 61, which reduces authorised capital and is reported in SH-7. Reducing issued or paid-up capital is a different process under Section 66."),
 ("Does an increase in authorised capital affect income tax?", "No tax arises on increasing authorised capital itself. Share issues that follow are reported in the company's income tax return under the Income-tax Act, 2025 from tax year 2026-27, so keep allotment records ready."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-capital p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Authorised Capital Increase"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Authorised Capital Increase",
  "alternateName": ["Increase in authorised share capital", "SH-7 filing", "Alteration of share capital", "Share split and consolidation"],
  "serviceType": "Alteration of a company's share capital filed with the Registrar of Companies",
  "description": "Increase of authorised share capital under Section 61 with an ordinary resolution, altered memorandum and SH-7 within 30 days, plus share sub-division, consolidation and follow-on allotments with PAS-3.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Private, public and one person companies in India issuing new shares"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Share Capital Plans", "itemListElement": [
    {"@type": "Offer", "name": "Split or Consolidation", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Authorised Capital Increase", "price": "3999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Increase + Allotment", "price": "7999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to increase the authorised capital of a company", "totalTime": "P14D",
  "supply": [{"@type": "HowToSupply", "name": "Current memorandum and articles"}, {"@type": "HowToSupply", "name": "Notice of general meeting"},
             {"@type": "HowToSupply", "name": "Ordinary resolution"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check the articles", "text": "Confirm that the articles authorise an increase in share capital; if not, plan a special resolution to alter them."},
   {"@type": "HowToStep", "position": 2, "name": "Decide the amount", "text": "Fix the new authorised capital to cover the planned issue with headroom for future needs."},
   {"@type": "HowToStep", "position": 3, "name": "Board meeting", "text": "Hold a board meeting to approve the increase and call a general meeting."},
   {"@type": "HowToStep", "position": 4, "name": "Ordinary resolution", "text": "Pass an ordinary resolution under Section 61 altering the capital clause of the memorandum."},
   {"@type": "HowToStep", "position": 5, "name": "File SH-7", "text": "File SH-7 with the altered memorandum within 30 days, then allot shares within the new limit."}]},
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
    <meta property="og:title" content="Increase Authorised Capital – SH-7" />
    <meta property="og:description" content="Raise your company's authorised capital before the next allotment, with resolutions and SH-7 handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Authorised Capital Increase" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Increase Authorised Capital – SH-7" />
    <meta name="twitter:description" content="Issuing new shares? Increase authorised capital first, with SH-7 in 30 days." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "authorised-capital-increase"')
assert 'service: "authorised-capital-increase"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="authorised-capital-increase"')
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
