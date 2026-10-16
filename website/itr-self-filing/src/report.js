// Computation of Total Income — downloadable PDF (CA-style statement). Uses jsPDF + autoTable (loaded on demand).
const inr = (v) => (Math.round(Number(v) || 0) < 0 ? "-" : "") + "Rs. " + Math.abs(Math.round(Number(v) || 0)).toLocaleString("en-IN");

export function computationRows(data, c) {
  const rows = [];
  const H = (t) => rows.push({ head: t });
  const L = (t, a = "", b = "") => rows.push({ t, a, b });
  H("1. Income from Salaries");
  for (const e of c.salary.rows) {
    L(`${e.isPension ? "Pension" : "Salary"} — ${e.name}${e.tan ? " (" + e.tan + ")" : ""}`, inr(e.gross));
    if (e.exempt) L("   Less: Allowances exempt u/s 10", inr(-e.exempt));
  }
  L("Net salary", "", inr(c.salary.net));
  L("Less: Standard deduction u/s 16(ia)", inr(-c.salary.standardDeduction));
  if (c.salary.entAllow) L("Less: Entertainment allowance u/s 16(ii)", inr(-c.salary.entAllow));
  if (c.salary.profTax) L("Less: Professional tax u/s 16(iii)", inr(-c.salary.profTax));
  L("Income chargeable under the head Salaries", "", inr(c.salary.income));
  H("2. Income from House Property");
  if (!c.houseProperty.rows.length) L("No house property", "", inr(0));
  c.houseProperty.rows.forEach((h, i) => {
    const kind = h.type === "self" ? "Self-occupied" : h.type === "deemed" ? "Deemed let-out" : "Let-out";
    L(`Property ${i + 1}: ${kind}${h.address ? " — " + h.address : ""}`);
    if (h.type !== "self") {
      L("   Gross annual value (rent)", inr(h.gav));
      L("   Less: Municipal taxes paid", inr(-(h.gav - h.annualValue)));
      L("   Net annual value", inr(h.annualValue));
      L("   Less: Standard deduction u/s 24(a) @ 30%", inr(-h.standard30));
    }
    L("   Less: Interest on borrowed capital u/s 24(b)", inr(-h.interestClaimed));
    L("   Income from this property", "", inr(h.income));
  });
  L("Income chargeable under the head House Property", "", inr(c.houseProperty.income));
  H("3. Capital Gains");
  L("Long-term capital gains u/s 112A (listed equity / equity funds)", "", inr(c.ltcg112a.gain));
  if (c.ltcg112a.gain) L("   Exempt up to Rs. 1,25,000 (tax nil within ITR-1 limit)", inr(c.ltcg112a.exempt));
  H("4. Income from Other Sources");
  c.otherSources.items.forEach(([label, amt]) => L(label, inr(amt)));
  if (c.otherSources.familyPensionDeduction) L("Less: Deduction u/s 57(iia) on family pension", inr(-c.otherSources.familyPensionDeduction));
  L("Income chargeable under the head Other Sources", "", inr(c.otherSources.income));
  H("5. Profits and Gains of Business or Profession");
  L("Not applicable (ITR-1)", "", inr(0));
  H("Gross Total Income");
  L("Gross total income", "", inr(c.grossTotalIncome));
  H("Less: Deductions under Chapter VI-A");
  if (!c.deductions.list.length) L("None claimed", "", inr(0));
  c.deductions.list.forEach((d) => L(`Section ${d.code} — ${d.label}`, inr(d.allowed)));
  L("Total deductions", "", inr(-c.deductions.total));
  H("Total Income (rounded off u/s 288A)");
  L("Total income", "", inr(c.totalIncome));
  H(`Tax Computation — ${c.meta.regime === "new" ? "New tax regime (s.115BAC)" : "Old tax regime"}`);
  L("Tax on total income at slab rates", inr(c.tax.slabTax));
  if (c.tax.tax112A) L("Tax on LTCG u/s 112A @ 12.5%", inr(c.tax.tax112A));
  L("Less: Rebate u/s 87A", inr(-c.tax.rebate87A));
  L("Add: Health and education cess @ 4%", inr(c.tax.cess));
  if (c.tax.relief89) L("Less: Relief u/s 89", inr(-c.tax.relief89));
  L("Net tax liability (rounded off u/s 288B)", "", inr(c.tax.netTax));
  if (c.interest.i234A) L(`Interest u/s 234A (${c.interest.months234A} months)`, inr(c.interest.i234A));
  if (c.interest.i234B) L("Interest u/s 234B", inr(c.interest.i234B));
  if (c.interest.i234C) L("Interest u/s 234C", inr(c.interest.i234C));
  if (c.lateFee) L("Fee for late filing u/s 234F", inr(c.lateFee));
  L("Total tax, interest and fee", "", inr(c.totalLiability));
  H("Less: Taxes Paid");
  L("TDS on salary (Form 16 / 26AS)", inr(c.paid.tdsSalary));
  if (c.paid.tdsOther) L("TDS on other income (26AS)", inr(c.paid.tdsOther));
  if (c.paid.tcs) L("TCS", inr(c.paid.tcs));
  if (c.paid.advance) L("Advance tax", inr(c.paid.advance));
  if (c.paid.selfAssessment) L("Self-assessment tax", inr(c.paid.selfAssessment));
  L("Total taxes paid", "", inr(c.paid.total));
  H(c.refund ? "Refund Due" : c.payable ? "Balance Tax Payable" : "Balance");
  L(c.refund ? "Refund due to you" : c.payable ? "Tax payable before filing (challan 280, self-assessment)" : "Nil — no tax payable or refund", "", inr(c.refund || c.payable || 0));
  return rows;
}

