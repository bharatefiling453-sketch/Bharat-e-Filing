// ERI (e-Return Intermediary) API layer.
// DEMO MODE: every call below returns sample data so the whole flow can be used end to end.
// When the Type-2 ERI registration is approved, replace each function body with the real call
// (same names and return shapes) — the UI does not need to change.
//   addClient / validateClientOtp      → ERI "add client" with taxpayer consent (Aadhaar OTP #1)
//   requestPrefillOtp / getPrefill      → pre-filled data + AIS + TIS + Form 26AS (Aadhaar OTP #2)
//   submitReturn / eVerify             → upload ITR JSON, e-verify with Aadhaar OTP
export const DEMO = true;
const DEMO_OTP = "123456";
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const txn = () => "TXN" + Math.random().toString(36).slice(2, 10).toUpperCase();

export async function verifyPan(pan, dob) {
  await wait(500);
  if (!/^[A-Z]{5}[0-9]{4}[A-Z]$/.test(pan)) throw new Error("Enter a valid 10-character PAN, e.g. ABCPS1234K.");
  if (pan[3] !== "P") throw new Error("ITR-1 is only for individuals: the 4th letter of an individual's PAN is P.");
  return { pan, name: pan === "ABCPS1234K" ? "RAHUL KUMAR SHARMA" : "DEMO TAXPAYER", aadhaarLinked: true, aadhaarMasked: "XXXX XXXX 4321", mobileMasked: "+91 98XXXXXX21" };
}

export async function addClient(pan) { await wait(600); return { txnId: txn(), sentTo: "+91 98XXXXXX21" }; }
export async function validateClientOtp(txnId, otp) {
  await wait(500);
  if (DEMO && otp !== DEMO_OTP) throw new Error("Incorrect OTP. (Demo: use 123456)");
  return { clientAdded: true, eriClientId: "BEF-" + Date.now().toString(36).toUpperCase() };
}

export async function requestPrefillOtp(pan) { await wait(600); return { txnId: txn(), sentTo: "+91 98XXXXXX21" }; }
export async function getPrefill(txnId, otp, pan) {
  await wait(900);
  if (DEMO && otp !== DEMO_OTP) throw new Error("Incorrect OTP. (Demo: use 123456)");
  const demoName = pan === "ABCPS1234K";
  return {
    personal: {
      name: demoName ? "RAHUL KUMAR SHARMA" : "DEMO TAXPAYER", pan, dob: demoName ? "1990-05-10" : "1988-01-15", aadhaar: "XXXX XXXX 4321",
      mobile: "98XXXXXX21", email: "r****@gmail.com", address: "B-12, Green Avenue, Pune, Maharashtra 411001", residentialStatus: "RES",
    },
    bankAccounts: [
      { bank: "State Bank of India", ifsc: "SBIN0001234", account: "XXXXXXX4521", type: "Savings", prevalidated: true, refund: true },
      { bank: "HDFC Bank", ifsc: "HDFC0000123", account: "XXXXXXX8890", type: "Savings", prevalidated: true, refund: false },
    ],
    // Form 26AS / AIS (TDS on salary by employer)
    tdsSalary: [{ employer: "ACME SOFTWARE PRIVATE LIMITED", tan: "MUMA12345B", amountPaid: 1456000, tds: 82836 }],
    tdsOther: [{ deductor: "HDFC BANK LIMITED", tan: "MUMH03189E", section: "194A", amountPaid: 24600, tds: 2460 }],
    tcs: [],
    taxPayments: [],
    // AIS / TIS income items
    ais: {
      savingsInterest: [{ source: "State Bank of India", amount: 8420 }, { source: "HDFC Bank", amount: 1210 }],
      depositInterest: [{ source: "HDFC Bank (fixed deposit)", amount: 24600 }],
      dividend: [{ source: "Infosys Ltd", amount: 3150 }],
      refundInterest: [],
      salary: [{ source: "ACME SOFTWARE PRIVATE LIMITED (MUMA12345B)", amount: 1456000 }],
      securitiesSold: [{ source: "Equity shares (listed) — sale value reported by broker", amount: 120500 }],
    },
  };
}

export async function submitReturn(itrJson) {
  await wait(1200);
  return { status: "SUBMITTED", ackNo: "4" + String(Date.now()).slice(-14), filedOn: new Date().toISOString().slice(0, 10) };
}
export async function requestEVerifyOtp(ackNo) { await wait(500); return { txnId: txn(), sentTo: "+91 98XXXXXX21" }; }
export async function eVerify(ackNo, otp) {
  await wait(800);
  if (DEMO && otp !== DEMO_OTP) throw new Error("Incorrect OTP. (Demo: use 123456)");
  return { verified: true, verifiedOn: new Date().toISOString().slice(0, 10) };
}
