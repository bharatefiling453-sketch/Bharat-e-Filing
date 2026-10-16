// Form 16 (Part A + Part B, Rule 31(1)(a)) and Form 12BA reader.
// Works on positioned text items from pdftext.js (text layer or OCR). Pure functions — no DOM.
// Accuracy rule: every value is cross-checked against the form's own arithmetic, Part A, Form 12BA and the
// taxpayer's PAN / AY. Anything that does not reconcile, or came from OCR with low confidence, is flagged
// for the user to confirm before it is used.
import { toLines, normalize, amountsRightOf, parseAmount } from "./pdftext.js";

const PAN_RE = /\b[A-Z]{5}[0-9]{4}[A-Z]\b/g;
const TAN_RE = /\b[A-Z]{4}[0-9]{5}[A-Z]\b/g;

// Part B fields in form order. `re` is tested on the normalised text of one line, or of two joined lines.
export const PART_B_FIELDS = [
  ["s17_1", "1(a) Salary as per section 17(1)", /salary as per provisions contained in section 17\(1\)/],
  ["s17_2", "1(b) Value of perquisites u/s 17(2)", /value of perquisites under section 17\(2\)/],
  ["s17_3", "1(c) Profits in lieu of salary u/s 17(3)", /profits in lieu of salary under section 17\(3\)/],
  ["gross", "1(d) Total gross salary", /^\(d\)\s*total$|^1\(d\)\s*total$|^\(d\)\s*total\b(?!.*(amount|deduction|income))/, { after: "s17_3" }],
  ["otherEmployer", "1(e) Salary from other employer(s)", /reported total amount of salary received from other employer/],
  ["lta", "2(a) Leave travel concession 10(5)", /travel concession or assistance under section 10\(5\)/],
  ["gratuity", "2(b) Gratuity 10(10)", /death-?cum-?retirement gratuity under section 10\(10\)/],
  ["commutedPension", "2(c) Commuted pension 10(10A)", /commuted value of pension under section 10\(10a\)/],
  ["leaveEncashment", "2(d) Leave encashment 10(10AA)", /cash equivalent of leave salary encashment/],
  ["hra", "2(e) House rent allowance 10(13A)", /house rent allowance under section 10\(13a\)/],
  ["special10_14", "2(f) Special allowances 10(14)", /other special allowances under section 10\(14\)/],
  ["otherExempt", "2(g) Any other exemption u/s 10", /^(\(g\)\s*)?amount of any other exemption under section 10/],
  ["otherExemptTotal", "2(h) Total of any other exemption u/s 10", /total amount of any other exemption under section 10/],
  ["exemptTotal", "2(i) Total exemption u/s 10", /total amount of exemption claimed under section 10/],
  ["salaryCurrent", "3. Salary from current employer", /total amount of salary received from current employer/],
  ["stdDeduction", "4(a) Standard deduction 16(ia)", /standard deduction under section 16\(ia\)/],
  ["entAllow", "4(b) Entertainment allowance 16(ii)", /entertainment allowance under section 16\(ii\)/],
  ["profTax", "4(c) Professional tax 16(iii)", /tax on employment under section 16\(iii\)/],
  ["total16", "5. Total deductions u/s 16", /total amount of deductions under section 16/],
  ["incomeSalary", "6. Income chargeable under Salaries", /income chargeable under the head salaries/],
  ["hpReported", "7(a) House property reported for TDS", /income\(or admissible loss\) from house property/],
  ["osReported", "7(b) Other sources reported for TDS", /income under the head other sources offered for tds/],
  ["otherReported", "8. Total other income reported", /total amount of other income reported by the employee/],
  ["gti", "9. Gross total income", /gross total income/],
  ["s80c", "10(a) 80C", /life insurance premia.*80c\b/],
  ["s80ccc", "10(b) 80CCC", /contribution to certain pension funds under section 80ccc/],
  ["s80ccd1", "10(c) 80CCD(1)", /contribution by taxpayer to pension scheme under section 80ccd\(1\)/],
  ["total80c", "10(d) Total of 80C, 80CCC, 80CCD(1)", /total deduction under section 80c,?\s*80ccc and 80ccd\(1\)/],
  ["s80ccd1b", "10(e) 80CCD(1B)", /80ccd\(1b\)/],
  ["s80ccd2", "10(f) 80CCD(2) employer NPS", /contribution by employer to pension scheme under section 80ccd\(2\)/],
  ["s80d", "10(g) 80D", /health insurance premia under section 80d/],
  ["s80e", "10(h) 80E", /loan taken for higher\s*education/],
  ["s80cchEmp", "10(i) 80CCH employee", /contribution by the employee to agnipath/],
  ["s80cchGov", "10(j) 80CCH Government", /contribution by the central government to agnipath/],
  ["s80g", "10(k) 80G", /donations to certain funds/],
  ["s80tta", "10(l) 80TTA", /interest on deposits in savings account under section 80tta/],
  ["otherVIA", "10(m) Other Chapter VI-A", /^(\(m\)\s*)?amount deductible under any other provision/],
  ["otherVIATotal", "10(n) Total other Chapter VI-A", /total of amount deductible under any other provision/],
  ["aggVIA", "11. Aggregate Chapter VI-A", /aggregate of deductible amount under chapter vi-?a/],
  ["totalIncome", "12. Total taxable income", /total taxable income/],
  ["taxOnIncome", "13. Tax on total income", /tax on total income/],
  ["rebate87A", "14. Rebate u/s 87A", /rebate under section 87a/],
  ["surcharge", "15. Surcharge", /surcharge,?\s*wherever applicable/],
  ["cess", "16. Health and education cess", /health and education cess/],
  ["taxPayable", "17. Tax payable", /tax payable\(13\+15\+16-14\)|^17\.?\s*tax payable/],
  ["relief89", "18. Relief u/s 89", /relief under section 89/],
  ["tds192_2B", "19. TDS as per Form 12BAA (other income)", /tax deducted at source as per form no\.?\s*12baa/],
  ["tcs192_2B", "20. TCS as per Form 12BAA", /tax collected at source as per form no\.?\s*12baa/],
  ["netTax", "21. Net tax payable", /net tax payable/],
];

