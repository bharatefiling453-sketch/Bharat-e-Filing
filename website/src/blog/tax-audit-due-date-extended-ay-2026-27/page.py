# BLOG POST — Tax audit due date extended (CBDT Circular No. 07/2026)
# STANDARD BLOG FORMAT for Bharat e-Filing. Copy this folder for every new post and keep the section order:
#   read-progress → hero (chips, H1, dek, byline, share) → cover image → [article: mobile TOC, quick answer, key takeaways,
#   body H2s, inline images, mid-article CTA, author/reviewer card, FAQ, sources] + [sticky aside: TOC, CTA] → related posts.
# Facts checked 4 Oct 2026: Circular 07/2026 dated 28 Sep 2026 (audit report 30 Sep → 21 Oct 2026; ITR for serial 2 of
# Explanation 2 to s.139(1) 31 Oct → 21 Nov 2026); four-row due-date table substituted by Finance Act, 2026 w.e.f. 1 Mar 2026;
# s.536 ITA 2025 savings; s.44AB limits; s.271B (0.5%, max ₹1.5 lakh); s.234F; s.139(4) belated till 31 Dec.

SLUG = "blog/tax-audit-due-date-extended-ay-2026-27"
URL = f"https://bharatefiling.com/{SLUG}/"
BASE = "https://bharatefiling.com"
HEADLINE = "Tax Audit Due Date Extended to 21 October 2026: What CBDT Circular 7/2026 Means for You"
# Image placeholders: upload artwork to these paths (WebP/JPG, sizes as noted) and swap the .img-ph blocks for <img>.
IMG_COVER = f"{BASE}/wp-content/uploads/blog/tax-audit-due-date-extended-2026-cover-1200x675.jpg"

META = dict(
    slug=SLUG,
    title="Tax Audit Due Date Extended to 21 Oct 2026 | Bharat e-Filing",
    description="CBDT Circular 7/2026 extends the tax audit report date for AY 2026-27 to 21 October and the ITR date for audit cases to 21 November 2026. Who is covered.",
    h1_crumb="Tax audit due date extended",
    crumbs=[("Blog", f"{BASE}/blog/"), ("Income Tax", f"{BASE}/blog/category/income-tax/"), ("Tax audit due date extended", None)],
    service="blog-tax-audit-due-date",
    category="income-tax",
    dl_page_type="blog",
    og_type="article",
    section="Income Tax",
    tags=["Tax audit", "CBDT Circular 7/2026", "ITR due date", "AY 2026-27", "Section 44AB"],
    author_name="Bharat e-Filing Tax Desk",
    og_title="Tax audit due date extended to 21 Oct 2026; ITR for audit cases to 21 Nov",
    og_desc="What CBDT Circular 7/2026 changes, who is covered, what it does not fix (interest, penalties) and a 7-step plan to finish your audit on time.",
    ribbon_html='Tax audit report now due <strong>21 October 2026</strong>; ITR for audit cases <strong>21 November 2026</strong>. <a href="#get-started" data-modal-open data-track="cta_click" data-location="ribbon">Get it done by a CA ›</a>',
    localnav=None,
    cta_label="Talk to a CA",
    actionbar_label="Talk to a CA",
    modal_heading="Get your tax audit and ITR done on time",
    modal_tick="Tax audit coordination, ITR filing, notices",
    modal_select_label="I need help with",
    modal_options=[
        ("audit-itr", "Tax audit + ITR filing", "0"),
        ("itr-audit-case", "ITR for an audit case", "0"),
        ("company", "Company / LLP ITR · from ₹3,499", "3499"),
        ("firm", "Partnership firm ITR · from ₹2,999", "2999"),
        ("unsure", "Not sure if I need an audit", "0"),
    ],
    whatsapp_text="Hi, I need help with my tax audit and ITR",
    reviewed_by={"@id": f"{BASE}/#reviewer-ca"},
    published="2026-10-01",
    modified="2026-10-04",
    page_type="WebPage",
)

