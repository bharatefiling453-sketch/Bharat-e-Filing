# Income Tax Return (ITR) Filing — Bharat e-Filing
# Facts checked 4 Oct 2026: AY 2026-27 due dates (31 Jul ITR-1/2; 31 Aug ITR-3/4 non-audit per Finance Act 2026; 31 Oct audit;
# belated 31 Dec 2026; revised to 31 Mar 2027), slabs FY 2025-26 = FY 2026-27, 87A ₹60,000 (new) / ₹12,500 (old), ITR forms
# notified 30 Mar 2026 (ITR-1: two house properties), ITR-U 48 months (Finance Act 2025), Income-tax Act 2025 mapping.
# Prices from live site: individuals ₹2,499–4,499, firms ₹2,999–4,999, LLP/company ₹3,499–5,999 (salaried price to confirm).

SLUG = "income-tax-return-filing"

# PROPOSED package prices (benchmarked against ClearTax / TaxBuddy, Oct 2026) — CONFIRM with Bharat e-Filing before launch.
# Keep in sync with: packages section, hero plan picker, pop-up options and JSON-LD (all generated from / checked against this list).
PACKAGES = [
    ("salary", "Salary & Pension", "2499"),
    ("freelancer", "Freelancers & Professionals", "2999"),
    ("late-revised", "Belated, Revised & Updated Return", "2999"),
    ("capital-gains", "Capital Gains", "3499"),
    ("fno", "F&O & Intraday Traders", "4499"),
    ("crypto", "Crypto & VDA", "4499"),
    ("nri", "NRI Returns", "4499"),
    ("foreign", "Foreign Income, RSU & ESOP", "6999"),
    ("all-in-one", "All-in-One / High Income", "7999"),
    ("business", "Proprietors & Small Business", "3499"),
    ("firm", "Partnership Firm", "2999"),
    ("company", "LLP or Company", "3499"),
]

# APP_URL: the self-filing web app. REPLACE with the live URL once the ERI (Type-2) app is launched.
APP_URL = "https://bharatefiling.com/itr/start/"
# PROPOSED self-filing prices (benchmarked: ClearTax DIY free for basic salary, paid tiers for capital gains/F&O) — CONFIRM.
SELF_PLANS = [
    ("self-basic", "Self-file Basic", "Free", "ITR-1", ["Salary or pension (one Form 16)", "Up to two house properties", "Interest and dividend income", "Auto-import from AIS and Form 26AS", "Regime comparison and e-verify"]),
    ("self-plus", "Self-file Plus", "₹499", "ITR-1 / ITR-2", ["Everything in Basic", "Multiple Form 16 (job change)", "Capital gains from broker and CAS statements", "Property sale with indexation choice", "Loss carry-forward"]),
    ("self-pro", "Self-file Pro", "₹999", "ITR-2 / ITR-3 / ITR-4", ["Everything in Plus", "F&O and intraday with turnover auto-calculated", "Crypto (Schedule VDA)", "Freelancer and presumptive business income", "Foreign assets (Schedule FA) and Form 67 reminder"]),
]

URL = f"https://bharatefiling.com/{SLUG}/"

META = dict(
    slug=SLUG,
    title="File ITR Online Yourself or with a CA | Bharat e-Filing",
    description="File your ITR yourself in minutes with data imported from AIS and Form 26AS, or let a CA file it. AY 2026-27 due dates, calculators, F&O, crypto and NRI.",
    h1_crumb="Income Tax Return Filing",
    crumbs=[("Income Tax", "https://bharatefiling.com/product/income-tax-e-filing/"), ("Income Tax Return Filing", None)],
    service=SLUG,
    category="income-tax",
    og_title="File your ITR yourself in minutes, or with a CA",
    og_desc="Self-file with auto-import from the Income Tax Department, or choose a CA-assisted package for capital gains, F&O, crypto, NRI and business income.",
    ribbon_html='Missed 31 July? A belated ITR for FY 2025-26 can still be filed until 31 December 2026. <a href="#due-dates" data-track="cta_click" data-location="ribbon">See all dates ›</a>',
    localnav=[
        ("self-filing", "Self-file"),
        ("expert", "CA-assisted"),
        ("packages", "Packages"),
        ("self-vs-ca", "Compare"),
        ("tools", "Calculators"),
        ("due-dates", "Due dates"),
        ("tax-regimes", "Tax slabs"),
        ("special-income", "F&O, crypto, foreign"),
        ("faqs", "FAQs"),
    ],
    cta_label="Start filing",
    cta_href="https://bharatefiling.com/itr/start/",  # = APP_URL
    cta_modal=False,
    actionbar_label="Start filing",
    modal_heading="Start your ITR filing",
    modal_tick="Salaried, business, firm, LLP or company",
    modal_select_label="Package",
    modal_options=[(v, f"{n} · ₹{int(p):,}", p) for v, n, p in PACKAGES] + [("unsure", "Not sure yet", "0")],
    whatsapp_text="Hi, I need help filing my ITR",
    published="2026-10-04",
    modified="2026-10-04",
)

JSONLD = [
    {
        "@type": "Service",
        "@id": URL + "#service",
        "name": "Income Tax Return Filing",
        "alternateName": ["ITR Filing", "Income Tax e-Filing", "ITR Filing Online"],
        "serviceType": "Income tax return preparation and e-filing",
        "description": "CA-reviewed preparation, e-filing and e-verification of ITR-1 to ITR-7 for individuals, HUFs, firms, LLPs and companies, including belated, revised and updated returns.",
        "provider": {"@id": "https://bharatefiling.com/#organization"},
        "areaServed": {"@type": "Country", "name": "India"},
        "termsOfService": "https://bharatefiling.com/terms-and-conditions/",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "ITR filing plans",
            "itemListElement": [
                {"@type": "Offer", "name": n, "price": p, "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": URL + "#packages"}
                for _, n, p in PACKAGES
            ] + [
                {"@type": "Offer", "name": n, "price": "0" if p == "Free" else p.strip("₹"), "priceCurrency": "INR", "url": URL + "#self-filing"}
                for _, n, p, _f, _i in SELF_PLANS
            ],
        },
    },
    {
        "@type": "HowTo",
        "@id": URL + "#howto",
        "name": "How to file an income tax return online",
        "step": [
            {"@type": "HowToStep", "position": 1, "name": "Collect documents", "text": "Gather Form 16, AIS/TIS, Form 26AS, bank interest certificates, capital-gain statements and deduction proofs."},
            {"@type": "HowToStep", "position": 2, "name": "Choose the ITR form and regime", "text": "Pick ITR-1 to ITR-7 based on your income sources and decide between the new and old tax regime."},
            {"@type": "HowToStep", "position": 3, "name": "Compute income and tax", "text": "Reconcile income with AIS and Form 26AS, claim eligible deductions and pay any balance tax as self-assessment tax."},
            {"@type": "HowToStep", "position": 4, "name": "File on the e-filing portal", "text": "Upload the return on incometax.gov.in before the due date."},
            {"@type": "HowToStep", "position": 5, "name": "E-verify within 30 days", "text": "E-verify with Aadhaar OTP, net banking or a pre-validated bank account within 30 days of filing."},
        ],
    },
]

