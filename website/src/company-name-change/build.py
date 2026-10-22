# Builds company-name-change/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/company-name-change/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/company-name-change/"
TITLE = "Company Name Change Online – INC-24 | Bharat e-Filing"
DESC = "Change your company or LLP name online: name check, RUN reservation, special resolution, MGT-14, INC-24 and new certificate, plus PAN, GST and bank updates."
OG = "https://bharatefiling.com/wp-content/uploads/og/company-name-change-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "company-name-change"

FAQ = [
 ("How do I change the name of a private limited company?", "Hold a board meeting, reserve the new name through RUN on the MCA portal, pass a special resolution at a general meeting, file it in MGT-14 within 30 days, and then apply to the Registrar in Form INC-24. Once approved, the Registrar issues a fresh certificate of incorporation in Form INC-25 with the new name."),
 ("How long does a company name change take?", "It usually takes three to five weeks: about a week for name approval through RUN, the notice period for the general meeting, and one to two weeks for the Registrar to approve INC-24, assuming the forms are not sent back for resubmission."),
 ("How long is a reserved name valid for a name change?", "A name approved through RUN for changing the name of an existing company is reserved for 60 days from approval. INC-24 must be filed within that time, or the name has to be applied for again."),
 ("Can every company change its name?", "No. Under Rule 29 of the Companies (Incorporation) Rules, a company cannot change its name if it has not filed its annual returns or financial statements, or has defaulted in repaying deposits or interest on them, until the default is made good."),
 ("Does the company get a new CIN after a name change?", "The company remains the same legal entity, with the same assets, liabilities, contracts and PAN number. The Registrar issues a fresh certificate of incorporation in the new name; the CIN may change only if the change also affects its type or listing status."),
 ("Is a special resolution required for a name change?", "Yes. Under Section 13 of the Companies Act, the memorandum's name clause is changed by a special resolution of the shareholders, passed with at least three-fourths of the votes cast, and filed with the Registrar in MGT-14 within 30 days."),
 ("Which words need special approval in a company name?", "Words such as Bank, Insurance, Stock Exchange, Mutual Fund, Board, Commission, Authority, National, Union, Central, Federal and Republic need approval or a no-objection from the Central Government or the relevant regulator, such as the RBI, SEBI or IRDAI, before they can be used."),
 ("How do I change the name of an LLP?", "Reserve the new name through RUN-LLP, obtain the consent of the partners as required by the LLP agreement, file Form 5 for the change of name within 30 days of the consent, and file Form 3 for the change in the LLP agreement. The Registrar then issues a fresh certificate of incorporation."),
 ("What must be updated after a company name change?", "Update the PAN and TAN records, apply for a GST amendment within 15 days, and inform the bank, the Udyam, IEC and shop registrations, trademarks, licences, customers and vendors. Change the name on the seal, letterheads, invoices, signboard and website."),
 ("Do I have to show the old name after the change?", "Yes. Under Section 12 of the Companies Act, for two years after the change, the company must show its former name along with its new name on its signboard, letterheads, invoices and other official documents."),
 ("Can the Registrar order a company to change its name?", "Yes. Under Section 16, if a name is identical or too similar to an existing company or a registered trademark, the Central Government can direct the company to change it, usually within three months of the direction."),
 ("Does a company name change affect income tax or GST registration?", "The PAN and GSTIN stay the same, but the name on them must be updated. A change of legal name in GST is a core amendment that needs officer approval, and the PAN record is corrected through the PAN change request."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-name-change p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Company Name Change"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Company Name Change",
  "alternateName": ["Change of company name", "INC-24 filing", "LLP name change"],
  "serviceType": "Change of name of a company or LLP with the Registrar of Companies",
  "description": "End-to-end change of name for private limited companies, OPCs and LLPs: name availability check and RUN reservation, board and shareholder resolutions, MGT-14, INC-24 or LLP Form 5 and Form 3, fresh certificate of incorporation, and PAN, GST and bank updates.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Companies, OPCs and LLPs in India changing their name"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Name Change Plans", "itemListElement": [
    {"@type": "Offer", "name": "LLP Name Change", "price": "6999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Company Name Change", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Name Change + Rebrand Updates", "price": "14999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to change the name of a private limited company", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Proposed names with their meaning"}, {"@type": "HowToSupply", "name": "Board and special resolutions"},
             {"@type": "HowToSupply", "name": "Altered memorandum and articles of association"}, {"@type": "HowToSupply", "name": "Director's DSC"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check and reserve the name", "text": "Check the new name against existing companies and trademarks, and reserve it through RUN, valid for 60 days for a name change."},
   {"@type": "HowToStep", "position": 2, "name": "Board approval", "text": "Hold a board meeting to approve the change and call a general meeting."},
   {"@type": "HowToStep", "position": 3, "name": "Special resolution", "text": "Pass a special resolution at the general meeting to change the name clause of the memorandum."},
   {"@type": "HowToStep", "position": 4, "name": "File MGT-14 and INC-24", "text": "File the special resolution in MGT-14 within 30 days, and apply to the Registrar in INC-24 with the altered memorandum and articles."},
   {"@type": "HowToStep", "position": 5, "name": "Update records", "text": "On receiving the fresh certificate of incorporation, update PAN, GST, bank, licences and stationery, and show the former name for two years."}]},
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
    <meta property="og:title" content="Company Name Change Online – INC-24" />
    <meta property="og:description" content="New name for your company or LLP: RUN, special resolution, MGT-14, INC-24 and PAN, GST and bank updates handled." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Company Name Change" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Company Name Change Online – INC-24" />
    <meta name="twitter:description" content="Rebranding? Change your company or LLP name the right way, with every record updated." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "company-name-change"')
assert 'service: "company-name-change"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="company-name-change"')
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
