# Privacy Policy — Bharat e-Filing
# Legal basis checked 4 Oct 2026: DPDP Act 2023 (in force in phases), DPDP Rules 2025 (notified 13 Nov 2025; most duties from
# 13 May 2027), IT Act 2000 s.43A + SPDI Rules 2011 (apply until DPDP fully commences), CGST Act s.36, UIDAI Aadhaar masking.
# Every REPLACE_ value must be filled and the text reviewed by your lawyer before publishing.

META = dict(
    slug="privacy-policy",
    title="Privacy Policy – DPDP Act 2023 Compliant | Bharat e-Filing",
    description="How Bharat e-Filing collects, uses, shares, protects and deletes your personal data under the DPDP Act, 2023 and DPDP Rules, 2025. Your rights explained.",
    h1_crumb="Privacy Policy",
    service="privacy-policy",
    category="legal",
    dl_page_type="legal",
    og_title="Privacy Policy – Bharat e-Filing",
    og_desc="Plain-language privacy policy: what we collect, why, who we share it with, how long we keep it and your rights under the DPDP Act, 2023.",
    ribbon_html='Updated for the DPDP Rules, 2025. <a href="#law-timeline" data-track="cta_click" data-location="ribbon">See what changed ›</a>',
    localnav=[
        ("summary", "Summary"),
        ("what-we-collect", "What we collect"),
        ("why-we-use-it", "Why"),
        ("who-we-share-with", "Sharing"),
        ("how-long-we-keep-it", "Retention"),
        ("your-rights", "Your rights"),
        ("security", "Security"),
        ("grievance", "Contact"),
    ],
    cta_label="Contact us",
    modal_heading="Talk to Bharat e-Filing",
    modal_tick="GST, income tax, company and trademark",
    modal_options=[
        ("privacy", "A privacy or data request", "0"),
        ("gst", "GST services", "0"),
        ("income-tax", "Income tax / ITR", "0"),
        ("business", "Company or business registration", "0"),
        ("trademark", "Trademark", "0"),
    ],
    whatsapp_text="Hi, I have a question about my data",
    published="2026-10-04",
    modified="2026-10-04",
)

JSONLD = []

FAQ = [
    ("Does Bharat e-Filing sell my personal data?",
     "No. We do not sell or rent your personal data. We share it only with government portals when you ask us to file something, with service providers who process it for us under contract, or when the law requires it."),
    ("Which law protects my personal data in India?",
     "The Digital Personal Data Protection Act, 2023 and the DPDP Rules, 2025. The Rules were notified on 13 November 2025 and most duties of businesses apply from 13 May 2027. Until then, Section 43A of the Information Technology Act, 2000 and the SPDI Rules, 2011 also apply. We follow both."),
    ("Why do you need my PAN and Aadhaar?",
     "Government portals require them. GST registration, income-tax returns, company incorporation and Udyam registration are all PAN-based, and Aadhaar authentication is part of these processes. We use them only to complete the service you asked for."),
    ("Do you store my full Aadhaar number?",
     "No. In line with UIDAI requirements we store only a masked Aadhaar number, showing at most the last four digits. If you send us an Aadhaar card image, we mask it before storing it in your file."),
    ("How long do you keep my documents?",
     "We keep service records for as long as tax and company laws require, for example GST records for 72 months from the due date of the annual return under Section 36 of the CGST Act, and then delete or anonymise them. Leads that never became clients are deleted after 24 months of inactivity."),
    ("How do I get a copy of my data or ask you to delete it?",
     "Email our Grievance Officer or use the contact form on this page. We confirm your identity, then respond within 30 days. Some records cannot be deleted while a law requires us to keep them; we will tell you which and for how long."),
    ("Can I withdraw my consent?",
     "Yes, at any time, as easily as you gave it, by email, WhatsApp or the unsubscribe link in our messages. Withdrawal stops future processing based on consent; it does not affect work already done or records the law requires us to keep."),
    ("What happens if there is a data breach?",
     "We will inform you without delay with what happened, the likely impact and what we are doing about it, and report it to the Data Protection Board of India, with a detailed report within 72 hours as the DPDP Rules require."),
    ("Do you use cookies and tracking?",
     "Yes. Essential cookies keep the site working. Analytics and advertising tools such as Google Analytics, Google Ads, Meta Pixel and Microsoft Clarity run only after you accept them in our cookie banner, and you can change your choice at any time."),
    ("Who can I complain to if I am not satisfied?",
     "First contact our Grievance Officer, as the DPDP Act requires. If you are not satisfied with our response, you can complain to the Data Protection Board of India."),
]