FAQ = [
    ("What is the last date to file ITR for FY 2025-26 (AY 2026-27)?",
     "31 July 2026 for individuals filing ITR-1 or ITR-2, 31 August 2026 for non-audit business and professional cases filing ITR-3 or ITR-4 (extended by the Finance Act, 2026), 31 October 2026 for tax-audit cases and 30 November 2026 for transfer-pricing cases. A belated return can be filed until 31 December 2026."),
    ("Can I still file my ITR after the due date?",
     "Yes. You can file a belated return until 31 December 2026 with a late fee of ₹5,000, or ₹1,000 if total income is up to ₹5 lakh, plus 1% a month interest on unpaid tax. Losses other than house-property loss cannot be carried forward in a belated return. After that, an updated return (ITR-U) can be filed within 48 months."),
    ("Which ITR form should I file?",
     "ITR-1 for resident individuals with income up to ₹50 lakh from salary, up to two house properties and other sources; ITR-2 for individuals with capital gains or foreign assets but no business income; ITR-3 for business or professional income; ITR-4 for presumptive income up to ₹50 lakh; ITR-5 for firms and LLPs; ITR-6 for companies; and ITR-7 for trusts and similar entities."),
    ("Do I need to file ITR if my income is below the taxable limit?",
     "Yes, in several cases: if you deposited over ₹1 crore in current accounts or ₹50 lakh in savings accounts, spent over ₹2 lakh on foreign travel or ₹1 lakh on electricity, had TDS or TCS of ₹25,000 or more (₹50,000 for senior citizens), business turnover above ₹60 lakh, professional receipts above ₹10 lakh, or foreign assets. Filing is also the only way to claim a refund."),
    ("Is income up to ₹12 lakh tax-free?",
     "Under the new tax regime, resident individuals with taxable income up to ₹12 lakh get a full rebate of up to ₹60,000, so they pay no tax; with the ₹75,000 standard deduction, salary up to ₹12.75 lakh is effectively tax-free. The rebate does not apply to tax on special-rate income such as capital gains."),
    ("Which is better for me: the new or the old tax regime?",
     "The new regime is the default and usually better unless your deductions are large, for example a home-loan interest claim, full 80C investments and HRA. Salaried taxpayers can choose a regime every year while filing; taxpayers with business income can switch back to the new regime only once. Use our calculator to compare."),
    ("What is an updated return (ITR-U)?",
     "An updated return lets you report income you missed, within 48 months from the end of the assessment year, after the Finance Act, 2025 extended the window from 24 months. You pay additional tax of 25%, 50%, 60% or 70% of the tax and interest due, depending on whether you file within the first, second, third or fourth year."),
    ("Can I revise my ITR if I made a mistake?",
     "Yes. After Budget 2026, a revised return for AY 2026-27 can be filed until 31 March 2027, before assessment is completed. A fee applies if you revise after 31 December 2026."),
    ("Is e-verification mandatory after filing?",
     "Yes. You must e-verify within 30 days of filing, using Aadhaar OTP, net banking, a pre-validated bank or demat account, or by sending a signed ITR-V. If you verify late, the verification date is treated as the filing date and a late fee may apply."),
    ("How long does an income tax refund take?",
     "Refunds are issued after the return is processed, which starts only after e-verification. Many simple returns are processed within a few weeks. The refund goes to a pre-validated bank account linked to your PAN, and delayed refunds earn interest under Section 244A."),
    ("What documents do I need to file my ITR?",
     "PAN, Aadhaar, Form 16 if salaried, AIS, TIS and Form 26AS, bank interest certificates, capital-gain statements from your broker or mutual fund, rent receipts and investment proofs if you choose the old regime, and books of account or a profit-and-loss statement if you have business income."),
    ("How are capital gains on shares taxed now?",
     "For listed equity shares and equity mutual funds sold on or after 23 July 2024, short-term gains are taxed at 20% and long-term gains above ₹1.25 lakh a year at 12.5%. These rates apply on top of your slab income and the Section 87A rebate does not reduce them."),
    ("What changes for ITR filing under the Income-tax Act, 2025?",
     "Returns for FY 2025-26 are filed under the Income-tax Act, 1961. From tax year 2026-27, the Income-tax Act, 2025 applies: return filing moves from Section 139 to Section 263, the new regime from Section 115BAC to Section 202, the rebate from Section 87A to Section 156 and the 80C deduction to Section 123."),
    ("Can I file my ITR myself on Bharat e-Filing?",
     "Yes. Sign up with your PAN, approve access with the OTP sent by the Income Tax Department, and we import your pre-filled data, AIS and Form 26AS. You review the suggested ITR form, regime and deductions, then file and e-verify with Aadhaar OTP. Self-filing is free for simple salary returns."),
    ("Is it safe to file my ITR through Bharat e-Filing?",
     "Bharat e-Filing files through the Income Tax Department's e-Return Intermediary (ERI) system. We access your data only after you approve with an OTP from the department, use it only to prepare and file your return under the DPDP Act, 2023, and never sell it. You can withdraw access anytime."),
    ("What is an e-Return Intermediary (ERI)?",
     "An ERI is an entity registered with the Income Tax Department to file returns on behalf of taxpayers. Type-2 ERIs build their own filing software that connects to the department's APIs to fetch pre-filled data, validate and submit returns, so taxpayers do not have to retype their information."),
    ("Should I file my ITR myself or with a CA?",
     "Self-filing on Bharat e-Filing suits salary, interest, rent and most capital gains, because data is imported and checked automatically. Choose CA-assisted filing if you hold foreign assets or RSUs, are an NRI, need a tax audit, have business income with books, received a notice, or want an expert to take responsibility for the return."),
    ("Which ITR do F&O traders file, and how is F&O income taxed?",
     "F&O traders file ITR-3 with a profit-and-loss account and balance sheet. F&O income is non-speculative business income taxed at slab rates after expenses; intraday equity is speculative. F&O losses can be set off against other income except salary and carried forward for 8 years if you file by the due date."),
    ("Do I need a tax audit for F&O trading losses?",
     "Only in some cases. An audit is required if trading turnover, calculated as the sum of absolute profits and losses, exceeds ₹10 crore. Below that, an audit may apply if you opted out of presumptive taxation under Section 44AD in the last five years and your income exceeds the basic exemption limit."),
    ("How is cryptocurrency taxed in India?",
     "Gains on crypto and other virtual digital assets are taxed at a flat 30% plus cess under Section 115BBH. Only the purchase cost is deductible, losses cannot be set off or carried forward, and 1% TDS under Section 194S applies on sales. Every transfer is reported in Schedule VDA."),
    ("Do I have to report foreign stocks, RSUs or foreign bank accounts?",
     "Yes, if you are resident and ordinarily resident. Report every foreign asset held at any time in the calendar year in Schedule FA, even without income. RSUs are taxed as salary on vesting, and you claim credit for foreign tax by filing Form 67 before the return. Non-disclosure can attract a ₹10 lakh penalty."),
    ("Do NRIs need to file an income tax return in India?",
     "An NRI must file if Indian income exceeds the basic exemption limit, and should file to claim refunds of TDS deducted on property sales, NRO interest or rent. NRIs file ITR-2, or ITR-3 with business income, and cannot claim the Section 87A rebate."),
    ("What is included in your ITR filing packages?",
     "Every package includes a free document review, old vs new regime comparison, AIS and Form 26AS reconciliation, preparation of the right ITR form, CA review, filing, e-verification help and refund tracking. Specialised packages add schedules for capital gains, F&O, crypto, foreign assets or NRI status."),
    ("What happens if I don't file my ITR at all?",
     "You pay a late fee and interest if you file late, cannot carry forward most losses, may receive a notice for non-filing based on AIS data, and lose refunds you are owed. Loan and visa applications usually ask for ITRs of the last two or three years."),
]

