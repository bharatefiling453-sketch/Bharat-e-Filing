// Bharat e-Filing — ITR-1 self-filing app (5 steps). Vanilla JS, no framework.
import * as api from "./api.js";
import { compute, compareRegimes, DUE_DATE, ageCategory, n } from "./tax.js";
import { extractItems, toLines, OCR_OPTS } from "./pdftext.js";
import { parseForm16, toModel } from "./form16.js";
import { parsePnl, readWorkbook } from "./pnl.js";
import { parseSlip } from "./slip.js";
import { computationRows, downloadComputationPdf } from "./report.js";
import { buildItr1Json } from "./itrjson.js";

// ------------------------------------------------------------------ state
const KEY = "bef-itr1-draft-v1";
const blank = () => ({
  step: 1,
  personal: { pan: "", dob: "", name: "", mobile: "", email: "", address: "", aadhaar: "" },
  onboarding: { panVerified: false, otp1: {}, otp2: {}, imported: false },
  eligibility: {},
  bankAccounts: [],
  prefill: null,
  salary: { employers: [] },
  form16s: [],
  noForm16: false,
  houseProperties: [],
  ltcg112a: { saleValue: 0, costOfAcquisition: 0, stcg: 0, otherCG: false, source: "" },
  otherSources: { savingsInterest: 0, depositInterest: 0, refundInterest: 0, dividend: 0, familyPension: 0, others: [] },
  exemptIncome: { agriculture: 0 },
  deductions: {},
  regime: "new",
  taxes: { tdsOther: [], tcs: [], advance: [], selfAssessment: [], relief89: 0 },
  computed: false,
  filing: {},
});
let S = load() || blank();
function load() { try { return JSON.parse(localStorage.getItem(KEY)); } catch { return null; } }
function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch {} }
const today = () => new Date().toISOString().slice(0, 10);
const track = (event, p = {}) => (window.dataLayer = window.dataLayer || []).push({ event, ...p });

// ------------------------------------------------------------------ helpers
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const inr = (v) => { const x = Math.round(Number(v) || 0); return (x < 0 ? "−₹" : "₹") + Math.abs(x).toLocaleString("en-IN"); };
const uid = () => Math.random().toString(36).slice(2, 9);
const get = (obj, path) => path.split(".").reduce((o, k) => (o == null ? o : o[k]), obj);
function set(obj, path, val) { const ks = path.split("."); const last = ks.pop(); const t = ks.reduce((o, k) => (o[k] ??= /^\d+$/.test(k) ? [] : {}), obj); t[last] = val; }
const $ = (sel, root = document) => root.querySelector(sel);
const sumArr = (arr, k) => (arr || []).reduce((a, x) => a + n(x[k]), 0);

function data() {
  return { personal: S.personal, salary: S.salary, houseProperties: S.houseProperties, ltcg112a: S.ltcg112a, otherSources: S.otherSources, exemptIncome: S.exemptIncome,
    deductions: S.deductions, regime: S.regime, taxes: S.taxes, eligibility: S.eligibility, bankAccounts: S.bankAccounts };
}
const calc = () => compute(data(), { filingDate: today() });
const isBelated = () => today() > DUE_DATE;

function field(label, path, { type = "number", hint = "", disabled = false, attrs = "", value, help = "" } = {}) {
  const v = value !== undefined ? value : get(S, path);
  const id = "f-" + path.replace(/[^a-z0-9]/gi, "-");
  return `<div class="field"><label for="${id}">${label}${help ? ` <span class="hint-i" title="${esc(help)}">ⓘ</span>` : ""}</label>
    <input id="${id}" ${type === "number" ? 'type="number" inputmode="decimal" min="0" step="1"' : `type="${type}"`} data-bind="${path}" data-type="${type}" value="${esc(v ?? "")}" ${disabled ? "disabled" : ""} ${attrs}>
    ${hint ? `<p class="field-hint">${hint}</p>` : ""}</div>`;
}
const rupee = (s) => String(s || "").replace(/^-Rs\. /, "−₹").replace(/^Rs\. /, "₹");
const chip = (t, cls = "") => `<span class="chip ${cls}">${t}</span>`;

let toastTimer;
function toast(msg) {
  let el = document.getElementById("toast");
  if (!el) { el = Object.assign(document.createElement("div"), { id: "toast", className: "toast" }); el.setAttribute("role", "status"); document.body.appendChild(el); }
  el.textContent = msg; el.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => (el.hidden = true), 4500);
}

// ------------------------------------------------------------------ shell
const STEPS = ["PAN & consent", "Form 16", "Income", "Deductions & taxes", "Computation & file"];
const root = document.getElementById("app");

function render() {
  save();
  root.innerHTML = `
    <ol class="app-steps" aria-label="Filing steps">${STEPS.map((t, i) => `<li class="${S.step === i + 1 ? "is-current" : S.step > i + 1 ? "is-done" : ""}">
      <button type="button" data-action="goto" data-step="${i + 1}" ${canGo(i + 1) ? "" : "disabled"} ${S.step === i + 1 ? 'aria-current="step"' : ""}><span class="app-steps__n">${S.step > i + 1 ? "✓" : i + 1}</span><span class="app-steps__t">${t}</span></button></li>`).join("")}</ol>
    <div class="layout">
      <section class="panel" aria-live="polite">${[step1, step2, step3, step4, step5][S.step - 1]()}</section>
      <aside class="summary" id="summary">${summary()}</aside>
    </div>`;
  track("itr_step_view", { step: S.step });
}
function canGo(step) {
  if (step <= S.step) return true;
  if (step >= 2 && !(S.onboarding.otp1.verified && S.onboarding.imported)) return false;
  if (step >= 3 && !S.salary.employers.length && !S.noForm16) return false;
  return true;
}
function refreshSummary() { const el = $("#summary"); if (el) el.innerHTML = summary(); const live = $("[data-live]"); if (live) live.outerHTML = liveBlocks(); save(); }

function summary() {
  if (!S.onboarding.imported) return `<div class="sum-card"><p class="sum-k">ITR-1 · AY 2026-27</p><p class="sum-muted">Your tax summary appears here once your data is imported.</p>${belatedNote()}</div>`;
  const c = calc();
  const refund = c.refund > 0, pay = c.payable > 0;
  return `<div class="sum-card">
    <p class="sum-k">ITR-1 · AY 2026-27 · ${c.meta.regime === "new" ? "New regime" : "Old regime"}</p>
    <dl class="sum-rows">
      <div><dt>Gross total income</dt><dd>${inr(c.grossTotalIncome)}</dd></div>
      <div><dt>Deductions</dt><dd>${inr(-c.deductions.total)}</dd></div>
      <div><dt>Total income</dt><dd>${inr(c.totalIncome)}</dd></div>
      <div><dt>Tax + cess</dt><dd>${inr(c.tax.netTax)}</dd></div>
      ${c.interest.i234A + c.interest.i234B + c.interest.i234C + c.lateFee ? `<div><dt>Interest & late fee</dt><dd>${inr(c.interest.i234A + c.interest.i234B + c.interest.i234C + c.lateFee)}</dd></div>` : ""}
      <div><dt>Taxes paid (TDS etc.)</dt><dd>${inr(-c.paid.total)}</dd></div>
    </dl>
    <div class="sum-result ${refund ? "is-refund" : pay ? "is-pay" : ""}"><span>${refund ? "Refund due" : pay ? "Tax payable" : "Nothing to pay"}</span><strong>${inr(c.refund || c.payable || 0)}</strong></div>
    ${c.warnings.filter((w) => w.level === "block").length ? `<p class="sum-warn">⚠ ${c.warnings.filter((w) => w.level === "block").length} issue(s) to fix before filing</p>` : ""}
    ${belatedNote()}
  </div>
  <div class="sum-help"><p><strong>Stuck?</strong> Hand your draft to a CA. Nothing to re-upload.</p><a class="btn btn--ghost btn--sm btn--block" href="https://bharatefiling.com/income-tax-return-filing/#expert" target="_blank" rel="noopener" data-track="cta_click" data-location="app-ca-help">Get CA help</a></div>`;
}
function belatedNote() {
  return isBelated() ? `<p class="sum-note">Filing after 31 July 2026 is a belated return (s.139(4)), allowed until 31 December 2026, with a late fee and only under the new regime.</p>` : "";
}

