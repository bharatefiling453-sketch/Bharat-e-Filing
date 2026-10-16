// node itr-self-filing/tests/form16.test.mjs — reads the digital fixture with pdf.js (same text layer the browser sees)
import { getDocument } from "pdfjs-dist/legacy/build/pdf.mjs";
import { readFileSync } from "node:fs";
import { parseForm16, toModel } from "../src/form16.js";
import { compute } from "../src/tax.js";

const file = process.argv[2] || new URL("./fixtures/form16-digital.pdf", import.meta.url).pathname;
const doc = await getDocument({ data: new Uint8Array(readFileSync(file)), isEvalSupported: false }).promise;
const items = [];
for (let p = 1; p <= doc.numPages; p++) {
  const page = await doc.getPage(p), vp = page.getViewport({ scale: 1 });
  for (const it of (await page.getTextContent()).items) {
    const str = (it.str || "").trim(); if (!str) continue;
    const [, , c, d, e, f] = it.transform;
    items.push({ str, x: e, y: vp.height - f, w: it.width, h: Math.hypot(c, d), page: p, pageW: vp.width, conf: 100, ocr: false });
  }
}
const parsed = parseForm16(items, { pan: "ABCPS1234K" });
let fail = 0;
const expect = { s17_1: 1420000, s17_2: 36000, s17_3: 0, gross: 1456000, otherEmployer: 0, exemptTotal: 0, salaryCurrent: 1456000, stdDeduction: 75000, total16: 75000,
  incomeSalary: 1381000, gti: 1381000, s80ccd2: 50000, aggVIA: 50000, totalIncome: 1331000, taxOnIncome: 79650, cess: 3186, taxPayable: 82836, netTax: 82836 };
for (const [k, exp] of Object.entries(expect)) {
  const got = parsed.partB.fields[k]?.value;
  const ok = got === exp; if (!ok) fail++;
  console.log(`${ok ? "✔" : "✖"} ${k}: ${got} (expected ${exp})`);
}
const a = parsed.partA;
for (const [name, ok] of [["employer", a.employer === "ACME SOFTWARE PRIVATE LIMITED"], ["TAN", a.tan === "MUMA12345B"], ["AY", a.ay === "2026-27"], ["PAN found", a.pans.includes("ABCPS1234K")],
  ["Part A total TDS", a.totals?.taxDeducted === 82836], ["Part A amount paid", a.totals?.amountPaid === 1456000], ["optOut = No", parsed.partB.optOut === false],
  ["12BA total perquisites", parsed.form12BA?.totalPerquisites === 36000], ["12BA rows", (parsed.form12BA?.rows || []).filter((r) => r.chargeable > 0).length === 2]]) {
  if (!ok) fail++; console.log(`${ok ? "✔" : "✖"} ${name}`, name === "employer" ? a.employer : "");
}
console.log("cross-checks:", parsed.validation.checks.map((c) => `${c.ok ? "✔" : "✖"} ${c.text}`).join("\n  "));
console.log("flagged:", parsed.validation.flagged);
if (!parsed.validation.allOk) fail++;
const m = toModel(parsed);
const c = compute({ personal: { dob: "1990-05-10" }, salary: { employers: [m.employer] }, deductions: { ...m.deductions, basicPlusDA: 600000 }, otherSources: {}, houseProperties: [], taxes: {} }, { filingDate: "2026-07-20" });
const ok = c.totalIncome === 1331000 && c.tax.netTax === 82840 && c.balance === 0;
if (!ok) fail++;
console.log(`${ok ? "✔" : "✖"} engine from Form 16: TI ${c.totalIncome}, tax ${c.tax.netTax}, TDS ${c.paid.tdsSalary}, balance ${c.balance}`);
console.log(fail ? `\n${fail} FAILED` : "\nall passed");
process.exit(fail ? 1 : 0);