MAIN = r"""
<!--HERO-->
      <!-- ================= TICKER ================= -->
      <section class="ticker" aria-label="Latest income tax updates" tabindex="0">
        <ul class="ticker__track">
          <li><time datetime="2026-12-31">31 Dec 2026</time>Last date for belated ITR for FY 2025-26</li>
          <li><time datetime="2026-04-01">1 Apr 2026</time>Income-tax Act, 2025 in force; returns for FY 2025-26 still under the 1961 Act</li>
          <li><time datetime="2026-02-01">Budget 2026</time>ITR-3/4 non-audit due date moved to 31 August; revised returns till 31 March</li>
          <li><time datetime="2026-03-30">30 Mar 2026</time>ITR forms for AY 2026-27 notified; ITR-1 now covers two house properties</li>
          <li><time datetime="2025-04-01">FY 2025-26</time>Zero tax up to ₹12 lakh under the new regime</li>
          <li><time datetime="2026-04-01">1 Apr 2026</time>STT on futures up to 0.05%, on options to 0.15%</li>
          <li aria-hidden="true"><time>31 Dec 2026</time>Last date for belated ITR for FY 2025-26</li>
          <li aria-hidden="true"><time>1 Apr 2026</time>Income-tax Act, 2025 in force; returns for FY 2025-26 still under the 1961 Act</li>
          <li aria-hidden="true"><time>Budget 2026</time>ITR-3/4 non-audit due date moved to 31 August; revised returns till 31 March</li>
          <li aria-hidden="true"><time>30 Mar 2026</time>ITR forms for AY 2026-27 notified; ITR-1 now covers two house properties</li>
          <li aria-hidden="true"><time>FY 2025-26</time>Zero tax up to ₹12 lakh under the new regime</li>
          <li aria-hidden="true"><time>1 Apr 2026</time>STT on futures up to 0.05%, on options to 0.15%</li>
        </ul>
      </section>

<!--SELF-FILING-->
<!--EXPERT-->
<!--PACKAGES-->
<!--SELF-VS-CA-->
      <!-- ================= AT A GLANCE ================= -->
      <section class="section" aria-labelledby="h-glance">
        <div class="wrap">
          <div class="section-head reveal">
            <h2 id="h-glance">Your ITR year. At a glance.</h2>
            <p>Deadlines for FY 2025-26 (AY 2026-27), checked against the Finance Act, 2026.</p>
          </div>
          <div class="bento">
            <div class="tile tile--wide tile--navy reveal">
              <h3>ITR deadlines, FY 2025-26</h3>
              <p>Dates in 2026 unless stated. Audit reports are due one month before the audit-case ITR date.</p>
              <ul class="rhythm" aria-label="ITR deadlines">
                <li class="is-key"><b>31 Jul</b>ITR-1 / ITR-2</li>
                <li class="is-key"><b>31 Aug</b>ITR-3 / ITR-4</li>
                <li><b>31 Oct</b>Audit cases</li>
                <li><b>31 Dec</b>Belated return</li>
                <li><b>31 Mar</b>Revised (2027)</li>
              </ul>
            </div>
            <div class="tile tile--brand reveal">
              <span class="tile__stat">₹12 L</span>
              <h3>Tax-free income</h3>
              <p>Under the new regime with the Section 87A rebate (₹12.75 lakh for salaried).</p>
            </div>
            <div class="tile reveal">
              <span class="tile__stat">48 mo</span>
              <h3>To file ITR-U</h3>
              <p>Updated-return window, doubled by the Finance Act, 2025.</p>
            </div>
            <div class="tile tile--leaf reveal">
              <span class="tile__stat">30 days</span>
              <h3>To e-verify</h3>
              <p>Or the return is treated as filed on the verification date.</p>
            </div>
            <div class="tile reveal">
              <span class="tile__stat">₹5,000</span>
              <h3>Late fee</h3>
              <p>₹1,000 if total income is up to ₹5 lakh.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= TOOLS ================= -->
      <section id="tools" class="section section--glow" aria-labelledby="h-tools">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">Free tools</span>
            <h2 id="h-tools">Find your regime. Find your form. Know your fee.</h2>
            <p>Estimates for FY 2025-26 (the regime calculator also works for FY 2026-27, which has the same slabs). Special-rate income such as capital gains is excluded.</p>
          </div>
          <div class="tools">
            <section class="tool reveal" id="regime-calc" aria-labelledby="h-regime">
              <div class="tool__head">
                <span class="tool__icon" aria-hidden="true">⚖</span>
                <div>
                  <h3 id="h-regime">Old vs new regime calculator</h3>
                  <p>Resident individuals. Includes rebate, surcharge, marginal relief and 4% cess.</p>
                </div>
              </div>
              <fieldset class="seg">
                <legend>Income type</legend>
                <label><input type="radio" name="salaried" value="yes" checked />Salaried / pension</label>
                <label><input type="radio" name="salaried" value="no" />Other income</label>
              </fieldset>
              <div class="field-row">
                <div class="field">
                  <label for="rc-income">Gross annual income (₹)</label>
                  <input id="rc-income" name="income" type="number" inputmode="numeric" min="0" step="10000" value="1500000" />
                </div>
                <div class="field">
                  <label for="rc-age">Age</label>
                  <select id="rc-age" name="age">
                    <option value="0">Below 60</option>
                    <option value="1">60 to 79</option>
                    <option value="2">80 or above</option>
                  </select>
                </div>
              </div>
              <div class="field-row">
                <div class="field">
                  <label for="rc-80c">80C investments (₹, old regime)</label>
                  <input id="rc-80c" name="d80c" type="number" inputmode="numeric" min="0" step="5000" value="150000" />
                </div>
                <div class="field">
                  <label for="rc-80d">80D health insurance (₹)</label>
                  <input id="rc-80d" name="d80d" type="number" inputmode="numeric" min="0" step="1000" value="25000" />
                </div>
              </div>
              <div class="field-row">
                <div class="field">
                  <label for="rc-hl">Home-loan interest (₹)</label>
                  <input id="rc-hl" name="hl" type="number" inputmode="numeric" min="0" step="10000" value="0" />
                </div>
                <div class="field">
                  <label for="rc-other">HRA and other deductions (₹)</label>
                  <input id="rc-other" name="other" type="number" inputmode="numeric" min="0" step="5000" value="0" />
                </div>
              </div>
              <div class="result" aria-live="polite">
                <dl class="result__rows" id="regime-out"></dl>
                <p class="result__note" id="regime-note"></p>
              </div>
            </section>

            <section class="tool reveal" id="form-finder" aria-labelledby="h-form">
              <div class="tool__head">
                <span class="tool__icon" aria-hidden="true">📄</span>
                <div>
                  <h3 id="h-form">Which ITR form do I need?</h3>
                  <p>For AY 2026-27 forms, notified 30 March 2026.</p>
                </div>
              </div>
              <div class="field">
                <label for="ff-who">Who is filing?</label>
                <select id="ff-who" name="who">
                  <option value="ind">Individual or HUF</option>
                  <option value="firm">Partnership firm</option>
                  <option value="llp">LLP</option>
                  <option value="co">Company</option>
                  <option value="trust">Trust, society or political party</option>
                </select>
              </div>
              <fieldset class="checks" id="ff-sources">
                <legend>Tick everything that applies</legend>
                <label><input type="checkbox" name="biz" />Business or professional income with regular books</label>
                <label><input type="checkbox" name="presumptive" />Presumptive income (44AD / 44ADA / 44AE)</label>
                <label><input type="checkbox" name="cg" />Capital gains (other than LTCG on shares/equity MF up to ₹1.25 lakh)</label>
                <label><input type="checkbox" name="over50" />Total income above ₹50 lakh</label>
                <label><input type="checkbox" name="foreign" />Foreign assets or foreign income</label>
                <label><input type="checkbox" name="director" />Director in a company or unlisted shares held</label>
                <label><input type="checkbox" name="hp" />More than two house properties</label>
                <label><input type="checkbox" name="nr" />Non-resident or not ordinarily resident</label>
              </fieldset>
              <div class="result" aria-live="polite">
                <dl class="result__rows" id="form-out"></dl>
                <p class="result__note" id="form-note"></p>
              </div>
            </section>

            <section class="tool reveal" id="late-calc" aria-labelledby="h-late">
              <div class="tool__head">
                <span class="tool__icon" aria-hidden="true">⏰</span>
                <div>
                  <h3 id="h-late">Late ITR: fee and interest</h3>
                  <p>Section 234F fee and Section 234A interest for FY 2025-26.</p>
                </div>
              </div>
              <div class="field">
                <label for="lc-type">Your return</label>
                <select id="lc-type" name="type">
                  <option value="2026-07-31">ITR-1 / ITR-2 (due 31 July)</option>
                  <option value="2026-08-31">ITR-3 / ITR-4, no audit (due 31 August)</option>
                  <option value="2026-10-31">Tax-audit case (due 31 October)</option>
                </select>
              </div>
              <div class="field-row">
                <div class="field">
                  <label for="lc-date">Filing date</label>
                  <input id="lc-date" name="date" type="date" value="2026-10-15" min="2026-04-01" max="2027-03-31" />
                </div>
                <div class="field">
                  <label for="lc-tax">Unpaid tax (₹)</label>
                  <input id="lc-tax" name="tax" type="number" inputmode="numeric" min="0" step="1000" value="20000" />
                </div>
              </div>
              <fieldset class="seg">
                <legend>Total income</legend>
                <label><input type="radio" name="small" value="no" checked />Above ₹5 lakh</label>
                <label><input type="radio" name="small" value="yes" />Up to ₹5 lakh</label>
              </fieldset>
              <div class="result" aria-live="polite">
                <dl class="result__rows" id="late-out"></dl>
                <p class="result__note" id="late-note"></p>
              </div>
            </section>
          </div>
        </div>
      </section>

      <!-- ================= GUIDE ================= -->
      <div class="section">
        <article class="wrap wrap--read">
          <section id="what-is-itr" class="chapter prose reveal" aria-labelledby="h-what">
            <span class="kicker">Overview</span>
            <h2 id="h-what">What is income tax return filing?</h2>
            <p class="answer">
              An <strong>income tax return (ITR)</strong> is the form in which you report your income, deductions and taxes paid to the Income Tax
              Department for a financial year. For <strong>FY 2025-26 (AY 2026-27)</strong>, most individuals file by <strong>31 July 2026</strong> and
              non-audit businesses by <strong>31 August 2026</strong>. Filing is how you claim refunds, carry forward losses and prove your income.
            </p>
            <p>
              Returns for FY 2025-26 are filed under <strong>Section 139 of the Income-tax Act, 1961</strong>. From tax year 2026-27 onwards, the
              <strong>Income-tax Act, 2025</strong> applies and return filing moves to <strong>Section 263</strong>. Your ITR is an important document
              for bank loans, visas, government tenders and credit cards.
            </p>
            <div class="example">
              <span class="example__label">Example · Salaried</span>
              <p>
                <strong>Neha, an IT employee in Bengaluru,</strong> earns ₹12.5 lakh a year. Under the new regime, her taxable income after the ₹75,000
                standard deduction is ₹11.75 lakh, so the Section 87A rebate brings her tax to <strong>zero</strong>. She still files ITR-1 to get back
                ₹38,000 of TDS her employer deducted before she submitted her regime choice.
              </p>
            </div>
          </section>

          <section id="who-must-file" class="chapter prose reveal" aria-labelledby="h-who">
            <span class="kicker">Who must file</span>
            <h2 id="h-who">Who must file an income tax return?</h2>
            <p>You must file if your gross total income (before deductions) exceeds the basic exemption limit:</p>
            <div class="table" tabindex="0">
              <table>
                <caption>Basic exemption limits, FY 2025-26</caption>
                <thead><tr><th scope="col">Taxpayer</th><th scope="col">New regime</th><th scope="col">Old regime</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Individual below 60</th><td>₹4 lakh</td><td>₹2.5 lakh</td></tr>
                  <tr><th scope="row">Senior citizen (60–79)</th><td>₹4 lakh</td><td>₹3 lakh</td></tr>
                  <tr><th scope="row">Super senior (80+)</th><td>₹4 lakh</td><td>₹5 lakh</td></tr>
                  <tr><th scope="row">Firms, LLPs, companies</th><td colspan="2">Must file every year, even with a loss or nil income</td></tr>
                </tbody>
              </table>
            </div>
            <h3>You must also file, whatever your income, if during the year you:</h3>
            <ul>
              <li>Deposited more than <strong>₹1 crore</strong> in current accounts or <strong>₹50 lakh</strong> in savings accounts</li>
              <li>Spent more than <strong>₹2 lakh</strong> on foreign travel or <strong>₹1 lakh</strong> on electricity bills</li>
              <li>Had TDS or TCS of <strong>₹25,000</strong> or more (₹50,000 for senior citizens)</li>
              <li>Had business turnover above <strong>₹60 lakh</strong> or professional receipts above <strong>₹10 lakh</strong></li>
              <li>Held foreign assets, signing authority in a foreign account, or foreign income (residents)</li>
            </ul>
            <div class="note">
              <span class="note__title">Senior citizens aged 75+</span>
              <p>Those with only pension and interest from the same specified bank can skip filing by submitting a declaration to the bank (Section 194P), which then deducts their tax.</p>
            </div>
          </section>

          <section id="itr-forms" class="chapter prose reveal" aria-labelledby="h-forms">
            <span class="kicker">ITR forms</span>
            <h2 id="h-forms">Which ITR form applies to you?</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>ITR forms for AY 2026-27</caption>
                <thead><tr><th scope="col">Form</th><th scope="col">Who files it</th><th scope="col">Key limits</th></tr></thead>
                <tbody>
                  <tr><th scope="row">ITR-1 Sahaj</th><td>Resident individuals with salary, pension, up to two house properties, interest</td><td>Income up to ₹50 lakh; LTCG (112A) up to ₹1.25 lakh</td></tr>
                  <tr><th scope="row">ITR-2</th><td>Individuals/HUFs with capital gains, foreign assets, more property, directorship</td><td>No business income</td></tr>
                  <tr><th scope="row">ITR-3</th><td>Individuals/HUFs with business or professional income, including partners</td><td>Regular books of account</td></tr>
                  <tr><th scope="row">ITR-4 Sugam</th><td>Resident individuals, HUFs and firms (not LLPs) on presumptive income</td><td>Income up to ₹50 lakh</td></tr>
                  <tr><th scope="row">ITR-5</th><td>Partnership firms, LLPs, AOPs, BOIs</td><td>—</td></tr>
                  <tr><th scope="row">ITR-6</th><td>Companies (other than those claiming Section 11 exemption)</td><td>—</td></tr>
                  <tr><th scope="row">ITR-7</th><td>Trusts, political parties, institutions filing under Sections 139(4A)–(4D)</td><td>—</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="due-dates" class="chapter prose reveal" aria-labelledby="h-due">
            <span class="kicker">Due dates</span>
            <h2 id="h-due">ITR due dates for FY 2025-26 (AY 2026-27)</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Due dates under Section 139 (as amended by the Finance Act, 2026)</caption>
                <thead><tr><th scope="col">Return</th><th scope="col">Due date</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Individuals filing ITR-1 or ITR-2</th><td>31 July 2026</td></tr>
                  <tr><th scope="row">Non-audit business or profession (ITR-3, ITR-4)</th><td>31 August 2026</td></tr>
                  <tr><th scope="row">Tax-audit report (Form 3CA/3CB-3CD)</th><td>30 September 2026</td></tr>
                  <tr><th scope="row">Tax-audit cases and companies</th><td>31 October 2026</td></tr>
                  <tr><th scope="row">Transfer-pricing cases</th><td>30 November 2026</td></tr>
                  <tr><th scope="row">Belated return</th><td>31 December 2026</td></tr>
                  <tr><th scope="row">Revised return</th><td>31 March 2027 (fee after 31 December)</td></tr>
                  <tr><th scope="row">Updated return (ITR-U)</th><td>Within 48 months from the end of the assessment year</td></tr>
                </tbody>
              </table>
            </div>
            <p class="muted" style="font-size: var(--fs-14)">The CBDT can extend dates by notification. We confirm the live date before filing.</p>
          </section>

          <section id="tax-regimes" class="chapter prose reveal" aria-labelledby="h-slabs">
            <span class="kicker">Tax slabs</span>
            <h2 id="h-slabs">Income tax slabs: new vs old regime</h2>
            <p>The same slabs apply for FY 2025-26 and FY 2026-27; Budget 2026 made no change.</p>
            <div class="table" tabindex="0">
              <table>
                <caption>New tax regime (default) — Section 115BAC, now Section 202</caption>
                <thead><tr><th scope="col">Taxable income</th><th scope="col">Rate</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Up to ₹4 lakh</th><td>Nil</td></tr>
                  <tr><th scope="row">₹4–8 lakh</th><td>5%</td></tr>
                  <tr><th scope="row">₹8–12 lakh</th><td>10%</td></tr>
                  <tr><th scope="row">₹12–16 lakh</th><td>15%</td></tr>
                  <tr><th scope="row">₹16–20 lakh</th><td>20%</td></tr>
                  <tr><th scope="row">₹20–24 lakh</th><td>25%</td></tr>
                  <tr><th scope="row">Above ₹24 lakh</th><td>30%</td></tr>
                </tbody>
              </table>
            </div>
            <div class="table" tabindex="0">
              <table>
                <caption>Old tax regime — individuals below 60</caption>
                <thead><tr><th scope="col">Taxable income</th><th scope="col">Rate</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Up to ₹2.5 lakh</th><td>Nil (₹3 lakh at 60–79; ₹5 lakh at 80+)</td></tr>
                  <tr><th scope="row">₹2.5–5 lakh</th><td>5%</td></tr>
                  <tr><th scope="row">₹5–10 lakh</th><td>20%</td></tr>
                  <tr><th scope="row">Above ₹10 lakh</th><td>30%</td></tr>
                </tbody>
              </table>
            </div>
            <ul>
              <li><strong>Rebate (87A, now Section 156):</strong> up to ₹60,000 for income up to ₹12 lakh in the new regime; up to ₹12,500 for income up to ₹5 lakh in the old regime.</li>
              <li><strong>Standard deduction for salary and pension:</strong> ₹75,000 (new) or ₹50,000 (old).</li>
              <li><strong>Surcharge:</strong> 10% above ₹50 lakh, 15% above ₹1 crore, 25% above ₹2 crore; the old regime adds 37% above ₹5 crore. Plus 4% health and education cess.</li>
              <li><strong>Deductions</strong> such as 80C, 80D, HRA and home-loan interest are available only in the old regime; employer NPS contributions are allowed in both.</li>
            </ul>
          </section>

          <section id="whats-new" class="chapter prose" aria-labelledby="h-new">
            <span class="kicker reveal">What’s new</span>
            <h2 id="h-new" class="reveal">Latest income tax changes, 2025–26</h2>
            <ol class="timeline">
              <li class="timeline__item">
                <time datetime="2026-04-01">1 April 2026</time>
                <h3>Income-tax Act, 2025 in force <span class="tag tag--leaf">New law</span></h3>
                <p>Replaces the 1961 Act from tax year 2026-27, with a single "tax year" and renumbered sections. Returns for FY 2025-26 are still filed under the old Act.</p>
              </li>
              <li class="timeline__item">
                <time datetime="2026-03-30">30 March 2026</time>
                <h3>ITR forms for AY 2026-27 notified</h3>
                <p>ITR-1 and ITR-4 now cover income from up to two house properties, so more people can use the simple forms.</p>
              </li>
              <li class="timeline__item">
                <time datetime="2026-02-01">Budget 2026 (Finance Act, 2026)</time>
                <h3>More time for business returns and revisions <span class="tag">Changed</span></h3>
                <p>Non-audit ITR-3 and ITR-4 due date moved from 31 July to 31 August, and revised returns allowed until 31 March. Tax slabs unchanged.</p>
              </li>
              <li class="timeline__item">
                <time datetime="2025-04-01">FY 2025-26 (Finance Act, 2025)</time>
                <h3>Zero tax up to ₹12 lakh; ITR-U window doubled</h3>
                <p>New slabs with a ₹60,000 rebate, and the updated-return window extended from 24 to 48 months.</p>
              </li>
              <li class="timeline__item">
                <time datetime="2024-07-23">23 July 2024</time>
                <h3>Capital gains rates changed</h3>
                <p>Listed equity: short-term gains at 20%, long-term gains at 12.5% above ₹1.25 lakh. Indexation removed for most assets, with a choice for land and buildings bought before this date.</p>
              </li>
            </ol>
          </section>

          <section id="documents" class="chapter prose reveal" aria-labelledby="h-docs">
            <span class="kicker">Checklist</span>
            <h2 id="h-docs">Documents required to file your ITR</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>What to keep ready</caption>
                <thead><tr><th scope="col">For</th><th scope="col">Documents</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Everyone</th><td>PAN, Aadhaar (linked to PAN), bank account details, AIS, TIS and Form 26AS</td></tr>
                  <tr><th scope="row">Salaried</th><td>Form 16, salary slips, rent receipts for HRA (old regime)</td></tr>
                  <tr><th scope="row">Investors</th><td>Broker and mutual-fund capital-gain statements, dividend and interest certificates</td></tr>
                  <tr><th scope="row">Property owners</th><td>Rent received, municipal tax paid, home-loan interest certificate</td></tr>
                  <tr><th scope="row">Business and professionals</th><td>Books of account or P&amp;L and balance sheet, GST returns, TDS certificates</td></tr>
                  <tr><th scope="row">Old-regime deductions</th><td>80C, 80D, 80G, 80E proofs; NPS statements</td></tr>
                </tbody>
              </table>
            </div>
          </section>
<!--SPECIAL-CHAPTERS-->
        </article>
      </div>

      <!-- ================= PROCESS ================= -->
      <section id="process" class="section section--glow" aria-labelledby="h-process">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">Process</span>
            <h2 id="h-process">Your ITR, filed in five steps.</h2>
            <p>Most individual returns are ready within two working days of receiving your documents.</p>
          </div>
          <ol class="stepper">
            <li style="--i: 0"><span class="when">Day 0</span><h3>Free call</h3><p>We understand your income sources and confirm the plan and fee.</p></li>
            <li style="--i: 1"><span class="when">Day 0–1</span><h3>Share documents</h3><p>Upload on WhatsApp or our secure portal. We pull AIS and Form 26AS with your consent.</p></li>
            <li style="--i: 2"><span class="when">Day 1–2</span><h3>Computation</h3><p>Regime comparison, deductions and tax computed; a CA reviews it.</p></li>
            <li style="--i: 3"><span class="when">Day 2</span><h3>Your approval</h3><p>You approve the draft and pay any balance tax with our help.</p></li>
            <li style="--i: 4"><span class="when">Same day</span><h3>Filed &amp; verified</h3><p>We file, help you e-verify and track your refund until it arrives.</p></li>
          </ol>
        </div>
      </section>

      <!-- ================= GUIDE CONTINUED ================= -->
      <div class="section">
        <article class="wrap wrap--read">
          <section id="penalties" class="chapter prose reveal" aria-labelledby="h-pen">
            <span class="kicker">Risk</span>
            <h2 id="h-pen">Late fee, interest and penalties</h2>
            <ul>
              <li><strong>Late fee (Section 234F):</strong> ₹5,000 for returns filed after the due date; ₹1,000 if total income is up to ₹5 lakh.</li>
              <li><strong>Interest:</strong> 1% a month for late filing (234A), short advance tax (234B) and deferred instalments (234C).</li>
              <li><strong>Losses lost:</strong> business and capital losses cannot be carried forward in a belated return.</li>
              <li><strong>Under-reporting:</strong> penalty of 50% of the tax, or 200% for misreporting (Section 270A).</li>
            </ul>
            <div class="example">
              <span class="example__label">Worked example</span>
              <p>
                A Jaipur consultant with ₹9 lakh income and ₹20,000 tax unpaid files on 15 November instead of 31 August. Late fee ₹5,000, plus interest
                under 234A of about ₹600 (1% for three months on ₹20,000), plus any 234B/234C interest for missed advance tax. Filing on time would have
                cost nothing extra.
              </p>
            </div>
          </section>

          <section id="refunds" class="chapter prose reveal" aria-labelledby="h-refund">
            <span class="kicker">Refunds</span>
            <h2 id="h-refund">Getting your refund faster</h2>
            <ul>
              <li><strong>E-verify immediately</strong>: processing starts only after verification.</li>
              <li><strong>Pre-validate your bank account</strong> on the e-filing portal; refunds go only to a pre-validated account linked to your PAN.</li>
              <li><strong>Match AIS and Form 26AS</strong>: mismatches are the most common reason for delays and notices.</li>
              <li><strong>Respond to Section 143(1)(a) communications</strong> within 30 days if the department proposes adjustments.</li>
              <li>Delayed refunds earn <strong>interest at 0.5% a month</strong> under Section 244A.</li>
            </ul>
          </section>

          <section id="new-act" class="chapter prose reveal" aria-labelledby="h-act">
            <span class="kicker">Old Act vs new Act</span>
            <h2 id="h-act">Income-tax Act, 1961 vs 2025: sections you will see</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Key provisions for ITR filers</caption>
                <thead><tr><th scope="col">Topic</th><th scope="col">1961 Act</th><th scope="col">2025 Act</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Filing of return</th><td>Section 139</td><td>Section 263</td></tr>
                  <tr><th scope="row">New tax regime</th><td>Section 115BAC</td><td>Section 202</td></tr>
                  <tr><th scope="row">Rebate</th><td>Section 87A</td><td>Section 156</td></tr>
                  <tr><th scope="row">80C deduction</th><td>Section 80C</td><td>Section 123</td></tr>
                  <tr><th scope="row">Health insurance deduction</th><td>Section 80D</td><td>Section 126</td></tr>
                  <tr><th scope="row">Presumptive income</th><td>Sections 44AD, 44ADA, 44AE</td><td>Section 58</td></tr>
                  <tr><th scope="row">Tax audit</th><td>Section 44AB</td><td>Section 63</td></tr>
                  <tr><th scope="row">TDS</th><td>Sections 192–194T</td><td>Section 393</td></tr>
                  <tr><th scope="row">Year of income</th><td>Previous year &amp; assessment year</td><td>Tax year</td></tr>
                </tbody>
              </table>
            </div>
            <p>Income of FY 2025-26 is filed under the 1961 Act. Income from 1 April 2026 (tax year 2026-27) is filed in 2027 under the 2025 Act.</p>
          </section>

<!--MORE-CHAPTERS-->
        </article>
      </div>

<!--REVIEWS-->
      <!-- ================= RELATED ================= -->
      <section id="related" class="section" aria-labelledby="h-related">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">Related services</span>
            <h2 id="h-related">More ways we can help.</h2>
          </div>
          <div class="grid grid--3">
            <a class="card reveal" href="https://bharatefiling.com/product/itr-for-salaried-guide/"><h3>ITR for Salaried</h3><p>Form 16, HRA and regime choice handled.</p></a>
            <a class="card reveal" href="https://bharatefiling.com/product/itr-for-sole-proprietorship/"><h3>ITR for Proprietors</h3><p>Business income, presumptive or regular books.</p></a>
            <a class="card reveal" href="https://bharatefiling.com/services/itr-for-llp/"><h3>ITR for LLP</h3><p>ITR-5 with audit and partner coordination.</p></a>
            <a class="card reveal" href="https://bharatefiling.com/services/tds-return-filing/"><h3>TDS Return Filing</h3><p>24Q, 26Q and 27Q filed on time.</p></a>
            <a class="card reveal" href="https://bharatefiling.com/gst-return-filing/"><h3>GST Return Filing</h3><p>Keep GST and ITR turnover in sync.</p></a>
            <a class="card reveal" href="https://bharatefiling.com/gst-registration/"><h3>GST Registration</h3><p>Single or multi-state GSTIN.</p></a>
          </div>
        </div>
      </section>

      <!-- ================= REVIEWER & SOURCES ================= -->
      <section class="wrap wrap--read" aria-label="About this page">
        <div class="reviewer reveal">
          <div class="reviewer__avatar" aria-hidden="true">CA</div>
          <div>
            <p><strong>Reviewed by REPLACE_CA_NAME, Chartered Accountant</strong> · ICAI M. No. REPLACE</p>
            <p class="muted">REPLACE: one line on direct-tax experience.</p>
            <div class="meta">
              <span>Published <time datetime="2026-10-04">4 Oct 2026</time></span>
              <span>Last fact-checked <time datetime="2026-10-04">4 Oct 2026</time></span>
              <a href="https://bharatefiling.com/editorial-policy/">Editorial policy</a>
            </div>
          </div>
        </div>
        <h2 class="mt-16" style="font-size: var(--fs-19)">Sources and official references</h2>
        <ul class="sources">
          <li><a href="https://www.incometax.gov.in/" rel="noopener" target="_blank">Income Tax e-filing portal</a></li>
          <li><a href="https://www.incometaxindia.gov.in/" rel="noopener" target="_blank">Income Tax Department — Acts, rules and ITR forms</a></li>
          <li><a href="https://www.indiabudget.gov.in/" rel="noopener" target="_blank">Union Budget 2026-27 — Finance Act, 2026</a></li>
          <li><a href="https://www.cbdt.gov.in/" rel="noopener" target="_blank">CBDT — notifications and circulars</a></li>
        </ul>
      </section>

<!--FAQ-->
      <section class="wrap" aria-labelledby="h-cta" style="padding-bottom: var(--section)">
        <div class="cta reveal">
          <h2 id="h-cta">File your ITR the right way.</h2>
          <p>Talk to a tax expert in Hindi or English. Free first review of your documents.</p>
          <div class="btn-row">
            <a class="btn btn--brand" href="#get-started" data-modal-open data-track="cta_click" data-location="cta-band">File my ITR</a>
            <a class="btn btn--outline-light" href="tel:+910000000000" data-track="click_call" data-location="cta-band"><svg width="16" height="16" aria-hidden="true"><use href="#i-phone" /></svg>&nbsp;Call&nbsp;us</a>
          </div>
        </div>
      </section>
"""

