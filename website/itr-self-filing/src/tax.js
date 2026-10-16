// ITR-1 (Sahaj) computation engine — AY 2026-27 (FY 2025-26), resident individuals.
// Pure functions, no DOM. Law: Income-tax Act, 1961 (applies to FY 2025-26 via s.536 of the 2025 Act),
// as amended by the Finance Acts 2025 and 2026.

export const AY = "2026-27";
export const FY = "2025-26";
export const DUE_DATE = "2026-07-31"; // s.139(1) for ITR-1 filers (non-audit, non-business)
export const BELATED_LAST_DATE = "2026-12-31"; // s.139(4)
export const ITR1_INCOME_LIMIT = 5000000;
export const LTCG_112A_EXEMPT = 125000;

const NEW_SLABS = [[400000, 0], [800000, 0.05], [1200000, 0.1], [1600000, 0.15], [2000000, 0.2], [2400000, 0.25], [Infinity, 0.3]];
const OLD_SLABS = {
  normal: [[250000, 0], [500000, 0.05], [1000000, 0.2], [Infinity, 0.3]],
  senior: [[300000, 0], [500000, 0.05], [1000000, 0.2], [Infinity, 0.3]],
  superSenior: [[500000, 0], [1000000, 0.2], [Infinity, 0.3]],
};

export const n = (v) => {
  const x = typeof v === "string" ? Number(v.replace(/[,₹\s]/g, "")) : Number(v);
  return Number.isFinite(x) ? x : 0;
};
const pos = (v) => Math.max(0, n(v));
const sum = (arr, f = (x) => x) => arr.reduce((a, x) => a + n(f(x)), 0);
export const round10 = (v) => Math.round(n(v) / 10) * 10; // ss. 288A and 288B
const floor100 = (v) => Math.floor(n(v) / 100) * 100; // Rule 119A

export function slabTax(income, slabs) {
  let tax = 0, prev = 0;
  for (const [upto, rate] of slabs) {
    if (income > prev) tax += (Math.min(income, upto) - prev) * rate;
    prev = upto;
  }
  return tax;
}

// Age category for FY 2025-26: a person born on 1 April is treated as attaining the age on 31 March (CBDT).
export function ageCategory(dob) {
  if (!dob) return "normal";
  const d = new Date(dob + "T00:00:00");
  const ref = new Date("2026-04-01T00:00:00");
  let age = ref.getFullYear() - d.getFullYear();
  if (ref.getMonth() < d.getMonth() || (ref.getMonth() === d.getMonth() && ref.getDate() < d.getDate())) age--;
  return age >= 80 ? "superSenior" : age >= 60 ? "senior" : "normal";
}

const months = (fromISO, toISO) => {
  // number of months or part of months, both ends counted the way the department does (1 Aug .. filing date)
  const a = new Date(fromISO + "T00:00:00"), b = new Date(toISO + "T00:00:00");
  if (b < a) return 0;
  return (b.getFullYear() - a.getFullYear()) * 12 + (b.getMonth() - a.getMonth()) + 1;
};

// ---------------------------------------------------------------- heads of income
export function salaryHead(data, regime) {
  const emps = data.salary?.employers || [];
  const rows = emps.map((e) => {
    const gross = pos(e.s17_1) + pos(e.s17_2) + pos(e.s17_3);
    const ex = e.exemptions || {};
    // Exemptions allowed in the new regime: gratuity 10(10), commuted pension 10(10A), leave encashment 10(10AA)
    // and the "other" bucket only where it is regime-neutral (user-declared). HRA, LTA and 10(14) are old-regime only.
    const bothRegimes = pos(ex.gratuity) + pos(ex.commutedPension) + pos(ex.leaveEncashment);
    const oldOnly = pos(ex.hra) + pos(ex.lta) + pos(ex.special10_14) + pos(ex.other);
    const exempt = regime === "old" ? bothRegimes + oldOnly : bothRegimes;
    return { name: e.name || "Employer", tan: e.tan || "", gross, exempt: Math.min(exempt, gross), net: Math.max(0, gross - exempt),
      profTax: regime === "old" ? pos(e.profTax) : 0, entAllow: regime === "old" ? pos(e.entAllow) : 0, isPension: !!e.isPension };
  });
  const net = sum(rows, (r) => r.net);
  const stdCap = regime === "old" ? 50000 : 75000;
  const standardDeduction = rows.length ? Math.min(stdCap, net) : 0;
  const profTax = Math.min(sum(rows, (r) => r.profTax), 2500 * Math.max(1, rows.length)); // Article 276: max ₹2,500 a year per state
  const entAllow = sum(rows, (r) => r.entAllow);
  const income = Math.max(0, net - standardDeduction - profTax - entAllow);
  return { rows, gross: sum(rows, (r) => r.gross), exempt: sum(rows, (r) => r.exempt), net, standardDeduction, profTax, entAllow, income };
}