const ITEM_START = /^[({\[|]?\s*(\d{1,2}[.,]|\d{1,2}\s|[a-n][a-z]?[)}\]]|[ivx]{1,4}[)}\]])/; // tolerant of OCR misreads like {f) or 4,
const amountOnly = (line) => line.items.every((it) => parseAmount(it.str) !== null || /^(rs\.?|₹)$/i.test(it.str));

/** Finds a label that may wrap over up to 3 lines (amount-only lines in between are skipped). */
function findLine(lines, re, startIdx = 0, endIdx = lines.length) {
  // pass 1: whole label on one line
  for (let i = startIdx; i < endIdx; i++) {
    if (!(re.test(lines[i].labelNorm) || re.test(lines[i].norm))) continue;
    // a continuation line (no item marker, no amount) belongs to the item that started on an earlier line
    const used = [i];
    if (!ITEM_START.test(lines[i].labelNorm) && !amountsRightOf(lines[i], 0, { minFrac: 0.45 }).length) {
      for (let k = i - 1; k >= Math.max(0, i - 3) && lines[k].page === lines[i].page; k--) {
        used.unshift(k);
        if (ITEM_START.test(lines[k].labelNorm)) break;
      }
    }
    return { i: used[0], used };
  }
  // pass 2: label wrapped onto following lines of the same item
  for (let i = startIdx; i < endIdx; i++) {
    if (amountOnly(lines[i])) continue;
    let text = lines[i].labelNorm;
    const used = [i];
    for (let j = i + 1; j < Math.min(lines.length, i + 5) && used.length < 4; j++) {
      const l = lines[j];
      if (l.page !== lines[i].page) break;
      used.push(j);
      if (amountOnly(l)) continue;
      if (ITEM_START.test(l.labelNorm)) break; // the next item starts: the match would belong to it
      text = normalize(text + " " + l.labelNorm);
      if (re.test(text)) return { i, used };
    }
  }
  return null;
}

function labelEndX(line) {
  let end = 0;
  for (const it of line.items) if (parseAmount(it.str) === null) end = Math.max(end, it.x + (it.w || 0));
  return end;
}

