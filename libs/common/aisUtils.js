/**
 * Parse Indian-formatted amount strings like "7,45,778.00" → 745778
 * @param {string|number} s
 * @returns {number}
 */
export function parseAmt(s) {
  if (typeof s === "number") return s;
  return parseFloat((s || "0").replace(/,/g, "")) || 0;
}

/**
 * Walks partB.sections[].elements[].l2.columnData and sums the Amount column
 * for all rows whose "Information Category Code" matches any of the given codes.
 * Supports ignoring elements from specific l1Src to avoid duplicate calculations.
 * @param {Object} ais - Parsed AIS JSON
 * @param {string[]} catCodes - e.g. ["SAL"], ["INS"], ["IND", "TDN"], ["DIV"]
 * @param {string[]} [ignoreL1Src] - Sources to ignore (e.g. ["AIS_TDS_ANNEX2", "AIS_TDS_TCS"])
 * @returns {number}
 */
export function sumAisCatCodes(ais, catCodes, ignoreL1Src = []) {
  if (!ais?.partB?.sections) return 0;
  let total = 0;
  const codeSet = new Set(catCodes);
  const ignoreSet = new Set(ignoreL1Src);
  for (const sec of ais.partB.sections) {
    if (!Array.isArray(sec.elements)) continue;
    for (const el of sec.elements) {
      if (ignoreSet.has(el.l1Src)) continue;
      if (!el.l2?.columnLabel || !el.l2?.columnData) continue;
      const cols = el.l2.columnLabel;
      const amtIdx = cols.indexOf("Amount");
      const catCodeIdx = cols.indexOf("Information Category Code");
      if (amtIdx === -1 || catCodeIdx === -1) continue;
      for (const row of el.l2.columnData) {
        if (codeSet.has(row[catCodeIdx])) {
          total += parseAmt(row[amtIdx]);
        }
      }
    }
  }
  return total;
}