// ------------------------------------------------------------------ step 1: PAN + 2 OTPs + import
function step1() {
  const o = S.onboarding, p = S.personal;
  const otpBlock = (n, title, desc, st, sendAction, verifyAction, doneText) => `
    <div class="otp ${st.verified ? "is-done" : ""} ${!o.panVerified || (n === 2 && !o.otp1.verified) ? "is-locked" : ""}">
      <div class="otp__head"><span class="otp__n">${st.verified ? "✓" : n}</span><div><h3>${title}</h3><p>${desc}</p></div></div>
      ${st.verified ? `<p class="ok-line">${doneText}</p>` : `
        <div class="otp__row">
          <button class="btn btn--ghost btn--sm" type="button" data-action="${sendAction}" ${!o.panVerified || (n === 2 && !o.otp1.verified) ? "disabled" : ""}>${st.sent ? "Resend OTP" : "Send Aadhaar OTP"}</button>
          ${st.sent ? `<input class="otp__input" inputmode="numeric" maxlength="6" autocomplete="one-time-code" aria-label="OTP ${n}" data-otp="${n}" placeholder="6-digit OTP">
          <button class="btn btn--brand btn--sm" type="button" data-action="${verifyAction}">Verify</button>` : ""}
        </div>${st.sent ? `<p class="field-hint">Sent to the mobile linked with Aadhaar ${esc(o.mobileMasked || "")}${api.DEMO ? " · Demo OTP: 123456" : ""}</p>` : ""}
        ${st.error ? `<p class="err">${esc(st.error)}</p>` : ""}`}
    </div>`;
  return `
    <header class="panel__head"><p class="kicker">Step 1 of 5</p><h1>Start with your PAN</h1>
      <p class="lede-s">We confirm your PAN, add Bharat e-Filing as your authorised e-Return Intermediary with your consent, and import your pre-filled data, AIS, TIS and Form 26AS.</p></header>
    <div class="grid2">
      <div class="field"><label for="pan">PAN</label><input id="pan" data-bind="personal.pan" data-type="pan" value="${esc(p.pan)}" maxlength="10" autocomplete="off" placeholder="ABCPS1234K" ${o.panVerified ? "disabled" : ""} style="text-transform:uppercase"></div>
      <div class="field"><label for="dob">Date of birth</label><input id="dob" type="date" data-bind="personal.dob" data-type="text" value="${esc(p.dob)}" ${o.panVerified ? "disabled" : ""}></div>
    </div>
    ${o.panVerified ? `<p class="ok-line">✓ PAN verified: <strong>${esc(p.name)}</strong> · Aadhaar linked (${esc(o.aadhaarMasked || "")}) <button class="linkbtn" type="button" data-action="change-pan">Change</button></p>`
      : `<button class="btn btn--brand" type="button" data-action="verify-pan">Verify PAN</button>${o.panError ? `<p class="err">${esc(o.panError)}</p>` : ""}`}
    ${otpBlock(1, "Authorise Bharat e-Filing (client onboarding)", "OTP 1 adds us as your e-Return Intermediary on the income-tax portal. You can remove access anytime.", o.otp1, "send-otp1", "verify-otp1", "Bharat e-Filing is authorised to file for you.")}
    ${otpBlock(2, "Import pre-filled data, AIS, TIS and Form 26AS", "OTP 2 is your consent to fetch your income and tax data for AY 2026-27 from the Income Tax Department.", o.otp2, "send-otp2", "verify-otp2", "Imported: personal details, bank accounts, Form 26AS and AIS.")}
    ${o.imported ? importedSummary() : ""}
    <details class="elig" ${Object.values(S.eligibility).some(Boolean) ? "open" : ""}><summary>ITR-1 check: tick anything that applies to you</summary>
      <div class="checks2">${[["director", "I was a director in a company"], ["unlistedShares", "I held unlisted equity shares"], ["foreignAssets", "I have foreign assets or foreign income"], ["nonResident", "I am a non-resident / RNOR"], ["business", "I have business or professional income"], ["lottery", "I won lotteries, races or online games"], ["esopDeferred", "Tax on start-up ESOPs was deferred"], ["tds194N", "TDS was deducted u/s 194N (cash withdrawal)"]]
        .map(([k, t]) => `<label class="check"><input type="checkbox" data-bind="eligibility.${k}" data-type="bool" ${S.eligibility[k] ? "checked" : ""}> ${t}</label>`).join("")}</div>
      <p class="field-hint">Any tick means ITR-1 is not the right form. Our CA team can file the correct return for you.</p></details>
    <div class="actions-bar"><span></span><button class="btn btn--brand" type="button" data-action="next" ${canGo(2) ? "" : "disabled"}>Continue to Form 16 →</button></div>`;
}
function importedSummary() {
  const pf = S.prefill || {};
  const ais = pf.ais || {};
  const cnt = Object.values(ais).reduce((a, arr) => a + (arr?.length || 0), 0);
  return `<div class="imported"><h3>Imported from the Income Tax Department</h3><ul>
    <li>${chip("Pre-fill")} ${esc(pf.personal?.name)} · DOB ${esc(pf.personal?.dob)} · ${esc(pf.personal?.address)}</li>
    <li>${chip("Bank")} ${(pf.bankAccounts || []).length} pre-validated account(s)</li>
    <li>${chip("26AS")} TDS on salary from ${(pf.tdsSalary || []).map((t) => esc(t.employer)).join(", ") || "—"} · TDS on other income: ${(pf.tdsOther || []).length} entr${(pf.tdsOther || []).length === 1 ? "y" : "ies"}</li>
    <li>${chip("AIS / TIS")} ${cnt} income item(s): salary, interest, dividend, securities sold</li></ul></div>`;
}

// ------------------------------------------------------------------ step 2: Form 16
function step2() {
  return `
    <header class="panel__head"><p class="kicker">Step 2 of 5</p><h1>Upload your Form 16</h1>
      <p class="lede-s">We read Part A, Part B and Form 12BA directly from the PDF and check every total. If you changed jobs, upload each employer's Form 16.</p></header>
    <label class="drop" for="f16-input" data-drop="form16">
      <input id="f16-input" type="file" accept="application/pdf,image/*" multiple data-upload="form16" hidden>
      <span class="drop__icon" aria-hidden="true">📄</span><strong>Upload Form 16 (PDF)</strong><span>Drag and drop, or click to choose. Digital PDFs from TRACES are read exactly; scanned copies and photos use OCR and every value is shown for you to confirm.</span>
    </label>
    ${api.DEMO ? `<p class="samples">Demo: <button type="button" class="linkbtn" data-action="sample" data-kind="form16" data-file="sample-form16.pdf">try a sample Form 16</button> · <button type="button" class="linkbtn" data-action="sample" data-kind="form16" data-file="sample-form16-scanned.pdf">a scanned one (OCR)</button></p>` : ""}
    <p class="no-f16">Don't have Form 16? <button type="button" class="linkbtn" data-action="no-form16">Click here to enter your salary manually</button></p>
    ${S._needPw ? `<div class="field" style="max-width:320px"><label for="f16-pw">Form 16 password</label><input id="f16-pw" type="text" autocomplete="off"></div>` : ""}
    <p class="status" id="f16-status" role="status">${esc(S._f16status || "")}</p>
    ${S.form16s.map((f, i) => form16Card(f, i)).join("")}
    <div class="actions-bar"><button class="btn btn--ghost" type="button" data-action="prev">← Back</button>
      <button class="btn btn--brand" type="button" data-action="next" ${S.salary.employers.length || S.noForm16 ? "" : "disabled"}>Continue to income →</button></div>`;
}