export function housePropertyHead(data, regime) {
  const props = (data.houseProperties || []).slice(0, 2);
  let sopInterest = 0;
  const rows = props.map((p) => {
    const share = Math.min(100, Math.max(0, p.sharePct === undefined || p.sharePct === "" ? 100 : n(p.sharePct))) / 100;
    if (p.type === "self") {
      const interest = pos(p.interest) * share;
      sopInterest += interest;
      return { ...p, type: "self", annualValue: 0, standard30: 0, interestClaimed: interest, income: -interest, share };
    }
    const gav = pos(p.rent) * share;
    const nav = Math.max(0, gav - pos(p.municipalTax) * share);
    const standard30 = Math.round(nav * 0.3);
    const interest = pos(p.interest) * share;
    return { ...p, annualValue: nav, standard30, interestClaimed: interest, income: nav - standard30 - interest, share, gav };
  });
  // Self-occupied interest: ₹2 lakh overall (s.24(b)), and not at all in the new regime (s.115BAC(2)).
  const sopAllowed = regime === "old" ? Math.min(sopInterest, 200000) : 0;
  let scale = sopInterest > 0 ? sopAllowed / sopInterest : 0;
  rows.forEach((r) => { if (r.type === "self") { r.interestClaimed = Math.round(r.interestClaimed * scale); r.income = -r.interestClaimed; } });
  const total = sum(rows, (r) => r.income);
  let income, lossNotSetOff = 0;
  if (total >= 0) income = total;
  else if (regime === "new") { income = 0; lossNotSetOff = -total; } // new regime: HP loss cannot be set off against other heads
  else { income = Math.max(total, -200000); lossNotSetOff = Math.max(0, -total - 200000); } // s.71(3A) cap ₹2 lakh
  return { rows, total, income, lossNotSetOff };
}

export function otherSourcesHead(data, regime) {
  const o = data.otherSources || {};
  const items = [
    ["Interest from savings bank accounts", pos(o.savingsInterest), "savings"],
    ["Interest from deposits (bank / post office / co-op)", pos(o.depositInterest), "deposit"],
    ["Interest on income-tax refund", pos(o.refundInterest), "refund"],
    ["Dividend income", pos(o.dividend), "dividend"],
    ["Family pension", pos(o.familyPension), "familyPension"],
    ...(o.others || []).map((x) => [x.label || "Other income", pos(x.amount), "other"]),
  ].filter((r) => r[1] > 0);
  const gross = sum(items, (r) => r[1]);
  const fp = pos(o.familyPension);
  const familyPensionDeduction = Math.min(Math.round(fp / 3), regime === "old" ? 15000 : 25000); // s.57(iia)
  return { items, gross, familyPensionDeduction, income: Math.max(0, gross - familyPensionDeduction) };
}

export function ltcgHead(data) {
  const l = data.ltcg112a || {};
  const gain = Math.max(0, pos(l.saleValue) - pos(l.costOfAcquisition));
  const total = l.mode === "gain" ? pos(l.gain) : gain;
  return { gain: total, exempt: Math.min(total, LTCG_112A_EXEMPT), taxable: Math.max(0, total - LTCG_112A_EXEMPT) };
}