function valueFor(lines, hit) {
  // amounts on the label's own lines (rightmost wins: it is the outer/total column)
  const found = [];
  for (const k of hit.used) {
    const line = lines[k];
    const am = amountOnly(line) ? amountsRightOf(line, 0, { minFrac: 0.45 }) : amountsRightOf(line, labelEndX(line) - 2);
    found.push(...am);
  }
  if (found.length) return { value: found[found.length - 1].v, items: found.map((a) => a.item) };
  // otherwise the amount may sit on the next line(s), as long as no new item has started
  const last = hit.used[hit.used.length - 1];
  for (let k = last + 1; k <= last + 2; k++) {
    const line = lines[k];
    if (!line || line.page !== lines[hit.i].page) break;
    if (!amountOnly(line) && ITEM_START.test(line.norm)) break;
    const am = amountsRightOf(line, 0, { minFrac: 0.45 });
    if (am.length) return { value: am[am.length - 1].v, items: am.map((a) => a.item) };
  }
  return null;
}

function partBStart(lines) {
  const i = lines.findIndex((l) => /part b|details of salary paid and any other income and tax deducted/.test(l.norm));
  return i < 0 ? 0 : i;
}

function readPartB(lines) {
  const out = {};
  const pos = {};
  const start = partBStart(lines);
  for (const [key, label, re, opt] of PART_B_FIELDS) {
    const from = opt?.after && pos[opt.after] !== undefined ? pos[opt.after] + 1 : start;
    const to = opt?.after ? Math.min(lines.length, from + 4) : lines.length;
    const hit = findLine(lines, re, from, to);
    if (!hit) { out[key] = { key, label, value: null, found: false }; continue; }
    pos[key] = hit.i;
    const v = valueFor(lines, hit);
    const conf = v ? Math.min(...v.items.map((it) => it.conf ?? 100)) : 100;
    out[key] = { key, label, value: v ? v.value : 0, found: true, valueFound: !!v, ocr: v ? v.items.some((it) => it.ocr) : false, conf, page: lines[hit.i].page };
  }
  // A: opting out of the new regime?
  const optHit = findLine(lines, /whether opting out of taxation u\/s 115bac/, 0, lines.length);
  let optOut = null;
  if (optHit) {
    const last = optHit.used[optHit.used.length - 1];
    const txt = lines.slice(last, last + 2).map((l) => l.norm).join(" ");
    optOut = /\byes\b/.test(txt) ? true : /\bno\b/.test(txt) ? false : null;
  }
  return { fields: out, optOut };
}

function readPartA(lines, items) {
  const all = items.map((i) => i.str).join(" ");
  const pans = [...new Set(all.match(PAN_RE) || [])];
  const tans = [...new Set(all.match(TAN_RE) || [])].filter((t) => !pans.includes(t));
  const ayLine = lines.find((l) => /assessment year/.test(l.norm));
  const ayAll = all.match(/20\d{2}-\d{2}/g) || [];
  const ay = (ayLine && (ayLine.text.match(/20\d{2}-\d{2}/) || [])[0]) || ayAll.find((a) => a === "2026-27") || ayAll[0] || null;
  // employer name: first line below the "Name and address of the Employer" header, left column
  let employer = null;
  const hi = lines.findIndex((l) => /name and address of the employer/.test(l.norm));
  if (hi >= 0) {
    const header = lines[hi];
    const empHdr = header.items.find((i) => /employee|specified senior/i.test(i.str));
    const erHdr = header.items.find((i) => /employer/i.test(i.str) && !/employee/i.test(i.str));
    const mid = empHdr ? (erHdr ? (erHdr.x + empHdr.x) / 2 : empHdr.x - 15) : (header.pageW || 600) / 2;
    for (let k = hi + 1; k < Math.min(lines.length, hi + 5); k++) {
      const left = lines[k].items.filter((i) => i.x < mid).map((i) => i.str).join(" ").trim();
      if (left && !/name and address|employee|pan|tan/i.test(left)) { employer = left; break; }
    }
  }
  // quarterly summary: the "Total (Rs.)" row → [amount paid/credited, tax deducted, tax deposited]
  let totals = null;
  const tl = lines.find((l) => /^total\s*\(rs\.?\)/.test(l.norm) && amountsRightOf(l, 0, { minFrac: 0.2 }).length >= 2);
  if (tl) {
    const am = amountsRightOf(tl, 0, { minFrac: 0.2 }).map((a) => a.v);
    totals = { amountPaid: am[0] ?? null, taxDeducted: am[1] ?? null, taxDeposited: am[2] ?? am[1] ?? null };
  }
  const period = (all.match(/(\d{2}-[A-Za-z]{3}-\d{4})/g) || []).slice(0, 2);
  return { pans, tans, tan: tans[0] || null, ay, employer, totals, period };
}