const F16_GROUPS = [
  ["Salary", ["s17_1", "s17_2", "s17_3", "gross", "otherEmployer"]],
  ["Exempt allowances (section 10)", ["lta", "gratuity", "commutedPension", "leaveEncashment", "hra", "special10_14", "otherExemptTotal", "exemptTotal"]],
  ["Deductions under section 16", ["salaryCurrent", "stdDeduction", "entAllow", "profTax", "total16", "incomeSalary"]],
  ["Other income reported to employer", ["hpReported", "osReported", "otherReported", "gti"]],
  ["Chapter VI-A deductions", ["s80c", "s80ccc", "s80ccd1", "total80c", "s80ccd1b", "s80ccd2", "s80d", "s80e", "s80cchEmp", "s80cchGov", "s80g", "s80tta", "otherVIATotal", "aggVIA"]],
  ["Tax", ["totalIncome", "taxOnIncome", "rebate87A", "surcharge", "cess", "taxPayable", "relief89", "tds192_2B", "tcs192_2B", "netTax"]],
];
function form16Card(f, i) {
  const p = f.parsed;
  const flagged = new Set(p.validation.flagged);
  const unconfirmed = [...flagged].filter((k) => !f.confirm?.[k]);
  const tdsMatch = (S.prefill?.tdsSalary || []).find((t) => t.tan === p.partA.tan);
  return `<article class="f16 ${f.applied ? "is-applied" : ""}">
    <header class="f16__head"><div><h3>${esc(p.partA.employer || "Employer")}</h3>
      <p>${chip(esc(f.fileName), "chip--file")} ${chip("TAN " + esc(p.partA.tan || "?"))} ${chip("AY " + esc(p.partA.ay || "?"))} ${chip(p.source === "text" ? "Read from PDF text ✓" : "OCR — please check", p.source === "text" ? "chip--ok" : "chip--warn")}</p></div>
      <button class="linkbtn" type="button" data-action="remove-f16" data-i="${i}">Remove</button></header>
    <div class="f16__checks"><h4>Automatic checks</h4><ul>${p.validation.checks.map((c) => `<li class="${c.ok ? "ok" : "bad"}">${c.ok ? "✓" : "✗"} ${esc(c.text)}</li>`).join("")}
      ${tdsMatch ? `<li class="${Math.abs(tdsMatch.tds - (p.partA.totals?.taxDeducted ?? 0)) <= 10 ? "ok" : "bad"}">${Math.abs(tdsMatch.tds - (p.partA.totals?.taxDeducted ?? 0)) <= 10 ? "✓" : "✗"} TDS matches Form 26AS (${inr(tdsMatch.tds)})</li>` : `<li class="bad">✗ This employer's TAN was not found in Form 26AS — check the TAN or ask your employer to file the TDS return</li>`}</ul></div>
    ${unconfirmed.length ? `<p class="note-warn">${unconfirmed.length} value(s) need your confirmation (highlighted). Compare them with your Form 16, correct if needed, and tick “Confirmed”.</p>` : `<p class="note-ok">All values read and reconciled.</p>`}
    ${F16_GROUPS.map(([g, keys]) => `<details class="f16__group" ${keys.some((k) => flagged.has(k)) || g === "Salary" ? "open" : ""}><summary>${g}</summary><table class="f16__table"><tbody>
      ${keys.map((k) => { const x = p.partB.fields[k]; if (!x) return ""; const fl = flagged.has(k);
        return `<tr class="${fl ? (f.confirm?.[k] ? "is-confirmed" : "is-flagged") : ""}"><th scope="row">${esc(x.label)}${x.found ? "" : ' <span class="tag-miss">not found</span>'}</th>
        <td><input type="number" inputmode="decimal" data-f16="${i}.${k}" value="${x.value ?? 0}" aria-label="${esc(x.label)}"></td>
        <td>${fl ? `<label class="check"><input type="checkbox" data-f16confirm="${i}.${k}" ${f.confirm?.[k] ? "checked" : ""}> Confirmed</label>` : '<span class="ok">✓</span>'}</td></tr>`; }).join("")}
    </tbody></table></details>`).join("")}
    ${p.form12BA?.rows?.filter((r) => r.chargeable).length ? `<details class="f16__group"><summary>Form 12BA — perquisites</summary><table class="f16__table"><tbody>${p.form12BA.rows.filter((r) => r.chargeable).map((r) => `<tr><th scope="row">${esc(r.label)}</th><td class="num">${inr(r.chargeable)}</td><td></td></tr>`).join("")}</tbody></table></details>` : ""}
    <p class="field-hint">Regime chosen with employer: ${p.partB.optOut === true ? "Old regime (opted out)" : p.partB.optOut === false ? "New regime" : "not stated"}. You can choose again in step 4${isBelated() ? " (belated returns are new-regime only)" : ""}.</p>
    <div class="actions-bar"><span></span><button class="btn ${f.applied ? "btn--ghost" : "btn--brand"}" type="button" data-action="apply-f16" data-i="${i}" ${unconfirmed.length ? "disabled" : ""}>${f.applied ? "✓ Figures used — update" : "Use these figures"}</button></div>
  </article>`;
}

async function handleForm16Files(files) {
  for (const file of files) {
    setF16Status(`Reading ${file.name}…`);
    try {
      const pw = S.personal.pan ? [S.personal.pan.toLowerCase(), S.personal.pan.toUpperCase(), (S.personal.dob || "").split("-").reverse().join("")] : [];
      let res;
      try { res = await extractItems(file, { passwords: pw, onStatus: setF16Status }); }
      catch (e) {
        if (e.code !== "PASSWORD") throw e;
        const p = (typeof prompt === "function" ? prompt(`${file.name} is password-protected. Enter its password:`) : null) || ($("#f16-pw")?.value || "");
        if (!p) { S._needPw = true; throw new Error("This PDF is password-protected. Type its password in the box below and upload it again."); }
        res = await extractItems(file, { passwords: [p], onStatus: setF16Status });
      }
      const parsed = parseForm16(res.items, { pan: S.personal.pan });
      if (!parsed.partB.fields.s17_1.found && !parsed.partB.fields.gross.found) throw new Error("This does not look like a Form 16 Part B. Upload the full Form 16 (Part A and Part B), or enter salary manually.");
      S.form16s.push({ id: uid(), fileName: file.name, parsed, confirm: {}, applied: false });
      track("form16_parsed", { source: parsed.source, all_ok: parsed.validation.allOk });
      setF16Status(parsed.validation.allOk ? `${file.name}: all values read and reconciled.` : `${file.name}: read — please confirm the highlighted values.`);
    } catch (e) {
      setF16Status(`${file.name}: ${e.message}`);
    }
  }
  render();
}
function setF16Status(t) { S._f16status = t; const el = $("#f16-status"); if (el) el.textContent = t; }

function applyForm16(i) {
  const f = S.form16s[i];
  const m = toModel(f.parsed);
  const emp = { id: f.empId || uid(), ...m.employer, source: "form16" };
  f.empId = emp.id;
  const idx = S.salary.employers.findIndex((e) => e.id === emp.id || (e.tan && e.tan === emp.tan));
  if (idx >= 0) S.salary.employers[idx] = { ...S.salary.employers[idx], ...emp };
  else S.salary.employers.push(emp);
  for (const [k, v] of Object.entries(m.deductions)) if (v) S.deductions[k] = v;
  if (m.relief89) S.taxes.relief89 = m.relief89;
  if (m.optOutNewRegime === true && !isBelated()) S.regime = "old";
  f.applied = true;
  S.noForm16 = false;
  track("form16_applied");
  render();
}

// ------------------------------------------------------------------ step 3: income (5 heads)
function step3() {
  const c = calc();
  const emps = S.salary.employers;
  const ais = S.prefill?.ais || {};
  return `
    <header class="panel__head"><p class="kicker">Step 3 of 5</p><h1>Review all your income</h1>
      <p class="lede-s">Everything we found from your Form 16, pre-fill and AIS is filled in below. Check each head, edit any figure and add anything that is missing.</p></header>
    ${headCard("1", "Income from Salary / Pension", c.salary.income, `
      ${emps.length ? `<table class="rows"><thead><tr><th>Employer / payer</th><th class="num">Gross</th><th class="num">Exempt</th><th class="num">TDS</th><th></th></tr></thead><tbody>
        ${c.salary.rows.map((r, i) => `<tr><td>${esc(r.name)} ${chip(emps[i].isPension ? "Pension" : emps[i].source === "form16" ? "Form 16" : emps[i].source === "ais" ? "26AS" : emps[i].source === "slip" ? "Salary slip" : "Manual", "chip--src")}<br><small>${esc(emps[i].tan || "")}</small></td>
          <td class="num">${inr(r.gross)}</td><td class="num">${inr(r.exempt)}</td><td class="num">${inr(emps[i].tds)}</td>
          <td class="row-actions"><button class="btn btn--ghost btn--xs" type="button" data-action="salary-modal" data-i="${i}">${emps[i].isPension ? "Edit" : "Add bifurcation"}</button><button class="linkbtn" type="button" data-action="remove-emp" data-i="${i}" aria-label="Remove ${esc(r.name)}">✕</button></td></tr>`).join("")}
      </tbody></table>
      <dl class="mini"><div><dt>Less: standard deduction u/s 16(ia)</dt><dd>${inr(-c.salary.standardDeduction)}</dd></div>${c.salary.profTax ? `<div><dt>Less: professional tax</dt><dd>${inr(-c.salary.profTax)}</dd></div>` : ""}</dl>`
        : `<p class="empty">No salary added yet.</p>`}
      <div class="add-row"><button class="btn btn--ghost btn--sm" type="button" data-action="salary-modal" data-i="new">+ Add salary / employer</button>
        <button class="btn btn--ghost btn--sm" type="button" data-action="pension-modal">+ Add pension</button></div>
      ${ais.salary?.length ? `<p class="field-hint">AIS shows salary of ${ais.salary.map((s) => `${inr(s.amount)} from ${esc(s.source)}`).join("; ")}.</p>` : ""}`)}

    ${headCard("2", "Income from House Property", c.houseProperty.income, `
      ${S.houseProperties.length ? `<table class="rows"><thead><tr><th>Property</th><th class="num">Rent</th><th class="num">Interest</th><th class="num">Income</th><th></th></tr></thead><tbody>
        ${c.houseProperty.rows.map((h, i) => `<tr><td>${h.type === "self" ? "Self-occupied" : h.type === "deemed" ? "Deemed let-out" : "Let-out"}<br><small>${esc(h.address || "")}</small></td><td class="num">${inr(h.gav || 0)}</td><td class="num">${inr(h.interestClaimed)}</td><td class="num">${inr(h.income)}</td>
          <td class="row-actions"><button class="btn btn--ghost btn--xs" type="button" data-action="hp-modal" data-i="${i}">Edit</button><button class="linkbtn" type="button" data-action="remove-hp" data-i="${i}" aria-label="Remove property">✕</button></td></tr>`).join("")}</tbody></table>` : `<p class="empty">No house property added.</p>`}
      <div class="add-row"><button class="btn btn--ghost btn--sm" type="button" data-action="hp-modal" data-i="new" ${S.houseProperties.length >= 2 ? "disabled" : ""}>+ Add rental income / property</button></div>
      ${S.houseProperties.length >= 2 ? `<p class="field-hint">ITR-1 allows up to two house properties.</p>` : ""}
      ${c.houseProperty.lossNotSetOff && c.meta.regime === "new" ? `<p class="field-hint">In the new regime a house-property loss cannot be set off against other income.</p>` : ""}`)}

    ${headCard("3", "Capital Gains (LTCG u/s 112A)", c.ltcg112a.gain, `
      <p class="field-hint">ITR-1 allows long-term gains on listed shares and equity mutual funds up to ₹1.25 lakh (tax-free up to that limit). Short-term gains need ITR-2.</p>
      ${S.ltcg112a.saleValue || S.ltcg112a.gain ? `<dl class="mini"><div><dt>Sale consideration</dt><dd>${inr(S.ltcg112a.saleValue)}</dd></div><div><dt>Cost of acquisition (after grandfathering)</dt><dd>${inr(S.ltcg112a.costOfAcquisition)}</dd></div><div><dt>LTCG u/s 112A</dt><dd>${inr(c.ltcg112a.gain)}</dd></div></dl>
        ${S.ltcg112a.source ? `<p class="field-hint">Source: ${esc(S.ltcg112a.source)}</p>` : ""}` : `<p class="empty">No capital gains added.</p>`}
      ${(S.prefill?.ais?.securitiesSold || []).length ? `<p class="field-hint">AIS shows securities sold: ${S.prefill.ais.securitiesSold.map((s) => inr(s.amount)).join(", ")}. Add the gain if you sold shares or equity funds.</p>` : ""}
      <div class="add-row"><button class="btn btn--ghost btn--sm" type="button" data-action="ltcg-modal">+ Add LTCG manually</button>
        <label class="btn btn--ghost btn--sm" for="pnl-input">⬆ Upload broker Tax P&amp;L (Excel)</label><input id="pnl-input" type="file" accept=".xlsx,.xls,.csv" data-upload="pnl" hidden>${api.DEMO ? `<button type="button" class="linkbtn" data-action="sample" data-kind="pnl" data-file="sample-broker-tax-pnl.csv">Demo: sample P&amp;L</button>` : ""}</div>`)}

    ${headCard("4", "Income from Other Sources", c.otherSources.income, `
      <div class="grid2">
        ${field(`Savings bank interest ${srcTag("savingsInterest")}`, "otherSources.savingsInterest")}
        ${field(`Deposit interest (FD / RD / post office) ${srcTag("depositInterest")}`, "otherSources.depositInterest")}
        ${field(`Dividend ${srcTag("dividend")}`, "otherSources.dividend")}
        ${field(`Interest on income-tax refund ${srcTag("refundInterest")}`, "otherSources.refundInterest")}
        ${field("Family pension", "otherSources.familyPension", { hint: `Deduction u/s 57(iia): one-third, up to ${c.meta.regime === "old" ? "₹15,000" : "₹25,000"}` })}
      </div>
      ${(S.otherSources.others || []).length ? `<table class="rows"><tbody>${S.otherSources.others.map((o, i) => `<tr><td>${esc(o.label)}<br><small>${esc(o.payer || "")}</small></td><td class="num">${inr(o.amount)}</td><td class="row-actions"><button class="linkbtn" type="button" data-action="remove-os" data-i="${i}" aria-label="Remove">✕</button></td></tr>`).join("")}</tbody></table>` : ""}
      <div class="add-row"><button class="btn btn--ghost btn--sm" type="button" data-action="os-modal">+ Add any other income</button></div>`)}

    ${headCard("5", "Profits and Gains of Business or Profession", 0, `<p class="empty">Not applicable in ITR-1. Business or professional income needs ITR-3 or ITR-4 — <a href="https://bharatefiling.com/income-tax-return-filing/#packages" target="_blank" rel="noopener">let our CAs file it</a>.</p>`, true)}

    <div class="card-lite">${field("Exempt agricultural income (up to ₹5,000 in ITR-1)", "exemptIncome.agriculture")}</div>
    <div data-live>${liveBlocks()}</div>
    <div class="actions-bar"><button class="btn btn--ghost" type="button" data-action="prev">← Back</button><button class="btn btn--brand" type="button" data-action="next">Continue to deductions →</button></div>`;
}
function srcTag(k) { const ais = S.prefill?.ais || {}; const map = { savingsInterest: "savingsInterest", depositInterest: "depositInterest", dividend: "dividend", refundInterest: "refundInterest" }; return (ais[map[k]] || []).length ? chip("AIS", "chip--src") : ""; }
function headCard(no, title, total, body, disabled = false) {
  return `<section class="head ${disabled ? "is-disabled" : ""}"><header class="head__top"><span class="head__no">${no}</span><h2>${title}</h2><strong class="head__amt">${inr(total)}</strong></header><div class="head__body">${body}</div></section>`;
}
function liveBlocks() {
  const c = calc();
  const w = c.warnings;
  return `<div data-live>${w.length ? `<div class="warns">${w.map((x) => `<p class="${x.level === "block" ? "note-bad" : "note-info"}">${x.level === "block" ? "⛔" : "ℹ"} ${esc(x.text)}</p>`).join("")}</div>` : ""}</div>`;
}

// ------------------------------------------------------------------ step 4: deductions, regime, taxes paid
function step4() {
  const c = calc();
  const belated = isBelated();
  const cmp = compareRegimes(data(), { filingDate: today() });
  const old = c.meta.regime === "old";
  const dis = !old;
  const D = (label, key, opts = {}) => field(label, "deductions." + key, { disabled: opts.always ? false : dis, hint: opts.hint });
  const challans = [...S.taxes.advance.map((x, i) => ({ ...x, kind: "advance", i })), ...S.taxes.selfAssessment.map((x, i) => ({ ...x, kind: "selfAssessment", i }))];
  return `
    <header class="panel__head"><p class="kicker">Step 4 of 5</p><h1>Deductions, regime and taxes paid</h1></header>
    <section class="head"><header class="head__top"><h2>Tax regime</h2></header><div class="head__body">
      ${belated ? `<p class="note-info">You are filing after the due date (31 July 2026). A belated return can only use the <strong>new tax regime</strong> (s.115BAC(6)). Old-regime deductions below are not allowed.</p>
        <p class="field-hint">For reference, on a due-date basis: new regime ${inr(cmp.new)} vs old regime ${inr(cmp.old)}.</p>`
      : `<div class="seg" role="radiogroup" aria-label="Tax regime"><label><input type="radio" name="regime" value="new" data-bind="regime" data-type="radio" ${S.regime === "new" ? "checked" : ""}>New regime · ${inr(cmp.new)}</label><label><input type="radio" name="regime" value="old" data-bind="regime" data-type="radio" ${S.regime === "old" ? "checked" : ""}>Old regime · ${inr(cmp.old)}</label></div>
        <p class="field-hint">${cmp.new <= cmp.old ? `The new regime saves ${inr(cmp.old - cmp.new)}.` : `The old regime saves ${inr(cmp.new - cmp.old)}.`}</p>`}
    </div></section>
    <section class="head"><header class="head__top"><h2>Deductions (Chapter VI-A)</h2><strong class="head__amt">${inr(c.deductions.total)}</strong></header><div class="head__body">
      <p class="field-hint">${old ? "Old regime: all deductions below are available." : "New regime: only employer NPS (80CCD(2)) and Agnipath (80CCH) are allowed; other fields are kept for reference."}</p>
      <div class="grid2">
        ${D("80CCD(2) Employer NPS contribution", "s80ccd2", { always: true })}
        ${D("Basic salary + DA (for the 80CCD(2) limit)", "basicPlusDA", { always: true, hint: "Limit: 14% (new) / 10% (old)" })}
        ${D("80CCH Agnipath contribution", "s80cch", { always: true })}
        ${D("80C (PPF, EPF, ELSS, LIC, tuition, home-loan principal)", "s80c", { hint: "Up to ₹1.5 lakh with 80CCC and 80CCD(1)" })}
        ${D("80CCC pension fund", "s80ccc")}${D("80CCD(1) own NPS", "s80ccd1")}${D("80CCD(1B) additional NPS", "s80ccd1b", { hint: "Up to ₹50,000" })}
        ${D("80D health insurance — self & family", "s80dSelf", { hint: "₹25,000 (₹50,000 if senior)" })}${D("80D — parents", "s80dParents")}${D("80D preventive check-up", "s80dCheckup", { hint: "Up to ₹5,000 within the limit" })}
        ${D("80E education-loan interest", "s80e")}${D("80G donations (eligible amount)", "s80g")}${D("80GG rent paid (no HRA)", "s80gg")}${D("80U / 80DD disability", "s80u")}
      </div>
      <div class="checks2">${old ? `<label class="check"><input type="checkbox" data-bind="deductions.selfSenior" data-type="bool" ${S.deductions.selfSenior ? "checked" : ""}> Self/spouse is a senior citizen</label><label class="check"><input type="checkbox" data-bind="deductions.parentsSenior" data-type="bool" ${S.deductions.parentsSenior ? "checked" : ""}> Parents are senior citizens</label>` : ""}</div>
      ${old ? `<p class="field-hint">80TTA / 80TTB on interest is applied automatically.</p>` : ""}
    </div></section>
    <section class="head"><header class="head__top"><h2>Taxes paid</h2><strong class="head__amt">${inr(c.paid.total)}</strong></header><div class="head__body">
      <dl class="mini"><div><dt>TDS on salary (Form 16 / 26AS)</dt><dd>${inr(c.paid.tdsSalary)}</dd></div></dl>
      <h3 class="sub">TDS on other income (Form 26AS)</h3>
      ${S.taxes.tdsOther.length ? `<table class="rows"><thead><tr><th>Deductor</th><th>TAN</th><th class="num">Income</th><th class="num">TDS</th><th></th></tr></thead><tbody>${S.taxes.tdsOther.map((t, i) => `<tr><td>${esc(t.deductor)} <small>${esc(t.section || "")}</small></td><td>${esc(t.tan)}</td><td class="num">${inr(t.amountPaid)}</td><td class="num"><input class="cell-in" type="number" data-bind="taxes.tdsOther.${i}.tds" data-type="number" value="${t.tds}" aria-label="TDS"></td><td class="row-actions"><button class="linkbtn" data-action="remove-tds" data-i="${i}" type="button" aria-label="Remove">✕</button></td></tr>`).join("")}</tbody></table>` : `<p class="empty">None.</p>`}
      <h3 class="sub">Advance tax and self-assessment tax challans</h3>
      ${challans.length ? `<table class="rows"><thead><tr><th>Type</th><th>Date</th><th>BSR</th><th>Challan no.</th><th class="num">Amount</th><th></th></tr></thead><tbody>${challans.map((t) => `<tr><td>${t.kind === "advance" ? "Advance" : "Self-assessment"}</td><td>${esc(t.date)}</td><td>${esc(t.bsr)}</td><td>${esc(t.challan)}</td><td class="num">${inr(t.amount)}</td><td class="row-actions"><button class="linkbtn" type="button" data-action="remove-challan" data-kind="${t.kind}" data-i="${t.i}" aria-label="Remove">✕</button></td></tr>`).join("")}</tbody></table>` : `<p class="empty">No challans added.</p>`}
      <div class="add-row"><button class="btn btn--ghost btn--sm" type="button" data-action="challan-modal">+ Add challan</button></div>
    </div></section>
    <section class="head"><header class="head__top"><h2>Bank account for refund</h2></header><div class="head__body">
      ${S.bankAccounts.length ? S.bankAccounts.map((b, i) => `<label class="radio-card"><input type="radio" name="refund-bank" data-action="refund-bank" data-i="${i}" ${b.refund ? "checked" : ""}><span><strong>${esc(b.bank)}</strong> · ${esc(b.account)} · ${esc(b.ifsc)} ${b.prevalidated ? chip("Pre-validated", "chip--ok") : chip("Not pre-validated", "chip--warn")}</span></label>`).join("") : `<p class="empty">No bank account found. Pre-validate one on the e-filing portal.</p>`}
    </div></section>
    <div data-live>${liveBlocks()}</div>
    <div class="actions-bar"><button class="btn btn--ghost" type="button" data-action="prev">← Back</button><button class="btn btn--brand" type="button" data-action="next">Continue to computation →</button></div>`;
}

// ------------------------------------------------------------------ step 5: computation, PDF, file
function step5() {
  const c = calc();
  const blocks = c.warnings.filter((w) => w.level === "block");
  if (!S.computed) return `<header class="panel__head"><p class="kicker">Step 5 of 5</p><h1>Create your computation</h1><p class="lede-s">We will compute your total income, tax, interest and refund from everything you have confirmed.</p></header>
    <button class="btn btn--brand" type="button" data-action="create-computation">Create computation</button>
    <div class="actions-bar"><button class="btn btn--ghost" type="button" data-action="prev">← Back</button><span></span></div>`;
  const rows = computationRows(data(), c);
  const f = S.filing;
  return `
    <header class="panel__head"><p class="kicker">Step 5 of 5</p><h1>Your computation</h1>
      <p class="lede-s">${esc(S.personal.name)} · PAN ${esc(S.personal.pan)} · ITR-1 u/s ${c.meta.section}${c.meta.belated ? " (belated)" : ""} · ${c.meta.regime === "new" ? "New regime" : "Old regime"}</p></header>
    <div class="result-banner ${c.refund ? "is-refund" : c.payable ? "is-pay" : ""}"><span>${c.refund ? "Refund due to you" : c.payable ? "Tax to pay before filing" : "No tax payable"}</span><strong>${inr(c.refund || c.payable || 0)}</strong></div>
    ${blocks.length ? `<div class="warns">${blocks.map((x) => `<p class="note-bad">⛔ ${esc(x.text)}</p>`).join("")}</div>` : ""}
    ${c.warnings.filter((w) => w.level !== "block").map((x) => `<p class="note-info">ℹ ${esc(x.text)}</p>`).join("")}
    <div class="comp" role="region" aria-label="Computation of total income" tabindex="0"><table><tbody>${rows.map((r) => r.head ? `<tr class="comp__h"><th colspan="3" scope="colgroup">${esc(r.head)}</th></tr>` : `<tr><td>${esc(r.t)}</td><td class="num">${esc(rupee(r.a))}</td><td class="num"><strong>${esc(rupee(r.b))}</strong></td></tr>`).join("")}</tbody></table></div>
    <div class="file-actions">
      <button class="btn btn--ghost" type="button" data-action="download-pdf">⬇ Download computation (PDF)</button>
      <button class="btn btn--ghost" type="button" data-action="download-json">⬇ Download ITR-1 JSON</button>
      <button class="btn btn--brand" type="button" data-action="file-now" ${blocks.length || f.verified ? "disabled" : ""}>${f.verified ? "✓ Filed & e-verified" : "File now"}</button>
    </div>
    ${f.ackNo ? `<div class="ack"><h3>${f.verified ? "Return filed and e-verified" : "Return submitted — e-verify within 30 days"}</h3><p>Acknowledgement number <strong>${esc(f.ackNo)}</strong> · filed on ${esc(f.filedOn)}${f.verified ? ` · e-verified on ${esc(f.verifiedOn)}` : ""}</p></div>` : ""}
    <div class="actions-bar"><button class="btn btn--ghost" type="button" data-action="prev">← Back</button><button class="linkbtn" type="button" data-action="reset">Start a new return</button></div>`;
}

// ------------------------------------------------------------------ modals
const dlg = document.getElementById("modal");
let M = null; // modal draft
function openModal(kind, draft, opts = {}) { M = { kind, draft, ...opts }; renderModal(); if (!dlg.open) dlg.showModal(); }
function closeModal() { dlg.close(); M = null; }
function renderModal() {
  const body = { salary: salaryModal, pension: pensionModal, hp: hpModal, ltcg: ltcgModal, pnl: pnlModal, os: osModal, challan: challanModal, file: fileModal }[M.kind]();
  dlg.innerHTML = `<form method="dialog" class="m" data-modal-form><button class="m__close" type="button" data-action="close-modal" aria-label="Close">×</button>${body}</form>`;
}
const mField = (label, key, { type = "number", hint = "", attrs = "" } = {}) => {
  const v = get(M.draft, key);
  return `<div class="field"><label for="m-${key.replace(/\W/g, "-")}">${label}</label><input id="m-${key.replace(/\W/g, "-")}" ${type === "number" ? 'type="number" inputmode="decimal" min="0"' : `type="${type}"`} data-mbind="${key}" data-type="${type}" value="${esc(v ?? "")}" ${attrs}>${hint ? `<p class="field-hint">${hint}</p>` : ""}</div>`;
};
const COMP = [["basic", "Basic salary"], ["da", "Dearness allowance"], ["hraReceived", "House rent allowance received"], ["special", "Special allowance"], ["bonus", "Bonus / incentive"], ["ltaReceived", "Leave travel allowance received"], ["conveyance", "Conveyance / other allowances"]];

function salaryModal() {
  const d = M.draft, tab = M.tab || "manual";
  const compSum = COMP.reduce((a, [k]) => a + n(d.components?.[k]), 0);
  const regimeNote = calc().meta.regime === "new" ? `<p class="note-info">New regime: HRA, LTA, 10(14) allowances and professional tax are not deductible. Enter them anyway; they are used only if you choose the old regime.</p>` : "";
  return `<h2>Salary details — ${esc(d.name || "new employer")}</h2>
    <div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="${tab === "manual"}" data-action="mtab" data-tab="manual">Enter head-wise</button><button type="button" role="tab" aria-selected="${tab === "slip"}" data-action="mtab" data-tab="slip">Upload salary slip</button></div>
    ${tab === "slip" ? `
      <label class="drop drop--sm" for="slip-input"><input id="slip-input" type="file" accept="application/pdf,image/*" data-upload="slip" hidden><span class="drop__icon" aria-hidden="true">🧾</span><strong>Upload a salary slip (PDF or photo)</strong><span>We read the components and multiply by the months you choose.</span></label>
      ${api.DEMO ? `<p class="samples"><button type="button" class="linkbtn" data-action="sample" data-kind="slip" data-file="sample-salary-slip.png">Demo: try a sample salary slip</button></p>` : ""}
      <p class="status" id="slip-status" role="status">${esc(M.slipStatus || "")}</p>
      ${M.slip ? `<table class="f16__table"><tbody>${Object.entries(M.slip.components).map(([k, x]) => `<tr class="${x.ocr && x.conf < 85 ? "is-flagged" : ""}"><th scope="row">${esc(x.label)}</th><td class="num">${inr(x.value)}</td><td>${x.ocr ? `OCR ${Math.round(x.conf)}%` : "✓"}</td></tr>`).join("")}</tbody></table>
        ${M.slip.checks.map((c) => `<p class="${c.ok ? "note-ok" : "note-warn"}">${c.ok ? "✓" : "⚠"} ${esc(c.text)}</p>`).join("")}
        <div class="grid2">${mField("Months this salary applies to", "slipMonths", { hint: M.slip.month ? `Slip for ${esc(M.slip.month)}` : "" })}</div>
        <button class="btn btn--brand btn--sm" type="button" data-action="apply-slip">Fill the form from this slip</button>` : ""}`
    : `
      <div class="grid2">${mField("Employer name", "name", { type: "text" })}${mField("Employer TAN", "tan", { type: "text", attrs: 'maxlength="10" style="text-transform:uppercase"' })}</div>
      <h3 class="sub">Salary u/s 17(1) — break-up</h3>
      <div class="grid3">${COMP.map(([k, l]) => mField(l, "components." + k)).join("")}</div>
      <div class="grid2">${mField("Total salary u/s 17(1)", "s17_1", { hint: compSum ? `Break-up adds up to ${inr(compSum)}` : "Or enter the total directly" })}${mField("Perquisites u/s 17(2) (Form 12BA)", "s17_2")}${mField("Profits in lieu of salary u/s 17(3)", "s17_3")}</div>
      <h3 class="sub">Exempt allowances (section 10)</h3>${regimeNote}
      <div class="grid3">${mField("HRA exempt 10(13A)", "exemptions.hra", { hint: '<button type="button" class="linkbtn" data-action="hra-calc">Calculate HRA exemption</button>' })}${mField("LTA 10(5)", "exemptions.lta")}${mField("Gratuity 10(10)", "exemptions.gratuity")}${mField("Leave encashment 10(10AA)", "exemptions.leaveEncashment")}${mField("Commuted pension 10(10A)", "exemptions.commutedPension")}${mField("Allowances u/s 10(14)", "exemptions.special10_14")}${mField("Other exemption u/s 10", "exemptions.other")}</div>
      ${M.hra ? `<div class="calc-box"><h4>HRA exemption calculator</h4><div class="grid3">${mField("HRA received (year)", "hra.received")}${mField("Rent paid (year)", "hra.rent")}${mField("Basic + DA (year)", "hra.basic")}</div><label class="check"><input type="checkbox" data-mbind="hra.metro" data-type="bool" ${d.hra?.metro ? "checked" : ""}> Living in Mumbai, Delhi, Kolkata or Chennai</label>
        <p>Exempt HRA = least of HRA received, rent − 10% of salary, ${d.hra?.metro ? "50%" : "40%"} of salary: <strong>${inr(hraExempt(d.hra))}</strong> <button type="button" class="btn btn--ghost btn--xs" data-action="use-hra">Use this</button></p></div>` : ""}
      <h3 class="sub">Deductions u/s 16 and TDS</h3>
      <div class="grid3">${mField("Professional tax 16(iii)", "profTax")}${mField("Entertainment allowance 16(ii) (govt. only)", "entAllow")}${mField("TDS deducted by this employer", "tds")}</div>`}
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">Cancel</button><button class="btn btn--brand" type="button" data-action="save-salary">Save salary</button></div>`;
}
const hraExempt = (h = {}) => { const rec = n(h.received), rent = n(h.rent), b = n(h.basic); if (!rec) return 0; return Math.max(0, Math.min(rec, Math.max(0, rent - 0.1 * b), (h.metro ? 0.5 : 0.4) * b)); };