// ---------------------------------------------------------------- deductions (Chapter VI-A)
export function deductions(data, regime, gtiBeforeDed, category) {
  const d = data.deductions || {};
  const list = [];
  const add = (code, label, claimed, allowed, note) => { if (n(claimed) > 0 || allowed > 0) list.push({ code, label, claimed: n(claimed), allowed: Math.round(allowed), note }); };
  const salaryBasic = pos(d.basicPlusDA);
  // Employer NPS 80CCD(2): 14% of basic+DA in the new regime, 10% in the old regime (14% for govt employers).
  const ccd2Cap = salaryBasic > 0 ? salaryBasic * (regime === "new" || d.govtEmployer ? 0.14 : 0.1) : Infinity;
  add("80CCD(2)", "Employer contribution to NPS", d.s80ccd2, Math.min(pos(d.s80ccd2), ccd2Cap), salaryBasic ? "" : "Cap not checked: enter basic + DA");
  add("80CCH", "Agnipath Scheme contribution", d.s80cch, pos(d.s80cch));
  if (regime === "old") {
    const c = Math.min(pos(d.s80c) + pos(d.s80ccc) + pos(d.s80ccd1), 150000);
    add("80C/80CCC/80CCD(1)", "LIC, PPF, EPF, ELSS, tuition, home-loan principal, pension funds", pos(d.s80c) + pos(d.s80ccc) + pos(d.s80ccd1), c);
    add("80CCD(1B)", "Own NPS contribution (additional)", d.s80ccd1b, Math.min(pos(d.s80ccd1b), 50000));
    const selfCap = d.selfSenior ? 50000 : 25000, parentCap = d.parentsSenior ? 50000 : 25000;
    const checkup = Math.min(pos(d.s80dCheckup), 5000);
    const selfAmt = Math.min(pos(d.s80dSelf) + checkup, selfCap);
    add("80D", "Health insurance and preventive check-up", pos(d.s80dSelf) + pos(d.s80dParents) + pos(d.s80dCheckup), selfAmt + Math.min(pos(d.s80dParents), parentCap));
    add("80E", "Interest on education loan", d.s80e, pos(d.s80e));
    add("80EEA/80EEB", "Housing (affordable) / electric-vehicle loan interest", d.s80eeb, Math.min(pos(d.s80eeb), 150000));
    add("80G", "Donations (eligible amount)", d.s80g, pos(d.s80g));
    add("80GG", "Rent paid (no HRA received)", d.s80gg, Math.min(pos(d.s80gg), 60000));
    add("80DD/80U", "Disability (self or dependant)", d.s80u, Math.min(pos(d.s80u), 125000));
    const interestBase = pos(data.otherSources?.savingsInterest);
    if (category === "normal") add("80TTA", "Savings bank interest", interestBase, Math.min(interestBase, 10000));
    else {
      const all = interestBase + pos(data.otherSources?.depositInterest);
      add("80TTB", "Interest on deposits (senior citizens)", all, Math.min(all, 50000));
    }
  }
  // Chapter VI-A cannot exceed gross total income (excluding s.112A LTCG — s.80A / s.112A(6)).
  let total = sum(list, (x) => x.allowed);
  if (total > gtiBeforeDed) {
    const k = gtiBeforeDed / total;
    list.forEach((x) => (x.allowed = Math.floor(x.allowed * k)));
    total = sum(list, (x) => x.allowed);
  }
  return { list, total };
}

// ---------------------------------------------------------------- tax
export function taxOn(totalIncomeNormal, regime, category) {
  const slabs = regime === "new" ? NEW_SLABS : OLD_SLABS[category];
  const tax = slabTax(totalIncomeNormal, slabs);
  let rebate = 0;
  if (regime === "new") {
    if (totalIncomeNormal <= 1200000) rebate = Math.min(tax, 60000);
    else rebate = Math.max(0, tax - (totalIncomeNormal - 1200000)); // marginal relief on the s.87A rebate
  } else if (totalIncomeNormal <= 500000) rebate = Math.min(tax, 12500);
  return { tax, rebate };
}

