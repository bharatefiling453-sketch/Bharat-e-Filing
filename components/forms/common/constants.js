export const INITIAL_PROFILE = {
  name: "",
  pan: "",
  dob: "",
  employerCategory: "OTH",
  aadhaarCardNo: "",
  email: "",
  phone: "",
  section80C: "",
  section80D: "",
  section80TTA: ""
};

export const INITIAL_ADDRESS = {
  residenceNo: "",
  residenceName: "",
  roadOrStreet: "",
  localityOrArea: "",
  cityOrTownOrDistrict: "",
  stateCode: "15", // Karnataka default
  pinCode: ""
};

export const INITIAL_BANK = {
  ifscCode: "",
  bankName: "",
  bankAccountNo: "",
  accountType: "SB",
  useForRefund: true
};

export const INITIAL_VERIFICATION = {
  fatherName: "",
  capacity: "S", // Self
  place: "",
  optOutNewTaxRegime: "N" // Default New Tax Regime
};

export const PLACEHOLDERS = {
  profile: {
    name: "John Doe",
    pan: "ABCDE1234F",
    dob: "YYYY-MM-DD",
    aadhaarCardNo: "123456789012",
    phone: "9876543210",
    email: "john.doe@example.com",
    section80C: "150000",
    section80D: "25000",
    section80TTA: "10000"
  },
  address: {
    residenceNo: "Flat 402",
    residenceName: "Sunshine Apartments",
    roadOrStreet: "Main MG Road",
    localityOrArea: "Sector 5, Whitefield",
    cityOrTownOrDistrict: "Bengaluru",
    pinCode: "560066"
  },
  bank: {
    bankName: "Bank of Baroda",
    ifscCode: "BARB0WHITEF",
    bankAccountNo: "12345678901"
  },
  verification: {
    fatherName: "Richard Doe",
    place: "Bengaluru"
  }
};

export const STATE_CODES = {
  "andaman": "01",
  "andhra": "02",
  "arunachal": "03",
  "assam": "04",
  "bihar": "05",
  "chandigarh": "06",
  "chhattisgarh": "07",
  "dadra": "08",
  "daman": "08",
  "delhi": "09",
  "goa": "10",
  "gujarat": "11",
  "haryana": "12",
  "himachal": "13",
  "jammu": "14",
  "kashmir": "14",
  "jharkhand": "15",
  "karnataka": "16",
  "kerala": "17",
  "lakshadweep": "18",
  "madhya": "19",
  "maharashtra": "20",
  "manipur": "21",
  "meghalaya": "22",
  "mizoram": "23",
  "nagaland": "24",
  "odisha": "25",
  "orissa": "25",
  "puducherry": "26",
  "pondicherry": "26",
  "punjab": "27",
  "rajasthan": "28",
  "sikkim": "29",
  "tamil": "30",
  "tripura": "31",
  "uttar": "32",
  "west bengal": "33",
  "bengal": "33",
  "uttarakhand": "34",
  "telangana": "35",
  "ladakh": "36"
};

export const mapStateToCode = (stateName) => {
  if (!stateName) return "";
  const normalized = stateName.toLowerCase().replace(/[^a-z\s]/g, "").trim();
  for (const key of Object.keys(STATE_CODES)) {
    if (normalized.includes(key)) {
      return STATE_CODES[key];
    }
  }
  return "";
};