PAGE_JS = r"""
      (function () {
        "use strict";
        var used = {};
        function trackUse(tool) {
          if (used[tool]) return;
          used[tool] = true;
          (window.dataLayer = window.dataLayer || []).push({ event: "calculator_use", service: "income-tax-return-filing", tool: tool });
        }
        function rupees(n) { return "₹" + Math.round(n).toLocaleString("en-IN"); }
        function row(label, value, total) { return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>"; }
        function num(el) { var v = Number(el.value); return Number.isFinite(v) && v > 0 ? v : 0; }

        /* ---- Regime calculator (FY 2025-26 = FY 2026-27 rates) ---- */
        var NEW = [[400000, 0], [800000, 0.05], [1200000, 0.1], [1600000, 0.15], [2000000, 0.2], [2400000, 0.25], [Infinity, 0.3]];
        var OLD = [
          [[250000, 0], [500000, 0.05], [1000000, 0.2], [Infinity, 0.3]],
          [[300000, 0], [500000, 0.05], [1000000, 0.2], [Infinity, 0.3]],
          [[500000, 0], [1000000, 0.2], [Infinity, 0.3]]
        ];
        function slabTax(income, slabs) {
          var tax = 0, prev = 0;
          for (var i = 0; i < slabs.length; i++) {
            if (income > prev) tax += (Math.min(income, slabs[i][0]) - prev) * slabs[i][1];
            prev = slabs[i][0];
          }
          return tax;
        }
        function withSurcharge(income, slabs, cap) {
          var base = slabTax(income, slabs);
          var bands = [[5e6, 0.1], [1e7, 0.15], [2e7, 0.25], [5e7, 0.37]];
          var rate = 0, threshold = 0, prevRate = 0;
          for (var i = 0; i < bands.length; i++) {
            if (income > bands[i][0]) { prevRate = rate; rate = Math.min(bands[i][1], cap); threshold = bands[i][0]; }
          }
          if (!rate) return base;
          var full = base * (1 + rate);
          var atThreshold = slabTax(threshold, slabs) * (1 + prevRate);
          return Math.min(full, atThreshold + (income - threshold)); // marginal relief
        }
        function newRegime(taxable) {
          var tax = slabTax(taxable, NEW);
          if (taxable <= 1200000) return 0; // Section 87A rebate (up to ₹60,000)
          tax = Math.min(tax, taxable - 1200000); // marginal relief on rebate
          if (taxable > 5e6) tax = withSurcharge(taxable, NEW, 0.25);
          return tax * 1.04;
        }
        function oldRegime(taxable, age) {
          var slabs = OLD[age];
          var tax = taxable > 5e6 ? withSurcharge(taxable, slabs, 0.37) : slabTax(taxable, slabs);
          if (taxable <= 500000) tax = Math.max(0, tax - 12500);
          return tax * 1.04;
        }
        var rc = document.getElementById("regime-calc");
        if (rc) {
          var q = function (n) { return rc.querySelector("[name='" + n + "']"); };
          var render = function () {
            var salaried = rc.querySelector("[name='salaried']:checked").value === "yes";
            var gross = num(q("income"));
            var age = Number(q("age").value);
            var newTaxable = Math.max(0, gross - (salaried ? 75000 : 0));
            var ded = Math.min(num(q("d80c")), 150000) + Math.min(num(q("d80d")), 100000) + Math.min(num(q("hl")), 200000) + num(q("other"));
            var oldTaxable = Math.max(0, gross - (salaried ? 50000 : 0) - ded);
            var tNew = newRegime(newTaxable), tOld = oldRegime(oldTaxable, age);
            var diff = Math.abs(tNew - tOld);
            var best = Math.round(diff) === 0 ? "Both regimes cost the same" : (tNew < tOld ? "New regime saves" : "Old regime saves");
            document.getElementById("regime-out").innerHTML =
              row("New regime tax", rupees(tNew)) + row("Old regime tax", rupees(tOld)) + row(best, Math.round(diff) === 0 ? "—" : rupees(diff), true);
            document.getElementById("regime-note").textContent =
              "Taxable income: new " + rupees(newTaxable) + ", old " + rupees(oldTaxable) + ". Caps applied: 80C ₹1.5 lakh, 80D ₹1 lakh, home-loan interest ₹2 lakh. Estimate only.";
          };
          rc.addEventListener("input", function () { trackUse("regime_calculator"); render(); });
          rc.addEventListener("change", render);
          render();
        }

        /* ---- ITR form finder ---- */
        var ff = document.getElementById("form-finder");
        if (ff) {
          var pick = function () {
            var who = ff.querySelector("[name='who']").value;
            var has = function (n) { return ff.querySelector("[name='" + n + "']").checked; };
            var form, why;
            if (who === "co") { form = "ITR-6"; why = "Companies file ITR-6 (ITR-7 if claiming Section 11 exemption)."; }
            else if (who === "trust") { form = "ITR-7"; why = "Trusts, political parties and institutions file ITR-7."; }
            else if (who === "llp") { form = "ITR-5"; why = "LLPs always file ITR-5; they cannot use ITR-4."; }
            else if (who === "firm") {
              form = has("presumptive") && !has("biz") && !has("over50") ? "ITR-4" : "ITR-5";
              why = form === "ITR-4" ? "A resident firm on presumptive income up to ₹50 lakh can use ITR-4." : "Firms with regular books or income above ₹50 lakh file ITR-5.";
            } else {
              var complex = has("cg") || has("over50") || has("foreign") || has("director") || has("hp") || has("nr");
              if (has("biz")) { form = "ITR-3"; why = "Business or professional income with regular books needs ITR-3."; }
              else if (has("presumptive")) {
                form = complex ? "ITR-3" : "ITR-4";
                why = form === "ITR-4" ? "Presumptive income up to ₹50 lakh for a resident: ITR-4 (Sugam)." : "Presumptive income plus capital gains, foreign assets, directorship or high income needs ITR-3.";
              } else {
                form = complex ? "ITR-2" : "ITR-1";
                why = form === "ITR-1" ? "Salary, pension, up to two house properties and interest, income up to ₹50 lakh: ITR-1 (Sahaj)." : "Capital gains, foreign assets, directorship, high income or more property without business income: ITR-2.";
              }
            }
            document.getElementById("form-out").innerHTML = row("Your form", form, true);
            document.getElementById("form-note").textContent = why + " We confirm before filing.";
          };
          ff.addEventListener("change", function () { trackUse("itr_form_finder"); pick(); });
          pick();
        }

        /* ---- Late fee (234F) and interest (234A) ---- */
        var lc = document.getElementById("late-calc");
        if (lc) {
          var late = function () {
            var due = new Date(lc.querySelector("[name='type']").value + "T00:00:00");
            var filed = new Date((lc.querySelector("[name='date']").value || "2026-07-31") + "T00:00:00");
            var tax = num(lc.querySelector("[name='tax']"));
            var small = lc.querySelector("[name='small']:checked").value === "yes";
            var months = 0;
            if (filed > due) {
              months = (filed.getFullYear() - due.getFullYear()) * 12 + (filed.getMonth() - due.getMonth());
              if (filed.getDate() > due.getDate()) months += 1; // part of a month counts as a full month (due dates are month-ends)
            }
            var fee = filed > due ? (small ? 1000 : 5000) : 0;
            var interest = Math.floor(tax / 100) * 100 * 0.01 * months;
            document.getElementById("late-out").innerHTML =
              row("Months late (234A)", String(months)) + row("Late fee (234F)", rupees(fee)) + row("Interest (234A)", rupees(interest)) + row("Extra cost of filing late", rupees(fee + interest), true);
            var belatedEnd = new Date("2026-12-31T00:00:00");
            document.getElementById("late-note").textContent = filed > belatedEnd
              ? "After 31 December 2026 a belated return is no longer possible; you would need an updated return (ITR-U) with additional tax of 25% or more."
              : (filed > due ? "Filed as a belated return. Losses (except house property) cannot be carried forward. 234B/234C interest for missed advance tax is extra." : "On time: no late fee or 234A interest.");
          };
          lc.addEventListener("input", function () { trackUse("late_fee_calculator"); late(); });
          lc.addEventListener("change", late);
          late();
        }
      })();
"""

