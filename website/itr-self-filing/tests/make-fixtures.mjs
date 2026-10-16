// Generates test fixtures: a digital Form 16 PDF (TRACES-style layout), a scanned (image-only) copy,
// a salary slip image and a broker tax P&L workbook.   node itr-self-filing/tests/make-fixtures.mjs
import { chromium } from "playwright";
import { writeFileSync } from "node:fs";
import * as XLSX from "xlsx";
const OUT = new URL("./fixtures/", import.meta.url).pathname;

const r = (v) => (v === "" ? "" : Number(v).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
const rowB = (no, label, inner = "", outer = "") => `<tr><td class="no">${no}</td><td>${label}</td><td class="amt">${inner === "" ? "" : r(inner)}</td><td class="amt">${outer === "" ? "" : r(outer)}</td></tr>`;
const css = `body{font-family:"Times New Roman",serif;font-size:11px;margin:28px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #333;padding:3px 5px;vertical-align:top}
.amt{text-align:right;width:95px}.no{width:28px}h2{text-align:center;font-size:13px;margin:4px 0}.pb{page-break-before:always}`;

const partA = `<h2>FORM NO. 16</h2><p style="text-align:center">[See rule 31(1)(a)]</p><h2>PART A</h2>
<p style="text-align:center">Certificate under Section 203 of the Income-tax Act, 1961 for tax deducted at source on salary paid to an employee under section 192</p>
<table><tr><td>Certificate No. XKQWERT</td><td>Last updated on 12-Jun-2026</td></tr>
<tr><th>Name and address of the Employer/Specified Bank</th><th>Name and address of the Employee/Specified senior citizen</th></tr>
<tr><td>ACME SOFTWARE PRIVATE LIMITED<br>4TH FLOOR, TECH PARK, ANDHERI EAST, MUMBAI - 400069 Maharashtra</td><td>RAHUL KUMAR SHARMA<br>B-12, GREEN AVENUE, PUNE - 411001 Maharashtra</td></tr></table>
<table><tr><th>PAN of the Deductor</th><th>TAN of the Deductor</th><th>PAN of the Employee/Specified senior citizen</th><th>Employee Reference No.</th></tr>
<tr><td>AAACA1234C</td><td>MUMA12345B</td><td>ABCPS1234K</td><td>E1043</td></tr></table>
<table><tr><th>CIT (TDS)</th><th>Assessment Year</th><th>Period with the Employer From</th><th>To</th></tr>
<tr><td>The Commissioner of Income Tax (TDS), Mumbai</td><td>2026-27</td><td>01-Apr-2025</td><td>31-Mar-2026</td></tr></table>
<h2>Summary of amount paid/credited and tax deducted at source thereon in respect of the employee</h2>
<table><tr><th>Quarter(s)</th><th>Receipt Numbers of original quarterly statements of TDS under sub-section (3) of Section 200</th><th>Amount paid/credited</th><th>Amount of tax deducted (Rs.)</th><th>Amount of tax deposited/remitted (Rs.)</th></tr>
<tr><td>Q1</td><td>QVBNMKLO</td><td class="amt">${r(364000)}</td><td class="amt">${r(20709)}</td><td class="amt">${r(20709)}</td></tr>
<tr><td>Q2</td><td>QVBNMKLP</td><td class="amt">${r(364000)}</td><td class="amt">${r(20709)}</td><td class="amt">${r(20709)}</td></tr>
<tr><td>Q3</td><td>QVBNMKLQ</td><td class="amt">${r(364000)}</td><td class="amt">${r(20709)}</td><td class="amt">${r(20709)}</td></tr>
<tr><td>Q4</td><td>QVBNMKLR</td><td class="amt">${r(364000)}</td><td class="amt">${r(20709)}</td><td class="amt">${r(20709)}</td></tr>
<tr><td>Total (Rs.)</td><td></td><td class="amt">${r(1456000)}</td><td class="amt">${r(82836)}</td><td class="amt">${r(82836)}</td></tr></table>`;

const partB = `<div class="pb"></div><h2>FORM NO. 16</h2><h2>PART B</h2><p style="text-align:center">Annexure</p>
<table><tr><th colspan="4">Details of Salary Paid and any other income and tax deducted</th></tr>
<tr><td class="no">A</td><td>Whether opting out of taxation u/s 115BAC(1A)?</td><td></td><td>No</td></tr>
${rowB("1.", "Gross Salary")}
${rowB("(a)", "Salary as per provisions contained in section 17(1)", 1420000)}
${rowB("(b)", "Value of perquisites under section 17(2) (as per Form No. 12BA, wherever applicable)", 36000)}
${rowB("(c)", "Profits in lieu of salary under section 17(3) (as per Form No. 12BA, wherever applicable)", 0)}
${rowB("(d)", "Total", "", 1456000)}
${rowB("(e)", "Reported total amount of salary received from other employer(s)", "", 0)}
${rowB("2.", "Less: Allowances to the extent exempt under section 10")}
${rowB("(a)", "Travel concession or assistance under section 10(5)", 0)}
${rowB("(b)", "Death-cum-retirement gratuity under section 10(10)", 0)}
${rowB("(c)", "Commuted value of pension under section 10(10A)", 0)}
${rowB("(d)", "Cash equivalent of leave salary encashment under section 10(10AA)", 0)}
${rowB("(e)", "House rent allowance under section 10(13A)", 0)}
${rowB("(f)", "Other special allowances under section 10(14)", 0)}
${rowB("(g)", "Amount of any other exemption under section 10 [Note: Break-up to be filled and signed by employer in the table provide at the bottom of this form]", 0)}
${rowB("(h)", "Total amount of any other exemption under section 10", 0)}
${rowB("(i)", "Total amount of exemption claimed under section 10 [2(a)+2(b)+2(c)+2(d)+2(e)+2(f)+2(h)]", "", 0)}
${rowB("3.", "Total amount of salary received from current employer [1(d)-2(i)]", "", 1456000)}
${rowB("4.", "Less: Deductions under section 16")}
${rowB("(a)", "Standard deduction under section 16(ia)", 75000)}
${rowB("(b)", "Entertainment allowance under section 16(ii)", 0)}
${rowB("(c)", "Tax on employment under section 16(iii)", 0)}
${rowB("5.", "Total amount of deductions under section 16 [4(a)+4(b)+4(c)]", "", 75000)}
${rowB("6.", "Income chargeable under the head \"Salaries\" [(3+1(e)-5]", "", 1381000)}
${rowB("7.", "Add: Any other income reported by the employee under as per section 192 (2B)")}
${rowB("(a)", "Income (or admissible loss) from house property reported by employee offered for TDS", 0)}
${rowB("(b)", "Income under the head Other Sources offered for TDS", 0)}
${rowB("8.", "Total amount of other income reported by the employee [7(a)+7(b)]", "", 0)}
${rowB("9.", "Gross total income (6+8)", "", 1381000)}
${rowB("10.", "Deductions under Chapter VI-A")}
${rowB("(a)", "Deduction in respect of life insurance premia, contributions to provident fund etc. under section 80C", 0)}
${rowB("(b)", "Deduction in respect of contribution to certain pension funds under section 80CCC", 0)}
${rowB("(c)", "Deduction in respect of contribution by taxpayer to pension scheme under section 80CCD (1)", 0)}
${rowB("(d)", "Total deduction under section 80C, 80CCC and 80CCD(1)", 0)}
${rowB("(e)", "Deductions in respect of amount paid/deposited to notified pension scheme under section 80CCD (1B)", 0)}
${rowB("(f)", "Deduction in respect of contribution by Employer to pension scheme under section 80CCD (2)", 50000)}
${rowB("(g)", "Deduction in respect of health insurance premia under section 80D", 0)}
${rowB("(h)", "Deduction in respect of interest on loan taken for higher education under section 80E", 0)}
${rowB("(i)", "Deduction in respect of contribution by the employee to Agnipath Scheme under section 80CCH", 0)}
${rowB("(j)", "Deduction in respect of contribution by the Central Government to Agnipath Scheme under section 80CCH", 0)}
${rowB("(k)", "Total Deduction in respect of donations to certain funds, charitable institutions, etc. under section 80G", 0)}
${rowB("(l)", "Deduction in respect of interest on deposits in savings account under section 80TTA", 0)}
${rowB("(m)", "Amount Deductible under any other provision (s) of Chapter VI-A [Note: Break-up to be filled and signed by employer in the table provide at the bottom of this form]", 0)}
${rowB("(n)", "Total of amount deductible under any other provision(s) of Chapter VI-A", 0)}
${rowB("11.", "Aggregate of deductible amount under Chapter VI-A [10(d)+10(e)+10(f)+10(g)+10(h)+10(i)+10(j)+10(k)+10(l)+10(n)]", "", 50000)}
${rowB("12.", "Total taxable income (9-11)", "", 1331000)}
${rowB("13.", "Tax on total income", "", 79650)}
${rowB("14.", "Rebate under section 87A, if applicable", "", 0)}
${rowB("15.", "Surcharge, wherever applicable", "", 0)}
${rowB("16.", "Health and education cess", "", 3186)}
${rowB("17.", "Tax payable (13+15+16-14)", "", 82836)}
${rowB("18.", "Less: Relief under section 89 (attach details)", "", 0)}
${rowB("19.", "Less: Tax deducted at source as per Form No. 12BAA submitted under provisions of section 192(2B)", "", 0)}
${rowB("20.", "Less: Tax collected at source as per Form No. 12BAA submitted under provisions of section 192(2B)", "", 0)}
${rowB("21.", "Net tax payable (17-18-19-20)", "", 82836)}
</table>`;

const f12 = `<div class="pb"></div><h2>FORM NO. 12BA</h2><p style="text-align:center">[See rule 26A(2)(b)]</p>
<p>Statement showing particulars of perquisites, other fringe benefits or amenities and profits in lieu of salary with value thereof</p>
<table><tr><th>S. No.</th><th>Nature of perquisites</th><th>Value of perquisite as per rules (Rs.)</th><th>Amount, if any, recovered from the employee (Rs.)</th><th>Amount of perquisite chargeable to tax Col. (3) - Col. (4) (Rs.)</th></tr>
${[["1", "Accommodation", 0], ["2", "Cars/Other automotive", 21600], ["3", "Sweeper, gardener, watchman or personal attendant", 0], ["4", "Gas, electricity, water", 0], ["5", "Interest free or concessional loans", 0], ["6", "Holiday expenses", 0], ["7", "Free or concessional travel", 0], ["8", "Free meals", 14400], ["9", "Free education", 0], ["10", "Gifts, vouchers, etc.", 0]]
  .map(([a, b, c]) => `<tr><td>${a}</td><td>${b}</td><td class="amt">${r(c)}</td><td class="amt">${r(0)}</td><td class="amt">${r(c)}</td></tr>`).join("")}
<tr><td>21</td><td>Total value of perquisites</td><td class="amt">${r(36000)}</td><td class="amt">${r(0)}</td><td class="amt">${r(36000)}</td></tr>
<tr><td>22</td><td>Total value of profits in lieu of salary as per section 17(3)</td><td class="amt">${r(0)}</td><td class="amt">${r(0)}</td><td class="amt">${r(0)}</td></tr></table>`;

const slip = `<div style="font-family:Arial;font-size:15px;width:760px;padding:24px;background:#fff"><h2 style="font-size:20px">ACME SOFTWARE PRIVATE LIMITED</h2><p>Payslip for the month of March 2026</p>
<table style="width:100%;font-size:15px"><tr><th>Earnings</th><th>Amount</th><th>Deductions</th><th>Amount</th></tr>
<tr><td>Basic Salary</td><td style="text-align:right">50,000.00</td><td>Provident Fund</td><td style="text-align:right">6,000.00</td></tr>
<tr><td>House Rent Allowance</td><td style="text-align:right">25,000.00</td><td>Professional Tax</td><td style="text-align:right">200.00</td></tr>
<tr><td>Special Allowance</td><td style="text-align:right">38,333.00</td><td>Income Tax</td><td style="text-align:right">6,903.00</td></tr>
<tr><td>Leave Travel Allowance</td><td style="text-align:right">5,000.00</td><td></td><td></td></tr>
<tr><td><b>Gross Earnings</b></td><td style="text-align:right"><b>1,18,333.00</b></td><td><b>Total Deductions</b></td><td style="text-align:right"><b>13,103.00</b></td></tr></table><p><b>Net Pay: 1,05,230.00</b></p></div>`;

const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage();
await p.setContent(`<style>${css}</style>${partA}${partB}${f12}`);
await p.pdf({ path: OUT + "form16-digital.pdf", format: "A4", printBackground: true });
// scanned copy: screenshot each page area as an image, then make an image-only PDF
const shots = [];
for (const [i, html] of [partA, partB, f12].entries()) {
  const q = await b.newPage({ viewport: { width: 900, height: 1270 }, deviceScaleFactor: 2 });
  await q.setContent(`<style>${css}body{background:#fff}</style>${html.replace('<div class="pb"></div>', "")}`);
  shots.push((await q.screenshot({ fullPage: true })).toString("base64"));
}
await p.setContent(`<style>@page{margin:0}body{margin:0}img{width:100%;display:block;page-break-after:always}</style>${shots.map((s) => `<img src="data:image/png;base64,${s}">`).join("")}`);
await p.pdf({ path: OUT + "form16-scanned.pdf", format: "A4" });
const sp = await b.newPage({ viewport: { width: 820, height: 600 }, deviceScaleFactor: 2 });
await sp.setContent(slip);
await sp.locator("div").first().screenshot({ path: OUT + "salary-slip.png" });
await b.close();

// broker tax P&L (Zerodha-like layout: sections inside one Equity sheet)
const rows = [
  ["Tax P&L Statement for Equity from 2025-04-01 to 2026-03-31"], [],
  ["Short Term Trades"],
  ["Symbol", "ISIN", "Entry Date", "Exit Date", "Quantity", "Buy Value", "Sell Value", "Profit", "Period of Holding", "Fair Market Value", "Taxable Profit"],
  ["TCS", "INE467B01029", "2025-06-10", "2025-11-20", 10, 34000, 36500, 2500, 163, "", 2500],
  [],
  ["Long Term Trades"],
  ["Symbol", "ISIN", "Entry Date", "Exit Date", "Quantity", "Buy Value", "Sell Value", "Profit", "Period of Holding", "Fair Market Value", "Taxable Profit"],
  ["INFY", "INE009A01021", "2017-05-02", "2025-08-14", 40, 19000, 62000, 43000, 3026, 41000, 21000],
  ["HDFCBANK", "INE040A01034", "2022-03-15", "2025-12-01", 30, 42000, 58500, 16500, 1357, "", 16500],
];
const wb = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(rows), "Equity");
XLSX.writeFile(wb, OUT + "broker-tax-pnl.xlsx");
const wb2 = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(wb2, XLSX.utils.aoa_to_sheet([rows[6], rows[7], rows[8], rows[9]]), "Equity");
XLSX.writeFile(wb2, OUT + "broker-tax-pnl-ltcg-only.xlsx");
console.log("fixtures written");
