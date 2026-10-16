# ITR-1 self-filing app (AY 2026-27)

Location: `website/itr-self-filing/`. Build with `npm run build:itr`, test with `npm run test:itr` (add `npm run test:itr:ocr` for the scanned-Form-16 OCR run). Serve the `website/` folder over HTTP and open `/itr-self-filing/`.

## The five steps

1. **PAN and consent.**
   - PAN check: the format is validated and the 4th letter must be P (individuals).
   - Date of birth is collected for the age slab.
   - **Aadhaar OTP 1** adds Bharat e-Filing as the taxpayer's ERI (client onboarding).
   - **Aadhaar OTP 2** gives consent to import pre-filled data, AIS, TIS and Form 26AS.
   - An ITR-1 disqualifier checklist follows.
2. **Form 16.**
   - Upload one or more Form 16s as PDF or photo.
   - Below the upload box: *"Don't have Form 16? Click here to enter your salary manually"*.
   - Digital PDFs are read from the text layer (exact). Scanned PDFs and photos use OCR after the gridlines are removed.
   - Password-protected PDFs are opened with the PAN or DOB automatically, or the user is asked for the password.
3. **Income: all five heads on one screen,** pre-filled from Form 16, pre-fill and AIS.
   - **Salary / pension:**
     - *Add bifurcation* popup: head-wise 17(1) break-up, 17(2), 17(3), the section 10 exemptions with an HRA calculator, 16(ii)/16(iii) and TDS.
     - Or *Upload salary slip* (PDF or photo, OCR), which annualises by the number of months.
     - *Add pension*: uncommuted and commuted pension, the 10(10A) exemption, and a family-pension shortcut.
   - **House property:** *Add rental income* popup (let-out, self-occupied or deemed let-out; share %; rent; municipal tax; tenant; home-loan interest), with a live income preview. Maximum of 2 properties.
   - **Capital gains:** LTCG u/s 112A entered manually, or *Upload broker Tax P&L (Excel/CSV)*.
     - Columns and sections are detected automatically, with 31 Jan 2018 grandfathering.
     - Short-term, intraday and F&O gains are flagged as needing ITR-2 or ITR-3.
   - **Other sources:** AIS figures pre-filled, plus *Add any other income*, which lists only the types ITR-1 allows.
   - **Business:** shown as not applicable in ITR-1.
4. **Deductions, regime and taxes paid.**
   - Regime comparison. A belated return is locked to the new regime under s.115BAC(6).
   - Chapter VI-A deductions with their statutory caps.
   - TDS/TCS from 26AS, advance and self-assessment challans, and the refund bank account.
5. **Computation and file.**
   - *Create computation* produces a CA-style statement.
   - *Download computation (PDF)* and *Download ITR-1 JSON*.
   - *File now*:
     1. If tax is due, pay it first.
     2. Declaration.
     3. Submit.
     4. Aadhaar OTP e-verification and acknowledgement.

## Accuracy safeguards ("no mistakes")

- **Form 16 cross-checks:**
  - **Totals:** 1(d)=a+b+c; 2(i); 3; 5; 6; 8; 9; 10(d); 11; 12; 17; 21.
  - **Part A:** total TDS equals Part B net tax; amount paid equals salary.
  - **Form 12BA:** perquisites and 17(3) totals equal Part B.
  - **Standard deduction:** ₹75,000 or ₹50,000.
  - **Identity:** employee PAN and AY 2026-27.
  - **Form 26AS:** TDS matches.
- **When checks fail:** any value that fails a check, is missing, or came from OCR below 90% confidence is highlighted. *Use these figures* stays disabled until the user corrects or confirms each one.
- **Tax engine** (`src/tax.js`):
  - FY 2025-26 slabs, the s.87A rebate with marginal relief, and the 4% cess.
  - Section 288A/288B rounding.
  - House-property rules (₹2 lakh caps; losses ignored in the new regime), s.57(iia) family pension, and the 80C/80D/80CCD caps.
  - Interest under 234A/234B/234C (Rule 119A rounding; seniors exempt) and the 234F fee.
  - ITR-1 eligibility blocks (₹50 lakh income, LTCG ₹1.25 lakh, 2 properties, STCG, directors, unlisted shares, foreign assets, and so on).
- **Tests:**
  - 21 tax tests and the Form 16 test (digital).
  - P&L tests.
  - Full browser runs:
    - the digital Form 16 run, with every figure checked against a hand computation;
    - the OCR run on a scanned Form 16, where all key fields are read exactly;
    - salary-slip OCR, the PDF and JSON downloads, filing and e-verification.

## What to do before go-live

- **ERI APIs:** replace the bodies in `src/api.js` (`addClient`, `validateClientOtp`, `requestPrefillOtp`, `getPrefill`, `submitReturn`, `requestEVerifyOtp`, `eVerify`) with the real calls. The UI does not change. Then remove *Demo mode* (`DEMO = false`).
- **ITR-1 JSON:** validate `src/itrjson.js` against the official AY 2026-27 schema and utility, and adjust field codes where needed.
- **Real Form 16s:** test with 20 or more real samples (TRACES, Zoho/Keka/Greythr payroll exports, scans and phone photos). Add any new label wording to `PART_B_FIELDS`.
- **Not automated yet:**
  - relief u/s 89 (Form 10E figure is entered manually);
  - the 234C dividend relief;
  - the TDS-certificate-wise claim split;
  - multiple-state professional tax.
