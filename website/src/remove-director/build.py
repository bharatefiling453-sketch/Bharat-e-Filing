# Builds remove-director/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/remove-director/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/remove-director/"
TITLE = "Remove a Director – Section 169, DIR-12 | Bharat e-Filing"
DESC = "Remove a company director the lawful way: special notice, the director's hearing, ordinary resolution and DIR-12, or get your own name removed with DIR-11."
OG = "https://bharatefiling.com/wp-content/uploads/og/remove-director-1200x630.jpg"
PUB = "2026-10-22"
SLUG = "remove-director"

FAQ = [
 ("How can shareholders remove a director?", "Under Section 169 of the Companies Act, shareholders can remove a director before the end of the term by passing an ordinary resolution at a general meeting, after a special notice and after giving the director a reasonable opportunity of being heard. The company then files DIR-12 within 30 days."),
 ("What is a special notice for removing a director?", "It is a notice of the intention to move the removal resolution, given to the company under Section 115 by members holding at least 1% of the voting power, or shares on which at least ₹5 lakh has been paid up. It must reach the company at least 14 clear days before the meeting, and not earlier than three months before it."),
 ("Can the director defend themselves?", "Yes. The company sends the director a copy of the special notice, and the director can make a written representation, ask for it to be sent to the members, and speak at the meeting. If it is not sent in time, it can be read out at the meeting."),
 ("Can the board remove a director?", "No. The board cannot remove a director appointed by the shareholders. Removal under Section 169 needs a resolution of the shareholders at a general meeting. The board can only call that meeting."),
 ("What if the board refuses to call the meeting?", "Members holding at least one-tenth of the paid-up voting capital can requisition an extraordinary general meeting under Section 100. The board must call it within 21 days, to be held within 45 days; if it does not, the requisitionists can hold it themselves within three months."),
 ("Which directors cannot be removed under Section 169?", "A director appointed by the Tribunal under Section 242, and directors elected by proportional representation where the articles provide for it under Section 163, cannot be removed this way."),
 ("Can a removed director be replaced at the same meeting?", "Yes. If special notice of the proposed appointment is also given, the shareholders can appoint another person in the removed director's place at the same meeting. The new director holds office for the remaining term of the removed director."),
 ("Does a director's office end automatically in any case?", "Yes. Under Section 167, the office is vacated if the director becomes disqualified under Section 164, or is absent from all board meetings held during 12 months, with or without leave, among other grounds. The company still files DIR-12 to record it."),
 ("How do I get my name removed as a director of a company?", "Resign by giving written notice to the company. The company must file DIR-12 within 30 days, and you can file DIR-11 yourself within 30 days with the reasons. If the company does not file, your DIR-11 gives the Registrar an independent record of the resignation."),
 ("Is a removed director entitled to compensation?", "Removal does not take away any compensation or damages payable to the director under a contract of appointment, for example as a managing or whole-time director. The terms of the contract decide this."),
 ("Is a removed director still liable for the company's past dues?", "Removal does not end liability for defaults during the director's tenure. Under the income-tax law, directors of a private company can be held liable for tax dues of the period they were directors if those dues cannot be recovered from the company."),
 ("What must be updated after removing a director?", "File DIR-12 within 30 days, update the register of directors, apply for the GST core amendment within 15 days, and change the bank's authorised signatories and the income-tax portal contacts."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-removal p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Remove a Director"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Remove a Director",
  "alternateName": ["Removal of director", "Section 169 removal", "Remove my name as director", "DIR-11 filing"],
  "serviceType": "Removal or cessation of a company director recorded with the Registrar of Companies",
  "description": "Removal of company directors under Section 169 with special notice, the director's representation and an ordinary resolution, EGM requisition support, cessation under Section 167, director exits with DIR-11, and DIR-12 filing.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Shareholders, companies and directors in India"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Director Removal Plans", "itemListElement": [
    {"@type": "Offer", "name": "Director Exit and Name Removal", "price": "2499", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Removal by Shareholders", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Removal with EGM Requisition", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to remove a director under Section 169", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Special notice signed by eligible members"}, {"@type": "HowToSupply", "name": "Notice of the general meeting"},
             {"@type": "HowToSupply", "name": "Ordinary resolution and minutes"}, {"@type": "HowToSupply", "name": "DSC of a continuing director"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Give special notice", "text": "Members holding at least 1% of the voting power give special notice of the removal resolution at least 14 clear days before the meeting."},
   {"@type": "HowToStep", "position": 2, "name": "Inform the director", "text": "The company sends a copy of the notice to the director, who may make a written representation."},
   {"@type": "HowToStep", "position": 3, "name": "Notify the members", "text": "The company gives members notice of the resolution at least seven days before the meeting, with the director's representation if received in time."},
   {"@type": "HowToStep", "position": 4, "name": "Hold the meeting", "text": "The director is heard and the shareholders pass an ordinary resolution, and may appoint a replacement if notice was given."},
   {"@type": "HowToStep", "position": 5, "name": "File DIR-12", "text": "File DIR-12 within 30 days and update the register, GST registration and bank signatories."}]},
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
    <meta property="og:title" content="Remove a Director – Section 169" />
    <meta property="og:description" content="Remove a director lawfully, or get your own name removed: special notice, hearing, resolution and DIR-12 handled by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Remove a Director" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Remove a Director – Section 169" />
    <meta name="twitter:description" content="Removing a director? Do it by the book under Section 169, with DIR-12 on time." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "remove-director"')
assert 'service: "remove-director"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="remove-director"')
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