FAQ = [
    ("What is the new tax audit due date for AY 2026-27?",
     "Under CBDT Circular No. 07/2026 dated 28 September 2026, the tax audit report for AY 2026-27 (FY 2025-26) can be furnished up to 21 October 2026 instead of 30 September 2026."),
    ("What is the new ITR due date for audit cases for AY 2026-27?",
     "Companies, taxpayers whose accounts must be audited under any law, and partners of such firms can file their AY 2026-27 return up to 21 November 2026 instead of 31 October 2026, provided transfer pricing does not apply."),
    ("Does the extension apply to salaried individuals?",
     "No. Salaried and other non-business taxpayers had a due date of 31 July 2026, and non-audit business and professional taxpayers had 31 August 2026. Circular 7/2026 does not change those dates."),
    ("Are transfer pricing cases filing Form 3CEB covered?",
     "No. Where section 92E applies, the ITR due date stays 30 November 2026 and the Form 3CEB report stays due on 31 October 2026. Circular 7/2026 covers only serial number 2 of the due date table."),
    ("Will I still pay interest if I file by 21 November 2026?",
     "Interest under sections 234B and 234C for advance tax shortfalls is not affected. The circular extends the date under section 119 and does not amend section 139(1), so interest under section 234A on unpaid tax may still run from 31 October. Pay any balance tax by 31 October 2026."),
    ("What if I miss the 21 November 2026 deadline?",
     "You can still file a belated return up to 31 December 2026, unless assessment is completed earlier. A late fee under section 234F applies, and business and capital losses of the year cannot be carried forward."),
    ("What is the penalty for not filing the tax audit report on time?",
     "Section 271B allows a penalty of 0.5% of turnover or gross receipts, up to ₹1,50,000. It is not levied if you show a reasonable cause for the delay under section 273B."),
    ("Does a voluntary audit qualify for the extended date?",
     "No. The extension applies where an audit is required by law, under the Income-tax Act or another law such as the Companies Act or LLP Act. Getting books audited by choice does not move you into the audit category."),
    ("Why does the circular refer to the Income-tax Act, 1961 when the new Act is in force?",
     "The Income-tax Act, 2025 applies from 1 April 2026, but income of FY 2025-26 (AY 2026-27) is still governed by the 1961 Act through the savings provision in section 536 of the 2025 Act. The circular uses section 119 of the 1961 Act read with section 536."),
]

JSONLD = [
    {"@type": "Person", "@id": f"{BASE}/#reviewer-ca", "name": "REPLACE_CA_NAME", "jobTitle": "Chartered Accountant",
     "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "Membership", "recognizedBy": {"@type": "Organization", "name": "Institute of Chartered Accountants of India"}},
     "worksFor": {"@id": f"{BASE}/#organization"}},
    {
        "@type": "BlogPosting",
        "@id": URL + "#article",
        "headline": HEADLINE,
        "alternativeHeadline": "CBDT extends tax audit report date to 21 October and ITR for audit cases to 21 November 2026",
        "description": META["description"],
        "image": {"@type": "ImageObject", "@id": URL + "#primaryimage", "url": IMG_COVER, "width": 1200, "height": 675,
                  "caption": "Tax audit report due date moved from 30 September to 21 October 2026; ITR for audit cases from 31 October to 21 November 2026"},
        "datePublished": "2026-10-01T09:00:00+05:30",
        "dateModified": "2026-10-04T10:00:00+05:30",
        "author": {"@type": "Organization", "name": "Bharat e-Filing Tax Desk", "url": f"{BASE}/about-us/", "parentOrganization": {"@id": f"{BASE}/#organization"}},
        "publisher": {"@id": f"{BASE}/#organization"},
        "mainEntityOfPage": {"@id": URL + "#webpage"},
        "isPartOf": {"@id": f"{BASE}/#website"},
        "articleSection": "Income Tax",
        "keywords": ["tax audit due date extended", "tax audit due date AY 2026-27", "CBDT circular 7/2026",
                     "ITR due date for audit cases 2026", "21 October 2026 tax audit", "section 44AB"],
        "inLanguage": "en-IN",
        "isAccessibleForFree": True,
        "about": [{"@type": "Thing", "name": "Tax audit under section 44AB of the Income-tax Act, 1961"},
                  {"@type": "Legislation", "name": "CBDT Circular No. 07/2026", "legislationDate": "2026-09-28",
                   "legislationPassedBy": {"@type": "GovernmentOrganization", "name": "Central Board of Direct Taxes"}}],
        "mentions": [{"@type": "GovernmentOrganization", "name": "Central Board of Direct Taxes", "sameAs": "https://en.wikipedia.org/wiki/Central_Board_of_Direct_Taxes"},
                     {"@type": "Legislation", "name": "Income-tax Act, 1961"}, {"@type": "Legislation", "name": "Income-tax Act, 2025"}],
        "citation": ["https://www.incometax.gov.in/iec/foportal/latest-news", "https://www.incometaxindia.gov.in/cbdt",
                     "https://www.incometaxindia.gov.in/notifications", "https://www.indiabudget.gov.in/"],
        "wordCount": 0,  # filled in below
    },
]

