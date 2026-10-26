# Builds share-transfer/index.html from the v2 service-page layout (gst-registration/index.html supplies the shared
# head boilerplate, icon sprite, global nav and footer). Run from website/: python3 src/share-transfer/build.py
import json, html, os
T = open("gst-registration/index.html").read()
def cut(a, b, src=T, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

URL = "https://bharatefiling.com/share-transfer/"
TITLE = "Share Transfer in Private Company – SH-4 | Bharat e-Filing"
DESC = "Transfer shares of a private company the right way: SH-4 deed, board approval, demat rules, register updates, valuation and capital gains under the 2025 Act."
OG = "https://bharatefiling.com/wp-content/uploads/og/share-transfer-1200x630.jpg"
PUB = "2026-10-26"
SLUG = "share-transfer"

FAQ = [
 ("How are shares of a private company transferred?", "The seller and buyer sign a share transfer deed in Form SH-4, which is stamped and delivered to the company with the share certificate within 60 days of signing. The board approves the transfer as the articles require, the company updates its register of members, and the transfer is endorsed on the certificate or a new certificate is issued."),
 ("What is Form SH-4?", "SH-4 is the securities transfer form prescribed under the Companies (Share Capital and Debentures) Rules, 2014. It records the transferor, transferee, number and distinctive numbers of shares, and the consideration, and is signed by both parties and a witness."),
 ("Within how many days must the transfer deed reach the company?", "Under Section 56 of the Companies Act, 2013, the executed transfer deed must be delivered to the company within 60 days of the date of execution, along with the share certificate."),
 ("How soon must the company issue the certificate?", "The company must deliver the certificate of transferred shares within one month from the date it receives the instrument of transfer, unless it is prohibited by law or an order."),
 ("Can a private company refuse a share transfer?", "Yes, if its articles allow, for example under a right of first refusal or board approval clause. The company must send a notice of refusal within 30 days of receiving the transfer, and the transferee can appeal to the Tribunal."),
 ("Do private company shares have to be in demat form?", "Private companies other than small companies must issue and allow transfer of securities only in demat form under Rule 9B of the Companies (Prospectus and Allotment of Securities) Rules, 2014, with the compliance date extended to 30 June 2025. Small companies are exempt, and producer companies have until 31 March 2028."),
 ("Is there a ROC form for a share transfer?", "There is no separate ROC form for an ordinary share transfer in a private company. The change appears in the annual return MGT-7. If the transfer changes a significant beneficial owner, the company files BEN-2 within 30 days of receiving the declaration."),
 ("Is capital gains tax payable on a share transfer?", "Yes, for the seller. Unlisted shares held for more than 24 months give long-term capital gains taxed at 12.5% without indexation, and those held for 24 months or less give short-term gains taxed at the seller's slab rate, under the rules carried into the Income-tax Act, 2025."),
 ("Can shares be transferred below fair market value?", "They can, but there are tax consequences. For unlisted shares, the seller's sale value can be taken as at least the fair market value, and the buyer can be taxed on the difference if the shares are bought below fair market value by more than ₹50,000. A valuation report helps."),
 ("What if the buyer or seller is a non-resident?", "A transfer between a resident and a non-resident is reported in Form FC-TRS on the RBI FIRMS portal, generally within 60 days of receiving or remitting the consideration, and must follow the pricing rules under FEMA."),
 ("What happens to shares when a shareholder dies?", "This is transmission, not transfer. The nominee, or the legal heir with a succession certificate or other proof, applies to the company, which registers the shares in their name. No SH-4 is needed."),
 ("What documents are needed for a share transfer?", "The original share certificate, the signed and stamped SH-4, PAN and identity proof of both parties, the board resolution approving the transfer, any consent or waiver under the articles, and a valuation report where the price is not at fair market value."),
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
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer", "#what-is-transfer p:first-of-type"]}, "primaryImageOfPage": OG},
 {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bharatefiling.com/"},
   {"@type": "ListItem", "position": 2, "name": "Compliance", "item": "https://bharatefiling.com/compliance/"},
   {"@type": "ListItem", "position": 3, "name": "Share Transfer"}]},
 {"@type": "Service", "@id": URL + "#service", "name": "Share Transfer",
  "alternateName": ["Transfer of shares in private company", "SH-4 share transfer deed", "Transmission of shares", "Demat share transfer"],
  "serviceType": "Transfer and transmission of shares in an Indian company",
  "description": "Share transfers in private companies: SH-4 deed, articles and right-of-first-refusal checks, board approval, register and certificate updates, demat compliance under Rule 9B, BEN-2 and FC-TRS where needed, and capital gains guidance.",
  "provider": {"@id": "https://bharatefiling.com/#organization"}, "areaServed": {"@type": "Country", "name": "India"},
  "audience": {"@type": "BusinessAudience", "audienceType": "Shareholders, founders and companies in India transferring shares"},
  "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Share Transfer Plans", "itemListElement": [
    {"@type": "Offer", "name": "Share Transmission", "price": "5999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Share Transfer", "price": "4999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"},
    {"@type": "Offer", "name": "Transfer + Valuation and Tax", "price": "9999", "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#pricing"}]}},
 {"@type": "HowTo", "@id": URL + "#howto", "name": "How to transfer shares of a private company", "totalTime": "P30D",
  "supply": [{"@type": "HowToSupply", "name": "Form SH-4 signed by both parties"}, {"@type": "HowToSupply", "name": "Original share certificate"},
             {"@type": "HowToSupply", "name": "PAN of transferor and transferee"}, {"@type": "HowToSupply", "name": "Valuation report, if needed"}],
  "step": [
   {"@type": "HowToStep", "position": 1, "name": "Check the articles", "text": "Check transfer restrictions, such as a right of first refusal or board approval, and get any waivers needed."},
   {"@type": "HowToStep", "position": 2, "name": "Agree the price", "text": "Agree the price and get a valuation report where the price may differ from fair market value."},
   {"@type": "HowToStep", "position": 3, "name": "Sign SH-4", "text": "Transferor and transferee sign and stamp the SH-4 transfer deed."},
   {"@type": "HowToStep", "position": 4, "name": "Lodge with the company", "text": "Deliver the deed and share certificate to the company within 60 days of signing."},
   {"@type": "HowToStep", "position": 5, "name": "Register and certify", "text": "The board approves, the register of members is updated, and the certificate is endorsed or reissued within one month."}]},
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
    <meta property="og:title" content="Share Transfer in Private Company – SH-4" />
    <meta property="og:description" content="Transfer private company shares the right way: SH-4, board approval, register updates and tax guidance by experts." />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Bharat e-Filing – Share Transfer" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bharatefiling" />
    <meta name="twitter:title" content="Share Transfer in Private Company – SH-4" />
    <meta name="twitter:description" content="Selling or gifting shares? Do the transfer right, from SH-4 to certificate." />
    <meta name="twitter:image" content="{OG}" />

'''
boiler = cut("    <!-- ===== SEARCH ENGINE VERIFICATION", "    <!-- ===== STRUCTURED DATA").replace(
    'service: "gst-registration"', 'service: "share-transfer"')
assert 'service: "share-transfer"' in boiler
sprite = cut("  <body", "    <!-- ================= ANNOUNCEMENT").replace('data-service="gst-registration"', 'data-service="share-transfer"')
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