MAIN = r"""
      <!-- ================= HERO ================= -->
      <section class="hero" aria-labelledby="page-title">
        <div class="hero__aurora" aria-hidden="true"><span></span><span></span><span></span></div>
        <div class="wrap hero__grid">
          <div>
            <nav class="crumbs" aria-label="Breadcrumb" data-rise style="--i: 0">
              <ol>
                <li><a href="https://bharatefiling.com/">Home</a></li>
                <li aria-current="page">Privacy Policy</li>
              </ol>
            </nav>
            <a class="pill-new" href="#law-timeline" data-rise style="--i: 1"><span class="pill-new__tag">Updated</span>DPDP Act 2023 &amp; DPDP Rules 2025</a>
            <h1 id="page-title" data-rise style="--i: 2">Privacy Policy. <span class="text-gradient">Your data, handled with care.</span></h1>
            <p class="hero__sub" data-rise style="--i: 3">
              You trust us with your PAN, Aadhaar, bank and tax details. This page explains, in plain words, exactly what we do with them and
              the rights you have.
            </p>
            <div class="btn-row" data-rise style="--i: 4">
              <a class="btn btn--brand" href="#summary" data-track="cta_click" data-location="hero">Read the 1-minute summary</a>
              <a class="btn btn--ghost" href="#grievance" data-track="cta_click" data-location="hero-grievance">Contact Grievance Officer</a>
            </div>
          </div>

          <aside class="factcard" data-rise style="--i: 3" aria-label="Policy at a glance">
            <h2>At a glance</h2>
            <dl>
              <div><dt>Effective from</dt><dd><time datetime="2026-10-04">4 October 2026</time></dd></div>
              <div><dt>Data fiduciary</dt><dd>REPLACE_LEGAL_ENTITY_NAME</dd></div>
              <div><dt>We sell your data?</dt><dd class="yes">Never</dd></div>
              <div><dt>Full Aadhaar stored?</dt><dd class="yes">No, masked</dd></div>
              <div><dt>Response to requests</dt><dd>Within 30 days</dd></div>
              <div><dt>Breach report to Board</dt><dd>Within 72 hours</dd></div>
              <div><dt>Grievance Officer</dt><dd><a href="#grievance">REPLACE_GRIEVANCE_OFFICER_NAME</a></dd></div>
            </dl>
          </aside>
        </div>
      </section>

      <!-- ================= SUMMARY (bento) ================= -->
      <section id="summary" class="section section--first" aria-labelledby="h-summary">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">The 1-minute version</span>
            <h2 id="h-summary">Our promises, at a glance.</h2>
            <p>The full policy follows below. If anything here conflicts with it, the full policy applies.</p>
          </div>
          <div class="bento">
            <div class="tile tile--wide tile--navy reveal">
              <h3>We collect only what the filing needs</h3>
              <p>
                Identity, contact, business and tax details needed to register, file or advise for you, plus basic website usage data. Nothing
                is collected "just in case".
              </p>
            </div>
            <div class="tile tile--brand reveal">
              <span class="tile__stat">Never</span>
              <h3>Sold or rented</h3>
              <p>Your personal data is not for sale, to anyone.</p>
            </div>
            <div class="tile reveal">
              <span class="tile__stat">30</span>
              <h3>Days to answer</h3>
              <p>Access, correction, erasure and grievance requests.</p>
            </div>
            <div class="tile tile--leaf reveal">
              <span class="tile__stat">XXXX</span>
              <h3>Aadhaar masked</h3>
              <p>Only the last four digits are ever stored.</p>
            </div>
            <div class="tile reveal">
              <span class="tile__stat">72 h</span>
              <h3>Breach reporting</h3>
              <p>Detailed report to the Data Protection Board.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= FULL POLICY ================= -->
      <div class="section">
        <article class="wrap wrap--read">
          <section class="chapter prose reveal" aria-labelledby="h-scope">
            <span class="kicker">1 · Scope</span>
            <h2 id="h-scope">Who we are and what this policy covers</h2>
            <p class="answer">
              <strong>Bharat e-Filing</strong> (operated by REPLACE_LEGAL_ENTITY_NAME, REPLACE_REGISTERED_ADDRESS) is the
              <strong>Data Fiduciary</strong> for personal data collected through bharatefiling.com, our WhatsApp, phone, email and offline
              channels. This policy explains what we collect, why, who we share it with, how long we keep it and how you can exercise your
              rights under the <strong>Digital Personal Data Protection Act, 2023</strong>.
            </p>
            <p>
              It applies to visitors, enquirers and clients, and to people whose data clients share with us (for example partners, directors or
              employees named in a filing). When we file on a government portal, that portal's own privacy terms also apply.
            </p>
          </section>

          <section id="what-we-collect" class="chapter prose reveal" aria-labelledby="h-collect">
            <span class="kicker">2 · What we collect</span>
            <h2 id="h-collect">The personal data we collect</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Categories of personal data</caption>
                <thead>
                  <tr>
                    <th scope="col">Category</th>
                    <th scope="col">Examples</th>
                    <th scope="col">Source</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><th scope="row">Contact</th><td>Name, mobile, email, city, preferred language</td><td>You (forms, WhatsApp, calls)</td></tr>
                  <tr><th scope="row">Identity</th><td>PAN, masked Aadhaar, photograph, date of birth, DIN/DSC details</td><td>You</td></tr>
                  <tr><th scope="row">Business &amp; tax</th><td>GSTIN, invoices, ledgers, bank statements, Form 16, AIS/TIS, financial statements</td><td>You or your accountant</td></tr>
                  <tr><th scope="row">Third-party people</th><td>Partners', directors' or employees' identity and contact details</td><td>Client providing them</td></tr>
                  <tr><th scope="row">Payment</th><td>Order amount, transaction ID, GSTIN for invoicing (card/UPI details stay with the payment gateway)</td><td>Payment partner</td></tr>
                  <tr><th scope="row">Website &amp; device</th><td>IP address, browser, pages viewed, campaign source (UTM, click IDs)</td><td>Cookies and analytics (with consent)</td></tr>
                  <tr><th scope="row">Communications</th><td>Call notes, WhatsApp and email messages, call recordings (announced before recording)</td><td>Our conversations with you</td></tr>
                </tbody>
              </table>
            </div>
            <div class="note note--good">
              <span class="note__title">In plain words</span>
              <p>We ask only for what a government form or your service actually needs. If a field is optional, the form says so.</p>
            </div>
          </section>

          <section id="why-we-use-it" class="chapter prose reveal" aria-labelledby="h-why">
            <span class="kicker">3 · Why we use it</span>
            <h2 id="h-why">Purposes and legal grounds</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Why we process personal data, and on what basis</caption>
                <thead>
                  <tr>
                    <th scope="col">Purpose</th>
                    <th scope="col">Legal ground (DPDP Act)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><th scope="row">Answer your enquiry and call you back</th><td>Consent you give on the form (Section 6), or a voluntary request by you (Section 7(a))</td></tr>
                  <tr><th scope="row">Prepare and file registrations and returns you asked for</th><td>Voluntary provision for a specified purpose (Section 7(a))</td></tr>
                  <tr><th scope="row">Invoices, payments, record-keeping</th><td>Records that tax and accounting laws require us to keep (retention permitted by Section 8(7))</td></tr>
                  <tr><th scope="row">Reminders about due dates for services you bought</th><td>Part of the service you requested (Section 7(a))</td></tr>
                  <tr><th scope="row">Offers, newsletters and ads tailored to you</th><td>Consent only, withdrawable any time (Section 6)</td></tr>
                  <tr><th scope="row">Security and fraud prevention</th><td>Reasonable security safeguards we must maintain (Section 8(5))</td></tr>
                  <tr><th scope="row">Responding to courts and authorities</th><td>Compliance with law, judgments and orders (Section 7(d) and 7(e))</td></tr>
                </tbody>
              </table>
            </div>
            <p>We do not use your data for automated decisions that legally affect you, and we do not track or target advertising at children.</p>
          </section>

          <section id="who-we-share-with" class="chapter prose reveal" aria-labelledby="h-share">
            <span class="kicker">4 · Sharing</span>
            <h2 id="h-share">Who we share it with</h2>
            <ul>
              <li><strong>Government portals, on your instruction:</strong> GST Network (for <a href="https://bharatefiling.com/gst-registration/">GST registration</a> and <a href="https://bharatefiling.com/gst-return-filing/">returns</a>), Income Tax Department (for <a href="https://bharatefiling.com/product/income-tax-e-filing/">ITR filing</a>), MCA, UIDAI (via portal authentication), DGFT, Udyam, IP India, FSSAI and others needed for your service.</li>
              <li><strong>Service providers (Data Processors)</strong> under written contracts: cloud hosting, email and WhatsApp messaging, CRM, payment gateway, e-signature and analytics. They may use the data only on our instructions.</li>
              <li><strong>Professionals</strong> working on your file: our Chartered Accountants, Company Secretaries and advocates, bound by confidentiality.</li>
              <li><strong>Authorities</strong> when a law, court order or government request requires it.</li>
              <li><strong>A successor business</strong> if we merge or transfer our business, with this policy continuing to apply.</li>
            </ul>
            <p>
              Some processors may store data outside India. Section 16 of the DPDP Act allows this except to countries the Government restricts;
              we will not transfer data to a restricted country.
            </p>
            <div class="note note--good">
              <span class="note__title">In plain words</span>
              <p>Your data goes to the government only when you ask us to file something, and to our vendors only so they can help us serve you.</p>
            </div>
          </section>

          <section id="how-long-we-keep-it" class="chapter prose reveal" aria-labelledby="h-keep">
            <span class="kicker">5 · Retention</span>
            <h2 id="h-keep">How long we keep it</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Retention periods</caption>
                <thead>
                  <tr>
                    <th scope="col">Data</th>
                    <th scope="col">Kept for</th>
                    <th scope="col">Why</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><th scope="row">Client service files and filed returns</th><td>8 years after the financial year of the service*</td><td>Covers GST (72 months from the annual-return due date, Section 36 CGST Act) and income-tax and company-law record periods</td></tr>
                  <tr><th scope="row">Invoices and payment records</th><td>8 years*</td><td>Our own tax and accounting obligations</td></tr>
                  <tr><th scope="row">Enquiries that did not become clients</th><td>24 months after last contact</td><td>Follow-up, then deleted</td></tr>
                  <tr><th scope="row">Security and access logs</th><td>1 year</td><td>Required by Rule 6 of the DPDP Rules, 2025</td></tr>
                  <tr><th scope="row">Marketing consent</th><td>Until you withdraw it</td><td>Proof of consent</td></tr>
                </tbody>
              </table>
            </div>
            <p class="muted" style="font-size: var(--fs-14)">* Longer if a notice, appeal or investigation is pending, until it is finally resolved.</p>
            <p>After the period ends, we delete or irreversibly anonymise the data. Where practical, we tell you before deleting data linked to an active account.</p>
          </section>

          <section id="your-rights" class="chapter prose reveal" aria-labelledby="h-rights">
            <span class="kicker">6 · Your rights</span>
            <h2 id="h-rights">Your rights under the DPDP Act</h2>
            <div class="grid grid--2">
              <div class="card"><h3>Access</h3><p>A summary of your data, what we do with it and who we shared it with (Section 11).</p></div>
              <div class="card"><h3>Correct &amp; erase</h3><p>Fix, complete or update your data, or have it erased when no longer needed (Section 12).</p></div>
              <div class="card"><h3>Withdraw consent</h3><p>As easily as you gave it. Future consent-based processing stops (Section 6(4)).</p></div>
              <div class="card"><h3>Grievance</h3><p>A response from our Grievance Officer, then the Data Protection Board if needed (Section 13).</p></div>
              <div class="card"><h3>Nominate</h3><p>Name someone to exercise your rights if you die or become unable to (Section 14).</p></div>
              <div class="card"><h3>Opt out of marketing</h3><p>Reply STOP on WhatsApp or use the unsubscribe link in any email.</p></div>
            </div>
            <p class="mt-8">
              <strong>How to use them:</strong> email REPLACE_GRIEVANCE_EMAIL or use the contact form. We verify your identity first, then respond
              within <strong>30 days</strong>, well inside the 90 days the DPDP Rules allow.
            </p>
            <p>
              <strong>Your duties too (Section 15):</strong> give accurate information, do not impersonate anyone, and do not file false complaints. The
              Act provides a penalty of up to ₹10,000 for breaching these duties.
            </p>
          </section>

          <section id="security" class="chapter prose reveal" aria-labelledby="h-security">
            <span class="kicker">7 · Security</span>
            <h2 id="h-security">How we protect your data</h2>
            <ul>
              <li>Encryption in transit (HTTPS) and at rest for stored documents.</li>
              <li>Role-based access: only the team handling your file can open it, with multi-factor sign-in.</li>
              <li>Aadhaar numbers masked to the last four digits; card images masked before storage.</li>
              <li>Access logs kept for one year and reviewed for unusual activity.</li>
              <li>Written confidentiality and data-protection terms with every employee and vendor.</li>
              <li>Backups to recover data if something goes wrong.</li>
            </ul>
            <div class="note note--alert">
              <span class="note__title">If a breach happens</span>
              <p>
                We will tell affected people without delay what happened, the likely impact and the steps we are taking, and report it to the
                Data Protection Board of India, with a detailed report within <strong>72 hours</strong> (Rule 7, DPDP Rules, 2025).
              </p>
            </div>
          </section>

          <section id="cookies" class="chapter prose reveal" aria-labelledby="h-cookies">
            <span class="kicker">8 · Cookies</span>
            <h2 id="h-cookies">Cookies and tracking</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Cookies we use</caption>
                <thead>
                  <tr>
                    <th scope="col">Type</th>
                    <th scope="col">Examples</th>
                    <th scope="col">Needs your consent?</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><th scope="row">Essential</th><td>Login, cart, checkout, security, cookie choice</td><td>No</td></tr>
                  <tr><th scope="row">Analytics</th><td>Google Analytics 4, Microsoft Clarity</td><td>Yes</td></tr>
                  <tr><th scope="row">Advertising</th><td>Google Ads, Meta Pixel, Microsoft Advertising</td><td>Yes</td></tr>
                </tbody>
              </table>
            </div>
            <p>Analytics and advertising tags stay off until you accept them in the cookie banner. You can change your choice any time from the "Cookie settings" link in the footer.</p>
          </section>

          <section id="children" class="chapter prose reveal" aria-labelledby="h-children">
            <span class="kicker">9 · Children</span>
            <h2 id="h-children">Children's data</h2>
            <p>
              Our services are for adults and businesses. If we need a minor's data (for example to file a return for a minor with income), we
              process it only with verifiable consent of the parent or lawful guardian, as Section 9 of the DPDP Act requires, and never for
              tracking, behavioural monitoring or targeted advertising.
            </p>
          </section>

          <section id="law-timeline" class="chapter prose" aria-labelledby="h-law">
            <span class="kicker reveal">10 · The law</span>
            <h2 id="h-law" class="reveal">How India's privacy law is changing</h2>
            <ol class="timeline">
              <li class="timeline__item">
                <time datetime="2027-05-13">13 May 2027</time>
                <h3>Most DPDP duties apply <span class="tag">Upcoming</span></h3>
                <p>Notice, consent, security, breach reporting, retention and rights rules (Rules 3 and 5–16) take effect, 18 months after notification. We already follow them.</p>
              </li>
              <li class="timeline__item">
                <time datetime="2026-11-13">13 November 2026</time>
                <h3>Consent Managers <span class="tag">Upcoming</span></h3>
                <p>Registration of Consent Managers begins (Rule 4), letting you manage consents across companies from one platform.</p>
              </li>
              <li class="timeline__item">
                <time datetime="2025-11-13">13 November 2025</time>
                <h3>DPDP Rules, 2025 notified <span class="tag tag--leaf">In force</span></h3>
                <p>The Data Protection Board of India is set up (Rules 1, 2 and 17–21). The phased timeline starts.</p>
              </li>
              <li class="timeline__item">
                <time datetime="2023-08-11">11 August 2023</time>
                <h3>DPDP Act, 2023 enacted</h3>
                <p>India's first comprehensive data protection law. Until it fully applies, Section 43A of the IT Act, 2000 and the SPDI Rules, 2011 continue to protect sensitive data such as financial information.</p>
              </li>
            </ol>
          </section>

          <section id="grievance" class="chapter prose reveal" aria-labelledby="h-grievance">
            <span class="kicker">11 · Contact</span>
            <h2 id="h-grievance">Grievance Officer and contact</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Who to contact about your personal data</caption>
                <tbody>
                  <tr><th scope="row">Grievance Officer</th><td>REPLACE_GRIEVANCE_OFFICER_NAME</td></tr>
                  <tr><th scope="row">Email</th><td>REPLACE_GRIEVANCE_EMAIL</td></tr>
                  <tr><th scope="row">Post</th><td>REPLACE_LEGAL_ENTITY_NAME, REPLACE_REGISTERED_ADDRESS</td></tr>
                  <tr><th scope="row">Response time</th><td>Acknowledged within 2 working days; resolved within 30 days</td></tr>
                  <tr><th scope="row">Escalation</th><td>Data Protection Board of India, after our response</td></tr>
                </tbody>
              </table>
            </div>
            <p>
              <strong>Changes to this policy:</strong> we will post updates here with a new effective date and, for material changes, tell clients
              by email or WhatsApp before they apply.
            </p>
            <p class="btn-row">
              <a class="btn btn--primary" href="#contact" data-modal-open data-plan="privacy" data-track="cta_click" data-location="grievance">Send a data request</a>
              <a class="link-arrow" href="https://bharatefiling.com/terms-and-conditions/">Read our Terms &amp; Conditions</a>
            </p>
          </section>
        </article>
      </div>

<!--FAQ-->
      <section class="wrap" aria-label="Related policies" style="padding-bottom: var(--section)">
        <div class="grid grid--3">
          <a class="card reveal" href="https://bharatefiling.com/terms-and-conditions/"><h3>Terms &amp; Conditions</h3><p>The rules for using our services.</p></a>
          <a class="card reveal" href="https://bharatefiling.com/refund-policy/"><h3>Refund Policy</h3><p>When and how fees are refunded.</p></a>
          <a class="card reveal" href="https://bharatefiling.com/confidentiality-policy/"><h3>Confidentiality Policy</h3><p>How we protect your business information.</p></a>
          <a class="card reveal" href="https://bharatefiling.com/disclaimer/"><h3>Disclaimer</h3><p>The limits of the information on our website.</p></a>
          <a class="card reveal" href="https://bharatefiling.com/contact-us/"><h3>Contact Us</h3><p>Call, WhatsApp or email our team.</p></a>
          <a class="card reveal" href="https://bharatefiling.com/about-us/"><h3>About Bharat e-Filing</h3><p>The CAs, CSs and lawyers behind your filings.</p></a>
        </div>
        <h2 class="mt-16" style="font-size: var(--fs-19)">Laws and official sources</h2>
        <ul class="sources">
          <li><a href="https://www.meity.gov.in/" rel="noopener" target="_blank">MeitY — DPDP Act, 2023 and DPDP Rules, 2025</a></li>
          <li><a href="https://www.indiacode.nic.in/" rel="noopener" target="_blank">India Code — Information Technology Act, 2000</a></li>
          <li><a href="https://cbic-gst.gov.in/" rel="noopener" target="_blank">CBIC — CGST Act, 2017 (Section 36 retention)</a></li>
          <li><a href="https://uidai.gov.in/" rel="noopener" target="_blank">UIDAI — Aadhaar handling and masking</a></li>
        </ul>
        <p class="muted mt-8" style="font-size: var(--fs-12)">
          This policy describes our practices and is not legal advice. Last reviewed <time datetime="2026-10-04">4 October 2026</time>.
        </p>
      </section>
"""
