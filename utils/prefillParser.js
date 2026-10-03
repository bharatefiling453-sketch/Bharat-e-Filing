import {
  INITIAL_PROFILE,
  INITIAL_ADDRESS,
  INITIAL_BANK,
  INITIAL_VERIFICATION,
  mapStateToCode
} from "@/components/forms/common/constants";
import { decodeAadhaar } from "@/utils/aadhaarDecoder";

export const parsePrefillData = (data) => {
  if (!data) {
    return {
      profile: INITIAL_PROFILE,
      address: INITIAL_ADDRESS,
      bank: INITIAL_BANK,
      verification: INITIAL_VERIFICATION
    };
  }

  const pInfo = data.personalInfo || {};
  const pAddr = pInfo.address || {};
  const pBank = data.bankAccountDtls?.[0]?.addtnlBankDetails?.[0] || {};
  const pVerify = data.verification || {};

  const profile = {
    name: pInfo.assesseeVerName || "",
    pan: pInfo.pan || "",
    dob: pInfo.dob || "",
    employerCategory: data.lastFiledITR?.employerCategory || "",
    aadhaarCardNo: decodeAadhaar(pInfo.aadhaarCardNo) || "",
    email: pAddr.emailAddress || "",
    phone: pAddr.mobileNo ? String(pAddr.mobileNo) : "",
    section80C: data.insights?.UsrDeductUndChapVIAType?.Section80C || "",
    section80D: data.insights?.UsrDeductUndChapVIAType?.Section80D || "",
    section80TTA: data.insights?.UsrDeductUndChapVIAType?.Section80TTA || ""
  };

  const address = {
    residenceNo: pAddr.residenceNo || "",
    residenceName: pAddr.residenceName || "",
    roadOrStreet: pAddr.roadOrStreet || "",
    localityOrArea: pAddr.localityOrArea || "",
    cityOrTownOrDistrict: pAddr.cityOrTownOrDistrict || "",
    stateCode: pAddr.stateCode || "",
    pinCode: pAddr.pinCode ? String(pAddr.pinCode) : ""
  };

  const bank = {
    ifscCode: pBank.ifsccode || "",
    bankName: pBank.bankName || "",
    bankAccountNo: pBank.bankAccountNo || "",
    accountType: pBank.AccountType || "",
    useForRefund: pBank.useForRefund !== undefined ? (pBank.useForRefund === "true" || pBank.useForRefund === true) : false
  };

  const verification = {
    fatherName: pVerify.declaration?.fatherName || pInfo.fatherName || "",
    capacity: pVerify.capacity || pInfo.capacity || "",
    place: pAddr.localityOrArea || "",
    optOutNewTaxRegime: pVerify.optOutNewTaxRegime || ""
  };

  return { profile, address, bank, verification };
};

/**
 * Merges prefill data with extracted PAN and Aadhaar details in a prioritized fallback order.
 * 
 * @param {Object|null} prefillData - Raw prefill JSON data
 * @param {Object|null} panData - Extracted PAN card details
 * @param {Object|null} aadhaarData - Extracted Aadhaar card details
 * @returns {Object} Structured data with merged profile, address, bank, and verification
 */
export const mergeTaxpayerData = (prefillData, panData, aadhaarData) => {
  if (prefillData) {
    return parsePrefillData(prefillData);
  }

  const profileMerged = { ...INITIAL_PROFILE };
  const addressMerged = { ...INITIAL_ADDRESS };
  const bankMerged = { ...INITIAL_BANK };
  const verificationMerged = { ...INITIAL_VERIFICATION };

  if (panData) {
    profileMerged.name = panData.name || profileMerged.name;
    profileMerged.pan = panData.pan || profileMerged.pan;
    profileMerged.dob = panData.dob || profileMerged.dob;
    verificationMerged.fatherName = panData.fatherName || verificationMerged.fatherName;
  }

  if (aadhaarData) {
    profileMerged.name = aadhaarData.name || profileMerged.name || "";
    profileMerged.aadhaarCardNo = aadhaarData.aadhaarCardNo || profileMerged.aadhaarCardNo;
    profileMerged.dob = aadhaarData.dob || profileMerged.dob || "";
    profileMerged.email = aadhaarData.email || profileMerged.email;
    profileMerged.phone = aadhaarData.phone || profileMerged.phone;

    if (aadhaarData.address) {
      const addr = aadhaarData.address;
      addressMerged.residenceNo = addr.residenceNo || addressMerged.residenceNo;
      addressMerged.residenceName = addr.residenceName || addressMerged.residenceName;
      addressMerged.roadOrStreet = addr.roadOrStreet || addressMerged.roadOrStreet;
      addressMerged.localityOrArea = addr.localityOrArea || addressMerged.localityOrArea;
      addressMerged.cityOrTownOrDistrict = addr.cityOrTownOrDistrict || addressMerged.cityOrTownOrDistrict;
      addressMerged.stateCode = addr.state ? (mapStateToCode(addr.state) || addressMerged.stateCode) : addressMerged.stateCode;
      addressMerged.pinCode = addr.pinCode || addressMerged.pinCode;
    }
  }

  return {
    profile: profileMerged,
    address: addressMerged,
    bank: bankMerged,
    verification: verificationMerged
  };
};