function read12BA(lines) {
  const i = lines.findIndex((l) => /^form no\.?\s*12ba$/.test(l.norm));
  if (i < 0) return null;
  const rows = [];
  let totalPerq = null, total173 = null;
  for (let k = i; k < lines.length; k++) {
    const l = lines[k];
    if (k > i && /form no\.?\s*16\b|part a\b/.test(l.norm)) break;
    const am = amountsRightOf(l, 0, { minFrac: 0.45 });
    if (/total value of perquisites/.test(l.norm) && am.length) totalPerq = am[am.length - 1].v;
    else if (/total value of profits in lieu of salary/.test(l.norm) && am.length) total173 = am[am.length - 1].v;
    else {
      const m = l.text.match(/^(\d{1,2})\.?\s+(.+?)$/);
      if (m && am.length && Number(m[1]) <= 20) {
        const label = l.items.filter((it) => parseAmount(it.str) === null).map((it) => it.str).join(" ").replace(/^\d{1,2}\.?\s*/, "");
        rows.push({ no: Number(m[1]), label, chargeable: am[am.length - 1].v });
      }
    }
  }
  return { rows, totalPerquisites: totalPerq, total17_3: total173 };
}

const near = (a, b, tol = 1) => Math.abs((a || 0) - (b || 0)) <= tol;
const v = (f, k) => (f[k] && f[k].value) || 0;

export function crossCheck(parsed, ctx = {}) {
  const f = parsed.partB.fields;
  const checks = [];
  const add = (ok, text, keys) => checks.push({ ok, text, keys });
  add(near(v(f, "gross"), v(f, "s17_1") + v(f, "s17_2") + v(f, "s17_3")), "1(d) = 1(a) + 1(b) + 1(c)", ["gross", "s17_1", "s17_2", "s17_3"]);
  add(near(v(f, "exemptTotal"), v(f, "lta") + v(f, "gratuity") + v(f, "commutedPension") + v(f, "leaveEncashment") + v(f, "hra") + v(f, "special10_14") + v(f, "otherExemptTotal")),
    "2(i) = 2(a) + … + 2(f) + 2(h)", ["exemptTotal", "lta", "gratuity", "commutedPension", "leaveEncashment", "hra", "special10_14", "otherExemptTotal"]);
  add(near(v(f, "salaryCurrent"), v(f, "gross") - v(f, "exemptTotal")), "3 = 1(d) − 2(i)", ["salaryCurrent", "gross", "exemptTotal"]);
  add(near(v(f, "total16"), v(f, "stdDeduction") + v(f, "entAllow") + v(f, "profTax")), "5 = 4(a) + 4(b) + 4(c)", ["total16", "stdDeduction", "entAllow", "profTax"]);
  add(near(v(f, "incomeSalary"), v(f, "salaryCurrent") + v(f, "otherEmployer") - v(f, "total16")), "6 = 3 + 1(e) − 5", ["incomeSalary", "salaryCurrent", "otherEmployer", "total16"]);
  add(near(v(f, "otherReported"), v(f, "hpReported") + v(f, "osReported")), "8 = 7(a) + 7(b)", ["otherReported", "hpReported", "osReported"]);
  add(near(v(f, "gti"), v(f, "incomeSalary") + v(f, "otherReported")), "9 = 6 + 8", ["gti", "incomeSalary", "otherReported"]);
  add(near(v(f, "total80c"), v(f, "s80c") + v(f, "s80ccc") + v(f, "s80ccd1")), "10(d) = 10(a) + 10(b) + 10(c)", ["total80c", "s80c", "s80ccc", "s80ccd1"]);
  const via = ["total80c", "s80ccd1b", "s80ccd2", "s80d", "s80e", "s80cchEmp", "s80cchGov", "s80g", "s80tta", "otherVIATotal"].reduce((a, k) => a + v(f, k), 0);
  add(near(v(f, "aggVIA"), via), "11 = sum of Chapter VI-A items", ["aggVIA"]);
  add(near(v(f, "totalIncome"), v(f, "gti") - v(f, "aggVIA"), 10), "12 = 9 − 11 (rounded to ₹10)", ["totalIncome", "gti", "aggVIA"]);
  add(near(v(f, "taxPayable"), v(f, "taxOnIncome") + v(f, "surcharge") + v(f, "cess") - v(f, "rebate87A"), 2), "17 = 13 + 15 + 16 − 14", ["taxPayable", "taxOnIncome", "surcharge", "cess", "rebate87A"]);
  add(near(v(f, "netTax"), v(f, "taxPayable") - v(f, "relief89") - v(f, "tds192_2B") - v(f, "tcs192_2B"), 2), "21 = 17 − 18 − 19 − 20", ["netTax", "taxPayable", "relief89", "tds192_2B", "tcs192_2B"]);
  const a = parsed.partA;
  if (a.totals?.taxDeducted != null) add(near(a.totals.taxDeducted, v(f, "netTax"), 10), "Part A total tax deducted = Part B net tax payable", ["netTax"]);
  if (a.totals?.amountPaid != null) add(near(a.totals.amountPaid, v(f, "gross"), 10) || near(a.totals.amountPaid, v(f, "salaryCurrent"), 10), "Part A amount paid matches Part B salary", ["gross"]);
  if (parsed.form12BA?.totalPerquisites != null) add(near(parsed.form12BA.totalPerquisites, v(f, "s17_2")), "Form 12BA perquisites = Part B 1(b)", ["s17_2"]);
  if (parsed.form12BA?.total17_3 != null) add(near(parsed.form12BA.total17_3, v(f, "s17_3")), "Form 12BA profits in lieu = Part B 1(c)", ["s17_3"]);
  const std = v(f, "stdDeduction");
  if (std) add(std === 75000 || std === 50000 || std < 50000, "Standard deduction is ₹75,000 (new) or ₹50,000 (old)", ["stdDeduction"]);
  if (ctx.pan) add(a.pans.includes(ctx.pan.toUpperCase()), `Employee PAN ${ctx.pan.toUpperCase()} appears on the Form 16`, []);
  add(a.ay === "2026-27", `Assessment year is 2026-27 (found ${a.ay || "none"})`, []);
  // values that failed a check, or OCR values below 90% confidence, need the user's confirmation
  const flagged = new Set();
  checks.filter((c) => !c.ok).forEach((c) => c.keys.forEach((k) => flagged.add(k)));
  Object.values(f).forEach((x) => { if (x.ocr && x.conf < 90) flagged.add(x.key); });
  const required = ["s17_1", "gross", "salaryCurrent", "incomeSalary", "netTax"];
  required.forEach((k) => { if (!f[k]?.found) flagged.add(k); });
  return { checks, flagged: [...flagged], allOk: checks.every((c) => c.ok) && flagged.size === 0 };
}

