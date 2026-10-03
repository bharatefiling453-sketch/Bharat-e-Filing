import { extractPan } from "../../utils/panExtractor.js";
import { parseAmt, sumAisCatCodes } from "../common/aisUtils.js";

/**
 * Compiles tax documents and returns a structured Indian Income Tax ITR-1 JSON document
 * that conforms strictly to the official AY 2026-27 CBDT JSON Schema.
 * 
 * @param {Object} taxpayerInfo - General profile details (name, dob, email, phone, pan, employerCategory, aadhaarCardNo)
 * @param {Object} addressInfo - Structured address details (residenceNo, residenceName, roadOrStreet, localityOrArea, cityOrTownOrDistrict, stateCode, pinCode)
 * @param {Object} bankInfo - Bank account details (ifscCode, bankName, bankAccountNo, accountType, useForRefund)
 * @param {Object} verificationInfo - Verification metadata (fatherName, capacity, place, optOutNewTaxRegime, returnFileSec)
 * @param {Object} ais - Selected AIS document data
 * @param {Object} tis - Selected TIS document data
 * @param {Object} form26as - Selected Form 26AS data
 * @returns {Object} Structured ITR-1 JSON payload compliant with CBDT schemas
 */
export function generateItr1Json({
  taxpayerInfo = {},
  addressInfo = {},
  bankInfo = {},
  verificationInfo = {},
  ais = null,
  tis = null,
  form26as = null
}) {
  // 1. Dynamic PAN & Name Extraction
  // AIS stores PAN in metadata.loggedInPan; partA.columnData[0] is a fallback
  const aisPartAPan = ais?.partA?.columnData?.[0] || null;
  const resolvedPan = (ais?.metadata?.loggedInPan || aisPartAPan ||
    extractPan(ais) || extractPan(tis) || extractPan(form26as) || taxpayerInfo.pan || "").toUpperCase();

  // Also extract name/personal info from AIS partA if not provided in taxpayerInfo
  // partA.columnLabel: ["PAN", "Aadhaar", "Name", "DOB", "Mobile", "Email", "Address"]
  const aisPartAData = ais?.partA?.columnData || [];
  const aisName = aisPartAData[2] || "";
  const aisPhone = aisPartAData[4] || "";
  const aisEmail = aisPartAData[5] || "";
  
  // Split name for AssesseeName schema compliance
  const fullName = taxpayerInfo.name || aisName || "Taxpayer";
  const nameParts = fullName.trim().split(/\s+/);
  let firstName = taxpayerInfo.firstName || "";
  let middleName = taxpayerInfo.middleName || "";
  let lastName = taxpayerInfo.lastName || "";

  if (!lastName) {
    if (nameParts.length === 1) {
      lastName = nameParts[0];
    } else if (nameParts.length === 2) {
      firstName = nameParts[0];
      lastName = nameParts[1];
    } else {
      firstName = nameParts[0];
      middleName = nameParts.slice(1, -1).join(" ");
      lastName = nameParts[nameParts.length - 1];
    }
  }

  // 2. Financial Ingestion
  // Primary source: AIS partB catCode-based extraction
  // Fallback: TIS categories (for future TIS support)
  const getSalaryIncome = () => {
    // AIS catCode SAL (TDS-192 salary rows), deduplicate by taking TDS-TCS source only
    // to avoid double-counting with AIS_TDS_ANNEX2 (which repeats same salary)
    const v = sumAisCatCodes(ais, ["SAL"], ["AIS_TDS_ANNEX2"]);
    if (v > 0) return v;
    if (tis?.categories) {
      const tisVal = tis.categories.find(c => c.code === "SLR" || c.name === "Salary")?.derivedValue;
      if (tisVal !== undefined) return tisVal;
    }
    return 0;
  };

  const getSavingsInterest = () => {
    // catCode INS = Interest from savings bank
    const v = sumAisCatCodes(ais, ["INS"]);
    if (v > 0) return v;
    if (tis?.categories) {
      const tisVal = tis.categories.find(c => c.code === "SBN" || c.name?.includes("Savings Bank"))?.derivedValue;
      if (tisVal !== undefined) return tisVal;
    }
    return 0;
  };

  const getDepositInterest = () => {
    // catCode IND = Interest from term deposits
    const v = sumAisCatCodes(ais, ["IND", "TDN"]);
    if (v > 0) return v;
    if (tis?.categories) {
      const tisVal = tis.categories.find(c => c.code === "TDN" || c.name?.includes("Deposits"))?.derivedValue;
      if (tisVal !== undefined) return tisVal;
    }
    return 0;
  };

  const getDividends = () => {
    // DIV income: exclude AIS_TDS_TCS sources — TDS-194 DIV rows are duplicates of SFT-015/SFT-18(Div).
    // Only sum SFT_PRSN and SFT_MF_HLD_PUR_DIV sources.
    const v = sumAisCatCodes(ais, ["DIV"], ["AIS_TDS_TCS"]);
    if (v > 0) return v;
    if (tis?.categories) {
      const tisVal = tis.categories.find(c => c.code === "DIV" || c.name === "Dividend")?.derivedValue;
      if (tisVal !== undefined) return tisVal;
    }
    return 0;
  };

  // 3. Tax Credit / TDS Mapping
  const mapSectionToSchemaCode = (sec) => {
    if (!sec) return "94A";
    const cleanSec = sec.replace("Sec ", "").replace("Section ", "").trim();
    if (cleanSec === "192") return "92B";
    if (cleanSec === "192A") return "192A";
    if (cleanSec === "193") return "193";
    if (cleanSec === "194") return "194";
    if (cleanSec === "194A") return "94A";
    if (cleanSec === "194B") return "94B";
    if (cleanSec === "194BA") return "94BA";
    if (cleanSec === "194C") return "94C";
    if (cleanSec === "194D") return "94D";
    if (cleanSec === "194DA") return "4DA";
    if (cleanSec === "194G") return "4G";
    if (cleanSec === "194H") return "4H";
    if (cleanSec === "194I" || cleanSec === "194I(a)") return "4-IA";
    if (cleanSec === "194I(b)") return "4-IB";
    if (cleanSec === "194IA") return "4IA";
    if (cleanSec === "194IB") return "4IB";
    if (cleanSec === "194J" || cleanSec === "194J(a)") return "94J-A";
    if (cleanSec === "194J(b)") return "94J-B";
    if (cleanSec === "194K") return "94K";
    if (cleanSec === "194N") return "94N";
    if (cleanSec === "194O") return "94O";
    if (cleanSec === "194Q") return "94Q";
    return "94A"; // sensible fallback
  };

  /**
   * Build TDS-on-Salary list from AIS partB.
   * For each Salary element (l1Src=AIS_TDS_TCS, catCode=SAL), sum l1 transaction
   * rows' amtPaid (gross salary) and amountDeposited (TDS deposited) per deductor
   * identified by infoSrcId (which is the TAN).
   */
  const getTdsSalaryList = () => {
    if (form26as?.taxDeductedAtSource) {
      return form26as.taxDeductedAtSource
        .filter(t => t.section === "192")
        .map(t => ({
          EmployerOrDeductorOrCollectDetl: {
            TAN: t.tanOfDeductor || "DELA12345B",
            EmployerOrDeductorOrCollecterName: t.deductorName || "Employer"
          },
          IncChrgSal: Math.round(t.totalAmountPaid || 0),
          TotalTDSSal: Math.round(t.totalTaxDeposited || 0)
        }));
    }
    if (ais?.partB?.sections) {
      // Group by infoSrcId (TAN) across all Salary elements with l1Src=AIS_TDS_TCS
      const deductorMap = {};
      for (const sec of ais.partB.sections) {
        if (!Array.isArray(sec.elements)) continue;
        for (const el of sec.elements) {
          if (el.l1Src !== "AIS_TDS_TCS") continue;
          if (!el.l2?.columnLabel || !el.l2?.columnData) continue;
          const l2Cols = el.l2.columnLabel;
          const catCodeIdx = l2Cols.indexOf("Information Category Code");
          if (catCodeIdx === -1) continue;
          const isSalary = el.l2.columnData.some(row => row[catCodeIdx] === "SAL");
          if (!isSalary) continue;
          // Get deductor name from l2 Information Source column
          const srcIdx = l2Cols.indexOf("Information Source");
          const srcName = el.l2.columnData[0]?.[srcIdx] || el.infoSrcId || "Employer";
          const tan = el.infoSrcId || "DELA12345B";
          if (!deductorMap[tan]) {
            deductorMap[tan] = { name: srcName, amtPaid: 0, amtDeposited: 0 };
          }
          // Sum l1 transaction rows
          if (el.l1?.columnLabel && el.l1?.columnData) {
            const fieldNames = el.l1.columnLabel.map(c => c.field);
            const amtPaidIdx = fieldNames.indexOf("amtPaid");
            const amtDepIdx = fieldNames.indexOf("amountDeposited");
            for (const row of el.l1.columnData) {
              if (amtPaidIdx >= 0) deductorMap[tan].amtPaid += parseAmt(row[amtPaidIdx]);
              if (amtDepIdx >= 0) deductorMap[tan].amtDeposited += parseAmt(row[amtDepIdx]);
            }
          }
        }
      }
      const list = Object.entries(deductorMap).map(([tan, d]) => ({
        EmployerOrDeductorOrCollectDetl: {
          TAN: tan,
          EmployerOrDeductorOrCollecterName: d.name
        },
        IncChrgSal: Math.round(d.amtPaid),
        TotalTDSSal: Math.round(d.amtDeposited)
      }));
      if (list.length > 0) return list;
    }
    return [];
  };

  /**
   * Build TDS-on-Others list from AIS partB.
   * Covers catCodes: IND (deposit interest), DIV (dividend), etc.
   * Groups by infoSrcId + infoCode per element.
   */
  const getTdsOthersList = () => {
    if (ais?.partB?.sections) {
      const others = [];
      const seenElement = new Set(); // only process first element per TAN+section
      const NON_SALARY_CODES = new Set(["IND", "INS", "DIV", "TDN"]);
      for (const sec of ais.partB.sections) {
        if (!Array.isArray(sec.elements)) continue;
        for (const el of sec.elements) {
          if (el.l1Src !== "AIS_TDS_TCS") continue;
          if (!el.l2?.columnLabel || !el.l2?.columnData) continue;
          const l2Cols = el.l2.columnLabel;
          const catCodeIdx = l2Cols.indexOf("Information Category Code");
          const codeIdx = l2Cols.indexOf("Information Code");
          if (catCodeIdx === -1) continue;
          const matchRow = el.l2.columnData.find(row => NON_SALARY_CODES.has(row[catCodeIdx]));
          if (!matchRow) continue;
          const infoCode = matchRow[codeIdx] || "";
          const section = infoCode.replace("TDS-", "");
          const tdsSection = mapSectionToSchemaCode(section);
          const tan = el.infoSrcId || "DELA12345B";
          // Only use the first element per TAN+section (avoids duplicate sub-batches)
          const elementKey = `${tan}|${tdsSection}`;
          if (seenElement.has(elementKey)) continue;
          seenElement.add(elementKey);
          const srcIdx = l2Cols.indexOf("Information Source");
          const deductorName = matchRow[srcIdx] || tan;
          if (!el.l1?.columnLabel || !el.l1?.columnData) continue;
          const fieldNames = el.l1.columnLabel.map(c => c.field);
          const amtPaidIdx = fieldNames.indexOf("amtPaid");
          const amtDepIdx = fieldNames.indexOf("amountDeposited");
          // l2 declared amount is the authoritative total — stop once l1 sum reaches it
          const l2AmtIdx = l2Cols.indexOf("Amount");
          const l2DeclaredAmt = l2AmtIdx >= 0 ? parseAmt(matchRow[l2AmtIdx]) : Infinity;
          let runningAmt = 0;
          for (const row of el.l1.columnData) {
            if (runningAmt >= l2DeclaredAmt) break; // stop at l2 ceiling
            const amt = parseAmt(row[amtPaidIdx]);
            const dep = parseAmt(row[amtDepIdx]);
            if (amt === 0) continue;
            runningAmt += amt;
            others.push({
              EmployerOrDeductorOrCollectDetl: {
                TAN: tan,
                EmployerOrDeductorOrCollecterName: deductorName
              },
              TDSSection: tdsSection,
              AmtForTaxDeduct: Math.round(amt),
              DeductedYr: "2025",
              TotTDSOnAmtPaid: Math.round(dep),
              ClaimOutOfTotTDSOnAmtPaid: Math.round(dep)
            });
          }
        }
      }
      if (others.length > 0) return others;
    }
    return [];
  };

  // 4. Detailed Income Calculations
  const grossSalary = Math.round(getSalaryIncome());
  const optOutRegime = verificationInfo.optOutNewTaxRegime || "N";
  
  // Standard Deduction: ₹75,000 for New Regime, ₹50,000 for Old Regime
  const stdDeductionLimit = optOutRegime === "Y" ? 50000 : 75000;
  const stdDeduction = Math.min(grossSalary, stdDeductionLimit);
  const totalSalaryDeduction = stdDeduction; // entertainment or professional taxes not fetched

  const netSalary = grossSalary;
  const incomeFromSal = Math.max(0, netSalary - totalSalaryDeduction);

  const savingsInterest = getSavingsInterest();
  const depositInterest = getDepositInterest();
  const dividends = getDividends();
  const incomeOthSrc = Math.round(savingsInterest + depositInterest + dividends);

  // LTCG u/s 112A from MF equity redemptions (SOS catCode in AIS)
  const getLtcg112A = () => {
    if (!ais?.partB?.sections) return { sale: 0, cost: 0, gain: 0 };
    let totalSale = 0, totalCost = 0;
    for (const sec of ais.partB.sections) {
      if (!Array.isArray(sec.elements)) continue;
      for (const el of sec.elements) {
        if (!el.l2?.columnLabel || !el.l2?.columnData) continue;
        const l2Cols = el.l2.columnLabel;
        const catIdx = l2Cols.indexOf("Information Category Code");
        if (catIdx === -1 || !el.l2.columnData.some(r => r[catIdx] === "SOS")) continue;
        if (!el.l1?.columnLabel || !el.l1?.columnData) continue;
        const fields = el.l1.columnLabel.map(c => c.field);
        const saleIdx = fields.indexOf("salesConsideration");
        const costIdx = fields.indexOf("costOfAcquisition");
        for (const row of el.l1.columnData) {
          totalSale += Math.round(parseAmt(row[saleIdx]));
          totalCost += Math.round(parseAmt(row[costIdx]));
        }
      }
    }
    return {
      sale: Math.round(totalSale),
      cost: Math.round(totalCost),
      gain: Math.max(0, Math.round(totalSale - totalCost))
    };
  };
  const ltcg = getLtcg112A();

  const grossTotIncome = incomeFromSal + incomeOthSrc;
  const grossTotIncomeIncLTCG112A = grossTotIncome + ltcg.gain;

  // 5. Deductions (Chapter VI-A) Mapping
  const raw80C = parseInt(taxpayerInfo.section80C) || 0;
  const raw80D = parseInt(taxpayerInfo.section80D) || 0;
  const raw80TTA = parseInt(taxpayerInfo.section80TTA) || 0;

  // Allowed deductions under Old Tax Regime
  let allowed80C = 0;
  let allowed80D = 0;
  let allowed80TTA = 0;

  if (optOutRegime === "Y") {
    allowed80C = Math.min(raw80C, 150000);
    allowed80D = Math.min(raw80D, 25000); // base limit
    allowed80TTA = Math.min(savingsInterest, Math.min(raw80TTA || savingsInterest, 10000));
  } else {
    // Under New Regime (AY 2026-27), most Chapter VI-A deductions are nil
    allowed80C = 0;
    allowed80D = 0;
    allowed80TTA = 0;
  }

  const totalChapVIADeductions = allowed80C + allowed80D + allowed80TTA;
  // TotalIncome includes LTCG for reporting, but slab tax only applies to non-LTCG income
  const totalIncome = Math.max(0, grossTotIncomeIncLTCG112A - totalChapVIADeductions);
  const slabTaxableIncome = Math.max(0, grossTotIncome - totalChapVIADeductions);

  // 6. Progressive Tax Mathematical Layer (AY 2026-27 / FY 2025-26)
  let computedTax = 0;
  let rebate87A = 0;

  if (optOutRegime === "N") {
    // New Tax Regime Slabs (AY 2026-27):
    // Up to 4L: Nil
    // 4L to 8L: 5%
    // 8L to 12L: 10%
    // 12L to 16L: 15%
    // 16L to 20L: 20%
    // 20L to 24L: 25%
    // Above 24L: 30%
    const ti = slabTaxableIncome;
    if (ti > 2400000) {
      computedTax = (ti - 2400000) * 0.30 + 100000 + 80000 + 60000 + 40000 + 20000;
    } else if (ti > 2000000) {
      computedTax = (ti - 2000000) * 0.25 + 80000 + 60000 + 40000 + 20000;
    } else if (ti > 1600000) {
      computedTax = (ti - 1600000) * 0.20 + 60000 + 40000 + 20000;
    } else if (ti > 1200000) {
      computedTax = (ti - 1200000) * 0.15 + 40000 + 20000;
    } else if (ti > 800000) {
      computedTax = (ti - 800000) * 0.10 + 20000;
    } else if (ti > 400000) {
      computedTax = (ti - 400000) * 0.05;
    } else {
      computedTax = 0;
    }

    // Section 87A rebate for New Regime: Up to 12 Lakhs income, rebate is 100% of tax (max ₹60,000)
    if (ti <= 1200000) {
      rebate87A = Math.min(computedTax, 60000);
    }
  } else {
    // Old Tax Regime Slabs (AY 2026-27):
    // Up to 2.5L: Nil
    // 2.5L to 5L: 5%
    // 5L to 10L: 20%
    // Above 10L: 30%
    const ti = slabTaxableIncome;
    if (ti > 1000000) {
      computedTax = (ti - 1000000) * 0.30 + 100000 + 12500;
    } else if (ti > 500000) {
      computedTax = (ti - 500000) * 0.20 + 12500;
    } else if (ti > 250000) {
      computedTax = (ti - 250000) * 0.05;
    } else {
      computedTax = 0;
    }

    // Section 87A rebate for Old Regime: Up to 5 Lakhs income, rebate is 100% of tax (max ₹12,500)
    if (ti <= 500000) {
      rebate87A = Math.min(computedTax, 12500);
    }
  }

  computedTax = Math.round(computedTax);
  rebate87A = Math.round(rebate87A);

  const taxPayableOnRebate = Math.max(0, computedTax - rebate87A);
  const educationCess = Math.round(taxPayableOnRebate * 0.04);
  const grossTaxLiability = taxPayableOnRebate + educationCess;
  const netTaxLiability = grossTaxLiability; // no Section 89 relief
  const totTaxPlusIntrstPay = netTaxLiability; // no interest u/s 234A/B/C

  // 7. TDS and Net Dues / Refund
  const salaryTdsList = getTdsSalaryList();
  const othersTdsList = getTdsOthersList();

  const totalTdsSalary = salaryTdsList.reduce((sum, item) => sum + item.TotalTDSSal, 0);
  const totalTdsOthers = othersTdsList.reduce((sum, item) => sum + item.TotTDSOnAmtPaid, 0);
  
  const totalTds = totalTdsSalary + totalTdsOthers;
  const totalTaxesPaid = totalTds; // assuming no TCS, Advance or Self-Assessment taxes

  const balTaxPayable = Math.max(0, totTaxPlusIntrstPay - totalTaxesPaid);
  const refundDue = Math.max(0, totalTaxesPaid - totTaxPlusIntrstPay);

  // 8. Compile Compliant Structure
  const CreationInfo = {
    SWVersionNo: "1.0",
    SWCreatedBy: "SW12345678", // Must match pattern [S][W][0-9]{8}
    JSONCreatedBy: "SW12345678",
    JSONCreationDate: new Date().toISOString().slice(0, 10),
    IntermediaryCity: "Delhi",
    Digest: "-"
  };

  const Form_ITR1 = {
    FormName: "ITR-1",
    Description: "ITR-1 for AY 2026-27",
    AssessmentYear: "2026",
    SchemaVer: "Ver1.0",
    FormVer: "Ver1.0"
  };

  //< Income tax metadata
  const PersonalInfo = {
    AssesseeName: {
      FirstName: firstName,
      MiddleName: middleName,
      SurNameOrOrgName: lastName
    },
    PAN: resolvedPan,
    Address: {
      ResidenceNo: addressInfo.residenceNo || "",
      ResidenceName: addressInfo.residenceName || "",
      RoadOrStreet: addressInfo.roadOrStreet || "",
      LocalityOrArea: addressInfo.localityOrArea || "",
      CityOrTownOrDistrict: addressInfo.cityOrTownOrDistrict || "",
      StateCode: addressInfo.stateCode || "09", // Default Delhi
      PinCode: parseInt(addressInfo.pinCode) || 0,
      CountryCode: "91",
      CountryCodeMobile: 91,
      MobileNo: parseInt(taxpayerInfo.phone || aisPhone) || 9876543210,
      EmailAddress: taxpayerInfo.email || aisEmail || "taxpayer@example.com"
    },
    SecondaryAdd: "N",
    DOB: taxpayerInfo.dob || "1990-01-01",
    EmployerCategory: taxpayerInfo.employerCategory || "OTH",
    AadhaarCardNo: taxpayerInfo.aadhaarCardNo || undefined
  };
  //> Income tax metadata

  // Add to input
  const FilingStatus = {
    ReturnFileSec: parseInt(verificationInfo.returnFileSec) || 11,
    SeventhProvisio139: "N",
    OptOutNewTaxRegime: optOutRegime,
    ItrFilingDueDate: "2026-07-31",
    AsseseeRepFlg: "N"
  };

  const ITR1_IncomeDeductions = {
    GrossSalary: grossSalary,
    Salary: grossSalary,
    PerquisitesValue: 0,
    ProfitsInSalary: 0,
    AllwncExemptUs10: {
      TotalAllwncExemptUs10: 0
    },
    NetSalary: netSalary,
    DeductionUs16: totalSalaryDeduction,
    DeductionUs16ia: stdDeduction,
    EntertainmentAlw16ii: 0,
    ProfessionalTaxUs16iii: 0,
    IncomeFromSal: incomeFromSal,
    IncomeOthSrc: incomeOthSrc,
    OthersInc: {
      OthersIncDtlsOthSrc: []
    },
    GrossTotIncome: grossTotIncome,
    GrossTotIncomeIncLTCG112A: grossTotIncomeIncLTCG112A,
    UsrDeductUndChapVIA: {
      Section80C: raw80C,
      Section80CCC: 0,
      Section80CCDEmployeeOrSE: 0,
      Section80CCD1B: 0,
      Section80CCDEmployer: 0,
      Section80D: raw80D,
      Section80DD: 0,
      Section80DDB: 0,
      Section80E: 0,
      Section80EE: 0,
      Section80EEA: 0,
      Section80EEB: 0,
      Section80G: 0,
      Section80GG: 0,
      Section80GGA: 0,
      Section80GGC: 0,
      Section80U: 0,
      Section80TTA: raw80TTA,
      Section80TTB: 0,
      AnyOthSec80CCH: 0,
      TotalChapVIADeductions: raw80C + raw80D + raw80TTA
    },
    DeductUndChapVIA: {
      Section80C: allowed80C,
      Section80CCC: 0,
      Section80CCDEmployeeOrSE: 0,
      Section80CCD1B: 0,
      Section80CCDEmployer: 0,
      Section80D: allowed80D,
      Section80DD: 0,
      Section80DDB: 0,
      Section80E: 0,
      Section80EE: 0,
      Section80EEA: 0,
      Section80EEB: 0,
      Section80G: 0,
      Section80GG: 0,
      Section80GGA: 0,
      Section80GGC: 0,
      Section80U: 0,
      Section80TTA: allowed80TTA,
      Section80TTB: 0,
      AnyOthSec80CCH: 0,
      TotalChapVIADeductions: totalChapVIADeductions
    },
    TotalIncome: totalIncome,
    ExemptIncAgriOthUs10: { ExemptIncAgriOthUs10Total: 0 },
    PropertyDetails: [],
    TotalIncomeChargeableUnHP: 0,
    DeductionUs57iia: 0
  };

  // Build dividend quarter breakdown from AIS l1 transaction dates
  const buildDivDateRange = () => {
    // FY 2025-26 quarters for advance tax: Upto15Of6, Upto15Of9, Up16Of9To15Of12, Up16Of12To15Of3, Up16Of3To31Of3
    const buckets = { Upto15Of6: 0, Upto15Of9: 0, Up16Of9To15Of12: 0, Up16Of12To15Of3: 0, Up16Of3To31Of3: 0 };
    if (!ais?.partB?.sections) return buckets;
    for (const sec of ais.partB.sections) {
      if (!Array.isArray(sec.elements)) continue;
      for (const el of sec.elements) {
        if (el.l1Src !== "AIS_TDS_TCS") continue; 
        if (!el.l2?.columnLabel || !el.l2?.columnData) continue;
        const l2Cols = el.l2.columnLabel;
        const catIdx = l2Cols.indexOf("Information Category Code");
        if (catIdx === -1 || !el.l2.columnData.some(r => r[catIdx] === "DIV")) continue;
        if (!el.l1?.columnLabel || !el.l1?.columnData) continue;
        const fields = el.l1.columnLabel.map(c => c.field);
        // SFT-015 uses 'reportedOn'; TDS sources use 'transactionDate'
        const dateField = ["transactionDate", "reportedOn", "paymentDate", "dividendDate"].find(f => fields.includes(f));
        const dateIdx = dateField ? fields.indexOf(dateField) : -1;
        const amtIdx = fields.indexOf("amtPaid") >= 0 ? fields.indexOf("amtPaid") : fields.indexOf("dividendAmount");
        let dt = new Date(1950, 0, 1);
        let elementAmt = 0;
        const statusIdx = fields.indexOf("status");
        for (const row of el.l1.columnData) {
          if (statusIdx !== -1 && row[statusIdx] === "Inactive") continue;
          const amt = parseAmt(row[amtIdx]);
          if (!amt) continue;
          elementAmt += amt;
          const rawDate = row[dateIdx] || "";
          // Parse DD/MM/YYYY
          const [d, m, y] = rawDate.split("/").map(Number);
          if (!d || !m || !y) continue;
          
          const rowDt = new Date(y, m - 1, d);
          if (rowDt > dt) {
            dt = rowDt;
          }
        }
        if (dt.getFullYear() > 1950) {
          if (dt <= new Date(2025, 5, 15))      buckets.Upto15Of6 += elementAmt;
          else if (dt <= new Date(2025, 8, 15)) buckets.Upto15Of9 += elementAmt;
          else if (dt <= new Date(2025, 11, 15)) buckets.Up16Of9To15Of12 += elementAmt;
          else if (dt <= new Date(2026, 2, 15))  buckets.Up16Of12To15Of3 += elementAmt;
          else if (dt <= new Date(2026, 2, 31)) buckets.Up16Of3To31Of3 += elementAmt;
          else buckets.Upto15Of6 += elementAmt;
        } else {
          buckets.Upto15Of6 += elementAmt;
        }
      }
    }
    const dividends = getDividends();
    const sumBuckets = buckets.Upto15Of6 + buckets.Upto15Of9 + buckets.Up16Of9To15Of12 + buckets.Up16Of12To15Of3 + buckets.Up16Of3To31Of3;
    buckets.Upto15Of6 += (dividends - sumBuckets);
    // Round all
    Object.keys(buckets).forEach(k => { buckets[k] = Math.round(buckets[k]); });
    return buckets;
  };

  // Map other income sources inside detailed block if they exist
  if (savingsInterest > 0) {
    ITR1_IncomeDeductions.OthersInc.OthersIncDtlsOthSrc.push({
      OthSrcNatureDesc: "SAV",
      OthSrcOthNatOfInc: "Interest from Saving Account",
      OthSrcOthAmount: Math.round(savingsInterest)
    });
  }
  if (depositInterest > 0) {
    ITR1_IncomeDeductions.OthersInc.OthersIncDtlsOthSrc.push({
      OthSrcNatureDesc: "IFD",
      OthSrcOthNatOfInc: "Interest from Deposit(Bank/Post Office/Cooperative Society)",
      OthSrcOthAmount: Math.round(depositInterest)
    });
  }
  if (dividends > 0) {
    ITR1_IncomeDeductions.OthersInc.OthersIncDtlsOthSrc.push({
      OthSrcNatureDesc: "DIV",
      OthSrcOthNatOfInc: "Dividend",
      OthSrcOthAmount: Math.round(dividends),
      DividendInc: { DateRange: buildDivDateRange() }
    });
  }

  const ITR1_TaxComputation = {
    TotalTaxPayable: computedTax,
    Rebate87A: rebate87A,
    TaxPayableOnRebate: taxPayableOnRebate,
    EducationCess: educationCess,
    GrossTaxLiability: grossTaxLiability,
    Section89: 0,
    NetTaxLiability: netTaxLiability,
    TotalIntrstPay: 0,
    IntrstPay: {
      IntrstPayUs234A: 0,
      IntrstPayUs234B: 0,
      IntrstPayUs234C: 0,
      LateFilingFee234F: 0,
      FeeFurnish234I: 0
    },
    TotTaxPlusIntrstPay: totTaxPlusIntrstPay
  };

  const TaxPaid = {
    TaxesPaid: {
      AdvanceTax: 0,
      TDS: totalTds,
      TCS: 0,
      SelfAssessmentTax: 0,
      TotalTaxesPaid: totalTaxesPaid
    },
    BalTaxPayable: balTaxPayable
  };

  const Refund = {
    RefundDue: refundDue,
    BankAccountDtls: {
      AddtnlBankDetails: [
        {
          IFSCCode: bankInfo.ifscCode || "",
          BankName: bankInfo.bankName || "",
          BankAccountNo: bankInfo.bankAccountNo || "",
          AccountType: bankInfo.accountType || "SB",
          UseForRefund: bankInfo.useForRefund === true || bankInfo.useForRefund === "true" ? "true" : "false"
        }
      ]
    }
  };

  // Compile conditional TDS lists
  const TDSonSalaries = salaryTdsList.length > 0 ? {
    TDSonSalary: salaryTdsList,
    TotalTDSonSalaries: totalTdsSalary
  } : undefined;

  const TDSonOthThanSals = othersTdsList.length > 0 ? {
    TDSonOthThanSal: othersTdsList,
    TotalTDSonOthThanSals: totalTdsOthers
  } : undefined;

  const Verification = {
    Declaration: {
      AssesseeVerName: verificationInfo.assesseeVerName || fullName,
      FatherName: verificationInfo.fatherName || "",
      AssesseeVerPAN: resolvedPan
    },
    Capacity: verificationInfo.capacity || "S",
    Place: verificationInfo.place || ""
  };

  const Schedule80D = {
    Sec80DSelfFamSrCtznHealth: {
      SeniorCitizenFlag: "S",
      SelfAndFamily: 0,
      HealthInsPremSlfFam: 0,
      PrevHlthChckUpSlfFam: 0,
      SelfAndFamilySeniorCitizen: 0,
      HlthInsPremSlfFamSrCtzn: 0,
      PrevHlthChckUpSlfFamSrCtzn: 0,
      MedicalExpSlfFamSrCtzn: 0,
      ParentsSeniorCitizenFlag: "P",
      Parents: 0,
      HlthInsPremParents: 0,
      PrevHlthChckUpParents: 0,
      ParentsSeniorCitizen: 0,
      HlthInsPremParentsSrCtzn: 0,
      PrevHlthChckUpParentsSrCtzn: 0,
      MedicalExpParentsSrCtzn: 0,
      EligibleAmountOfDedn: 0
    }
  };

  const LTCG112A = ltcg.sale > 0 ? {
    TotSaleCnsdrn: ltcg.sale,
    TotCstAcqisn: ltcg.cost,
    LongCap112A: ltcg.gain
  } : undefined;

  return {
    ITR: {
      ITR1: {
        CreationInfo,
        Form_ITR1,
        PersonalInfo,
        FilingStatus,
        ITR1_IncomeDeductions,
        ITR1_TaxComputation,
        TaxPaid,
        Refund,
        Schedule80D,
        TDSonSalaries,
        TDSonOthThanSals,
        ScheduleTDS3Dtls: { TotalTDS3Details: 0 },
        ScheduleTCS: { TotalSchTCS: 0 },
        Verification,
        ...(LTCG112A ? { LTCG112A } : {})
      }
    }
  };
}