# ---------------------------------------------------------------- Packages (built from PACKAGES so prices never drift)
PACKAGE_DETAILS = {
    "salary": ("ITR-1 / ITR-2", "Salaried employees and pensioners", [
        "Single or multiple Form 16 (job change)", "Up to two house properties, interest income", "HRA, 80C, 80D, home-loan claims",
        "Old vs new regime comparison", "TDS refund claim and tracking"]),
    "freelancer": ("ITR-4 / ITR-3", "Consultants, doctors, designers, developers, creators", [
        "Presumptive taxation under Section 44ADA", "Foreign client receipts and Form 26AS/AIS match", "Expense and depreciation claims (regular books)",
        "Advance tax computation for next year", "GST turnover reconciliation"]),
    "late-revised": ("Any ITR", "Missed the date, made a mistake or under-reported", [
        "Belated return until 31 December 2026", "Revised return until 31 March 2027", "Updated return (ITR-U) up to 48 months",
        "Late fee, interest and additional-tax computation", "Reply to defective-return notice (Section 139(9))"]),
    "capital-gains": ("ITR-2", "Shares, mutual funds, property, gold, unlisted shares", [
        "Broker and CAS statements imported and checked", "Pre- and post-23 July 2024 rates applied correctly", "₹1.25 lakh equity LTCG exemption and grandfathering",
        "Loss set-off and 8-year carry-forward", "Property sale: indexation choice, 54/54EC/54F exemptions"]),
    "fno": ("ITR-3", "Futures, options, intraday and commodity traders", [
        "Turnover worked out per the ICAI guidance note", "Trading P&L and balance sheet prepared", "Speculative and non-speculative losses carried forward",
        "Tax-audit applicability check (Section 44AB / 44AD)", "Brokerage, internet and advisory expenses claimed"]),
    "crypto": ("ITR-2 / ITR-3", "Crypto, NFTs and other virtual digital assets", [
        "Schedule VDA from exchange and wallet statements", "30% tax under Section 115BBH computed per transfer", "1% TDS (Section 194S) credit matched with AIS",
        "Indian and foreign exchanges, P2P and airdrops", "Up to 500 transactions included"]),
    "nri": ("ITR-2 / ITR-3", "NRIs with income or property in India", [
        "Residential-status check (182/120-day rules)", "Rent, interest, capital gains in India", "Refund of excess TDS on property sale or NRO interest",
        "DTAA benefit with TRC and Form 10F", "Indian bank account pre-validation for refunds"]),
    "foreign": ("ITR-2 / ITR-3", "Residents with US stocks, RSUs, ESPP or foreign salary", [
        "Schedule FA for the calendar year (all foreign assets)", "RSU / ESOP / ESPP perquisite and sale gains", "Form 67 for foreign tax credit under the DTAA",
        "Schedules FSI and TR, dividends and foreign interest", "Exchange rates applied per Rule 115 / Rule 128"]),
    "all-in-one": ("Any ITR", "Income above ₹50 lakh or many income sources", [
        "Everything in Salary, Capital Gains, F&O, Crypto and Foreign", "Surcharge and marginal-relief optimisation", "Schedule AL (assets and liabilities)",
        "Advance tax plan for the next year", "Dedicated senior CA, priority turnaround"]),
    "business": ("ITR-4 / ITR-3", "Shops, traders, manufacturers, service businesses", [
        "Presumptive income under Section 44AD", "P&L and balance sheet from your books or bank statements", "GST turnover and ITR turnover reconciled",
        "Old vs new regime (Form 10-IEA where needed)", "Loss carry-forward and advance tax"]),
    "firm": ("ITR-5 / ITR-4", "Partnership firms", [
        "Firm and partner income computation", "Partner remuneration and interest within Section 40(b)", "Presumptive or regular books",
        "Advance tax and TDS credit check", "Partners’ ITR coordination"]),
    "company": ("ITR-5 / ITR-6", "LLPs and private limited companies", [
        "Return from audited financials", "Section 115BAA / 115BAB rate and MAT check", "Depreciation and loss set-off",
        "Coordination with your auditor", "Filing acknowledgement and computation"]),
}
PACKAGE_GROUPS = [
    ("Salaried &amp; personal", ["salary", "freelancer", "late-revised"]),
    ("Investors &amp; traders", ["capital-gains", "fno", "crypto"]),
    ("NRI &amp; global income", ["nri", "foreign", "all-in-one"]),
    ("Businesses", ["business", "firm", "company"]),
]
FEATURED = {"salary": "Most chosen", "fno": "Traders", "foreign": "Global"}