export function parseForm16(items, ctx = {}) {
  const lines = toLines(items);
  const partA = readPartA(lines, items);
  const partB = readPartB(lines);
  const form12BA = read12BA(lines);
  const parsed = { partA, partB, form12BA, source: items.some((i) => i.ocr) ? "ocr" : "text", lineCount: lines.length };
  parsed.validation = crossCheck(parsed, ctx);
  return parsed;
}

/** Maps a parsed (and user-confirmed) Form 16 to the app's employer + deduction model. */
export function toModel(parsed) {
  const f = parsed.partB.fields;
  const g = (k) => (f[k] && f[k].value) || 0;
  return {
    employer: {
      name: parsed.partA.employer || "Employer",
      tan: parsed.partA.tan || "",
      s17_1: g("s17_1"), s17_2: g("s17_2"), s17_3: g("s17_3"),
      exemptions: { lta: g("lta"), gratuity: g("gratuity"), commutedPension: g("commutedPension"), leaveEncashment: g("leaveEncashment"), hra: g("hra"), special10_14: g("special10_14"), other: g("otherExemptTotal") },
      entAllow: g("entAllow"), profTax: g("profTax"),
      tds: parsed.partA.totals?.taxDeducted ?? g("netTax"),
      source: "form16",
      perquisites: parsed.form12BA?.rows || [],
    },
    deductions: {
      s80c: g("s80c"), s80ccc: g("s80ccc"), s80ccd1: g("s80ccd1"), s80ccd1b: g("s80ccd1b"), s80ccd2: g("s80ccd2"),
      s80dSelf: g("s80d"), s80e: g("s80e"), s80cch: g("s80cchEmp") + g("s80cchGov"), s80g: g("s80g"),
    },
    otherEmployerSalary: g("otherEmployer"),
    reportedToEmployer: { houseProperty: g("hpReported"), otherSources: g("osReported") },
    optOutNewRegime: parsed.partB.optOut,
    relief89: g("relief89"),
  };
}
