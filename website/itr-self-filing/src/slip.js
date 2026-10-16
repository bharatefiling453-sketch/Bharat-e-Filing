// Salary slip reader (PDF text layer or OCR). Pairs each component label with the amount that follows it on
// the same line, so two-column slips (earnings | deductions) are read correctly. Values are monthly unless
// the slip shows year-to-date figures; the user confirms the number of months before annualising.
import { toLines, parseAmount } from "./pdftext.js";

const MAP = [
  ["basic", /^basic( salary| pay)?$/i],
  ["da", /^(da|dearness allowance)$/i],
  ["hra", /^(hra|house rent allowance)$/i],
  ["special", /^(special|spl\.?|other) allowance$/i],
  ["conveyance", /^conveyance( allowance)?$/i],
  ["lta", /^(lta|leave travel (allowance|concession))$/i],
  ["bonus", /^(bonus|performance (bonus|pay)|incentive)s?$/i],
  ["medical", /^medical( allowance)?$/i],
  ["employerNps", /^(employer('s)? )?nps( contribution)?( \(employer\))?$/i],
  ["gross", /^(gross (earnings|salary|pay)|total earnings)$/i],
  ["pf", /^(pf|provident fund|epf|employee pf)$/i],
  ["profTax", /^(pt|prof(essional)?\.? tax)$/i],
  ["tds", /^(tds|income tax|i\.?\s*tax)$/i],
  ["totalDeductions", /^total deductions$/i],
  ["net", /^net (pay|salary|take home)/i],
];

export function parseSlip(items) {
  const lines = toLines(items);
  const found = {};
  let monthText = null;
  for (const l of lines) {
    const mt = l.text.match(/(january|february|march|april|may|june|july|august|september|october|november|december)[\s,-]*(20\d{2})/i);
    if (mt && !monthText) monthText = `${mt[1]} ${mt[2]}`;
    // walk items: label words accumulate until an amount appears
    let label = [];
    for (const it of l.items) {
      const v = parseAmount(it.str);
      if (v === null) { label.push(it.str); continue; }
      const text = label.join(" ").replace(/[:₹]|rs\.?/gi, "").trim();
      label = [];
      if (!text) continue;
      const hit = MAP.find(([, re]) => re.test(text));
      if (hit && found[hit[0]] === undefined) found[hit[0]] = { value: v, label: text, ocr: !!it.ocr, conf: it.conf ?? 100 };
    }
  }
  const f = (k) => found[k]?.value || 0;
  const earnings = ["basic", "da", "hra", "special", "conveyance", "lta", "bonus", "medical"].reduce((a, k) => a + f(k), 0);
  const checks = [];
  if (found.gross) checks.push({ ok: Math.abs(found.gross.value - earnings) <= 1, text: `Components add up to gross (${earnings} vs ${found.gross.value})` });
  if (found.totalDeductions) {
    const ded = f("pf") + f("profTax") + f("tds");
    checks.push({ ok: Math.abs(found.totalDeductions.value - ded) <= 1, text: `Deductions add up (${ded} vs ${found.totalDeductions.value})` });
  }
  return { components: found, month: monthText, earnings, checks, allOk: checks.every((c) => c.ok) && Object.values(found).every((x) => !x.ocr || x.conf >= 85) };
}
