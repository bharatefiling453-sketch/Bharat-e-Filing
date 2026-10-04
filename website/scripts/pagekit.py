"""
Bharat e-Filing page kit — builds every new page with exactly the same shell as the GST pages
(head, header, local nav, footer, pop-up, mobile bar, fonts, tracking) so design never drifts.

A page source lives in  src/<slug>/page.py  and defines:
    META   = dict(slug, title, description, h1_crumb, service, og_title, og_desc, ribbon_html,
                  localnav: list[(anchor, label)], cta_label, modal_heading, modal_options: list[(value, label, price)],
                  whatsapp_text, published, modified)
    JSONLD = list of extra schema nodes (WebPage/Breadcrumb are added automatically)
    FAQ    = list[(question, answer)]          # rendered visibly AND as FAQPage schema (always identical)
    MAIN   = HTML string for everything inside <main> except the FAQ block; put <!--FAQ--> where it goes
    PAGE_JS (optional) = extra inline script

Build:  python3 scripts/pagekit.py <slug>      → <slug>/index.html
"""
import html as H
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://bharatefiling.com"
TEMPLATE = ROOT / "gst-registration" / "index.html"  # the reference page: shell is copied from here


def _between(text, start, end):
    i = text.index(start)
    return text[i : text.index(end, i)]


def _faq_html(faq):
    return "\n".join(
        f"""            <details{' open' if i == 0 else ''}>
              <summary>{H.escape(q, quote=False)}</summary>
              <div class="faq__a"><p>{H.escape(a, quote=False)}</p></div>
            </details>"""
        for i, (q, a) in enumerate(faq)
    )


def faq_section(faq, heading="Questions? Answered."):
    return f"""      <!-- Visible FAQ text MUST match the FAQPage JSON-LD word for word (built from one list by pagekit). -->
      <section id="faqs" class="section" aria-labelledby="h-faq">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">FAQs</span>
            <h2 id="h-faq">{heading}</h2>
          </div>
          <div class="faq">
{_faq_html(faq)}
          </div>
        </div>
      </section>
"""


def testimonials_section(service=None, heading="What our clients say."):
    """Renders ONLY real reviews from src/testimonials.json (optionally filtered by service). Empty list → empty string."""
    data = json.loads((ROOT / "src" / "testimonials.json").read_text())
    reviews = [r for r in data.get("reviews", []) if not service or service in r.get("services", [])]
    if not reviews:
        return ""
    cards = "\n".join(
        f"""            <figure class="review reveal">
              <div class="review__stars" aria-label="{int(r['rating'])} out of 5 stars">{'★' * int(r['rating'])}{'☆' * (5 - int(r['rating']))}</div>
              <blockquote><p>{H.escape(r['text'], quote=False)}</p></blockquote>
              <figcaption><strong>{H.escape(r['name'], quote=False)}</strong><span>{H.escape(r.get('city', ''), quote=False)}{' · ' + H.escape(r['service_label'], quote=False) if r.get('service_label') else ''}</span>
                <a href="{H.escape(r['url'])}" rel="noopener" target="_blank">{H.escape(r.get('source', 'Google'), quote=False)} review, <time datetime="{r['date']}">{r['date']}</time></a></figcaption>
            </figure>"""
        for r in reviews
    )
    more = data.get("google_profile_url")
    more_html = f'<p class="center mt-8"><a class="link-arrow" href="{H.escape(more)}" rel="noopener" target="_blank">Read all reviews on Google</a></p>' if more else ""
    return f"""      <section id="reviews" class="section" aria-labelledby="h-reviews">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">Client reviews</span>
            <h2 id="h-reviews">{heading}</h2>
            <p>Verified reviews, shown word for word from {H.escape(reviews[0].get('source', 'Google'), quote=False)}.</p>
          </div>
          <div class="reviews">
{cards}
          </div>
          {more_html}
        </div>
      </section>
"""


