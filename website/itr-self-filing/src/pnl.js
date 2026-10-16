// Broker tax P&L (Excel/CSV) reader for listed equity and equity mutual funds.
// Finds the header row on every sheet, works out each column's meaning, classifies each trade (long-term,
// short-term, intraday, F&O) and applies the 31-Jan-2018 grandfathering rule (s.112A / s.55(2)(ac)).
// Pure: takes an array of sheets ({ name, rows: any[][] }) so it can be tested without a browser.

const COLS = {
  symbol: /^(symbol|scrip|scrip name|security|stock|stock name|instrument|name of (the )?(share|security|scrip)|company)\b/i,
  isin: /\bisin\b/i,
  qty: /^(qty|quantity|units|no\.? of (shares|units))/i,
  buyDate: /(buy|purchase|entry|acquisition|acquired)\s*date|date of (purchase|acquisition)/i,
  sellDate: /(sell|sale|exit|transfer|redemption)\s*date|date of (sale|transfer|redemption)/i,
  buyValue: /(buy|purchase|entry)\s*(value|amount|cost)|cost of acquisition|total buy|purchase price total|^buy (value|amt)/i,
  sellValue: /(sell|sale|exit|redemption)\s*(value|amount|consideration)|full value of consideration|total sell|^sell (value|amt)/i,
  fmv: /fmv|fair market value|31[\s./-]*0?1[\s./-]*2018|grandfather/i,
  pnl: /^(realized|realised)?\s*(p\s*&\s*l|pnl|profit|gain|profit\/loss|p\/l)$/i,
  taxable: /taxable (profit|gain|p&l)|capital gain(s)? (after|post) grandfather/i,
  term: /^(term|type|category|ltcg\/stcg|gain type|nature)$/i,
};

const SECTION = [
  ["intraday", /intraday|speculat/i],
  ["fno", /f\s*&\s*o|futures|options|derivative/i],
  ["long", /long[\s-]*term|ltcg/i],
  ["short", /short[\s-]*term|stcg/i],
];

const toNum = (v) => {
  if (typeof v === "number") return v;
  if (v === null || v === undefined) return 0;
  const s = String(v).replace(/[,₹\s]/g, "").replace(/^\((.*)\)$/, "-$1");
  const x = Number(s);
  return Number.isFinite(x) ? x : 0;
};

export function toDate(v) {
  if (v === null || v === undefined || v === "") return null;
  if (v instanceof Date) return v;
  if (typeof v === "number") return new Date(Math.round((v - 25569) * 86400000)); // Excel serial
  const s = String(v).trim();
  let m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/);
  if (m) return new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
  m = s.match(/^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})$/); // dd-mm-yyyy (Indian format)
  if (m) return new Date(Date.UTC(+m[3] < 100 ? 2000 + +m[3] : +m[3], +m[2] - 1, +m[1]));
  m = s.match(/^(\d{1,2})[-\s]([A-Za-z]{3})[-\s,]*(\d{2,4})$/);
  if (m) return new Date(`${m[1]} ${m[2]} ${+m[3] < 100 ? 2000 + +m[3] : m[3]} UTC`);
  const d = new Date(s);
  return isNaN(d) ? null : d;
}

function headerMap(row) {
  const map = {};
  row.forEach((cell, idx) => {
    const t = String(cell ?? "").trim();
    if (!t) return;
    for (const [key, re] of Object.entries(COLS)) if (map[key] === undefined && re.test(t)) { map[key] = idx; break; }
  });
  const score = Object.keys(map).length;
  const usable = (map.sellValue !== undefined && (map.buyValue !== undefined || map.pnl !== undefined || map.taxable !== undefined)) || map.taxable !== undefined;
  return score >= 3 && usable ? map : null;
}

const GRANDFATHER_DATE = Date.UTC(2018, 1, 1);
const FY_START = Date.UTC(2025, 3, 1), FY_END = Date.UTC(2026, 2, 31, 23, 59, 59);

function monthsHeld(buy, sell) {
  if (!buy || !sell) return null;
  return (sell.getUTCFullYear() - buy.getUTCFullYear()) * 12 + (sell.getUTCMonth() - buy.getUTCMonth()) - (sell.getUTCDate() < buy.getUTCDate() ? 1 : 0);
}

