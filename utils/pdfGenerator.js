/**
 * Tax Computation PDF/Print Generator
 * Complies the output JSON with raw document details (AIS, Form 26AS) to generate
 * a highly detailed, professional print-ready Tax Computation Statement.
 */

import taxSlabs from "./taxSlabs.json";

// Helper to format numbers in Indian format (e.g. 6,70,778)
function formatIndianNumber(num) {
  if (num === null || num === undefined || isNaN(num)) return "0";
  const roundNum = Math.round(num);
  const numStr = Math.abs(roundNum).toString();
  const lastThree = numStr.slice(-3);
  const otherNumbers = numStr.slice(0, -3);
  const prefix = roundNum < 0 ? "-" : "";
  if (otherNumbers !== "") {
    return prefix + otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + "," + lastThree;
  }
  return prefix + lastThree;
}

// Extract specific elements from AIS
function extractAisElements(ais, catCodes) {
  const elements = [];
  if (!ais?.partB?.sections) return elements;
  for (const sec of ais.partB.sections) {
    if (!Array.isArray(sec.elements)) continue;
    for (const el of sec.elements) {
      if (!el.l2?.columnLabel || !el.l2?.columnData) continue;
      const l2Cols = el.l2.columnLabel;
      const catCodeIdx = l2Cols.indexOf("Information Category Code");
      if (catCodeIdx === -1) continue;
      const hasCatCode = el.l2.columnData.some(row => catCodes.includes(row[catCodeIdx]));
      if (hasCatCode) {
        elements.push(el);
      }
    }
  }
  return elements;
}

function parseAmt(val) {
  if (!val) return 0;
  if (typeof val === "number") return val;
  const clean = val.replace(/,/g, "").trim();
  return parseFloat(clean) || 0;
}

