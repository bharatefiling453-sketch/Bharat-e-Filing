// End-to-end test of the 5-step flow in Chromium.   node itr-self-filing/tests/e2e.mjs [--ocr]
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { readFileSync, mkdirSync } from "node:fs";
const site = new URL("../../", import.meta.url).pathname;
const fx = new URL("./fixtures/", import.meta.url).pathname;
const shots = process.env.SHOTS || "/tmp/itr-shots"; mkdirSync(shots, { recursive: true });
const OCR = process.argv.includes("--ocr");
const APP = process.env.APP_URL || "http://127.0.0.1:8765/itr-self-filing/"; // e.g. file:///…/dist/bef-itr1-self-filing.html
const srv = spawn("python3", ["-m", "http.server", "8765", "--bind", "127.0.0.1", "--directory", site], { stdio: "ignore" });
await new Promise((r) => setTimeout(r, 800));
let fail = 0; const ok = (name, cond, info = "") => { if (!cond) fail++; console.log(`${cond ? "✔" : "✖"} ${name} ${info}`); };
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 1360, height: 900 }, acceptDownloads: true });
const p = await ctx.newPage();
const errors = []; p.on("pageerror", (e) => errors.push(e.message)); p.on("console", (m) => m.type() === "error" && !/ERR_CERT|fonts\.g/.test(m.text() + (m.location()?.url || "")) && errors.push(m.text()));
p.on("dialog", (d) => d.accept());
try {
  await p.goto(APP);
  await p.evaluate(() => localStorage.clear()); await p.reload();
  // Step 1
  await p.fill("#pan", "abcps1234k"); await p.fill("#dob", "1990-05-10");
  await p.click('[data-action="verify-pan"]'); await p.waitForSelector("text=PAN verified");
  await p.click('[data-action="send-otp1"]'); await p.fill('[data-otp="1"]', "111111"); await p.click('[data-action="verify-otp1"]');
  await p.waitForSelector("text=Incorrect OTP"); ok("wrong OTP rejected", true);
  await p.fill('[data-otp="1"]', "123456"); await p.click('[data-action="verify-otp1"]'); await p.waitForSelector("text=authorised to file");
  await p.click('[data-action="send-otp2"]'); await p.fill('[data-otp="2"]', "123456"); await p.click('[data-action="verify-otp2"]');
  await p.waitForSelector("text=Imported from the Income Tax Department");
  await p.screenshot({ path: shots + "/1-pan.png", fullPage: true });
  await p.click('[data-action="next"]');
  // Step 2
  await p.setInputFiles("#f16-input", fx + (OCR ? "form16-scanned.pdf" : "form16-digital.pdf"));
  await p.waitForSelector(".f16", { timeout: OCR ? 240000 : 30000 });
  const allOk = await p.locator(".note-ok").count();
  const flagged = await p.locator("tr.is-flagged").count();
  ok(`Form 16 ${OCR ? "(OCR)" : "(digital)"} reconciled`, OCR ? true : allOk === 1, `flagged rows: ${flagged}`);
  if (OCR) {
    const vals = await p.$$eval("[data-f16]", (els) => Object.fromEntries(els.map((e) => [e.dataset.f16.split(".")[1], Number(e.value)])));
    const exp = { s17_1: 1420000, s17_2: 36000, gross: 1456000, stdDeduction: 75000, incomeSalary: 1381000, s80ccd2: 50000, totalIncome: 1331000, netTax: 82836 };
    for (const [k, v] of Object.entries(exp)) ok(`OCR ${k}`, vals[k] === v, `${vals[k]} vs ${v}`);
    for (const cb of await p.$$("[data-f16confirm]")) await cb.check();
  }
  await p.screenshot({ path: shots + "/2-form16.png", fullPage: true });
  await p.click('[data-action="apply-f16"]');
  await p.click('.actions-bar [data-action="next"]');
  // Step 3
  await p.waitForSelector("text=Review all your income");
  ok("salary from Form 16", (await p.textContent(".head:nth-of-type(1)")).includes("ACME SOFTWARE"));
  await p.click('[data-action="hp-modal"][data-i="new"]');
  await p.fill("#m-address", "Flat 4B, Baner, Pune"); await p.fill("#m-rent", "240000"); await p.fill("#m-municipalTax", "10000"); await p.fill("#m-interest", "100000");
  ok("HP live preview", (await p.textContent(".calc-line")).includes("61,000"));
  await p.screenshot({ path: shots + "/3b-hp-modal.png" });
  await p.click('[data-action="save-hp"]');
  await p.setInputFiles("#pnl-input", fx + "broker-tax-pnl-ltcg-only.xlsx");
  await p.waitForSelector("text=Broker Tax P&L");
  await p.screenshot({ path: shots + "/3c-pnl.png" });
  await p.click('[data-action="use-pnl"]');
  await p.click('[data-action="os-modal"]'); await p.fill("#m-payer", "NHAI bonds"); await p.fill("#m-amount", "5000"); await p.click('[data-action="save-os"]');
  // salary bifurcation popup with slip upload
  await p.click('[data-action="salary-modal"][data-i="0"]');
  await p.click('[data-action="mtab"][data-tab="slip"]');
  await p.setInputFiles("#slip-input", fx + "salary-slip.png");
  await p.waitForSelector('[data-action="apply-slip"]', { timeout: 180000 });
  const slipTxt = await p.textContent(".app-modal");
  ok("slip OCR read Basic 50,000", /50,000/.test(slipTxt));
  ok("slip OCR read HRA 25,000", /25,000/.test(slipTxt));
  await p.screenshot({ path: shots + "/3d-slip.png" });
  await p.click('[data-action="close-modal"]');
  await p.screenshot({ path: shots + "/3-income.png", fullPage: true });
  await p.click('.actions-bar [data-action="next"]');
  // Step 4
  await p.waitForSelector("text=Deductions, regime and taxes paid");
  await p.screenshot({ path: shots + "/4-deductions.png", fullPage: true });
  await p.click('.actions-bar [data-action="next"]');
  // Step 5
  await p.click('[data-action="create-computation"]');
  const c = await p.evaluate(() => window.__befItr.calc());
  ok("GTI 15,21,880", c.grossTotalIncome === 1521880, c.grossTotalIncome);
  ok("Total income 14,71,880", c.totalIncome === 1471880, c.totalIncome);
  ok("Net tax 98,960", c.tax.netTax === 98960, c.tax.netTax);
  ok("234A 408 / 234B 952 / 234C 685 / 234F 5,000", c.interest.i234A === 408 && c.interest.i234B === 952 && c.interest.i234C === 685 && c.lateFee === 5000, JSON.stringify(c.interest));
  ok("Balance payable 20,710", c.payable === 20710, c.payable);
  await p.screenshot({ path: shots + "/5-computation.png", fullPage: true });
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click('[data-action="download-pdf"]')]);
  const pdfPath = shots + "/" + dl.suggestedFilename(); await dl.saveAs(pdfPath);
  ok("computation PDF downloaded", readFileSync(pdfPath).subarray(0, 4).toString() === "%PDF", dl.suggestedFilename());
  const [dj] = await Promise.all([p.waitForEvent("download"), p.click('[data-action="download-json"]')]);
  const jsonPath = shots + "/" + dj.suggestedFilename(); await dj.saveAs(jsonPath);
  const j = JSON.parse(readFileSync(jsonPath, "utf8"));
  ok("ITR JSON total income", j.ITR.ITR1.ITR1_IncomeDeductions.TotalIncome === 1471880);
  // File now → pay first → add challan → file → e-verify
  await p.click('[data-action="file-now"]'); await p.waitForSelector("text=before filing");
  await p.click('[data-action="paid-add-challan"]'); await p.fill("#m-bsr", "0510308"); await p.fill("#m-challan", "12345"); await p.click('[data-action="save-challan"]');
  await p.click('[data-action="goto"][data-step="5"]');
  const c2 = await p.evaluate(() => window.__befItr.calc());
  ok("after challan: nothing payable", c2.payable === 0 && c2.refund === 0, JSON.stringify({ p: c2.payable, r: c2.refund }));
  await p.click('[data-action="file-now"]'); await p.check('[data-mbind="agree"]'); await p.fill("#m-place", "Pune"); await p.click('[data-action="submit-return"]');
  await p.waitForSelector('[data-otp="ev"]'); await p.fill('[data-otp="ev"]', "123456"); await p.click('[data-action="everify"]');
  await p.waitForSelector("text=Return filed and e-verified");
  await p.screenshot({ path: shots + "/6-filed.png", fullPage: true });
  ok("filed and e-verified", true);
  // mobile layout
  const m = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  await m.goto(APP);
  ok("no horizontal scroll on mobile", !(await m.evaluate(() => document.documentElement.scrollWidth > innerWidth)));
  await m.screenshot({ path: shots + "/m-1.png" });
} catch (e) { fail++; console.log("✖ exception:", e.message); await p.screenshot({ path: shots + "/error.png", fullPage: true }); }
ok("no JS errors", errors.length === 0, errors.join(" | "));
await b.close(); srv.kill();
console.log(fail ? `\n${fail} FAILED` : "\nall passed"); process.exit(fail ? 1 : 0);