export function parsePnl(sheets) {
  const trades = [];
  const notes = new Set();
  for (const sh of sheets) {
    let section = SECTION.find(([, re]) => re.test(sh.name))?.[0] || null;
    let map = null;
    for (const row of sh.rows) {
      const cells = (row || []).map((c) => (c === null || c === undefined ? "" : c));
      const nonEmpty = cells.filter((c) => String(c).trim() !== "");
      if (!nonEmpty.length) continue;
      const h = headerMap(cells);
      if (h) { map = h; continue; }
      if (nonEmpty.length <= 2 && typeof nonEmpty[0] === "string") {
        const sec = SECTION.find(([, re]) => re.test(nonEmpty[0]));
        if (sec) { section = sec[0]; map = null; }
        continue;
      }
      if (!map) continue;
      const get = (k) => (map[k] === undefined ? undefined : cells[map[k]]);
      const symbol = String(get("symbol") ?? get("isin") ?? "").trim();
      if (!symbol || /^(total|grand total|sub ?total)/i.test(symbol)) continue;
      const buyDate = toDate(get("buyDate")), sellDate = toDate(get("sellDate"));
      const sellValue = toNum(get("sellValue")), buyValue = toNum(get("buyValue"));
      const fmv = toNum(get("fmv"));
      const termCell = String(get("term") ?? "");
      let kind = section;
      const termSec = SECTION.find(([, re]) => re.test(termCell));
      if (termSec) kind = termSec[0];
      const held = monthsHeld(buyDate, sellDate);
      if (!kind) {
        if (buyDate && sellDate && buyDate.getTime() === sellDate.getTime()) kind = "intraday";
        else if (held !== null) kind = held >= 12 && !(held === 12 && sellDate.getUTCDate() === buyDate.getUTCDate()) ? "long" : "short";
        else kind = "unknown";
      }
      // gain: broker's taxable figure first, else grandfathered computation, else P&L column
      let cost = buyValue, gain;
      if (get("taxable") !== undefined && get("taxable") !== "") gain = toNum(get("taxable"));
      else if (kind === "long" && buyDate && buyDate.getTime() < GRANDFATHER_DATE && fmv > 0) {
        cost = Math.max(buyValue, Math.min(fmv, sellValue));
        gain = sellValue - cost;
      } else if (sellValue && (buyValue || get("buyValue") !== undefined)) gain = sellValue - buyValue;
      else gain = toNum(get("pnl"));
      if (kind === "long" && buyDate && buyDate.getTime() < GRANDFATHER_DATE && get("taxable") === undefined && !(fmv > 0)) notes.add(`${symbol}: bought before 1 Feb 2018 but no FMV on 31 Jan 2018 in the file — enter it to apply grandfathering.`);
      if (kind === "long" && get("taxable") !== undefined && buyDate && buyDate.getTime() < GRANDFATHER_DATE && fmv > 0) cost = sellValue - gain;
      if (sellDate && (sellDate.getTime() < FY_START || sellDate.getTime() > FY_END)) notes.add(`${symbol}: sold on ${sellDate.toISOString().slice(0, 10)}, outside FY 2025-26 — excluded.`);
      else trades.push({ sheet: sh.name, symbol, isin: get("isin") || "", qty: toNum(get("qty")), buyDate: buyDate?.toISOString().slice(0, 10) || "", sellDate: sellDate?.toISOString().slice(0, 10) || "", buyValue, sellValue, fmv, cost, gain: Math.round(gain * 100) / 100, kind });
      if (/mutual|mf\b|fund/i.test(sh.name + " " + symbol)) notes.add("Mutual fund rows found: only equity-oriented funds qualify under s.112A. Debt-fund gains need ITR-2.");
    }
  }
  const by = (k) => trades.filter((t) => t.kind === k);
  const sumBy = (arr, f) => Math.round(arr.reduce((a, t) => a + f(t), 0) * 100) / 100;
  const long = by("long");
  const summary = {
    ltcg112a: { saleValue: sumBy(long, (t) => t.sellValue), costOfAcquisition: sumBy(long, (t) => t.cost), gain: sumBy(long, (t) => t.gain), trades: long.length },
    stcg: sumBy(by("short"), (t) => t.gain),
    intraday: sumBy(by("intraday"), (t) => t.gain),
    fno: sumBy(by("fno"), (t) => t.gain),
    unknown: by("unknown").length,
  };
  const itr1 = [];
  if (by("short").length) itr1.push("Short-term capital gains found: ITR-1 cannot be used (ITR-2 needed).");
  if (by("intraday").length || by("fno").length) itr1.push("Intraday or F&O trades found: these are business income, so ITR-3 is needed.");
  if (summary.ltcg112a.gain > 125000) itr1.push("LTCG under s.112A is above ₹1.25 lakh: ITR-2 is needed.");
  if (summary.ltcg112a.gain < 0) itr1.push("Long-term capital loss: it can only be carried forward in ITR-2.");
  if (summary.unknown) itr1.push(`${summary.unknown} row(s) could not be classified as long- or short-term; please check them.`);
  return { trades, summary, notes: [...notes], itr1Issues: itr1 };
}

/** Browser helper: reads an .xlsx/.xls/.csv File into sheets for parsePnl. */
export async function readWorkbook(file) {
  const XLSX = await import("xlsx");
  const wb = XLSX.read(new Uint8Array(await file.arrayBuffer()), { type: "array", cellDates: true });
  return wb.SheetNames.map((name) => ({ name, rows: XLSX.utils.sheet_to_json(wb.Sheets[name], { header: 1, raw: true, defval: "" }) }));
}