function pensionModal() {
  return `<h2>Pension</h2><p class="field-hint">Pension from a former employer is taxed as salary (standard deduction applies). Family pension received after a family member's death goes under Other sources.</p>
    <div class="grid2">${mField("Paid by (bank / employer)", "name", { type: "text" })}${mField("TAN of payer (from 26AS)", "tan", { type: "text" })}${mField("Uncommuted pension received in the year", "s17_1")}${mField("Commuted pension received", "commutedReceived")}${mField("Exempt part of commuted pension 10(10A)", "exemptions.commutedPension", { hint: "Government: fully exempt. Others: one-third if gratuity received, else one-half." })}${mField("TDS on pension", "tds")}</div>
    <p><button type="button" class="linkbtn" data-action="family-pension">I receive family pension instead →</button></p>
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">Cancel</button><button class="btn btn--brand" type="button" data-action="save-pension">Save pension</button></div>`;
}

function hpModal() {
  const d = M.draft;
  const self = d.type === "self";
  const share = (d.sharePct === "" || d.sharePct === undefined ? 100 : n(d.sharePct)) / 100;
  const nav = Math.max(0, n(d.rent) * share - n(d.municipalTax) * share);
  const inc = self ? -n(d.interest) * share : nav - Math.round(nav * 0.3) - n(d.interest) * share;
  return `<h2>${self ? "Self-occupied property" : "Rental income"}</h2>
    <div class="seg" role="radiogroup" aria-label="Property type">${[["let", "Let out"], ["self", "Self-occupied"], ["deemed", "Deemed let-out"]].map(([v, l]) => `<label><input type="radio" name="hp-type" value="${v}" data-mbind="type" data-type="radio" ${d.type === v ? "checked" : ""}>${l}</label>`).join("")}</div>
    <div class="grid2">${mField("Address of the property", "address", { type: "text" })}${mField("PIN code", "pincode", { type: "text", attrs: 'inputmode="numeric" maxlength="6"' })}${mField("Your ownership share (%)", "sharePct", { hint: "100 if you own it alone" })}</div>
    ${self ? "" : `<h3 class="sub">Rent</h3><div class="grid2">${mField(d.type === "deemed" ? "Expected annual rent (deemed)" : "Annual rent received", "rent")}${mField("Municipal / property tax paid in the year", "municipalTax")}${mField("Tenant name", "tenantName", { type: "text" })}${mField("Tenant PAN / TAN (if TDS deducted)", "tenantPan", { type: "text" })}</div>`}
    <h3 class="sub">Home loan</h3><div class="grid2">${mField("Interest on housing loan for the year (incl. 1/5th pre-construction)", "interest", { hint: self ? "Self-occupied: up to ₹2 lakh, old regime only." : "Let-out: allowed in full; a resulting loss is limited by your regime." })}${mField("Lender name", "lender", { type: "text" })}</div>
    <p class="calc-line">Income from this property: <strong>${inr(inc)}</strong>${self ? "" : ` (NAV ${inr(nav)} − 30% ${inr(Math.round(nav * 0.3))} − interest ${inr(n(d.interest) * share)})`}</p>
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">Cancel</button><button class="btn btn--brand" type="button" data-action="save-hp">Save property</button></div>`;
}