// Generate the printable HTML view
export function generateTaxComputationHtml(generatedJson, uploadedFiles) {
  const itr1 = generatedJson?.ITR?.ITR1 || {};
  const personal = itr1.PersonalInfo || {};
  const incomeDec = itr1.ITR1_IncomeDeductions || {};
  const taxComp = itr1.ITR1_TaxComputation || {};
  const taxPaid = itr1.TaxPaid || {};
  const refund = itr1.Refund || {};
  const verification = itr1.Verification || {};
  
  const ais = uploadedFiles?.ais;
  const form26as = uploadedFiles?.form26as;

  // Extract Assessee Name
  const assesseeName = [
    personal.AssesseeName?.FirstName,
    personal.AssesseeName?.MiddleName,
    personal.AssesseeName?.SurNameOrOrgName
  ].filter(Boolean).join(" ") || "N/A";

  const resolvedPan = personal.PAN || "N/A";
  const metaDefaults = taxSlabs.defaultFilingMetaData;
  const assessmentYear = generatedJson?.ITR?.ITR1?.Form_ITR1?.AssessmentYear 
    ? `${generatedJson.ITR.ITR1.Form_ITR1.AssessmentYear}-${parseInt(generatedJson.ITR.ITR1.Form_ITR1.AssessmentYear) + 1}` 
    : metaDefaults.assessmentYearFallback;
  const yearEnded = metaDefaults.yearEnded;
  const status = metaDefaults.status;
  const residentialStatus = metaDefaults.residentialStatus;
  const filingStatus = itr1.FilingStatus?.ReturnFileSec === 11 ? metaDefaults.filingStatus : metaDefaults.filingStatus;
  const dob = personal.DOB || "N/A";
  const email = personal.Address?.EmailAddress || "N/A";
  const phone = personal.Address?.MobileNo || "N/A";
  const aadhaar = personal.AadhaarCardNo || "N/A";

  // Build Address
  const addrParts = [
    personal.Address?.ResidenceNo,
    personal.Address?.ResidenceName,
    personal.Address?.RoadOrStreet,
    personal.Address?.LocalityOrArea,
    personal.Address?.CityOrTownOrDistrict,
    personal.Address?.StateCode,
    personal.Address?.PinCode
  ].filter(Boolean);
  const address = addrParts.join(", ") || "N/A";

  // Parse Savings Bank Interest Details from AIS
  const insElements = extractAisElements(ais, ["INS"]);
  const savingsInterestList = [];
  let totalSavingsInterest = 0;
  for (const el of insElements) {
    const l2Cols = el.l2.columnLabel;
    const srcIdx = l2Cols.indexOf("Information Source");
    const sourceName = el.l2.columnData[0]?.[srcIdx] || el.infoSrcId || "Bank";
    let sumAmt = 0;
    if (el.l1?.columnLabel && el.l1?.columnData) {
      const fields = el.l1.columnLabel.map(c => c.field);
      const amtIdx = fields.indexOf("amtPaid");
      const statusIdx = fields.indexOf("status");
      for (const row of el.l1.columnData) {
        if (statusIdx !== -1 && row[statusIdx] === "Inactive") continue;
        sumAmt += parseAmt(row[amtIdx]);
      }
    }
    const cleanName = sourceName.replace(/\([^)]+\)/g, "").trim();
    if (sumAmt > 0) {
      savingsInterestList.push({ name: cleanName, amount: sumAmt });
      totalSavingsInterest += sumAmt;
    }
  }

  // Parse Term Deposit Interest (FDR) Details from AIS
  const indElements = extractAisElements(ais, ["IND", "TDN"]);
  const fdrInterestList = [];
  let totalFdrInterest = 0;
  for (const el of indElements) {
    const l2Cols = el.l2.columnLabel;
    const srcIdx = l2Cols.indexOf("Information Source");
    const sourceName = el.l2.columnData[0]?.[srcIdx] || el.infoSrcId || "Bank/FD Issuer";
    let sumAmt = 0;
    if (el.l1?.columnLabel && el.l1?.columnData) {
      const fields = el.l1.columnLabel.map(c => c.field);
      const amtIdx = fields.indexOf("amtPaid");
      const statusIdx = fields.indexOf("status");
      for (const row of el.l1.columnData) {
        if (statusIdx !== -1 && row[statusIdx] === "Inactive") continue;
        sumAmt += parseAmt(row[amtIdx]);
      }
    }
    const cleanName = sourceName.replace(/\([^)]+\)/g, "").trim();
    if (sumAmt > 0) {
      fdrInterestList.push({ name: cleanName, amount: sumAmt });
      totalFdrInterest += sumAmt;
    }
  }

  // Parse Dividend Details from AIS
  const divElements = extractAisElements(ais, ["DIV"]);
  const dividendList = [];
  let totalDividend = 0;
  for (const el of divElements) {
    if (el.l1Src === "AIS_TDS_TCS") continue;
    const l2Cols = el.l2.columnLabel;
    const srcIdx = l2Cols.indexOf("Information Source");
    const sourceName = el.l2.columnData[0]?.[srcIdx] || el.infoSrcId || "Company";
    let sumAmt = 0;
    if (el.l1?.columnLabel && el.l1?.columnData) {
      const fields = el.l1.columnLabel.map(c => c.field);
      const amtIdx = fields.indexOf("amtPaid") >= 0 ? fields.indexOf("amtPaid") : fields.indexOf("dividendAmount");
      const statusIdx = fields.indexOf("status");
      for (const row of el.l1.columnData) {
        if (statusIdx !== -1 && row[statusIdx] === "Inactive") continue;
        sumAmt += parseAmt(row[amtIdx]);
      }
    }
    const cleanName = sourceName.replace(/\([^)]+\)/g, "").trim();
    if (sumAmt > 0) {
      dividendList.push({ name: cleanName, amount: sumAmt });
      totalDividend += sumAmt;
    }
  }

  // Parse Capital Gain 112A transactions (SOS)
  const sosElements = extractAisElements(ais, ["SOS"]);
  const ltcgTransactions = [];
  let totalSalePrice = 0;
  let totalPurchasePrice = 0;
  let totalGain = 0;
  for (const el of sosElements) {
    if (el.l1?.columnLabel && el.l1?.columnData) {
      const fields = el.l1.columnLabel.map(c => c.field);
      const amcIdx = fields.indexOf("amcNameCode");
      const nameIdx = fields.indexOf("securityName");
      const dateIdx = fields.indexOf("transferDate");
      const qtyIdx = fields.indexOf("quantity");
      const saleIdx = fields.indexOf("salesConsideration");
      const costIdx = fields.indexOf("costOfAcquisition");
      const fmvIdx = fields.indexOf("fmvValue");
      const statusIdx = fields.indexOf("status");

      for (const row of el.l1.columnData) {
        if (statusIdx !== -1 && row[statusIdx] === "Inactive") continue;
        const rawName = row[nameIdx] || row[amcIdx] || "";
        const isinMatch = rawName.match(/\(([^)]+)\)/);
        const isin = isinMatch ? isinMatch[1] : "N/A";
        const nameClean = rawName.replace(/\([^)]+\)/g, "").trim();

        const sale = parseAmt(row[saleIdx]);
        const cost = parseAmt(row[costIdx]);
        const qty = parseFloat(row[qtyIdx]) || 0;
        const fmv = parseAmt(row[fmvIdx]);
        const date = row[dateIdx] || "";

        const gain = Math.max(0, sale - cost);
        ltcgTransactions.push({
          name: nameClean,
          isin,
          qty,
          date,
          salePrice: sale,
          netSalePrice: sale,
          purchasePrice: cost,
          purchaseDate: "N/A",
          marketValue: fmv,
          calculatedCost: cost,
          gain: gain
        });

        totalSalePrice += sale;
        totalPurchasePrice += cost;
        totalGain += gain;
      }
    }
  }

  // TDS salary list
  const salaryTdsList = itr1.TDSonSalaries?.TDSonSalary || [];
  const totalTdsSal = itr1.TDSonSalaries?.TotalTDSonSalaries || 0;

  // TDS non-salary list
  const nonSalaryTdsList = itr1.TDSonOthThanSals?.TDSonOthThanSal || [];
  const totalTdsOthers = itr1.TDSonOthThanSals?.TotalTDSonOthThanSals || 0;

  // Dynamic Slab Calculation Text
  const optOutRegime = itr1.FilingStatus?.OptOutNewTaxRegime || "N";
  const slabTaxableIncome = Math.max(0, (incomeDec.GrossTotIncome || 0) - (incomeDec.DeductUndChapVIA?.TotalChapVIADeductions || 0));
  
  const regimeConfig = optOutRegime === "N" ? taxSlabs.taxRegimes.new : taxSlabs.taxRegimes.old;
  const slabLines = [];
  slabLines.push(`Exemption Limit :${formatIndianNumber(regimeConfig.exemptionLimit)}`);

  if (slabTaxableIncome > regimeConfig.exemptionLimit) {
    for (const slab of regimeConfig.slabs) {
      if (slabTaxableIncome > slab.min) {
        const slabMax = slab.max === null ? slabTaxableIncome : Math.min(slab.max, slabTaxableIncome);
        const taxableInSlab = slabMax - slab.min;
        const slabTax = Math.round(taxableInSlab * slab.rate);
        const slabRatePercent = Math.round(slab.rate * 100);
        
        let label = "";
        if (slab.max === null) {
          label = `Tax on above ${formatIndianNumber(slab.min)}`;
        } else {
          label = `Tax on (${formatIndianNumber(slab.max)} - ${formatIndianNumber(slab.min)})`;
        }
        
        slabLines.push(`${label} = ${formatIndianNumber(taxableInSlab)} @${slabRatePercent}% = ${formatIndianNumber(slabTax)}`);
      }
    }
  }

  // HTML content
  return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${resolvedPan} - Tax Computation AY ${assessmentYear.replace("-", "_")}</title>
  <style>
    @media print {
      @page {
        size: A4;
        margin: 15mm 12mm;
      }
      body {
        background-color: #fff !important;
        color: #000 !important;
        padding: 0 !important;
        margin: 0 !important;
      }
      .page {
        page-break-after: always !important;
        page-break-inside: avoid !important;
        min-height: 0 !important;
        height: auto !important;
        width: 100% !important;
        box-shadow: none !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        background-color: #fff !important;
        color: #000 !important;
      }
      .no-print {
        display: none !important;
      }
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      background-color: #111827;
      color: #f3f4f6;
      margin: 0;
      padding: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    /* Outer layout showing A4 sheets styled cleanly */
    .page {
      background-color: #000;
      color: #fff;
      width: 210mm;
      min-height: 297mm;
      padding: 20mm 15mm;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      margin-bottom: 25px;
      box-sizing: border-box;
      position: relative;
      display: flex;
      flex-direction: column;
    }

    /* Controls Panel */
    .no-print {
      width: 210mm;
      background-color: #1f2937;
      padding: 12px 24px;
      border-radius: 12px;
      margin-bottom: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      box-sizing: border-box;
    }

    .btn {
      background: linear-gradient(135deg, #6366f1 0%, #10b981 100%);
      color: white;
      border: none;
      padding: 8px 18px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn:hover {
      opacity: 0.9;
      transform: translateY(-1px);
    }

    /* Typography & Structure */
    h1, h2, h3 {
      margin: 0 0 10px 0;
      font-weight: bold;
    }

    .section-title {
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid #4b5563;
      padding-bottom: 4px;
      margin-top: 25px;
      margin-bottom: 12px;
      font-weight: bold;
    }

    @media print {
      .section-title {
        border-bottom-color: #000;
      }
    }

    /* Grids & Layout details */
    .meta-grid {
      display: grid;
      grid-template-cols: 1.2fr 1fr;
      gap: 15px 40px;
      font-size: 12px;
      margin-bottom: 20px;
    }

    .meta-item {
      display: flex;
      justify-content: space-between;
      border-bottom: 1px dashed #374151;
      padding-bottom: 4px;
    }

    @media print {
      .meta-item {
        border-bottom-color: #ddd;
      }
    }

    .meta-label {
      color: #9ca3af;
      font-weight: 500;
    }

    @media print {
      .meta-label {
        color: #444;
      }
    }

    .meta-value {
      font-weight: 600;
      text-align: right;
    }

    .title-center {
      text-align: center;
      font-size: 15px;
      text-decoration: underline;
      margin: 25px 0 15px 0;
      font-weight: bold;
    }

    /* Computation Table layout */
    .comp-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-top: 10px;
    }

    .comp-table td {
      padding: 6px 0;
      vertical-align: top;
    }

    .comp-table .indent {
      padding-left: 20px;
    }

    .comp-table .amount-col {
      text-align: right;
      width: 130px;
      font-weight: 600;
    }

    .comp-table .subtotal-col {
      text-align: right;
      width: 130px;
      padding-right: 25px;
    }

    /* Double underline for totals */
    .double-underline {
      border-bottom: 3px double #4b5563;
      font-weight: bold;
    }

    @media print {
      .double-underline {
        border-bottom-color: #000;
      }
    }

    /* Detailed lists tables */
    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      margin-bottom: 20px;
    }

    .data-table th {
      background-color: #1f2937;
      text-align: left;
      padding: 6px 8px;
      font-weight: bold;
      border: 1px solid #374151;
    }

    @media print {
      .data-table th {
        background-color: #eee;
        color: #000;
        border-color: #000;
      }
    }

    .data-table td {
      padding: 6px 8px;
      border: 1px solid #374151;
    }

    @media print {
      .data-table td {
        border-color: #000;
      }
    }

    .data-table .num-cell {
      text-align: right;
    }

    .data-table .total-row {
      font-weight: bold;
      background-color: #111827;
    }

    @media print {
      .data-table .total-row {
        background-color: #fafafa;
      }
    }

    /* Footer Pagination */
    .page-footer {
      margin-top: auto;
      text-align: right;
      font-size: 10px;
      color: #9ca3af;
      padding-top: 15px;
      border-top: 1px solid #374151;
    }

    @media print {
      .page-footer {
        color: #000;
        border-top-color: #000;
      }
    }

    .header-box {
      border-bottom: 2px solid #fff;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }

    @media print {
      .header-box {
        border-bottom-color: #000;
      }
    }

    .page-header-meta {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: bold;
      border-bottom: 1.5px solid #fff;
      padding-bottom: 5px;
      margin-bottom: 20px;
    }

    @media print {
      .page-header-meta {
        border-bottom-color: #000;
      }
    }

    .note-text {
      font-size: 11px;
      color: #9ca3af;
      margin: 5px 0;
      line-height: 1.4;
    }

    @media print {
      .note-text {
        color: #555;
      }
    }
  </style>
</head>
<body>

  <!-- Controls Panel (Hidden in print) -->
  <div class="no-print">
    <div style="font-size:14px; font-weight:700;">Tax Computation Statement Preview</div>
    <button class="btn" onclick="window.print()">Print or Save PDF</button>
  </div>

  <!-- PAGE 1: Personal Details & Total Income -->
  <div class="page">
    <div class="header-box">
      <div style="font-size: 16px; font-weight: bold;">TAX COMPUTATION STATEMENT</div>
      <div style="font-size: 12px; color: #9ca3af;">AY ${assessmentYear} | FY 2025-26</div>
    </div>

    <!-- Personal details -->
    <div class="meta-grid">
      <div>
        <div class="meta-item">
          <span class="meta-label">Name of Assessee</span>
          <span class="meta-value">${assesseeName}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Father's Name</span>
          <span class="meta-value">${verification.Declaration?.FatherName || "N/A"}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Address</span>
          <span class="meta-value" style="font-size:10px; max-width:200px; line-height:1.2;">${address}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">E-Mail</span>
          <span class="meta-value">${email}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Status</span>
          <span class="meta-value">${status}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Ward</span>
          <span class="meta-value">N/A</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">PAN</span>
          <span class="meta-value">${resolvedPan}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Residential Status</span>
          <span class="meta-value">${residentialStatus}</span>
        </div>
      </div>

      <div>
        <div class="meta-item">
          <span class="meta-label">Assessment Year</span>
          <span class="meta-value">${assessmentYear}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Year Ended</span>
          <span class="meta-value">${yearEnded}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Date of Birth</span>
          <span class="meta-value">${dob}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Gender</span>
          <span class="meta-value">${personal.Gender || "Male"}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Filing Status</span>
          <span class="meta-value">${filingStatus}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Aadhaar No:</span>
          <span class="meta-value">${aadhaar}</span>
        </div>
        <div class="meta-item" style="margin-top: 6px;">
          <span class="meta-label">Mobile Linked Aadhaar</span>
          <span class="meta-value">${phone}</span>
        </div>
      </div>
    </div>

    <!-- Income Computation title -->
    <div class="title-center">
      Computation of Total Income [As per Section 115BAC (New Tax Regime)]
    </div>

    <!-- Computation table list -->
    <table class="comp-table">
      <!-- Salary -->
      <tr>
        <td style="font-weight: bold;">Income from Salary (Chapter IV A)</td>
        <td class="subtotal-col"></td>
        <td class="amount-col">${formatIndianNumber(incomeDec.IncomeFromSal || 0)}</td>
      </tr>
      ${grossSalaryTdsDetails(itr1)}

      <!-- Capital Gain -->
      <tr>
        <td style="font-weight: bold; padding-top: 15px;">Income from Capital Gain (Chapter IV E)</td>
        <td class="subtotal-col"></td>
        <td class="amount-col" style="padding-top: 15px;">${formatIndianNumber(totalGain)}</td>
      </tr>
      <tr>
        <td class="indent" style="text-decoration: underline;">Long Term Capital Gain</td>
        <td class="subtotal-col"></td>
        <td class="amount-col"></td>
      </tr>
      <tr>
        <td class="indent">Long Term Capital Gain u/s 112A as per Details Attached</td>
        <td class="subtotal-col">${formatIndianNumber(totalGain)}</td>
        <td class="amount-col"></td>
      </tr>
      <tr>
        <td colspan="3" class="note-text" style="padding-left: 20px;">
          Note: - Threshold Limit of Rs. 1,25,000 as given u/s 112A is the part of Total Income but in tax calculation this amount will be excluded.
        </td>
      </tr>

      <!-- Other Sources -->
      <tr>
        <td style="font-weight: bold; padding-top: 15px;">Income from Other Sources (Chapter IV F)</td>
        <td class="subtotal-col"></td>
        <td class="amount-col" style="padding-top: 15px;">${formatIndianNumber(incomeDec.IncomeOthSrc || 0)}</td>
      </tr>
      <tr>
        <td class="indent">Interest From Saving Bank A/c (as per Annexure)</td>
        <td class="subtotal-col">${formatIndianNumber(totalSavingsInterest)}</td>
        <td class="amount-col"></td>
      </tr>
      <tr>
        <td class="indent">Interest on F.D.R.(as per Annexure)</td>
        <td class="subtotal-col">${formatIndianNumber(totalFdrInterest)}</td>
        <td class="amount-col"></td>
      </tr>
      <tr>
        <td class="indent">Dividend From Shares</td>
        <td class="subtotal-col" style="border-bottom: 1px solid #4b5563;">${formatIndianNumber(totalDividend)}</td>
        <td class="amount-col"></td>
      </tr>
      <tr>
        <td class="indent"></td>
        <td class="subtotal-col">${formatIndianNumber(incomeDec.IncomeOthSrc || 0)}</td>
        <td class="amount-col"></td>
      </tr>

      <!-- Gross Total Income -->
      <tr>
        <td style="font-weight: bold; padding-top: 20px;">Gross Total Income</td>
        <td class="subtotal-col"></td>
        <td class="amount-col double-underline" style="padding-top: 20px;">${formatIndianNumber(incomeDec.GrossTotIncomeIncLTCG112A || 0)}</td>
      </tr>

      <!-- Deductions -->
      <tr>
        <td style="font-weight: bold; padding-top: 15px;">Less: Deductions (Chapter VI-A)</td>
        <td class="subtotal-col" style="border-bottom: 1px solid #4b5563;"></td>
        <td class="amount-col" style="padding-top: 15px;">${formatIndianNumber(incomeDec.DeductUndChapVIA?.TotalChapVIADeductions || 0)}</td>
      </tr>

      <!-- Total Income -->
      <tr>
        <td style="font-weight: bold; padding-top: 20px;">Total Income</td>
        <td class="subtotal-col"></td>
        <td class="amount-col double-underline" style="padding-top: 20px;">${formatIndianNumber(incomeDec.TotalIncome || 0)}</td>
      </tr>

      <!-- Round off -->
      <tr>
        <td style="font-weight: bold;">Round off u/s 288 A</td>
        <td class="subtotal-col"></td>
        <td class="amount-col double-underline">${formatIndianNumber(incomeDec.TotalIncome || 0)}</td>
      </tr>
      
      <tr>
        <td colspan="3" class="note-text" style="font-style: italic; padding-top: 10px;">
          Adjusted total income (ATI) is not more than Rs. 20 lakhs hence AMT not applicable.
        </td>
      </tr>
    </table>

    <div class="page-footer">Page 1</div>
  </div>

  <!-- PAGE 2: Tax Computation & Bank details -->
  <div class="page">
    <div class="page-header-meta">
      <span>NAME OF ASSESSEE : ${assesseeName.toUpperCase()}</span>
      <span>A.Y. ${assessmentYear}</span>
      <span>PAN : ${resolvedPan}</span>
    </div>

    <table class="comp-table" style="margin-top: 10px;">
      <tr>
        <td>Tax Due (Exemption Limit Rs. 400000)</td>
        <td class="subtotal-col"></td>
        <td class="amount-col">${formatIndianNumber(taxComp.TotalTaxPayable || 0)}</td>
      </tr>
      <tr>
        <td>Rebate u/s 87A</td>
        <td class="subtotal-col" style="border-bottom: 1px solid #4b5563;"></td>
        <td class="amount-col">${formatIndianNumber(taxComp.Rebate87A || 0)}</td>
      </tr>
      <tr>
        <td></td>
        <td class="subtotal-col"></td>
        <td class="amount-col" style="border-bottom: 1.5px solid #fff;">0</td>
      </tr>
      <tr>
        <td style="font-weight: bold;">T.D.S./T.C.S</td>
        <td class="subtotal-col" style="border-bottom: 1px solid #4b5563;"></td>
        <td class="amount-col">${formatIndianNumber(taxPaid.TaxesPaid?.TotalTaxesPaid || 0)}</td>
      </tr>
      <tr>
        <td></td>
        <td class="subtotal-col"></td>
        <td class="amount-col" style="border-bottom: 1.5px solid #fff;">-${formatIndianNumber(taxPaid.TaxesPaid?.TotalTaxesPaid || 0)}</td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Refundable (Round off u/s 288B)</td>
        <td class="subtotal-col"></td>
        <td class="amount-col double-underline">${formatIndianNumber(refund.RefundDue || 0)}</td>
      </tr>
    </table>

    <!-- Tax calculation details -->
    <div style="font-size: 12px; font-weight: bold; margin-top: 25px; margin-bottom: 10px;">
      Tax calculation on Normal income of Rs. ${formatIndianNumber(slabTaxableIncome)}/-
    </div>
    <div style="font-size: 11px; line-height: 1.6; padding-left: 10px;">
      ${slabLines.map(line => `<div>${line}</div>`).join("")}
      <div style="font-weight: bold; margin-top: 4px;">Total Tax = ${formatIndianNumber(taxComp.TotalTaxPayable || 0)}</div>
    </div>

    <div class="note-text" style="margin-top: 15px; font-style: italic;">
      Assessee is Senior Citizen Individual and there is no Business Income in current financial year. So, there is no advance tax liability according to section 207.<br>
      Due Date for filing of Return July 31, 2026.
    </div>

    <!-- Special Rates table -->
    <div class="section-title">Tax Calculation on Capital Gain Income</div>
    <table class="data-table">
      <thead>
        <tr>
          <th>S.No.</th>
          <th>Head</th>
          <th>Income Before Loss Adjustment</th>
          <th>Income After Loss Adjustment</th>
          <th>Basic Exemption Adjusted</th>
          <th>Tax</th>
          <th>Excess Amount Ignored</th>
          <th>Net Tax</th>
        </tr>
      </thead>
      <tbody>
        ${renderSpecialRatesRow(totalGain)}
      </tbody>
    </table>

    <!-- Bank Account details table -->
    <div class="section-title">Bank Account Detail</div>
    <table class="data-table">
      <thead>
        <tr>
          <th>S.N.</th>
          <th>Bank</th>
          <th>Address</th>
          <th>Account No</th>
          <th>IFSC Code</th>
          <th>Type</th>
          <th>Prevalidated</th>
          <th>Nominate for refund</th>
        </tr>
      </thead>
      <tbody>
        ${renderBankDetails(refund.BankAccountDtls?.AddtnlBankDetails)}
      </tbody>
    </table>

    <!-- Interest Details List -->
    <div class="section-title">Details of Interest From Bank</div>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 50px;">S.NO.</th>
          <th>PARTICULARS</th>
          <th style="width: 150px; text-align: right;">AMOUNT</th>
        </tr>
      </thead>
      <tbody>
        ${renderInterestRows(savingsInterestList)}
        <tr class="total-row">
          <td colspan="2">TOTAL</td>
          <td class="num-cell">${formatIndianNumber(totalSavingsInterest)}</td>
        </tr>
      </tbody>
    </table>

    <div class="page-footer">Page 2</div>
  </div>

  <!-- PAGE 3: Annexures (FDR, Dividends, TDS) -->
  <div class="page">
    <div class="page-header-meta">
      <span>NAME OF ASSESSEE : ${assesseeName.toUpperCase()}</span>
      <span>A.Y. ${assessmentYear}</span>
      <span>PAN : ${resolvedPan}</span>
    </div>

    <!-- FDR details -->
    <div class="section-title">Details of Interest on F.D.R.</div>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 50px;">S.NO.</th>
          <th>PARTICULARS</th>
          <th style="width: 150px; text-align: right;">AMOUNT</th>
        </tr>
      </thead>
      <tbody>
        ${renderInterestRows(fdrInterestList)}
        <tr class="total-row">
          <td colspan="2">TOTAL</td>
          <td class="num-cell">${formatIndianNumber(totalFdrInterest)}</td>
        </tr>
      </tbody>
    </table>

    <!-- Dividend details -->
    <div class="section-title">Details of Dividend From Shares</div>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 50px;">S.NO.</th>
          <th>PARTICULARS</th>
          <th style="width: 150px; text-align: right;">AMOUNT</th>
        </tr>
      </thead>
      <tbody>
        ${renderInterestRows(dividendList)}
        <tr class="total-row">
          <td colspan="2">TOTAL</td>
          <td class="num-cell">${formatIndianNumber(totalDividend)}</td>
        </tr>
      </tbody>
    </table>

    <!-- Non-salary TDS details -->
    <div class="section-title">Details of T.D.S. on Non-Salary(26 AS Import Date:10 Jun 2026)</div>
    <table class="data-table">
      <thead>
        <tr>
          <th>S.No</th>
          <th>Name of the Deductor</th>
          <th>Tax deduction A/C No. of the deductor</th>
          <th style="text-align: right;">Amount Paid/credited</th>
          <th style="text-align: right;">Total Tax deducted</th>
          <th style="text-align: right;">Amount out of (5) claimed for this year</th>
        </tr>
      </thead>
      <tbody>
        ${renderNonSalTdsRows(nonSalaryTdsList)}
        <tr class="total-row">
          <td colspan="3">TOTAL</td>
          <td class="num-cell">${formatIndianNumber(nonSalaryTdsList.reduce((sum, item) => sum + (item.AmtForTaxDeduct || 0), 0))}</td>
          <td class="num-cell">${formatIndianNumber(totalTdsOthers)}</td>
          <td class="num-cell">${formatIndianNumber(totalTdsOthers)}</td>
        </tr>
      </tbody>
    </table>

    <!-- Head wise summary -->
    <div class="section-title">Head wise Summary on Income and TDS thereon</div>
    <table class="data-table">
      <thead>
        <tr>
          <th>Head</th>
          <th>Section</th>
          <th style="text-align: right;">Amount Paid/Credited As per 26AS</th>
          <th style="text-align: right;">As per Computation</th>
          <th>Location of Income for Comparison</th>
          <th style="text-align: right;">TDS</th>
        </tr>
      </thead>
      <tbody>
        ${renderHeadwiseSummary(nonSalaryTdsList, totalDividend, totalSavingsInterest, totalFdrInterest)}
      </tbody>
    </table>

    <!-- Salary TDS -->
    <div class="section-title">Details of T.D.S. on Salary(26 AS Import Date:10 Jun 2026)</div>
    <table class="data-table">
      <thead>
        <tr>
          <th>S.No</th>
          <th>Name of the employer</th>
          <th>Tax deduction A/C No. of the deductor</th>
          <th style="text-align: right;">Income chargeable under the head Salaries</th>
          <th style="text-align: right;">Tax deducted at source u/s. 192(1)</th>
        </tr>
      </thead>
      <tbody>
        ${renderSalaryTdsRows(salaryTdsList)}
        <tr class="total-row">
          <td colspan="3">TOTAL</td>
          <td class="num-cell">${formatIndianNumber(salaryTdsList.reduce((sum, item) => sum + (item.IncChrgSal || 0), 0))}</td>
          <td class="num-cell">${formatIndianNumber(totalTdsSal)}</td>
        </tr>
      </tbody>
    </table>

    <div class="page-footer">Page 3</div>
  </div>

  <!-- PAGE 4+: Capital Gains Details (Multi-page support) -->
  ${renderLtcgPages(ltcgTransactions, assesseeName, resolvedPan, assessmentYear)}

</body>
</html>
  `;
}

// Helper to render salary rows in computation list
function grossSalaryTdsDetails(itr1) {
  const gross = itr1.ITR1_IncomeDeductions?.GrossSalary || 0;
  const std = itr1.ITR1_IncomeDeductions?.DeductionUs16ia || 0;
  const net = gross - std;
  
  if (gross === 0) return "";
  
  const employerName = itr1.TDSonSalaries?.TDSonSalary?.[0]?.EmployerOrDeductorOrCollectDetl?.EmployerOrDeductorOrCollecterName || "Employer";
  const empCategory = itr1.PersonalInfo?.EmployerCategory === "OTH" ? "Other" : "Other";

  return `
    <tr>
      <td class="indent" style="text-decoration: underline; font-weight: 500;">
        ${employerName.toUpperCase()}
      </td>
      <td class="subtotal-col"></td>
      <td class="amount-col"></td>
    </tr>
    <tr>
      <td class="indent">Employer Status: ${empCategory}</td>
      <td class="subtotal-col"></td>
      <td class="amount-col"></td>
    </tr>
    <tr>
      <td class="indent">Salary</td>
      <td class="subtotal-col" style="font-weight: 500;">${formatIndianNumber(gross)}</td>
      <td class="amount-col"></td>
    </tr>
    <tr>
      <td class="indent">Less: Standard Deduction u/s 16(ia)</td>
      <td class="subtotal-col" style="border-bottom: 1px solid #4b5563; font-weight: 500;">${formatIndianNumber(std)}</td>
      <td class="amount-col"></td>
    </tr>
    <tr>
      <td class="indent"></td>
      <td class="subtotal-col" style="font-weight: 500;">${formatIndianNumber(net)}</td>
      <td class="amount-col"></td>
    </tr>
  `;
}

// Render row in Special Rates table
function renderSpecialRatesRow(totalGain) {
  if (totalGain <= 0) {
    return `
      <tr>
        <td colspan="8" style="text-align: center; color: #9ca3af;">No Capital Gains u/s 112A</td>
      </tr>
    `;
  }
  return `
    <tr>
      <td>1.</td>
      <td>Long Term Income 112A</td>
      <td class="num-cell">${formatIndianNumber(totalGain)}</td>
      <td class="num-cell">${formatIndianNumber(totalGain)}</td>
      <td class="num-cell">0</td>
      <td class="num-cell">0</td>
      <td class="num-cell">0</td>
      <td class="num-cell">0</td>
    </tr>
  `;
}

// Render rows in bank details table
function renderBankDetails(banks) {
  if (!banks || banks.length === 0) {
    return `
      <tr>
        <td colspan="8" style="text-align: center; color: #9ca3af;">No Bank Account Registered</td>
      </tr>
    `;
  }
  return banks.map((b, idx) => `
    <tr>
      <td>${idx + 1}</td>
      <td>${b.BankName || "N/A"}</td>
      <td>N/A</td>
      <td>${b.BankAccountNo || "N/A"}</td>
      <td>${b.IFSCCode || "N/A"}</td>
      <td>${b.AccountType === "SB" ? "Savings" : "Current"}</td>
      <td>Yes</td>
      <td>${b.UseForRefund === "true" || b.UseForRefund === true ? "Yes" : "No"}</td>
    </tr>
  `).join("");
}

// Render interest bank list rows
function renderInterestRows(list) {
  if (!list || list.length === 0) {
    return `
      <tr>
        <td colspan="3" style="text-align: center; color: #9ca3af;">Nil</td>
      </tr>
    `;
  }
  return list.map((item, idx) => `
    <tr>
      <td>${idx + 1}</td>
      <td>${item.name.toUpperCase()}</td>
      <td class="num-cell">${formatIndianNumber(item.amount)}</td>
    </tr>
  `).join("");
}

// Render non-salary TDS rows
function renderNonSalTdsRows(list) {
  if (!list || list.length === 0) {
    return `
      <tr>
        <td colspan="6" style="text-align: center; color: #9ca3af;">Nil</td>
      </tr>
    `;
  }
  return list.map((item, idx) => `
    <tr>
      <td>${idx + 1}</td>
      <td>${(item.EmployerOrDeductorOrCollectDetl?.EmployerOrDeductorOrCollecterName || "Deductor").toUpperCase()}</td>
      <td>${item.EmployerOrDeductorOrCollectDetl?.TAN || "N/A"}</td>
      <td class="num-cell">${formatIndianNumber(item.AmtForTaxDeduct)}</td>
      <td class="num-cell">${formatIndianNumber(item.TotTDSOnAmtPaid)}</td>
      <td class="num-cell">${formatIndianNumber(item.ClaimOutOfTotTDSOnAmtPaid)}</td>
    </tr>
  `).join("");
}

// Render salary TDS rows
function renderSalaryTdsRows(list) {
  if (!list || list.length === 0) {
    return `
      <tr>
        <td colspan="5" style="text-align: center; color: #9ca3af;">Nil</td>
      </tr>
    `;
  }
  return list.map((item, idx) => `
    <tr>
      <td>${idx + 1}</td>
      <td>${(item.EmployerOrDeductorOrCollectDetl?.EmployerOrDeductorOrCollecterName || "Employer").toUpperCase()}</td>
      <td>${item.EmployerOrDeductorOrCollectDetl?.TAN || "N/A"}</td>
      <td class="num-cell">${formatIndianNumber(item.IncChrgSal)}</td>
      <td class="num-cell">${formatIndianNumber(item.TotalTDSSal)}</td>
    </tr>
  `).join("");
}

// Render headwise summary table rows
function renderHeadwiseSummary(tdsList, totalDividend, totalSavings, totalFdr) {
  if (!tdsList || tdsList.length === 0) {
    return `
      <tr>
        <td colspan="6" style="text-align: center; color: #9ca3af;">No TDS on Non-Salary</td>
      </tr>
    `;
  }

  // Group TDS items by section
  const sectionSummary = {};
  for (const item of tdsList) {
    const sec = item.TDSSection || "94A";
    if (!sectionSummary[sec]) {
      sectionSummary[sec] = { paid: 0, tds: 0 };
    }
    sectionSummary[sec].paid += item.AmtForTaxDeduct || 0;
    sectionSummary[sec].tds += item.TotTDSOnAmtPaid || 0;
  }

  return Object.entries(sectionSummary).map(([sec, data], idx) => {
    let comparisonLocation = "N/A";
    let compAmount = 0;
    if (sec === "194" || sec === "94K") {
      comparisonLocation = `Dividend Income:${formatIndianNumber(totalDividend)}`;
      compAmount = totalDividend;
    } else if (sec === "94A" || sec === "194A") {
      comparisonLocation = `Interest Income:${formatIndianNumber(totalSavings + totalFdr)}`;
      compAmount = totalSavings + totalFdr;
    }

    return `
      <tr>
        <td>Other Sources</td>
        <td>${sec}</td>
        <td class="num-cell">${formatIndianNumber(data.paid)}</td>
        <td class="num-cell">${formatIndianNumber(compAmount)}</td>
        <td>${comparisonLocation}</td>
        <td class="num-cell">${formatIndianNumber(data.tds)}</td>
      </tr>
    `;
  }).join("");
}

// Render long term capital gain transaction pages (with clean page-break splitting)
function renderLtcgPages(transactions, name, pan, AY) {
  if (!transactions || transactions.length === 0) return "";

  const pageSize = 18; // maximum transactions per page to fit on standard A4 height
  const totalPages = Math.ceil(transactions.length / pageSize);
  let html = "";

  for (let p = 0; p < totalPages; p++) {
    const slice = transactions.slice(p * pageSize, (p + 1) * pageSize);
    html += `
      <div class="page">
        <div class="page-header-meta">
          <span>NAME OF ASSESSEE : ${name.toUpperCase()}</span>
          <span>A.Y. ${AY}</span>
          <span>PAN : ${pan}</span>
        </div>

        <div class="section-title">Statement of Long Term Capital Gain Transaction Tax u/s 112A</div>
        <table class="data-table" style="font-size: 9px;">
          <thead>
            <tr>
              <th>Name of Company</th>
              <th>ISIN</th>
              <th style="text-align: right;">Qty</th>
              <th>Date of Sale</th>
              <th style="text-align: right;">Sales Price</th>
              <th style="text-align: right;">Net Sale Price</th>
              <th style="text-align: right;">Purchase Price</th>
              <th>Purchase Date</th>
              <th style="text-align: right;">Market value 31/01/18</th>
              <th style="text-align: right;">Calculated Cost</th>
              <th style="text-align: right;">Capital gain</th>
            </tr>
          </thead>
          <tbody>
            ${slice.map(t => `
              <tr>
                <td style="max-width: 180px; word-break: break-all;">${t.name.toUpperCase()}</td>
                <td>${t.isin}</td>
                <td class="num-cell">${t.qty.toFixed(2)}</td>
                <td>${t.date}</td>
                <td class="num-cell">${formatIndianNumber(t.salePrice)}</td>
                <td class="num-cell">${formatIndianNumber(t.netSalePrice)}</td>
                <td class="num-cell">${formatIndianNumber(t.purchasePrice)}</td>
                <td>${t.purchaseDate}</td>
                <td class="num-cell">${formatIndianNumber(t.marketValue)}</td>
                <td class="num-cell">${formatIndianNumber(t.calculatedCost)}</td>
                <td class="num-cell">${formatIndianNumber(t.gain)}</td>
              </tr>
            `).join("")}
            ${p === totalPages - 1 ? `
              <tr class="total-row">
                <td colspan="2">TOTAL</td>
                <td class="num-cell">${transactions.reduce((sum, item) => sum + item.qty, 0).toFixed(2)}</td>
                <td></td>
                <td class="num-cell">${formatIndianNumber(transactions.reduce((sum, item) => sum + item.salePrice, 0))}</td>
                <td class="num-cell">${formatIndianNumber(transactions.reduce((sum, item) => sum + item.netSalePrice, 0))}</td>
                <td class="num-cell">${formatIndianNumber(transactions.reduce((sum, item) => sum + item.purchasePrice, 0))}</td>
                <td></td>
                <td class="num-cell">${formatIndianNumber(transactions.reduce((sum, item) => sum + item.marketValue, 0))}</td>
                <td class="num-cell">${formatIndianNumber(transactions.reduce((sum, item) => sum + item.calculatedCost, 0))}</td>
                <td class="num-cell">${formatIndianNumber(transactions.reduce((sum, item) => sum + item.gain, 0))}</td>
              </tr>
            ` : ""}
          </tbody>
        </table>

        <div class="page-footer">Page ${4 + p}</div>
      </div>
    `;
  }

  return html;
}

// Function to trigger client print action
export function printTaxComputation(generatedJson, uploadedFiles) {
  const html = generateTaxComputationHtml(generatedJson, uploadedFiles);
  const printWindow = window.open("", "_blank");
  if (printWindow) {
    printWindow.document.open();
    printWindow.document.write(html);
    printWindow.document.close();
  } else {
    alert("Popup blocker prevented opening print window. Please allow popups for this site.");
  }
}