export function interest(params) {
  const { assessedTax, taxPayableOnReturn, advance = [], selfAssessment = [], filingDate, category, noAdvanceTaxLiability } = params;
  const advTotal = sum(advance, (a) => a.amount);
  const satBeforeDue = sum(selfAssessment.filter((s) => s.date && s.date <= DUE_DATE), (s) => s.amount);
  // s.234A: tax on total income less TDS/TCS/advance tax/self-assessment tax paid by the due date, per month from 1 Aug.
  const base234A = floor100(Math.max(0, taxPayableOnReturn - advTotal - satBeforeDue));
  const late = filingDate > DUE_DATE;
  const m234A = late ? months("2026-08-01", filingDate) : 0;
  const i234A = base234A * 0.01 * m234A;

  // s.234B / s.234C apply only if tax after TDS/TCS is ₹10,000 or more, and not to resident seniors without business income (s.207(2)).
  let i234B = 0, i234C = 0;
  const exempt = noAdvanceTaxLiability || category === "senior" || category === "superSenior" || assessedTax < 10000;
  if (!exempt) {
    if (advTotal < 0.9 * assessedTax) {
      // 1% a month from 1 April to the month the tax is paid / return filed, reduced after self-assessment payments.
      let shortfall = floor100(assessedTax - advTotal);
      const sats = selfAssessment.filter((s) => s.date && s.date >= "2026-04-01" && s.date <= filingDate).sort((a, b) => a.date.localeCompare(b.date));
      let from = "2026-04-01";
      for (const s of sats) {
        const m = months(from, s.date);
        i234B += shortfall * 0.01 * m;
        shortfall = floor100(Math.max(0, shortfall - n(s.amount)));
        const d = new Date(s.date + "T00:00:00"); d.setMonth(d.getMonth() + 1, 1);
        from = d.toISOString().slice(0, 10);
      }
      if (shortfall > 0 && filingDate >= from) i234B += shortfall * 0.01 * months(from, filingDate);
    }
    const paidBy = (date) => sum(advance.filter((a) => a.date && a.date <= date), (a) => a.amount);
    const inst = [["2025-06-15", 0.15, 0.12, 3], ["2025-09-15", 0.45, 0.36, 3], ["2025-12-15", 0.75, 0.75, 3], ["2026-03-15", 1, 1, 1]];
    for (const [date, pct, safe, m] of inst) {
      const paid = paidBy(date);
      if (paid < safe * assessedTax) i234C += floor100(Math.max(0, pct * assessedTax - paid)) * 0.01 * m;
    }
  }
  return { i234A: Math.round(i234A), i234B: Math.round(i234B), i234C: Math.round(i234C), months234A: m234A };
}

export function lateFee(totalIncome, filingDate, category) {
  if (filingDate <= DUE_DATE) return 0;
  const basic = { normal: 400000, senior: 400000, superSenior: 400000 }[category]; // new-regime exemption limit (belated returns are new-regime)
  if (totalIncome <= basic) return 0;
  return totalIncome <= 500000 ? 1000 : 5000; // s.234F
}

// ---------------------------------------------------------------- full computation
export function compute(data, opts = {}) {
  const filingDate = opts.filingDate || new Date().toISOString().slice(0, 10);
  const category = ageCategory(data.personal?.dob);
  const belated = filingDate > DUE_DATE;
  const requested = opts.regime || data.regime || "new";
  // s.115BAC(6): a taxpayer without business income can opt out of the new regime only in a return filed by the s.139(1) due date.
  const regime = belated ? "new" : requested;

  const sal = salaryHead(data, regime);
  const hp = housePropertyHead(data, regime);
  const os = otherSourcesHead(data, regime);
  const lt = ltcgHead(data);
  const gtiNormal = Math.max(0, sal.income + hp.income + os.income);
  const gti = gtiNormal + lt.gain;
  const ded = deductions(data, regime, gtiNormal, category);
  const totalIncome = round10(Math.max(0, gti - ded.total));
  const normalIncome = Math.max(0, totalIncome - lt.gain);

  const { tax, rebate } = taxOn(normalIncome, regime, category);
  const tax112A = lt.taxable * 0.125; // nil within ITR-1 limits; s.87A rebate does not apply to s.112A tax
  const taxAfterRebate = Math.max(0, tax - rebate) + tax112A;
  const cess = taxAfterRebate * 0.04;
  const grossTax = taxAfterRebate + cess;
  const relief89 = pos(data.taxes?.relief89);
  const netTax = Math.max(0, grossTax - relief89);

  const t = data.taxes || {};
  const tdsSalary = sum(data.salary?.employers || [], (e) => e.tds);
  const tdsOther = sum(t.tdsOther || [], (x) => x.tds);
  const tcs = sum(t.tcs || [], (x) => x.amount);
  const advance = t.advance || [], sat = t.selfAssessment || [];
  const assessedTax = Math.max(0, netTax - tdsSalary - tdsOther - tcs);
  const intr = interest({ assessedTax, taxPayableOnReturn: assessedTax, advance, selfAssessment: sat, filingDate, category,
    noAdvanceTaxLiability: false });
  const fee = lateFee(totalIncome, filingDate, category);
  const totalLiability = round10(netTax) + intr.i234A + intr.i234B + intr.i234C + fee;
  const paid = tdsSalary + tdsOther + tcs + sum(advance, (a) => a.amount) + sum(sat, (s) => s.amount);
  const balance = round10(totalLiability - paid);

  const warnings = itr1Checks(data, { totalIncome, lt, hp, filingDate, regime, requested, belated });
  return {
    meta: { ay: AY, fy: FY, filingDate, belated, section: belated ? "139(4)" : "139(1)", regime, requestedRegime: requested, category },
    salary: sal, houseProperty: hp, otherSources: os, ltcg112a: lt,
    grossTotalIncome: gti, deductions: ded, totalIncome,
    tax: { normalIncome, slabTax: tax, rebate87A: rebate, tax112A, cess: Math.round(cess), grossTax: Math.round(grossTax), relief89, netTax: round10(netTax) },
    interest: intr, lateFee: fee, totalLiability,
    paid: { tdsSalary, tdsOther, tcs, advance: sum(advance, (a) => a.amount), selfAssessment: sum(sat, (s) => s.amount), total: paid },
    balance, refund: balance < 0 ? -balance : 0, payable: balance > 0 ? balance : 0,
    warnings,
  };
}