function ltcgModal() {
  const d = M.draft;
  const gain = Math.max(0, n(d.saleValue) - n(d.costOfAcquisition));
  return `<h2>Long-term capital gains u/s 112A</h2>
    <p class="field-hint">Listed equity shares and equity mutual funds held for more than 12 months, where STT was paid. For shares bought before 1 Feb 2018, cost = higher of actual cost and the lower of FMV on 31 Jan 2018 and sale value.</p>
    <div class="grid2">${mField("Total sale consideration", "saleValue")}${mField("Total cost of acquisition (after grandfathering)", "costOfAcquisition")}</div>
    <p class="calc-line">LTCG u/s 112A: <strong>${inr(gain)}</strong> ${gain > 125000 ? '<span class="tag-miss">Above ₹1.25 lakh — ITR-2 needed</span>' : "(tax-free up to ₹1.25 lakh)"}</p>
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">Cancel</button><button class="btn btn--brand" type="button" data-action="save-ltcg">Save</button></div>`;
}

function pnlModal() {
  const r = M.draft;
  const s = r.summary;
  return `<h2>Broker Tax P&amp;L — ${esc(M.fileName)}</h2>
    <dl class="mini"><div><dt>LTCG u/s 112A (${s.ltcg112a.trades} trades)</dt><dd>${inr(s.ltcg112a.gain)}</dd></div><div><dt>Sale consideration</dt><dd>${inr(s.ltcg112a.saleValue)}</dd></div><div><dt>Cost (after grandfathering)</dt><dd>${inr(s.ltcg112a.costOfAcquisition)}</dd></div>
      ${s.stcg ? `<div><dt>Short-term gains</dt><dd>${inr(s.stcg)}</dd></div>` : ""}${s.intraday ? `<div><dt>Intraday</dt><dd>${inr(s.intraday)}</dd></div>` : ""}${s.fno ? `<div><dt>F&amp;O</dt><dd>${inr(s.fno)}</dd></div>` : ""}</dl>
    ${r.itr1Issues.map((x) => `<p class="note-bad">⛔ ${esc(x)}</p>`).join("")}${r.notes.map((x) => `<p class="note-info">ℹ ${esc(x)}</p>`).join("")}
    <details><summary>See all ${r.trades.length} trades</summary><div class="comp" tabindex="0"><table><thead><tr><th>Scrip</th><th>Bought</th><th>Sold</th><th class="num">Cost</th><th class="num">Sale</th><th class="num">Gain</th><th>Type</th></tr></thead><tbody>
      ${r.trades.map((t) => `<tr><td>${esc(t.symbol)}</td><td>${esc(t.buyDate)}</td><td>${esc(t.sellDate)}</td><td class="num">${inr(t.cost)}</td><td class="num">${inr(t.sellValue)}</td><td class="num">${inr(t.gain)}</td><td>${{ long: "LTCG", short: "STCG", intraday: "Intraday", fno: "F&O", unknown: "?" }[t.kind]}</td></tr>`).join("")}</tbody></table></div></details>
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">Cancel</button><button class="btn btn--brand" type="button" data-action="use-pnl">Use LTCG ${inr(s.ltcg112a.gain)}</button></div>`;
}