def _package_card(key):
    name, price = next((n, p) for v, n, p in PACKAGES if v == key)
    form, who, items = PACKAGE_DETAILS[key]
    feat = FEATURED.get(key)
    ticks = "\n".join(f"                  <li>{i.replace('&', '&amp;')}</li>" for i in items)
    return f"""              <div class="plan{' plan--featured' if feat else ''} reveal">
                {f'<span class="plan__badge">{feat}</span>' if feat else ''}
                <h4>{name.replace('&', '&amp;')}</h4>
                <p class="plan__for">{who} · <strong>{form}</strong></p>
                <p class="plan__price">₹{int(price):,}</p>
                <p class="plan__tax">+ 18% GST</p>
                <ul class="ticks">
{ticks}
                </ul>
                <a class="btn {'btn--brand' if feat else 'btn--ghost'} btn--block" href="#get-started" data-modal-open data-plan="{key}" data-track="select_plan" data-location="package-{key}">Choose package<span class="visually-hidden">: {name.replace('&', '&amp;')}</span></a>
              </div>"""


PACKAGES_HTML = """      <!-- ================= PACKAGES ================= -->
      <section id="packages" class="section" aria-labelledby="h-packages">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">Packages</span>
            <h2 id="h-packages">CA-assisted packages for every kind of income.</h2>
            <p>Pick the package that matches your most complex income. Every package includes regime comparison, AIS reconciliation, CA review, e-verification and refund tracking. Your fee is confirmed after a free document review, before you pay.</p>
          </div>
""" + "\n".join(
    f"""          <h3 class="pkg-group reveal">{title}</h3>
          <div class="plans">
{chr(10).join(_package_card(k) for k in keys)}
          </div>"""
    for title, keys in PACKAGE_GROUPS
) + """
          <p class="plans-note">Tax-audit cases, books of account, more than 500 crypto transactions and notice replies are quoted separately. Tax, interest and late fees are paid to the government and are not part of our fee.</p>
        </div>
      </section>
"""

SELF_VS_CA_HTML = r"""      <!-- ================= THREE WAYS TO FILE ================= -->
      <section id="self-vs-ca" class="section" aria-labelledby="h-self">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">Compare</span>
            <h2 id="h-self">Three ways to file. One right answer for you.</h2>
            <p>Every route ends on the Income Tax Department’s e-filing system. The difference is how much work you do and who checks it.</p>
          </div>
          <div class="table compare reveal" tabindex="0">
            <table>
              <caption>Government portal vs Bharat e-Filing self-filing vs CA-assisted</caption>
              <thead><tr><th scope="col">What matters</th><th scope="col">Government portal, on your own</th><th scope="col">Bharat e-Filing self-filing</th><th scope="col">CA-assisted</th></tr></thead>
              <tbody>
                <tr><th scope="row">Your time</th><td>2–6 hours</td><td class="yes">About 10–15 minutes</td><td class="yes">15 minutes to share documents</td></tr>
                <tr><th scope="row">Data entry</th><td>Pre-fill, plus manual for the rest</td><td class="yes">Auto-import and statement reading</td><td class="yes">Done for you</td></tr>
                <tr><th scope="row">ITR form and regime</th><td>You decide</td><td class="yes">Suggested and compared</td><td class="yes">Chosen by an expert</td></tr>
                <tr><th scope="row">AIS mismatch check</th><td>Manual</td><td class="yes">Automatic alerts</td><td class="yes">Reconciled by an expert</td></tr>
                <tr><th scope="row">Capital gains, F&amp;O, crypto</th><td>Complex schedules</td><td class="yes">From your statements</td><td class="yes">Computed and reviewed</td></tr>
                <tr><th scope="row">Foreign assets, NRI, audit cases</th><td>Hard</td><td>Supported (Pro), CA review advised</td><td class="yes">Recommended route</td></tr>
                <tr><th scope="row">CA review</th><td>No</td><td>Optional add-on</td><td class="yes">Always</td></tr>
                <tr><th scope="row">Help after filing</th><td>On your own</td><td>Refund tracking and alerts</td><td class="yes">Notice guidance included</td></tr>
                <tr><th scope="row">Price</th><td>—</td><td class="yes">Free to ₹999</td><td>From ₹2,499</td></tr>
              </tbody>
            </table>
          </div>
          <div class="note reveal mt-16">
            <span class="note__title">Decide in 10 seconds</span>
            <p>Salary, interest and simple capital gains? <a href="https://bharatefiling.com/itr/start/" data-track="app_start" data-location="decide">File it yourself</a>. Choose <a href="#expert">CA-assisted</a> if you have foreign assets or RSUs, are an NRI, need a tax audit, earn business income with books, got a notice last year, or simply want an expert to own it.</p>
          </div>
        </div>
      </section>
"""

MAIN = MAIN.replace("<!--PACKAGES-->\n", PACKAGES_HTML).replace("<!--SELF-VS-CA-->\n", SELF_VS_CA_HTML)