export function compareRegimes(data, opts = {}) {
  const f = opts.filingDate || new Date().toISOString().slice(0, 10);
  // compare on the due-date basis so the user sees what each regime would cost (interest/fee excluded)
  const a = compute(data, { filingDate: f > DUE_DATE ? DUE_DATE : f, regime: "new" });
  const b = compute(data, { filingDate: f > DUE_DATE ? DUE_DATE : f, regime: "old" });
  return { new: a.tax.netTax, old: b.tax.netTax };
}

export function itr1Checks(data, c) {
  const w = [];
  const flags = data.eligibility || {};
  if (c.totalIncome > ITR1_INCOME_LIMIT) w.push({ level: "block", text: "Total income is above ₹50 lakh. ITR-1 cannot be used; ITR-2 is required." });
  if (c.lt.gain > LTCG_112A_EXEMPT) w.push({ level: "block", text: "Long-term capital gains under s.112A exceed ₹1.25 lakh. ITR-2 is required." });
  if ((data.ltcg112a?.stcg || 0) > 0 || data.ltcg112a?.otherCG) w.push({ level: "block", text: "Short-term or other capital gains found. ITR-1 allows only s.112A LTCG up to ₹1.25 lakh; ITR-2 is required." });
  if ((data.houseProperties || []).length > 2) w.push({ level: "block", text: "More than two house properties. ITR-2 is required." });
  if (c.hp.lossNotSetOff > 0 && c.regime === "old") w.push({ level: "block", text: "House-property loss above ₹2 lakh must be carried forward, which ITR-1 does not allow. ITR-2 is required." });
  if (c.hp.lossNotSetOff > 0 && c.regime === "new") w.push({ level: "info", text: "House-property loss cannot be set off against other income in the new regime and is ignored." });
  for (const [k, text] of [["director", "You were a director in a company"], ["unlistedShares", "You held unlisted equity shares"], ["foreignAssets", "You have foreign assets or foreign income"], ["nonResident", "You are not a resident (or are RNOR)"], ["esopDeferred", "Tax on ESOPs from an eligible start-up was deferred"], ["tds194N", "TDS was deducted under s.194N (cash withdrawals)"], ["business", "You have business or professional income"], ["lottery", "You won lotteries, races or online games"]])
    if (flags[k]) w.push({ level: "block", text: `${text}. ITR-1 cannot be used.` });
  if (c.belated && c.requested === "old") w.push({ level: "info", text: "The old regime is not available in a belated return (s.115BAC(6)); this return is computed under the new regime." });
  if (c.filingDate > BELATED_LAST_DATE) w.push({ level: "block", text: "The last date for a belated return (31 December 2026) has passed. Only an updated return (ITR-U) is possible." });
  const agri = n(data.exemptIncome?.agriculture);
  if (agri > 5000) w.push({ level: "block", text: "Agricultural income above ₹5,000. ITR-2 is required." });
  return w;
}