const OS_TYPES = [["savingsInterest", "Interest from savings bank account"], ["depositInterest", "Interest from deposits (bank / post office / co-op society)"], ["refundInterest", "Interest on income-tax refund"], ["dividend", "Dividend"], ["familyPension", "Family pension"], ["other:Interest on bonds / NSC / other securities", "Interest on bonds, NSC or other securities"], ["other:Gift received (taxable u/s 56(2)(x))", "Gifts above ₹50,000 from non-relatives (taxable)"], ["other:Any other income", "Any other income (describe)"]];
function osModal() {
  const d = M.draft;
  return `<h2>Add other income</h2><p class="field-hint">Only income types allowed in ITR-1 are listed. Lottery, horse-race and online-game winnings need ITR-2.</p>
    <div class="field"><label for="os-type">Type of income</label><select id="os-type" data-mbind="type" data-type="text">${OS_TYPES.map(([v, l]) => `<option value="${esc(v)}" ${d.type === v ? "selected" : ""}>${esc(l)}</option>`).join("")}</select></div>
    <div class="grid2">${d.type === "other:Any other income" ? mField("Describe the income", "label", { type: "text" }) : ""}${mField("Paid by (bank / company / person)", "payer", { type: "text" })}${mField("Amount for the year", "amount")}${mField("TDS deducted, if any", "tds")}</div>
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">Cancel</button><button class="btn btn--brand" type="button" data-action="save-os">Add income</button></div>`;
}

function challanModal() {
  return `<h2>Add tax challan</h2><div class="field"><label for="ch-k">Type</label><select id="ch-k" data-mbind="kind" data-type="text"><option value="selfAssessment" ${M.draft.kind === "selfAssessment" ? "selected" : ""}>Self-assessment tax (300)</option><option value="advance" ${M.draft.kind === "advance" ? "selected" : ""}>Advance tax (100)</option></select></div>
    <div class="grid2">${mField("Date of deposit", "date", { type: "date" })}${mField("BSR code", "bsr", { type: "text", attrs: 'maxlength="7" inputmode="numeric"' })}${mField("Challan serial number", "challan", { type: "text", attrs: 'maxlength="5" inputmode="numeric"' })}${mField("Amount", "amount")}</div>
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">Cancel</button><button class="btn btn--brand" type="button" data-action="save-challan">Add challan</button></div>`;
}

