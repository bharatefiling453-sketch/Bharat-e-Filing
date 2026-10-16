// Builds the ITR-1 return as JSON for upload. The structure follows the CBDT ITR-1 schema layout
// (ITR → ITR1 → PersonalInfo / FilingStatus / ITR1_IncomeDeductions / ITR1_TaxComputation / TaxPaid …).
// BEFORE GO-LIVE: validate against the official AY 2026-27 ITR-1 JSON schema published on the e-filing portal
// and adjust field names/codes where the schema differs. The figures come from compute() in tax.js.
const r = (v) => Math.round(Number(v) || 0);

export function buildItr1Json(data, c) {
  const p = data.personal || {};
  const [first, ...rest] = (p.name || "").split(" ");
  const bank = (data.bankAccounts || []).find((b) => b.refund) || (data.bankAccounts || [])[0] || {};
  return {
    ITR: {
      ITR1: {
        CreationInfo: { SWVersionNo: "1.0", SWCreatedBy: "BEFERI", JSONCreatedBy: "BEFERI", JSONCreationDate: new Date().toISOString().slice(0, 10), IntermediaryCity: "Pune", Digest: "-" },
        Form_ITR1: { FormName: "ITR-1", Description: "For Indls having Income from Salary, Pension, family pension and Interest", AssessmentYear: "2026", SchemaVer: "Ver1.0", FormVer: "Ver1.0" },
        PersonalInfo: {
          AssesseeName: { FirstName: first || "", SurNameOrOrgName: rest.join(" ") },
          PAN: p.pan, DOB: p.dob, AadhaarCardNo: p.aadhaar || "",
          Address: { ResidenceNo: "", LocalityOrArea: p.address || "", CountryCode: "91", MobileNo: p.mobile || "", EmailAddress: p.email || "" },
          EmployerCategory: "OTH",
        },
        FilingStatus: {
          ReturnFileSec: c.meta.belated ? 12 : 11, // 11 = 139(1), 12 = 139(4)
          OptOutNewTaxRegime: c.meta.regime === "old" ? "Y" : "N",
          ItrFilingDueDate: "2026-07-31",
        },
        ITR1_IncomeDeductions: {
          GrossSalary: r(c.salary.gross),
          Salary: r(sum(data.salary?.employers, "s17_1")),
          PerquisitesValue: r(sum(data.salary?.employers, "s17_2")),
          ProfitsInSalary: r(sum(data.salary?.employers, "s17_3")),
          AllwncExtentExemptUs10: r(c.salary.exempt),
          NetSalary: r(c.salary.net),
          DeductionUs16: r(c.salary.standardDeduction + c.salary.entAllow + c.salary.profTax),
          DeductionUs16ia: r(c.salary.standardDeduction),
          EntertainmentAlw16ii: r(c.salary.entAllow),
          ProfessionalTaxUs16iii: r(c.salary.profTax),
          IncomeFromSal: r(c.salary.income),
          HousePropertyDtls: c.houseProperty.rows.map((h) => ({
            TypeOfHP: h.type === "self" ? "S" : h.type === "deemed" ? "D" : "L",
            GrossRentReceived: r(h.gav || 0), TaxPaidlocalAuth: r((h.municipalTax || 0) * (h.share || 1)), AnnualValue: r(h.annualValue),
            StandardDeduction: r(h.standard30), InterestPayable: r(h.interestClaimed), TotalIncomeOfHP: r(h.income),
          })),
          TotalIncomeOfHP: r(c.houseProperty.income),
          IncomeOthSrc: r(c.otherSources.income),
          OthersInc: { OthersIncDtlsOthSrc: c.otherSources.items.map(([label, amt, code]) => ({ OthSrcNatureDesc: { savings: "SAV", deposit: "IFD", refund: "TAX", dividend: "DIV", familyPension: "FAP" }[code] || "OTH", OthSrcOthNatureDesc: label, OthSrcOthAmount: r(amt) })) },
          DeductionUs57iia: r(c.otherSources.familyPensionDeduction),
          LTCG112A: { TotSaleCnsdrn: r(data.ltcg112a?.saleValue), TotCstAcqisn: r(data.ltcg112a?.costOfAcquisition), LongCap112A: r(c.ltcg112a.gain) },
          GrossTotIncome: r(c.grossTotalIncome),
          DeductUndChapVIA: Object.fromEntries(c.deductions.list.map((d) => ["Section" + d.code.replace(/[^0-9A-Z]/gi, ""), r(d.allowed)])),
          TotalChapVIADeductions: r(c.deductions.total),
          TotalIncome: r(c.totalIncome),
          ExemptIncAgriOthUs10: { ExemptIncAgriOthUs10Total: r(data.exemptIncome?.agriculture) },
        },
        ITR1_TaxComputation: {
          TotalTaxPayable: r(c.tax.slabTax + c.tax.tax112A), Rebate87A: r(c.tax.rebate87A),
          TaxPayableOnRebate: r(c.tax.slabTax + c.tax.tax112A - c.tax.rebate87A), EducationCess: r(c.tax.cess),
          GrossTaxLiability: r(c.tax.grossTax), Section89: r(c.tax.relief89), NetTaxLiability: r(c.tax.netTax),
          TotalIntrstPay: r(c.interest.i234A + c.interest.i234B + c.interest.i234C + c.lateFee),
          IntrstPay: { IntrstPayUs234A: r(c.interest.i234A), IntrstPayUs234B: r(c.interest.i234B), IntrstPayUs234C: r(c.interest.i234C), LateFilingFee234F: r(c.lateFee) },
          TotTaxPlusIntrstPay: r(c.totalLiability),
        },
        TaxPaid: {
          TaxesPaid: { AdvanceTax: r(c.paid.advance), TDS: r(c.paid.tdsSalary + c.paid.tdsOther), TCS: r(c.paid.tcs), SelfAssessmentTax: r(c.paid.selfAssessment), TotalTaxesPaid: r(c.paid.total) },
          BalTaxPayable: r(c.payable),
        },
        Refund: {
          RefundDue: r(c.refund),
          BankAccountDtls: { AddtnlBankDetails: (data.bankAccounts || []).map((b) => ({ IFSCCode: b.ifsc, BankName: b.bank, BankAccountNo: b.account, AccountType: "SB", UseForRefund: b === bank ? "true" : "false" })) },
        },
        TDSonSalaries: { TDSonSalary: (data.salary?.employers || []).map((e) => ({ EmployerOrDeductorOrCollectDetl: { TAN: e.tan, EmployerOrDeductorOrCollecterName: e.name }, IncChrgSal: r(n(e.s17_1) + n(e.s17_2) + n(e.s17_3)), TotalTDSSal: r(e.tds) })) },
        TDSonOthThanSals: { TDSonOthThanSal: (data.taxes?.tdsOther || []).map((t) => ({ EmployerOrDeductorOrCollectDetl: { TAN: t.tan, EmployerOrDeductorOrCollecterName: t.deductor }, AmtForTaxDeduct: r(t.amountPaid), DeductedYr: "2025", TotTDSOnAmtPaid: r(t.tds), ClaimOutOfTotTDSOnAmtPaid: r(t.tds) })) },
        TaxPayments: { TaxPayment: [...(data.taxes?.advance || []), ...(data.taxes?.selfAssessment || [])].map((t) => ({ BSRCode: t.bsr || "", DateDep: t.date, SrlNoOfChaln: t.challan || "", Amt: r(t.amount) })) },
        Verification: { Declaration: { AssesseeVerName: p.name, FatherName: "", AssesseeVerPAN: p.pan }, Capacity: "S", Place: "" },
      },
    },
  };
}
const n = (v) => Number(v) || 0;
const sum = (arr, k) => (arr || []).reduce((a, x) => a + n(x[k]), 0);