IMG = lambda icon, title, note, cls="": f'''<div class="img-ph{(" " + cls) if cls else ""}" role="img" aria-label="{title}">
              <div><span class="img-ph__icon" aria-hidden="true">{icon}</span><strong>{title}</strong><span>{note}</span></div>
            </div>'''

TOC = [
    ("what-changed", "What CBDT announced"),
    ("who-is-covered", "Who gets the new dates"),
    ("not-changed", "What the extension does not change"),
    ("new-act", "Why the 1961 Act still applies"),
    ("key-dates", "Key dates at a glance"),
    ("audit-limits", "Who needs a tax audit"),
    ("penalties", "Penalties if you miss the dates"),
    ("action-plan", "7-step action plan"),
    ("faqs", "FAQs"),
]
_toc = "\n".join(f'                <li><a href="#{a}">{t}</a></li>' for a, t in TOC)

MAIN = f"""
      <div class="read-progress" aria-hidden="true"></div>

      <!-- ================= POST HERO ================= -->
      <header class="post-hero">
        <div class="hero__aurora" aria-hidden="true"><span></span><span></span><span></span></div>
        <div class="wrap">
          <div class="post-hero__inner">
            <nav class="crumbs" aria-label="Breadcrumb">
              <ol>
                <li><a href="{BASE}/">Home</a></li>
                <li><a href="{BASE}/blog/">Blog</a></li>
                <li><a href="{BASE}/blog/category/income-tax/">Income Tax</a></li>
                <li aria-current="page">Tax audit due date extended</li>
              </ol>
            </nav>
            <div class="post-chips">
              <span class="kicker">Income Tax · News</span>
              <span class="chip chip--live">Updated <time datetime="2026-10-04">4 Oct 2026</time></span>
              <span class="chip">AY 2026-27</span>
              <span class="chip"><span data-read-time>8</span>&nbsp;min read</span>
            </div>
            <h1 id="page-title">{HEADLINE}</h1>
            <p class="post-dek">CBDT has given audit cases 21 extra days. Here is exactly who benefits, what the extension does not fix, and a dated plan to finish your audit report and ITR without a penalty.</p>
            <div class="post-meta">
              <div class="post-meta__author">
                <span class="avatar" aria-hidden="true">BE</span>
                <div><strong>Bharat e-Filing Tax Desk</strong>Written by our tax team</div>
              </div>
              <div class="post-meta__author">
                <span class="avatar avatar--ca" aria-hidden="true">CA</span>
                <div><strong>REPLACE_CA_NAME, CA</strong>Fact-checked</div>
              </div>
              <ul class="post-meta__facts">
                <li>Published <time datetime="2026-10-01">1 Oct 2026</time></li>
              </ul>
              <div class="share" role="group" aria-label="Share this article">
                <a href="https://wa.me/?text=Tax%20audit%20due%20date%20extended%20to%2021%20Oct%202026%20{URL}" rel="noopener" target="_blank" data-track="share" data-location="whatsapp">WhatsApp</a>
                <a href="https://www.linkedin.com/sharing/share-offsite/?url={URL}" rel="noopener" target="_blank" data-track="share" data-location="linkedin">LinkedIn</a>
                <a href="https://x.com/intent/post?url={URL}&amp;text=Tax%20audit%20due%20date%20extended%20to%2021%20Oct%202026" rel="noopener" target="_blank" data-track="share" data-location="x">X</a>
                <button type="button" data-copy-link><span>Copy link</span></button>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div class="wrap">
        <!-- IMAGE PLACEHOLDER 1 (cover / featured image): 1200×675 WebP, also used as og:image. Alt text below. -->
        <figure class="post-figure post-figure--cover">
          {IMG("🗓️", "Featured image: tax audit due dates, old vs new", "1200 × 675 px · Infographic: 30 Sep → 21 Oct 2026 (audit report) and 31 Oct → 21 Nov 2026 (ITR for audit cases), Bharat e-Filing branding")}
          <figcaption>CBDT Circular No. 07/2026 moves both audit-case deadlines by 21 days.</figcaption>
        </figure>

        <div class="post-layout">
          <article class="post-body" data-article aria-labelledby="page-title">
            <details class="toc toc--mobile">
              <summary>In this article</summary>
              <ol>
{_toc}
              </ol>
            </details>

            <p class="answer lede"><strong>Quick answer:</strong> CBDT Circular No. 07/2026, dated 28 September 2026, extends the tax audit report deadline for AY 2026-27 from 30 September to <strong>21 October 2026</strong>, and the ITR deadline for companies, audit cases and partners of audited firms from 31 October to <strong>21 November 2026</strong>. Transfer-pricing cases and non-audit taxpayers are not covered.</p>

            <div class="datechange">
              <div class="datecard">
                <p class="datecard__what">Tax audit report (Form 3CA/3CB + 3CD)</p>
                <p class="datecard__old">30 September 2026</p>
                <p class="datecard__new">21 Oct 2026</p>
                <span class="datecard__left" data-deadline="2026-10-21">Deadline</span>
              </div>
              <div class="datecard">
                <p class="datecard__what">ITR for audit cases</p>
                <p class="datecard__old">31 October 2026</p>
                <p class="datecard__new">21 Nov 2026</p>
                <span class="datecard__left" data-deadline="2026-11-21">Deadline</span>
              </div>
            </div>

            <section class="takeaways mt-16" aria-labelledby="h-takeaways">
              <h2 id="h-takeaways">Key takeaways</h2>
              <ul>
                <li>Audit report: <strong>21 October 2026</strong>. ITR for audit cases: <strong>21 November 2026</strong>.</li>
                <li>Covers companies, taxpayers whose accounts must be audited by law, and partners of audited firms.</li>
                <li>Not covered: transfer-pricing cases (30 November), salaried (31 July) and non-audit business (31 August).</li>
                <li>Pay balance tax by <strong>31 October</strong>: the extension may not stop section 234A interest.</li>
                <li>Missing the audit report can cost up to <strong>₹1.5 lakh</strong>; a late ITR loses loss carry-forward.</li>
              </ul>
            </section>

            <p>If you run a business or practice that needs a tax audit, the last week of September was stressful. Two days before the deadline, the Central Board of Direct Taxes (CBDT) gave relief. This guide explains what changed, who benefits, what the extension does not fix, and how to use the extra 21 days well.</p>

            <h2 id="what-changed">What exactly did CBDT announce?</h2>
            <p>On 28 September 2026, CBDT issued <strong>Circular No. 07/2026</strong> under section 119 of the Income-tax Act, 1961. It extends the due date of the return of income for AY 2026-27 for one group of taxpayers: those at serial number 2 of the table in Explanation 2 to section 139(1). Under section 44AB, the tax audit report is due one month before that return due date, so the audit report date moved with it. The update is also listed on the Income Tax Department’s <a href="https://www.incometax.gov.in/iec/foportal/latest-news" rel="noopener" target="_blank">e-filing portal news page</a>.</p>
            <div class="table" tabindex="0">
              <table>
                <caption>Revised deadlines for AY 2026-27 under Circular No. 07/2026</caption>
                <thead><tr><th scope="col">Compliance</th><th scope="col">Earlier due date</th><th scope="col">Revised due date</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Tax audit report (Form 3CA-3CD or 3CB-3CD)</th><td>30 September 2026</td><td><strong>21 October 2026</strong></td></tr>
                  <tr><th scope="row">Income tax return for audit cases</th><td>31 October 2026</td><td><strong>21 November 2026</strong></td></tr>
                </tbody>
              </table>
            </div>

            <h2 id="who-is-covered">Who gets the extended due date?</h2>
            <p>The circular applies where transfer pricing (section 92E) does <em>not</em> apply and the taxpayer is one of these:</p>
            <ul>
              <li><strong>A company</strong>, whether or not it has income.</li>
              <li><strong>Any other taxpayer whose accounts must be audited</strong> under the Income-tax Act (a tax audit under section 44AB) or under any other law, such as proprietors, partnership firms, LLPs, HUFs, co-operative societies and trusts that need an audit.</li>
              <li><strong>A partner of a firm whose accounts must be audited</strong>, and the partner’s spouse where section 5A applies (income split under the Portuguese Civil Code, as in Goa).</li>
            </ul>

            <h3>Where you fit among the four ITR due dates</h3>
            <p>Many people still think there are only two ITR deadlines. The Finance Act, 2026 replaced Explanation 2 to section 139(1) with a four-row table from 1 March 2026, and it already applies to AY 2026-27. See all dates on our <a href="{BASE}/income-tax-return-filing/#due-dates">ITR filing guide</a>.</p>
            <!-- IMAGE PLACEHOLDER 2: 1200×675 infographic of the four due-date rows, with row 2 highlighted. -->
            <figure class="post-figure">
              {IMG("📊", "Infographic: the four ITR due dates for AY 2026-27", "1200 × 675 px · 31 Jul (others), 31 Aug (non-audit business), 21 Nov (audit cases, was 31 Oct), 30 Nov (transfer pricing)")}
              <figcaption>Only row 2 of the due-date table moves.</figcaption>
            </figure>
            <div class="table" tabindex="0">
              <table>
                <caption>ITR due dates for AY 2026-27 and the effect of Circular 7/2026</caption>
                <thead><tr><th scope="col">Who</th><th scope="col">Due date in law</th><th scope="col">After Circular 7/2026</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Transfer pricing cases (section 92E), including their partners</th><td>30 November 2026</td><td>No change</td></tr>
                  <tr><th scope="row">Companies, audit cases, partners of audited firms</th><td>31 October 2026</td><td><strong>21 November 2026</strong></td></tr>
                  <tr><th scope="row">Business or profession without audit, partners of non-audited firms</th><td>31 August 2026</td><td>No change (passed)</td></tr>
                  <tr><th scope="row">Everyone else, including salaried people</th><td>31 July 2026</td><td>No change (passed)</td></tr>
                </tbody>
              </table>
            </div>

            <h3>Am I covered? A quick check</h3>
            <ol class="decision">
              <li>
                <p class="decision__q">1. Must you file a transfer-pricing report (Form 3CEB)?</p>
                <p class="decision__a"><span class="decision__tag decision__tag--no">Yes</span>Not covered. ITR due 30 November 2026; Form 3CEB due 31 October 2026.</p>
                <p class="decision__a"><span class="decision__tag decision__tag--yes">No</span>Go to question 2.</p>
              </li>
              <li>
                <p class="decision__q">2. Is the taxpayer a company, or must its accounts be audited under any law?</p>
                <p class="decision__a"><span class="decision__tag decision__tag--yes">Yes</span>Covered. Audit report by 21 October, ITR by 21 November 2026.</p>
                <p class="decision__a"><span class="decision__tag decision__tag--no">No</span>Go to question 3.</p>
              </li>
              <li>
                <p class="decision__q">3. Are you a partner in a firm whose accounts must be audited?</p>
                <p class="decision__a"><span class="decision__tag decision__tag--yes">Yes</span>Covered for your own ITR. Deadline 21 November 2026.</p>
                <p class="decision__a"><span class="decision__tag decision__tag--no">No</span>This extension does not apply to you.</p>
              </li>
            </ol>
            <div class="note">
              <span class="note__title">A point most guides miss</span>
              <p>What matters is whether an audit is legally <em>required</em>, not whether you chose one. A small business that had its books audited voluntarily does not move into the audit category, so its due date stays 31 August.</p>
            </div>

            <h2 id="not-changed">What the extension does not change</h2>
            <p>An extended due date gives you more time to file. It does not change how tax and interest work.</p>
            <ul>
              <li><strong>Interest under sections 234B and 234C stays.</strong> These are for shortfalls or delays in advance tax, which was due during FY 2025-26.</li>
              <li><strong>Section 234A may still apply from 31 October.</strong> The circular extends the date administratively under section 119 and does not amend section 139(1). It is silent on 234A, so pay any balance self-assessment tax by 31 October 2026 to be safe.</li>
              <li><strong>Transfer-pricing deadlines stay.</strong> Form 3CEB remains due on 31 October 2026 and the ITR on 30 November 2026.</li>
              <li><strong>Audit limits stay the same.</strong> The extension does not change who needs an audit.</li>
              <li><strong>Other forms need their own check.</strong> Some forms are linked to the section 139(1) due date and others have fixed dates. Confirm each one with your CA.</li>
            </ul>

            <h2 id="new-act">Why is the 1961 Act still being used?</h2>
            <p>The Income-tax Act, 2025 came into force on 1 April 2026, so many taxpayers are surprised to see this circular cite the 1961 Act. Income earned between 1 April 2025 and 31 March 2026 belongs to the old law’s period, and <strong>section 536</strong> of the new Act (repeal and savings) lets the 1961 Act keep governing it.</p>
            <p>That is why the circular uses section 119 of the 1961 Act read with section 536 of the 2025 Act, and why “assessment year” and “previous year” still apply to this return. From FY 2026-27, the new Act’s single “tax year” takes over. Our <a href="{BASE}/income-tax-return-filing/#new-act">section map from the 1961 Act to the 2025 Act</a> shows the new numbers.</p>

            <h2 id="key-dates">Key dates at a glance</h2>
            <ol class="timeline">
              <li class="timeline__item"><time datetime="2026-09-28">28 September 2026</time><h3>Circular No. 07/2026 issued</h3><p>CBDT extends the dates for audit cases.</p></li>
              <li class="timeline__item"><time datetime="2026-10-21">21 October 2026</time><h3>Tax audit report deadline <span class="tag">Extended</span></h3><p>Your CA uploads the report and you accept it on the portal.</p></li>
              <li class="timeline__item"><time datetime="2026-10-31">31 October 2026</time><h3>Pay balance tax; Form 3CEB due</h3><p>Safe date for self-assessment tax; transfer-pricing report deadline.</p></li>
              <li class="timeline__item"><time datetime="2026-11-21">21 November 2026</time><h3>ITR deadline for audit cases <span class="tag">Extended</span></h3><p>File and e-verify within 30 days.</p></li>
              <li class="timeline__item"><time datetime="2026-12-31">31 December 2026</time><h3>Last date for a belated return</h3><p>With late fee and loss of carry-forward.</p></li>
            </ol>

            <h2 id="audit-limits">Who needs a tax audit for FY 2025-26?</h2>
            <p>A tax audit under section 44AB is a check of your books by a practising Chartered Accountant, reported in Form 3CA or 3CB along with Form 3CD. The main triggers:</p>
            <div class="table" tabindex="0">
              <table>
                <caption>Main tax audit triggers under section 44AB, FY 2025-26</caption>
                <thead><tr><th scope="col">Who</th><th scope="col">Audit needed when</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Business (general)</th><td>Turnover or gross receipts above ₹1 crore</td></tr>
                  <tr><th scope="row">Business with low cash dealings</th><td>Limit rises to ₹10 crore if cash receipts and cash payments are each within 5% of totals</td></tr>
                  <tr><th scope="row">Profession (doctor, lawyer, architect)</th><td>Gross receipts above ₹50 lakh</td></tr>
                  <tr><th scope="row">Professional under section 44ADA</th><td>Profit declared below 50% of receipts and income above the basic exemption limit</td></tr>
                  <tr><th scope="row">Business that left section 44AD early</th><td>Opted out within the five-year lock-in (section 44AD(4)) and income above the exemption limit</td></tr>
                  <tr><th scope="row">Sections 44AE, 44BB, 44BBB</th><td>Profit declared lower than the presumptive amount</td></tr>
                </tbody>
              </table>
            </div>
            <div class="note note--good">
              <span class="note__title">Good to know</span>
              <p>Presumptive taxpayers are outside the general limits. Section 44AD is available up to ₹2 crore turnover (₹3 crore if cash receipts are within 5%); section 44ADA up to ₹50 lakh of receipts (₹75 lakh if cash receipts are within 5%). F&amp;O traders: see our <a href="{BASE}/income-tax-return-filing/#fno">F&amp;O audit rules</a>.</p>
            </div>

            <h2 id="penalties">What happens if you miss the new dates?</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Consequences of missing the revised deadlines</caption>
                <thead><tr><th scope="col">Default</th><th scope="col">Consequence</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Audit report not furnished by 21 October 2026</th><td>Penalty under section 271B: 0.5% of turnover or gross receipts, up to ₹1,50,000. Not levied if you show reasonable cause (section 273B).</td></tr>
                  <tr><th scope="row">ITR filed after 21 November 2026</th><td>Late fee under section 234F: ₹5,000, or ₹1,000 if total income is up to ₹5 lakh. Belated return allowed only until 31 December 2026.</td></tr>
                  <tr><th scope="row">Tax unpaid on the due date</th><td>Interest of 1% a month under section 234A on the unpaid amount.</td></tr>
                  <tr><th scope="row">Loss return filed late</th><td>Business and capital losses of the year cannot be carried forward (unabsorbed depreciation is an exception).</td></tr>
                </tbody>
              </table>
            </div>
            <div class="note note--alert">
              <span class="note__title">The costliest mistake</span>
              <p>A firm with a loss this year can lose the right to set it off against future profits just because the ITR was filed one day late. Use our <a href="{BASE}/income-tax-return-filing/#late-calc">late fee and interest calculator</a> to see the cost.</p>
            </div>

            <aside class="post-cta" aria-labelledby="h-midcta">
              <div>
                <h2 id="h-midcta">Running out of time?</h2>
                <p>Our CAs coordinate your tax audit report and file your ITR before 21 November.</p>
              </div>
              <a class="btn btn--brand" href="#get-started" data-modal-open data-plan="audit-itr" data-track="cta_click" data-location="blog-mid">Talk to a CA</a>
            </aside>

            <h2 id="action-plan">Your 7-step action plan for the extra time</h2>
            <p>Three weeks sounds like plenty, but an audit depends on suppliers, banks and your CA. Work in this order:</p>
            <ol class="actions">
              <li><strong>Close the books for FY 2025-26 and freeze the trial balance.</strong><span class="by">By 8 October</span></li>
              <li><strong>Match turnover with GST returns and tax credits with Form 26AS and AIS.</strong> GSTR-1 and GSTR-3B turnover should agree with your books; see our <a href="{BASE}/gst-return-filing/">GST return filing guide</a>.<span class="by">By 10 October</span></li>
              <li><strong>Share supporting papers with your CA:</strong> loan statements, fixed-asset bills, <a href="{BASE}/services/tds-return-filing/">TDS returns</a> and related-party payments.<span class="by">By 12 October</span></li>
              <li><strong>Assign the audit form to your CA on the e-filing portal</strong> so they can upload it.<span class="by">By 12 October</span></li>
              <li><strong>Review the draft Form 3CD</strong>, especially cash payments above limits, late PF/ESI deposits and delayed MSME payments (section 43B(h)).<span class="by">By 16 October</span></li>
              <li><strong>Accept the uploaded report from your worklist.</strong> The filing is complete only after you accept it.<span class="by">By 19 October (buffer before the 21st)</span></li>
              <li><strong>Pay balance tax, file the ITR and e-verify</strong> within 30 days of filing.<span class="by">Tax by 31 October; ITR well before 21 November</span></li>
            </ol>
            <!-- IMAGE PLACEHOLDER 3: 1200×900 annotated screenshot of the e-filing portal Worklist → "For your action" → Accept/Reject audit form. Blur PAN/names. -->
            <figure class="post-figure">
              {IMG("🖥️", "Screenshot: accepting the tax audit report on the e-filing portal", "1200 × 900 px · Worklist → For your action → Accept, with PAN and names blurred", "img-ph--square")}
              <figcaption>Step 6: the audit report counts as filed only after the taxpayer accepts it.</figcaption>
            </figure>

            <div class="author-card">
              <span class="avatar" aria-hidden="true">BE</span>
              <div>
                <h2>About Bharat e-Filing Tax Desk</h2>
                <p>Our tax team tracks CBDT circulars and notifications daily and writes plain-English guides for businesses and individuals. Every article is fact-checked by a Chartered Accountant (REPLACE_CA_NAME, ICAI M. No. REPLACE) before publishing. Read our <a href="{BASE}/editorial-policy/">editorial policy</a> or learn more <a href="{BASE}/about-us/">about us</a>.</p>
              </div>
            </div>

            <h2 id="faqs">Frequently asked questions</h2>
<!--FAQ-INLINE-->

            <h2 class="mt-16" style="font-size: var(--fs-21)">Official sources</h2>
            <ul class="sources">
              <li><a href="https://www.incometax.gov.in/iec/foportal/latest-news" rel="noopener" target="_blank">Income Tax e-filing portal: News &amp; updates (Circular No. 07/2026)</a></li>
              <li><a href="https://www.incometaxindia.gov.in/cbdt" rel="noopener" target="_blank">CBDT: circulars and instructions</a></li>
              <li><a href="https://www.incometaxindia.gov.in/notifications" rel="noopener" target="_blank">Income Tax Department: notifications</a></li>
              <li><a href="https://www.indiabudget.gov.in/" rel="noopener" target="_blank">Finance Act, 2026 (Union Budget 2026-27)</a></li>
            </ul>
            <p class="muted" style="font-size: var(--fs-14)">This article is general information, not tax advice. Outcomes depend on your facts; consult a qualified professional before acting.</p>
          </article>

          <aside class="post-aside" aria-label="Article tools">
            <nav class="toc" aria-label="Table of contents">
              <p class="toc__title">In this article</p>
              <ol>
{_toc}
              </ol>
            </nav>
            <div class="aside-cta">
              <h2>Audit case? Let a CA handle it.</h2>
              <p>Tax audit coordination, ITR filing and e-verification, done before the deadline.</p>
              <a class="btn btn--brand btn--block" href="#get-started" data-modal-open data-plan="audit-itr" data-track="cta_click" data-location="blog-aside">Talk to a CA</a>
            </div>
          </aside>
        </div>
      </div>

      <!-- ================= RELATED ================= -->
      <section class="section section--glow" aria-labelledby="h-related">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">Keep reading</span>
            <h2 id="h-related">Related guides and services</h2>
          </div>
          <div class="post-cards">
            <!-- Blog URLs below are from the original draft; confirm they are live before publishing. -->
            <a class="post-card reveal" href="{BASE}/blog/tax-year-vs-assessment-year-income-tax-act-2025/">
              {IMG("📘", "Tax year vs assessment year", "Thumbnail 600 × 338")}
              <div class="post-card__body"><span>Income Tax</span><h3>Tax year vs assessment year: what changed from 1 April 2026</h3></div>
            </a>
            <a class="post-card reveal" href="{BASE}/income-tax-return-filing/">
              {IMG("🧾", "ITR filing", "Thumbnail 600 × 338")}
              <div class="post-card__body"><span>Service</span><h3>Income tax return filing: self-file or CA-assisted</h3></div>
            </a>
            <a class="post-card reveal" href="{BASE}/services/itr-for-llp/">
              {IMG("🏢", "ITR for LLP", "Thumbnail 600 × 338")}
              <div class="post-card__body"><span>Service</span><h3>ITR for LLPs and audited firms (ITR-5)</h3></div>
            </a>
          </div>
        </div>
      </section>
"""

PAGE_JS = r"""
      (function () {
        "use strict";
        var now = new Date();
        document.querySelectorAll("[data-deadline]").forEach(function (el) {
          var d = new Date(el.getAttribute("data-deadline") + "T23:59:59+05:30");
          var days = Math.ceil((d - now) / 86400000);
          el.textContent = days > 1 ? days + " days left" : days === 1 ? "Last day" : "Deadline passed";
        });
        var article = document.querySelector("[data-article]");
        var rt = document.querySelector("[data-read-time]");
        if (article && rt) rt.textContent = String(Math.max(1, Math.round(article.innerText.split(/\s+/).length / 220)));
      })();
"""

# wordCount for schema (visible article text, FAQ included)
import re as _re
_text = _re.sub(r"<[^>]+>", " ", MAIN.split('<article class="post-body"')[1].split("</article>")[0]) + " ".join(q + " " + a for q, a in FAQ)
JSONLD[1]["wordCount"] = len(_text.split())