export async function downloadComputationPdf(data, c) {
  const [{ jsPDF }, { default: autoTable }] = await Promise.all([import("jspdf"), import("jspdf-autotable")]);
  const doc = new jsPDF({ unit: "pt", format: "a4" });
  const W = doc.internal.pageSize.getWidth();
  const navy = [16, 33, 97], saffron = [255, 136, 19];
  doc.setFillColor(...navy); doc.rect(0, 0, W, 70, "F");
  doc.setFillColor(...saffron); doc.rect(0, 70, W, 4, "F");
  doc.setTextColor(255, 255, 255); doc.setFont("helvetica", "bold"); doc.setFontSize(18);
  doc.text("Bharat e-Filing", 40, 34);
  doc.setFont("helvetica", "normal"); doc.setFontSize(10);
  doc.text("Computation of Total Income  |  ITR-1 (Sahaj)  |  AY 2026-27", 40, 52);
  const p = data.personal || {};
  doc.setTextColor(30, 30, 30); doc.setFontSize(10);
  const info = [
    ["Name", p.name || "-"], ["PAN", p.pan || "-"], ["Assessment year", "2026-27 (FY 2025-26)"], ["Status", "Individual, Resident"],
    ["Return", `ITR-1 u/s ${c.meta.section}${c.meta.belated ? " (belated)" : ""}`], ["Tax regime", c.meta.regime === "new" ? "New (s.115BAC)" : "Old (opted out)"],
    ["Date of computation", c.meta.filingDate],
  ];
  autoTable(doc, { startY: 90, body: info, theme: "plain", styles: { fontSize: 9.5, cellPadding: 2.5 }, columnStyles: { 0: { fontStyle: "bold", cellWidth: 130 } }, margin: { left: 40, right: 40 } });
  const rows = computationRows(data, c);
  const body = rows.map((r) => (r.head ? [{ content: r.head, colSpan: 3, styles: { fontStyle: "bold", fillColor: [238, 241, 251], textColor: navy } }] : [r.t, r.a, r.b]));
  autoTable(doc, {
    startY: doc.lastAutoTable.finalY + 10, head: [["Particulars", "Amount", "Amount"]], body,
    styles: { fontSize: 9, cellPadding: 4 }, headStyles: { fillColor: navy, textColor: 255 },
    columnStyles: { 1: { halign: "right", cellWidth: 100 }, 2: { halign: "right", cellWidth: 110, fontStyle: "bold" } }, margin: { left: 40, right: 40 },
  });
  let y = doc.lastAutoTable.finalY + 18;
  if (c.warnings.length) {
    doc.setFontSize(9); doc.setTextColor(138, 75, 0);
    c.warnings.forEach((w) => { const t = doc.splitTextToSize("• " + w.text, W - 80); if (y > 780) { doc.addPage(); y = 50; } doc.text(t, 40, y); y += t.length * 12; });
  }
  doc.setFontSize(8); doc.setTextColor(110, 110, 115);
  const foot = "Prepared with Bharat e-Filing self-filing from Form 16, AIS / TIS / Form 26AS and details you entered. Check every figure before filing. This statement is not a substitute for professional advice.";
  doc.text(doc.splitTextToSize(foot, W - 80), 40, Math.min(y + 14, 815));
  const fn = `Computation_${p.pan || "ITR1"}_AY2026-27.pdf`;
  doc.save(fn);
  return fn;
}