function fileModal() {
  const c = calc(), d = M.draft;
  if (c.payable > 0) return `<h2>Pay ${inr(c.payable)} before filing</h2><p>A return with tax due is treated as defective. Pay self-assessment tax (minor head 300) on the e-filing portal, then add the challan.</p>
    <div class="m__actions"><a class="btn btn--ghost" href="https://eportal.incometax.gov.in/iec/foservices/#/e-pay-tax-prelogin/user-details" target="_blank" rel="noopener">Open e-Pay Tax</a><button class="btn btn--brand" type="button" data-action="paid-add-challan">I've paid — add challan</button></div>`;
  if (d.stage === "verify") return `<h2>E-verify your return</h2><p>Acknowledgement <strong>${esc(S.filing.ackNo)}</strong>. Enter the Aadhaar OTP to e-verify now.</p>
    <div class="otp__row"><input class="otp__input" inputmode="numeric" maxlength="6" data-otp="ev" placeholder="6-digit OTP" aria-label="E-verification OTP"><button class="btn btn--brand btn--sm" type="button" data-action="everify">E-verify</button></div>
    <p class="field-hint">${api.DEMO ? "Demo OTP: 123456 · " : ""}You can also e-verify later within 30 days.</p>${d.error ? `<p class="err">${esc(d.error)}</p>` : ""}
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">E-verify later</button></div>`;
  return `<h2>File your ITR-1</h2>
    <dl class="mini"><div><dt>Total income</dt><dd>${inr(c.totalIncome)}</dd></div><div><dt>Tax regime</dt><dd>${c.meta.regime === "new" ? "New" : "Old"}</dd></div><div><dt>${c.refund ? "Refund" : "Balance"}</dt><dd>${inr(c.refund || 0)}</dd></div><div><dt>Return type</dt><dd>${c.meta.belated ? "Belated, s.139(4)" : "Original, s.139(1)"}</dd></div></dl>
    <label class="check decl"><input type="checkbox" data-mbind="agree" data-type="bool" ${d.agree ? "checked" : ""}> I, ${esc(S.personal.name)}, declare that the information in this return is correct and complete and is in accordance with the Income-tax Act, 1961.</label>
    <div class="grid2">${mField("Place", "place", { type: "text" })}</div>${d.error ? `<p class="err">${esc(d.error)}</p>` : ""}
    <div class="m__actions"><button class="btn btn--ghost" type="button" data-action="close-modal">Cancel</button><button class="btn btn--brand" type="button" data-action="submit-return" ${d.agree && d.place ? "" : "disabled"}>${d.busy ? "Submitting…" : "Submit return"}</button></div>`;
}

// ------------------------------------------------------------------ events
document.addEventListener("input", (e) => {
  const t = e.target;
  if (t.dataset.bind) {
    let v = t.dataset.type === "bool" ? t.checked : t.dataset.type === "number" ? (t.value === "" ? "" : Number(t.value)) : t.value;
    if (t.dataset.type === "pan") { v = t.value.toUpperCase().replace(/[^A-Z0-9]/g, ""); t.value = v; }
    set(S, t.dataset.bind, v);
    if (t.dataset.type === "radio" || t.dataset.type === "bool") return render();
    refreshSummary();
  } else if (t.dataset.mbind && M) {
    const v = t.dataset.type === "bool" ? t.checked : t.dataset.type === "number" ? (t.value === "" ? "" : Number(t.value)) : t.value;
    set(M.draft, t.dataset.mbind, v);
    if (M.kind === "salary" && t.dataset.mbind.startsWith("components.")) {
      const s = COMP.reduce((a, [k]) => a + n(M.draft.components?.[k]), 0);
      M.draft.s17_1 = s;
      const el = document.getElementById("m-s17_1"); if (el) el.value = s;
    }
    if (["radio", "bool"].includes(t.dataset.type) || t.tagName === "SELECT" || M.kind === "hp" || M.kind === "ltcg" || M.kind === "file" || t.dataset.mbind.startsWith("hra.")) { const pos = t.selectionStart; renderModal(); const el = document.getElementById(t.id); if (el) { el.focus(); try { el.setSelectionRange(pos, pos); } catch {} } }
  } else if (t.dataset.f16) {
    const [i, k] = t.dataset.f16.split(".");
    S.form16s[i].parsed.partB.fields[k].value = t.value === "" ? 0 : Number(t.value);
    S.form16s[i].applied = false;
    save();
  }
});
document.addEventListener("change", (e) => {
  const t = e.target;
  if (t.dataset.f16confirm) { const [i, k] = t.dataset.f16confirm.split("."); (S.form16s[i].confirm ||= {})[k] = t.checked; render(); }
  if (t.tagName === "SELECT" && t.dataset.mbind && M) { set(M.draft, t.dataset.mbind, t.value); renderModal(); }
  if (t.dataset.upload) handleUpload(t.dataset.upload, [...t.files]).finally(() => (t.value = ""));
});
document.addEventListener("dragover", (e) => { const z = e.target.closest("[data-drop]"); if (z) { e.preventDefault(); z.classList.add("is-over"); } });
document.addEventListener("dragleave", (e) => { const z = e.target.closest("[data-drop]"); if (z) z.classList.remove("is-over"); });
document.addEventListener("drop", (e) => { const z = e.target.closest("[data-drop]"); if (!z) return; e.preventDefault(); z.classList.remove("is-over"); handleUpload(z.dataset.drop, [...e.dataTransfer.files]); });

async function handleUpload(kind, files) {
  if (!files.length) return;
  if (kind === "form16") return handleForm16Files(files);
  if (kind === "pnl") {
    try {
      const sheets = await readWorkbook(files[0]);
      const r = parsePnl(sheets);
      if (!r.trades.length) throw new Error("No trades found. Upload the broker's Tax P&L for FY 2025-26 (Excel), or enter LTCG manually.");
      openModal("pnl", r, { fileName: files[0].name });
      track("pnl_parsed", { trades: r.trades.length });
    } catch (e) { toast(e.message); }
  }
  if (kind === "slip") {
    M.slipStatus = "Reading the salary slip…"; renderModal();
    try {
      const res = await extractItems(files[0], { onStatus: (s) => { M.slipStatus = s; const el = $("#slip-status"); if (el) el.textContent = s; } });
      M.slip = parseSlip(res.items);
      M.draft.slipMonths = M.draft.slipMonths || 12;
      M.slipStatus = Object.keys(M.slip.components).length ? `Found ${Object.keys(M.slip.components).length} components.` : "Could not find salary components — please enter them head-wise.";
    } catch (e) { M.slipStatus = e.message; }
    renderModal();
  }
}