def build(slug):
    spec_path = ROOT / "src" / slug / "page.py"
    spec = importlib.util.spec_from_file_location("page", spec_path)
    page = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(page)
    M, FAQ = page.META, page.FAQ
    url = f"{BASE}/{slug}/"
    ref = TEMPLATE.read_text()
    ld_ref = json.loads(_between(ref, '<script type="application/ld+json">', "</script>").split(">", 1)[1])
    org, site = ld_ref["@graph"][0], ld_ref["@graph"][1]

    graph = [
        org,
        site,
        {
            "@type": M.get("page_type", "WebPage"),
            "@id": url + "#webpage",
            "url": url,
            "name": M["title"],
            "description": M["description"],
            "inLanguage": "en-IN",
            "isPartOf": {"@id": f"{BASE}/#website"},
            "breadcrumb": {"@id": url + "#breadcrumb"},
            "datePublished": M["published"],
            "dateModified": M["modified"],
            "publisher": {"@id": f"{BASE}/#organization"},
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".answer"]},
        },
        {
            "@type": "BreadcrumbList",
            "@id": url + "#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"}]
            + [
                {"@type": "ListItem", "position": i + 2, "name": name, **({"item": link} if link else {})}
                for i, (name, link) in enumerate(M.get("crumbs", [(M["h1_crumb"], None)]))
            ],
        },
        *page.JSONLD,
    ]
    if FAQ:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": url + "#faq",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
            }
        )
    jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    jsonld = "\n".join("      " + line for line in jsonld.splitlines())

    # ---- <head>: reference head with page values swapped in
    head = ref.split("<body", 1)[0]
    head = head.split('<script type="application/ld+json">', 1)[0]
    head = re.sub(r"<title>.*?</title>", "<title>" + H.escape(M["title"], quote=False) + "</title>", head, flags=re.S)
    head = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', lambda m: m.group(1) + H.escape(M["description"]) + m.group(2), head)
    head = head.replace(f"{BASE}/gst-registration/", url).replace("/hi/gst-registration/", f"/hi/{slug}/")
    head = re.sub(r'(property="og:title" content=")[^"]*', lambda m: m.group(1) + H.escape(M["og_title"]), head)
    head = re.sub(r'(property="og:description" content=")[^"]*', lambda m: m.group(1) + H.escape(M["og_desc"]), head)
    head = re.sub(r'(name="twitter:title" content=")[^"]*', lambda m: m.group(1) + H.escape(M["og_title"]), head)
    head = re.sub(r'(name="twitter:description" content=")[^"]*', lambda m: m.group(1) + H.escape(M["og_desc"]), head)
    head = head.replace("og/gst-registration-1200x630.jpg", f"og/{slug}-1200x630.jpg")
    head = re.sub(r'(property="og:image:alt" content=")[^"]*', lambda m: m.group(1) + "Bharat e-Filing – " + H.escape(M["h1_crumb"]), head)
    head = re.sub(r'service: "[^"]*", service_category: "[^"]*"', f'service: "{M["service"]}", service_category: "{M.get("category", "company")}"', head)
    head = head.replace('page_type: "service"', f'page_type: "{M.get("dl_page_type", "service")}"')
    head += '<script type="application/ld+json">\n' + jsonld + "\n    </script>\n  </head>\n\n  "
    assert "gst-registration" not in head.split("application/ld+json")[0], "stale reference page value in <head>"

    # ---- shared body pieces copied verbatim from the reference page
    top = _between(ref, "    <noscript", "    <!-- ================= LOCAL NAV")
    ribbon_old = top[top.index('<p class="ribbon">') : top.index("</p>", top.index('<p class="ribbon">')) + 4]
    top = top.replace(ribbon_old, f'<p class="ribbon">\n      {M["ribbon_html"]}\n    </p>')
    top = top.replace('<li><a href="https://bharatefiling.com/product-category/gst/" aria-current="page">GST</a></li>',
                      '<li><a href="https://bharatefiling.com/product-category/gst/">GST</a></li>')
    footer = _between(ref, "    <!-- ================= FOOTER", "    <!-- ================= LEAD POP-UP")
    modal = _between(ref, "    <!-- ================= LEAD POP-UP", "    <!-- Mobile action bar -->")
    actionbar = _between(ref, "    <!-- Mobile action bar -->", '    <script src="../assets/js/bef-page.js" defer></script>')

    opts = "\n".join(
        f'                <option value="{v}" data-price="{p}"{" selected" if i == 0 else ""}>{H.escape(lbl, quote=False)}</option>'
        for i, (v, lbl, p) in enumerate(M["modal_options"])
    )
    modal = re.sub(r"(<select id=\"m-plan\" name=\"plan\">).*?(</select>)", lambda m: m.group(1) + "\n" + opts + "\n              " + m.group(2), modal, flags=re.S)
    modal = re.sub(r'(<label for="m-plan">)[^<]*', r"\1" + M.get("modal_select_label", "I need help with"), modal)
    modal = modal.replace("Start your GST registration", M["modal_heading"]).replace('id="gst-popup-form"', f'id="{slug}-popup-form"')
    modal = modal.replace('value="gst-registration"', f'value="{M["service"]}"').replace("Single or multi-state registration", M.get("modal_tick", "GST, income tax, company and trademark"))
    wa = M["whatsapp_text"].replace(" ", "%20").replace(",", "%2C")
    actionbar = actionbar.replace("Hi%2C%20I%20need%20GST%20registration", wa).replace(">Apply now<", f">{M['cta_label']}<")

    localnav = "\n".join(f'          <li><a href="#{a}">{H.escape(l, quote=False)}</a></li>' for a, l in M["localnav"])
    localnav_html = f"""    <!-- ================= LOCAL NAV (sticky, Apple-style) ================= -->
    <nav class="localnav" aria-label="On this page">
      <div class="wrap">
        <span class="localnav__title">{H.escape(M["h1_crumb"], quote=False)}</span>
        <ul>
{localnav}
        </ul>
        <a class="btn btn--brand btn--sm" href="{M.get('cta_href', '#get-started')}" data-modal-open data-track="cta_click" data-location="localnav">{M["cta_label"]}</a>
      </div>
    </nav>

"""
    main = page.MAIN.replace("<!--FAQ-->", faq_section(FAQ) if FAQ else "")
    main = main.replace("<!--REVIEWS-->", testimonials_section(M.get("reviews_service")))
    page_js = getattr(page, "PAGE_JS", "")
    doc = (
        head
        + f'<body data-service="{M["service"]}">\n'
        + top
        + localnav_html
        + '    <main id="main">\n'
        + main
        + "    </main>\n\n"
        + footer
        + modal
        + actionbar
        + '    <script src="../assets/js/bef-page.js" defer></script>\n'
        + (f"    <script>\n{page_js}\n    </script>\n" if page_js else "")
        + "  </body>\n</html>\n"
    )
    out = ROOT / slug / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(doc)
    print(f"built {out.relative_to(ROOT)} ({len(doc) // 1024} KB)")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        build(s)