# ---------------------------------------------------------------- Income-specific guides (facts checked 4 Oct 2026)
SPECIAL_CHAPTERS = r"""          <section id="special-income" class="chapter prose reveal" aria-labelledby="h-cg">
            <span class="kicker">Capital gains</span>
            <h2 id="h-cg">Capital gains tax rates for FY 2025-26</h2>
            <p>Rates below apply to transfers on or after 23 July 2024 (Finance (No. 2) Act, 2024). Gains are reported in Schedule CG of ITR-2 or ITR-3; listed equity is also reported scrip-wise in Schedule 112A.</p>
            <div class="table" tabindex="0">
              <table>
                <caption>Holding periods and tax rates</caption>
                <thead><tr><th scope="col">Asset</th><th scope="col">Long-term after</th><th scope="col">Short-term rate</th><th scope="col">Long-term rate</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Listed shares, equity mutual funds (STT paid)</th><td>12 months</td><td>20%</td><td>12.5% above ₹1.25 lakh a year</td></tr>
                  <tr><th scope="row">Other listed securities (bonds, ETFs other than debt)</th><td>12 months</td><td>Slab rate</td><td>12.5%</td></tr>
                  <tr><th scope="row">Debt mutual funds bought on or after 1 April 2023</th><td>Never</td><td>Slab rate</td><td>Slab rate (Section 50AA)</td></tr>
                  <tr><th scope="row">Land, building, house</th><td>24 months</td><td>Slab rate</td><td>12.5%, or 20% with indexation for resident individuals/HUFs on property bought before 23 July 2024 (pay the lower)</td></tr>
                  <tr><th scope="row">Unlisted shares, foreign shares, physical gold</th><td>24 months</td><td>Slab rate</td><td>12.5%</td></tr>
                  <tr><th scope="row">Crypto and other VDAs</th><td>—</td><td colspan="2">30% flat on every transfer (Section 115BBH)</td></tr>
                </tbody>
              </table>
            </div>
            <ul>
              <li><strong>Exemptions on property gains:</strong> reinvest in a house (Section 54 / 54F, up to ₹10 crore) or in specified bonds within six months (Section 54EC, up to ₹50 lakh).</li>
              <li><strong>Losses:</strong> short-term capital loss can be set off against any capital gain; long-term loss only against long-term gains. Unused losses carry forward for 8 years if you file on time.</li>
              <li><strong>Section 87A rebate</strong> does not reduce tax on special-rate gains such as Section 111A or 112A.</li>
            </ul>
            <div class="example">
              <span class="example__label">Example · Investor</span>
              <p><strong>Rahul in Pune</strong> sold equity funds held for three years with a ₹2.4 lakh gain. The first ₹1.25 lakh is exempt; tax is 12.5% of ₹1.15 lakh = ₹14,375 plus 4% cess. He files ITR-2, not ITR-1, because the gain is above ₹1.25 lakh.</p>
            </div>
          </section>

          <section id="fno" class="chapter prose reveal" aria-labelledby="h-fno">
            <span class="kicker">F&amp;O and intraday</span>
            <h2 id="h-fno">ITR for F&amp;O and intraday traders</h2>
            <p class="lede">Futures and options are <strong>non-speculative business income</strong>; intraday equity trading is <strong>speculative business income</strong>. Both go in <strong>ITR-3</strong> with a profit-and-loss account and balance sheet, never in ITR-2.</p>
            <div class="table" tabindex="0">
              <table>
                <caption>How trading income is treated</caption>
                <thead><tr><th scope="col">Point</th><th scope="col">F&amp;O</th><th scope="col">Intraday equity</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Nature</th><td>Non-speculative business</td><td>Speculative business</td></tr>
                  <tr><th scope="row">Tax rate</th><td colspan="2">Your slab rate, after deducting brokerage, STT-exclusive expenses, internet, advisory and depreciation</td></tr>
                  <tr><th scope="row">Turnover (ICAI guidance note)</th><td>Sum of absolute profits and losses on each trade</td><td>Sum of absolute profits and losses</td></tr>
                  <tr><th scope="row">Loss set-off</th><td>Against any income except salary</td><td>Only against speculative income</td></tr>
                  <tr><th scope="row">Loss carry-forward</th><td>8 years</td><td>4 years</td></tr>
                </tbody>
              </table>
            </div>
            <ul>
              <li><strong>Tax audit (Section 44AB):</strong> required if trading turnover exceeds ₹10 crore (trading is fully digital). Below that, an audit can still apply if you opted out of presumptive taxation under Section 44AD in the last five years and your income exceeds the exemption limit. We check this before filing.</li>
              <li><strong>File by the due date</strong> (31 August 2026 without audit, 31 October with audit) or you lose the right to carry forward losses.</li>
              <li><strong>STT increase from 1 April 2026:</strong> 0.05% on futures (was 0.02%) and 0.15% on options premium (was 0.10%). This affects trading costs from FY 2026-27.</li>
            </ul>
          </section>

          <section id="crypto" class="chapter prose reveal" aria-labelledby="h-crypto">
            <span class="kicker">Crypto and VDA</span>
            <h2 id="h-crypto">How crypto is taxed in your ITR</h2>
            <ul>
              <li><strong>30% flat tax</strong> plus cess on gains from every transfer of a virtual digital asset (Section 115BBH), whatever your income slab.</li>
              <li><strong>No deductions</strong> except the cost of acquisition, and <strong>no loss set-off</strong>, even between two coins, and no carry-forward.</li>
              <li><strong>1% TDS</strong> under Section 194S on crypto sales above ₹50,000 or ₹10,000 a year, depending on who the buyer is. Claim it from AIS / Form 26AS.</li>
              <li><strong>Gifts and airdrops</strong> of crypto above ₹50,000 can be taxed as income from other sources in the receiver’s hands.</li>
              <li>Report every transfer in <strong>Schedule VDA</strong> (ITR-2, or ITR-3 if you trade as a business). Exchanges report your trades to the department, so mismatches lead to notices.</li>
            </ul>
          </section>

          <section id="foreign-nri" class="chapter prose reveal" aria-labelledby="h-foreign">
            <span class="kicker">Foreign income and NRIs</span>
            <h2 id="h-foreign">Foreign income, RSUs and NRI returns</h2>
            <h3>1. Check your residential status first</h3>
            <p>You are resident if you stayed in India <strong>182 days or more</strong> in the year, or <strong>60 days</strong> in the year and 365 days in the previous four years. For Indian citizens and PIOs visiting India, 60 becomes 182 days, or 120 days if Indian income exceeds ₹15 lakh. Residents are taxed on worldwide income; NRIs only on Indian income.</p>
            <h3>2. Residents with foreign assets (RSUs, US stocks, foreign accounts)</h3>
            <ul>
              <li><strong>RSUs and ESOPs</strong> are taxed as salary when they vest or are exercised; selling them later gives capital gains (foreign shares are long-term after 24 months).</li>
              <li><strong>Schedule FA</strong> lists every foreign asset held at any time in the <strong>calendar year</strong> (1 January–31 December 2025 for this return), even with no income.</li>
              <li><strong>Foreign tax credit:</strong> file <strong>Form 67</strong> before the return to claim credit for US or other tax withheld under the DTAA.</li>
              <li><strong>Penalty:</strong> not reporting foreign assets can attract a ₹10 lakh penalty under the Black Money Act. Since 1 October 2024, no penalty applies where non-property foreign assets total up to ₹20 lakh, and Budget 2026 announced a one-time disclosure window for small taxpayers.</li>
            </ul>
            <h3>3. NRIs with Indian income</h3>
            <ul>
              <li>File <strong>ITR-2</strong> (ITR-3 with business income). NRIs cannot use ITR-1 or ITR-4 and do not get the Section 87A rebate.</li>
              <li>File even below the taxable limit to <strong>claim refunds</strong> of TDS deducted on property sales, NRO interest or rent.</li>
              <li>Claim lower DTAA rates with a <strong>Tax Residency Certificate</strong> and Form 10F.</li>
            </ul>
          </section>

          <section id="deductions" class="chapter prose reveal" aria-labelledby="h-ded">
            <span class="kicker">Deductions</span>
            <h2 id="h-ded">Deductions you can claim, by regime</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Main deductions for individuals, FY 2025-26</caption>
                <thead><tr><th scope="col">Deduction</th><th scope="col">Limit</th><th scope="col">New regime?</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Standard deduction (salary, pension)</th><td>₹75,000 new / ₹50,000 old</td><td class="yes">Yes</td></tr>
                  <tr><th scope="row">80CCD(2) employer NPS</th><td>14% of salary (new), 10% (old, private employers)</td><td class="yes">Yes</td></tr>
                  <tr><th scope="row">80C (PPF, ELSS, EPF, LIC, principal, fees)</th><td>₹1.5 lakh</td><td>No</td></tr>
                  <tr><th scope="row">80CCD(1B) own NPS</th><td>₹50,000 extra</td><td>No</td></tr>
                  <tr><th scope="row">80D health insurance</th><td>₹25,000 self + ₹25,000 parents (₹50,000 each if senior)</td><td>No</td></tr>
                  <tr><th scope="row">Home-loan interest, self-occupied (24(b))</th><td>₹2 lakh</td><td>No (let-out property: yes)</td></tr>
                  <tr><th scope="row">HRA (10(13A)) or 80GG rent</th><td>As per formula / ₹60,000</td><td>No</td></tr>
                  <tr><th scope="row">80E education-loan interest</th><td>No cap, 8 years</td><td>No</td></tr>
                  <tr><th scope="row">80G donations</th><td>50% or 100%</td><td>No</td></tr>
                  <tr><th scope="row">80TTA / 80TTB interest</th><td>₹10,000 / ₹50,000 (seniors)</td><td>No</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="advance-tax" class="chapter prose reveal" aria-labelledby="h-adv">
            <span class="kicker">Advance tax</span>
            <h2 id="h-adv">Advance tax: pay during the year, not at filing</h2>
            <p>If your tax after TDS is <strong>₹10,000 or more</strong>, pay it in instalments. Resident senior citizens without business income are exempt. Missing them costs 1% a month under Sections 234B and 234C.</p>
            <div class="tile tile--navy">
            <ul class="rhythm" aria-label="Advance tax instalments">
              <li class="is-key"><b>15 Jun</b>15%</li>
              <li><b>15 Sep</b>45%</li>
              <li><b>15 Dec</b>75%</li>
              <li class="is-key"><b>15 Mar</b>100%</li>
            </ul>
            </div>
            <p class="muted" style="font-size: var(--fs-14)">Presumptive taxpayers under Sections 44AD and 44ADA can pay the full amount by 15 March.</p>
          </section>
"""

MORE_CHAPTERS = r"""          <section id="after-filing" class="chapter prose reveal" aria-labelledby="h-after">
            <span class="kicker">After filing</span>
            <h2 id="h-after">Intimations and notices after you file</h2>
            <div class="table" tabindex="0">
              <table>
                <caption>Common communications from the Income Tax Department</caption>
                <thead><tr><th scope="col">Section</th><th scope="col">What it means</th><th scope="col">What to do</th></tr></thead>
                <tbody>
                  <tr><th scope="row">143(1) intimation</th><td>Return processed; shows refund, demand or no change</td><td>Compare with your computation</td></tr>
                  <tr><th scope="row">143(1)(a) proposed adjustment</th><td>Mismatch with AIS, 26AS or Form 16</td><td>Respond online within 30 days</td></tr>
                  <tr><th scope="row">139(9) defective return</th><td>Wrong form or missing details</td><td>Correct within 15 days, or the return is treated as not filed</td></tr>
                  <tr><th scope="row">245 refund adjustment</th><td>Refund to be set off against an old demand</td><td>Agree or disagree within 30 days</td></tr>
                  <tr><th scope="row">143(2) scrutiny</th><td>Detailed assessment of your return</td><td>Reply with documents on the e-proceedings tab</td></tr>
                  <tr><th scope="row">148A / 148 reassessment</th><td>Department believes income escaped tax</td><td>Get professional help immediately</td></tr>
                </tbody>
              </table>
            </div>
            <p><strong>Check refund status:</strong> e-File → Income Tax Returns → View Filed Returns on the portal. Every Bharat e-Filing package includes guidance on intimations; full notice replies are quoted separately.</p>
          </section>

          <section id="mistakes" class="chapter prose reveal" aria-labelledby="h-mistakes">
            <span class="kicker">Avoid notices</span>
            <h2 id="h-mistakes">10 ITR mistakes that trigger notices</h2>
            <ol>
              <li>Filing the wrong ITR form (for example ITR-1 with F&amp;O or capital gains above ₹1.25 lakh).</li>
              <li>Ignoring income shown in AIS: savings and FD interest, dividends, rent.</li>
              <li>Leaving out a previous employer’s salary after a job change.</li>
              <li>Not reporting foreign shares, RSUs or bank accounts in Schedule FA.</li>
              <li>Reporting crypto as normal capital gains or setting off crypto losses.</li>
              <li>Claiming old-regime deductions with business income without filing Form 10-IEA.</li>
              <li>Claiming HRA and Section 80GG together, or HRA without rent receipts.</li>
              <li>Not paying self-assessment tax before filing.</li>
              <li>Filing after the due date and losing the right to carry forward losses.</li>
              <li>Forgetting to e-verify within 30 days.</li>
            </ol>
          </section>
"""

MAIN = MAIN.replace("<!--SPECIAL-CHAPTERS-->\n", SPECIAL_CHAPTERS).replace("<!--MORE-CHAPTERS-->\n", MORE_CHAPTERS)

