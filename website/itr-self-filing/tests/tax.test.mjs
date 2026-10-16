// node itr-self-filing/tests/tax.test.mjs — hand-computed expectations for AY 2026-27
import { compute, taxOn, ageCategory, interest, salaryHead } from "../src/tax.js";
let fail = 0;
const eq = (name, got, exp) => { const ok = Math.abs(got - exp) < 0.5; if (!ok) fail++; console.log(`${ok ? "✔" : "✖"} ${name}: got ${got}, expected ${exp}`); };
const base = (o = {}) => ({ personal: { dob: "1990-05-10" }, salary: { employers: [] }, houseProperties: [], otherSources: {}, deductions: {}, taxes: {}, ...o });
const ON_TIME = { filingDate: "2026-07-20" };

// 1) Salary ₹12,75,000, new regime → taxable ₹12,00,000 → tax 60,000 fully rebated → 0
let c = compute(base({ salary: { employers: [{ s17_1: 1275000 }] } }), ON_TIME);
eq("12.75L salary new regime net tax", c.tax.netTax, 0);
eq("12.75L salary total income", c.totalIncome, 1200000);

// 2) Salary 13L new: TI 12,25,000 → slab 63,750, marginal relief → tax 25,000, cess 1,000 → 26,000
c = compute(base({ salary: { employers: [{ s17_1: 1300000 }] } }), ON_TIME);
eq("13L salary marginal relief net tax", c.tax.netTax, 26000);

// 3) Salary 15L new: TI 14,25,000 → 20k+40k+33,750 = 93,750 + 4% = 97,500
c = compute(base({ salary: { employers: [{ s17_1: 1500000 }] } }), ON_TIME);
eq("15L salary new regime", c.tax.netTax, 97500);

// 4) Old regime 15L salary, 80C 1.5L, 80D 25k, HRA exempt 1L, PT 2,500
c = compute(base({ regime: "old", salary: { employers: [{ s17_1: 1500000, profTax: 2500, exemptions: { hra: 100000 } }] }, deductions: { s80c: 150000, s80dSelf: 25000 } }), ON_TIME);
// salary 15L - 1L HRA = 14L - 50k std - 2.5k PT = 13,47,500; less 1,75,000 = 11,72,500 → 12,500 + 1,00,000 + 51,750 = 1,64,250 ×1.04 = 1,70,820
eq("old regime TI", c.totalIncome, 1172500);
eq("old regime tax", c.tax.netTax, 170820);

// 5) Belated: old regime requested → forced new
c = compute(base({ regime: "old", salary: { employers: [{ s17_1: 1500000, tds: 97500 }] } }), { filingDate: "2026-10-16" });
eq("belated forces new regime (netTax)", c.tax.netTax, 97500);
eq("belated late fee 234F", c.lateFee, 5000);
eq("belated, fully paid by TDS → no 234A", c.interest.i234A, 0);

// 6) Self-occupied interest in new regime ignored; let-out property
c = compute(base({ salary: { employers: [{ s17_1: 1000000 }] }, houseProperties: [{ type: "let", rent: 240000, municipalTax: 10000, interest: 100000 }] }), ON_TIME);
// NAV 2,30,000; 30% 69,000; interest 1,00,000 → HP 61,000; salary 9,25,000; TI 9,86,000 → 20,000+18,600 = 38,600 → rebate 38,600 → 0
eq("let-out HP income", c.houseProperty.income, 61000);
eq("TI with HP", c.totalIncome, 986000);
eq("rebate within 12L", c.tax.netTax, 0);

// 7) Old regime HP loss capped at 2L
c = compute(base({ regime: "old", salary: { employers: [{ s17_1: 1200000 }] }, houseProperties: [{ type: "self", interest: 350000 }] }), ON_TIME);
eq("SOP interest capped at 2L (old)", c.houseProperty.income, -200000);

// 8) Family pension deduction: 90,000 → 1/3 = 30,000 capped 25,000 (new)
c = compute(base({ otherSources: { familyPension: 90000 } }), ON_TIME);
eq("family pension new regime", c.otherSources.familyPensionDeduction, 25000);

// 9) Senior citizen old slab 3L, 80TTB
eq("age category 1 Apr 1966 → senior", ageCategory("1966-04-01") === "senior" ? 1 : 0, 1);
eq("age category 2 Apr 1966 → normal", ageCategory("1966-04-02") === "normal" ? 1 : 0, 1);

// 10) 234A: tax due 50,000 after TDS, filed 16 Oct → Aug, Sep, Oct = 3 months → 1,500
const i = interest({ assessedTax: 50000, taxPayableOnReturn: 50000, advance: [], selfAssessment: [], filingDate: "2026-10-16", category: "normal" });
eq("234A 3 months", i.i234A, 1500);
// 234B: Apr..Oct = 7 months on 50,000 → 3,500
eq("234B 7 months", i.i234B, 3500);
// 234C: 15% of 50k=7,500×3% =225; 45%=22,500×3%=675; 75%=37,500×3%=1,125; 100%=50,000×1%=500 → 2,525
eq("234C", i.i234C, 2525);

// 11) Standard deduction capped at salary
eq("std deduction capped", salaryHead(base({ salary: { employers: [{ s17_1: 50000 }] } }), "new").standardDeduction, 50000);

// 12) ITR-1 eligibility: LTCG above 1.25L blocks
c = compute(base({ ltcg112a: { saleValue: 500000, costOfAcquisition: 300000 } }), ON_TIME);
eq("LTCG > 1.25L → ITR-2 warning", c.warnings.some((w) => w.level === "block" && /112A/.test(w.text)) ? 1 : 0, 1);

console.log(fail ? `\n${fail} FAILED` : "\nall passed");
process.exit(fail ? 1 : 0);