document.addEventListener("click", async (e) => {
  const b = e.target.closest("[data-action]");
  if (!b) return;
  const a = b.dataset.action, i = b.dataset.i;
  const o = S.onboarding;
  try {
    switch (a) {
      case "sample": {
        const res = await fetch(new URL("samples/" + b.dataset.file, document.baseURI));
        const blob = await res.blob();
        const type = b.dataset.file.endsWith(".pdf") ? "application/pdf" : b.dataset.file.endsWith(".png") ? "image/png" : "text/csv";
        await handleUpload(b.dataset.kind, [new File([blob], b.dataset.file, { type })]);
        break;
      }
      case "goto": S.step = Number(b.dataset.step); render(); window.scrollTo({ top: 0, behavior: "smooth" }); break;
      case "next": S.step = Math.min(5, S.step + 1); if (S.step === 3) seedFromPrefillIfNeeded(); render(); window.scrollTo({ top: 0, behavior: "smooth" }); break;
      case "prev": S.step = Math.max(1, S.step - 1); render(); window.scrollTo({ top: 0, behavior: "smooth" }); break;
      case "verify-pan": {
        o.panError = "";
        if (!S.personal.dob) throw Object.assign(new Error("Enter your date of birth."), { field: "pan" });
        const r = await api.verifyPan(S.personal.pan, S.personal.dob);
        Object.assign(o, { panVerified: true, aadhaarMasked: r.aadhaarMasked, mobileMasked: r.mobileMasked });
        S.personal.name = r.name; track("itr_pan_verified"); render(); break;
      }
      case "change-pan": S = { ...blank(), personal: { ...blank().personal, pan: S.personal.pan, dob: S.personal.dob } }; render(); break;
      case "send-otp1": { const r = await api.addClient(S.personal.pan); o.otp1 = { sent: true, txnId: r.txnId }; render(); break; }
      case "verify-otp1": { const otp = $('[data-otp="1"]').value.trim(); try { await api.validateClientOtp(o.otp1.txnId, otp); o.otp1.verified = true; o.otp1.error = ""; track("itr_client_added"); } catch (err) { o.otp1.error = err.message; } render(); break; }
      case "send-otp2": { const r = await api.requestPrefillOtp(S.personal.pan); o.otp2 = { sent: true, txnId: r.txnId }; render(); break; }
      case "verify-otp2": {
        const otp = $('[data-otp="2"]').value.trim();
        try { const pf = await api.getPrefill(o.otp2.txnId, otp, S.personal.pan); importPrefill(pf); o.otp2.verified = true; o.otp2.error = ""; o.imported = true; track("itr_prefill_imported"); }
        catch (err) { o.otp2.error = err.message; }
        render(); break;
      }
      case "no-form16": S.noForm16 = true; seedFromPrefillIfNeeded(); S.step = 3; render(); openSalaryModal(S.salary.employers.length ? 0 : "new"); break;
      case "remove-f16": { const f = S.form16s[i]; if (f.empId) S.salary.employers = S.salary.employers.filter((x) => x.id !== f.empId); S.form16s.splice(i, 1); render(); break; }
      case "apply-f16": applyForm16(Number(i)); break;
      case "salary-modal": openSalaryModal(i); break;
      case "pension-modal": openModal("pension", { isPension: true, name: "", tan: "", exemptions: {}, tds: 0 }); break;
      case "family-pension": closeModal(); openModal("os", { type: "familyPension", amount: "" }); break;
      case "remove-emp": S.salary.employers.splice(i, 1); render(); break;
      case "hp-modal": openModal("hp", i === "new" ? { type: "let", sharePct: 100 } : structuredClone(S.houseProperties[i]), { index: i }); break;
      case "remove-hp": S.houseProperties.splice(i, 1); render(); break;
      case "ltcg-modal": openModal("ltcg", { saleValue: S.ltcg112a.saleValue || "", costOfAcquisition: S.ltcg112a.costOfAcquisition || "" }); break;
      case "os-modal": openModal("os", { type: OS_TYPES[5][0], amount: "" }); break;
      case "remove-os": S.otherSources.others.splice(i, 1); render(); break;
      case "challan-modal": openModal("challan", { kind: "selfAssessment", date: today(), amount: "" }); break;
      case "remove-challan": S.taxes[b.dataset.kind].splice(i, 1); render(); break;
      case "remove-tds": S.taxes.tdsOther.splice(i, 1); render(); break;
      case "refund-bank": S.bankAccounts.forEach((x, k) => (x.refund = k === Number(i))); save(); break;
      case "close-modal": closeModal(); break;
      case "mtab": M.tab = b.dataset.tab; renderModal(); break;
      case "hra-calc": M.hra = true; M.draft.hra ||= { received: n(M.draft.components?.hraReceived), basic: n(M.draft.components?.basic) + n(M.draft.components?.da) }; renderModal(); break;
      case "use-hra": set(M.draft, "exemptions.hra", Math.round(hraExempt(M.draft.hra))); M.hra = false; renderModal(); break;
      case "apply-slip": {
        const m = n(M.draft.slipMonths) || 12, c = M.slip.components, g = (k) => n(c[k]?.value) * m;
        M.draft.components = { basic: g("basic"), da: g("da"), hraReceived: g("hra"), special: g("special"), bonus: g("bonus"), ltaReceived: g("lta"), conveyance: g("conveyance") + g("medical") };
        M.draft.s17_1 = COMP.reduce((a, [k]) => a + n(M.draft.components[k]), 0);
        if (c.profTax) M.draft.profTax = Math.min(2500, g("profTax"));
        if (c.tds) M.draft.tds = g("tds");
        if (c.employerNps) S.deductions.s80ccd2 = g("employerNps");
        if (!S.deductions.basicPlusDA) S.deductions.basicPlusDA = g("basic") + g("da");
        M.draft.source = M.draft.source === "form16" ? "form16" : "slip";
        M.tab = "manual"; renderModal(); break;
      }
      case "save-salary": {
        const d = M.draft;
        if (!n(d.s17_1) && !n(d.s17_2)) { toast("Enter the salary amount."); break; }
        d.tan = (d.tan || "").toUpperCase();
        if (M.index === "new") S.salary.employers.push({ id: uid(), source: d.source || "manual", ...d }); else S.salary.employers[M.index] = d;
        closeModal(); render(); break;
      }
      case "save-pension": {
        const d = M.draft; if (!n(d.s17_1) && !n(d.commutedReceived)) { toast("Enter the pension amount."); break; }
        d.s17_1 = n(d.s17_1) + n(d.commutedReceived); d.name ||= "Pension"; d.source = "manual";
        S.salary.employers.push({ id: uid(), ...d }); closeModal(); render(); break;
      }
      case "save-hp": {
        const d = M.draft;
        if (d.type !== "self" && !n(d.rent)) { toast("Enter the annual rent."); break; }
        if (M.index === "new") S.houseProperties.push(d); else S.houseProperties[M.index] = d;
        closeModal(); render(); break;
      }
      case "save-ltcg": Object.assign(S.ltcg112a, { saleValue: n(M.draft.saleValue), costOfAcquisition: n(M.draft.costOfAcquisition), source: "Entered manually", mode: "values" }); closeModal(); render(); break;
      case "use-pnl": {
        const s = M.draft.summary;
        Object.assign(S.ltcg112a, { saleValue: s.ltcg112a.saleValue, costOfAcquisition: s.ltcg112a.costOfAcquisition, stcg: s.stcg, otherCG: !!(s.intraday || s.fno), source: `Broker Tax P&L: ${M.fileName}`, mode: "values" });
        closeModal(); render(); break;
      }
      case "save-os": {
        const d = M.draft; const amt = n(d.amount); if (!amt) { toast("Enter the amount."); break; }
        if (d.type.startsWith("other:")) S.otherSources.others.push({ label: d.type === "other:Any other income" ? d.label || "Other income" : d.type.slice(6), payer: d.payer || "", amount: amt });
        else S.otherSources[d.type] = n(S.otherSources[d.type]) + amt;
        if (n(d.tds)) S.taxes.tdsOther.push({ deductor: d.payer || "Deductor", tan: "", section: "", amountPaid: amt, tds: n(d.tds) });
        closeModal(); render(); break;
      }
      case "save-challan": {
        const d = M.draft; if (!n(d.amount) || !d.date) { toast("Enter the date and amount."); break; }
        S.taxes[d.kind].push({ date: d.date, bsr: d.bsr || "", challan: d.challan || "", amount: n(d.amount) }); closeModal(); render(); break;
      }
      case "create-computation": S.computed = true; track("itr_computation_created"); render(); break;
      case "download-pdf": { const fn = await downloadComputationPdf(data(), calc()); track("itr_computation_pdf", { file: fn }); break; }
      case "download-json": {
        const json = buildItr1Json(data(), calc());
        const blob = new Blob([JSON.stringify(json, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob); const link = Object.assign(document.createElement("a"), { href: url, download: `ITR1_${S.personal.pan}_AY2026-27.json` }); link.click(); URL.revokeObjectURL(url);
        track("itr_json_download"); break;
      }
      case "file-now": openModal("file", { agree: false, place: "" }); track("itr_file_now"); break;
      case "paid-add-challan": closeModal(); S.step = 4; render(); openModal("challan", { kind: "selfAssessment", date: today(), amount: calc().payable }); break;
      case "submit-return": {
        M.draft.busy = true; renderModal();
        const r = await api.submitReturn(buildItr1Json(data(), calc()));
        S.filing = { ackNo: r.ackNo, filedOn: r.filedOn };
        await api.requestEVerifyOtp(r.ackNo);
        M.draft = { stage: "verify" }; renderModal(); render(); track("itr_submitted"); break;
      }
      case "everify": {
        const otp = $('[data-otp="ev"]').value.trim();
        try { const r = await api.eVerify(S.filing.ackNo, otp); Object.assign(S.filing, { verified: true, verifiedOn: r.verifiedOn }); closeModal(); render(); track("itr_everified"); }
        catch (err) { M.draft.error = err.message; renderModal(); }
        break;
      }
      case "reset":
        if (b.dataset.armed) { S = blank(); render(); toast("Started a new return."); }
        else { b.dataset.armed = "1"; b.textContent = "Click again to clear this draft"; setTimeout(() => { if (b.isConnected) { delete b.dataset.armed; b.textContent = "Start a new return"; } }, 4000); }
        break;
    }
  } catch (err) {
    if (a === "verify-pan") { o.panError = err.message; render(); } else toast(err.message);
  }
});

function openSalaryModal(i) {
  const d = i === "new" || i === undefined ? { name: "", tan: "", components: {}, exemptions: {}, s17_1: "", s17_2: "", s17_3: "", profTax: "", entAllow: "", tds: "" } : structuredClone(S.salary.employers[i]);
  d.components ||= {}; d.exemptions ||= {};
  openModal("salary", d, { index: i === undefined ? "new" : i, tab: "manual" });
}

function importPrefill(pf) {
  S.prefill = pf;
  Object.assign(S.personal, { ...pf.personal, pan: S.personal.pan, dob: S.personal.dob || pf.personal.dob });
  S.bankAccounts = pf.bankAccounts.map((b) => ({ ...b }));
  const sumA = (arr) => (arr || []).reduce((a, x) => a + n(x.amount), 0);
  S.otherSources.savingsInterest = sumA(pf.ais.savingsInterest);
  S.otherSources.depositInterest = sumA(pf.ais.depositInterest);
  S.otherSources.dividend = sumA(pf.ais.dividend);
  S.otherSources.refundInterest = sumA(pf.ais.refundInterest);
  S.taxes.tdsOther = (pf.tdsOther || []).map((t) => ({ ...t }));
  S.taxes.tcs = (pf.tcs || []).map((t) => ({ ...t }));
}
function seedFromPrefillIfNeeded() {
  // No Form 16 uploaded: start from Form 26AS salary (amount paid and TDS) so the user only adds the break-up.
  if (S.salary.employers.length || !S.prefill) return;
  for (const t of S.prefill.tdsSalary || []) S.salary.employers.push({ id: uid(), name: t.employer, tan: t.tan, s17_1: t.amountPaid, s17_2: 0, s17_3: 0, components: {}, exemptions: {}, tds: t.tds, source: "ais" });
}

render();
window.__befItr = { get state() { return S; }, calc, debug: { extractItems, toLines, parseForm16, OCR_OPTS } };