# ---------------------------------------------------------------- Self-filing app (first screen)
HERO_HTML = f"""      <!-- ================= HERO: SELF-FILING APP ================= -->
      <section class="hero" aria-labelledby="page-title">
        <div class="hero__aurora" aria-hidden="true"><span></span><span></span><span></span></div>
        <div class="wrap hero__grid">
          <div>
            <nav class="crumbs" aria-label="Breadcrumb" data-rise style="--i: 0">
              <ol>
                <li><a href="https://bharatefiling.com/">Home</a></li>
                <li><a href="https://bharatefiling.com/product/income-tax-e-filing/">Income Tax</a></li>
                <li aria-current="page">ITR Filing</li>
              </ol>
            </nav>
            <a class="pill-new" href="#self-filing" data-rise style="--i: 1"><span class="pill-new__tag">New</span>Self-filing for AY 2026-27 is here</a>
            <h1 id="page-title" data-rise style="--i: 2">File your ITR yourself, <span class="text-gradient">in minutes.</span></h1>
            <p class="hero__sub" data-rise style="--i: 3">With your consent, we fetch your AIS, Form 26AS and pre-filled data straight from the Income Tax Department, pick the right ITR form and regime, and you file and e-verify without leaving Bharat e-Filing.</p>
            <div class="btn-row" data-rise style="--i: 4">
              <a class="btn btn--brand" href="{APP_URL}" data-track="app_start" data-location="hero">Start filing free</a>
              <a class="btn btn--ghost" href="#expert" data-track="cta_click" data-location="hero-expert">Let a CA file it</a>
            </div>
            <ul class="assurances" data-rise style="--i: 5">
              <li><svg width="18" height="18" aria-hidden="true"><use href="#i-check" /></svg>Pre-filled from AIS</li>
              <li><svg width="18" height="18" aria-hidden="true"><use href="#i-check" /></svg>Regime auto-compared</li>
              <li><svg width="18" height="18" aria-hidden="true"><use href="#i-check" /></svg>E-verify with Aadhaar OTP</li>
            </ul>
          </div>

          <figure class="app-mock" data-rise style="--i: 3">
            <div class="app-mock__bar" aria-hidden="true"><span></span><span></span><span></span><b>Bharat e-Filing · ITR AY 2026-27</b></div>
            <ol class="app-mock__steps" aria-label="Sample self-filing flow">
              <li class="is-done"><span class="app-mock__dot" aria-hidden="true">✓</span><div><strong>PAN verified</strong><small>ABCPS1234K · Resident individual</small></div></li>
              <li class="is-done"><span class="app-mock__dot" aria-hidden="true">✓</span><div><strong>Imported from Income Tax Department</strong><small>Form 16 · AIS · Form 26AS · pre-filled data</small>
                <span class="app-mock__chips"><span>Salary ₹14,20,000</span><span>TDS ₹96,400</span><span>Interest ₹18,350</span></span></div></li>
              <li class="is-done"><span class="app-mock__dot" aria-hidden="true">✓</span><div><strong>ITR-1 selected · New regime</strong><small>Saves ₹41,600 over the old regime</small></div></li>
              <li class="is-active"><span class="app-mock__dot" aria-hidden="true">4</span><div><strong>Refund due: ₹22,150</strong><small>Ready to file and e-verify</small></div></li>
            </ol>
            <span class="app-mock__cta" aria-hidden="true">File &amp; e-verify</span>
            <figcaption>Illustrative example. Your figures come from your own records.</figcaption>
          </figure>
        </div>
      </section>

"""

_self_cards = "\n".join(
    f"""            <div class="plan{' plan--featured' if key == 'self-plus' else ''} reveal">
              {'<span class="plan__badge">Investors</span>' if key == 'self-plus' else ''}
              <h3>{name}</h3>
              <p class="plan__for">{forms}</p>
              <p class="plan__price">{price}</p>
              <p class="plan__tax">{'No card needed' if price == 'Free' else '+ 18% GST, per return'}</p>
              <ul class="ticks">
{chr(10).join(f'                <li>{i.replace("&", "&amp;")}</li>' for i in items)}
              </ul>
              <a class="btn {'btn--brand' if key == 'self-plus' else 'btn--ghost'} btn--block" href="{APP_URL}?plan={key}" data-track="app_start" data-location="plan-{key}">Start filing<span class="visually-hidden"> with {name}</span></a>
            </div>"""
    for key, name, price, forms, items in SELF_PLANS
)

SELF_FILING_HTML = f"""      <!-- ================= SELF-FILING ================= -->
      <section id="self-filing" class="section section--first" aria-labelledby="h-selffile">
        <div class="wrap">
          <div class="section-head reveal">
            <span class="kicker">Self-filing</span>
            <h2 id="h-selffile">Your data comes in. Your ITR goes out.</h2>
            <p>Bharat e-Filing connects to the Income Tax Department’s e-filing system through its official e-Return Intermediary (ERI) APIs, so you don’t retype anything and nothing is filed without your approval.</p>
          </div>
          <ol class="stepper">
            <li style="--i: 0"><span class="when">1 min</span><h3>Sign up with PAN</h3><p>Mobile OTP and PAN. No documents needed to start.</p></li>
            <li style="--i: 1"><span class="when">1 min</span><h3>Approve access</h3><p>Confirm with the OTP the Income Tax Department sends you. You can withdraw consent anytime.</p></li>
            <li style="--i: 2"><span class="when">Automatic</span><h3>We import</h3><p>Pre-filled return data, AIS, TIS and Form 26AS. Upload Form 16, broker or crypto statements and we read them.</p></li>
            <li style="--i: 3"><span class="when">5 min</span><h3>Review</h3><p>Right ITR form, cheaper regime, every deduction, and alerts for any mismatch with AIS.</p></li>
            <li style="--i: 4"><span class="when">1 min</span><h3>File &amp; e-verify</h3><p>Submit and e-verify with Aadhaar OTP in the app, then track your refund.</p></li>
          </ol>

          <div class="bento mt-16">
            <div class="tile tile--wide tile--navy reveal">
              <h3>Mismatch alerts before you file</h3>
              <p>Most tax notices start with income missing from the return but present in AIS. We compare every AIS line with your return and flag what is missing, before the department does.</p>
            </div>
            <div class="tile tile--brand reveal">
              <span class="tile__stat">2 regimes</span>
              <h3>Always compared</h3>
              <p>We compute old and new regime tax and pick the lower one.</p>
            </div>
            <div class="tile reveal">
              <span class="tile__stat">F&amp;O · crypto</span>
              <h3>Statements read for you</h3>
              <p>Broker P&amp;L, mutual-fund CAS and exchange reports become ready schedules.</p>
            </div>
            <div class="tile tile--leaf reveal">
              <span class="tile__stat">1 tap</span>
              <h3>Switch to a CA</h3>
              <p>Stuck? Hand your draft to our CA team. Nothing to re-upload.</p>
            </div>
            <div class="tile reveal">
              <span class="tile__stat">Your data</span>
              <h3>Consent first</h3>
              <p>Used only to file your return, under the DPDP Act, 2023. Never sold.</p>
            </div>
          </div>

          <h3 class="pkg-group center reveal">Self-filing plans</h3>
          <div class="plans">
{_self_cards}
          </div>
          <p class="plans-note">Add a <strong>CA review before you file</strong> to any self-filing plan for ₹999 + GST. ERI registration no.: REPLACE_ERI_ID.</p>
        </div>
      </section>

"""

EXPERT_HTML = """      <!-- ================= CA-ASSISTED (lead form) ================= -->
      <section id="expert" class="section section--glow" aria-labelledby="h-expert">
        <div class="wrap hero__grid">
          <div class="reveal">
            <span class="kicker">CA-assisted filing</span>
            <h2 id="h-expert">Prefer an expert? Let a CA file it.</h2>
            <p class="lede">Send your documents on WhatsApp. A tax expert prepares your return, a Chartered Accountant reviews it, and you approve it before filing. Best for capital gains, F&amp;O, crypto, foreign income, NRIs and business income.</p>
            <ul class="ticks">
              <li>Free first review of your documents and a fixed quote</li>
              <li>Old vs new regime and every deduction checked</li>
              <li>AIS and Form 26AS reconciled line by line</li>
              <li>Help with intimations and notices after filing</li>
            </ul>
            <p><a class="link-arrow" href="#packages">See all 12 CA-assisted packages</a></p>
          </div>
          <div class="form-card reveal" id="get-started">
            <h3>Get your ITR filed by a CA</h3>
            <p>Pick your plan. An expert calls you back to collect your documents.</p>
            <form id="itr-lead-form" data-lead-form novalidate>
              <!-- PROPOSED prices: keep in sync with PACKAGES at the top of this file. -->
              <fieldset class="plan-picker">
                <legend>What’s your main income?</legend>
                <div class="plan-picker__options">
                  <label><input type="radio" name="plan" value="salary" data-price="2499" checked /><span>Salary</span><strong>₹2,499</strong></label>
                  <label><input type="radio" name="plan" value="capital-gains" data-price="3499" /><span>Investor</span><strong>₹3,499</strong></label>
                  <label><input type="radio" name="plan" value="fno" data-price="4499" /><span>F&amp;O / Crypto</span><strong>₹4,499</strong></label>
                </div>
                <p class="plan-picker__hint">+ 18% GST. NRI, foreign income and business: <a href="#packages">all 12 packages</a></p>
              </fieldset>
              <div class="field">
                <label for="f-name">Full name</label>
                <input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-err" />
                <p class="field__error" id="f-name-err" aria-live="polite"></p>
              </div>
              <div class="field-row">
                <div class="field">
                  <label for="f-phone">Mobile number</label>
                  <input id="f-phone" name="phone" type="tel" inputmode="numeric" autocomplete="tel" maxlength="16" required aria-describedby="f-phone-err" />
                  <p class="field__error" id="f-phone-err" aria-live="polite"></p>
                </div>
                <div class="field">
                  <label for="f-email">Email</label>
                  <input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="f-email-err" />
                  <p class="field__error" id="f-email-err" aria-live="polite"></p>
                </div>
              </div>
              <input type="hidden" name="service" value="income-tax-return-filing" />
              <input type="hidden" name="utm_source" />
              <input type="hidden" name="utm_medium" />
              <input type="hidden" name="utm_campaign" />
              <input type="hidden" name="utm_term" />
              <input type="hidden" name="utm_content" />
              <input type="hidden" name="gclid" />
              <input type="hidden" name="fbclid" />
              <input type="hidden" name="msclkid" />
              <button class="btn btn--primary btn--block" type="submit">Get free consultation</button>
              <p class="form-note">Protected under the DPDP Act, 2023. <a href="https://bharatefiling.com/privacy-policy/">Privacy policy</a></p>
            </form>
          </div>
        </div>
      </section>

"""

MAIN = MAIN.replace("<!--HERO-->\n", HERO_HTML).replace("<!--SELF-FILING-->\n", SELF_FILING_HTML).replace("<!--EXPERT-->\n", EXPERT_HTML)
