import * as zip from "@zip.js/zip.js";

/**
 * Converts a DOB string from YYYY-MM-DD (HTML date input format) to DDMMYYYY.
 * If the input is already in a clean 8-digit format, returns it as is.
 * 
 * @param {string} dobStr - The DOB string (e.g. "1990-01-01")
 * @returns {string} The formatted DOB (e.g. "01011990")
 */
function formatDobToDdMmYyyy(dobStr) {
  if (!dobStr) return "";
  const cleaned = dobStr.trim();
  
  // Handle YYYY-MM-DD
  if (cleaned.includes("-")) {
    const parts = cleaned.split("-");
    if (parts.length === 3) {
      const [year, month, day] = parts;
      return `${day}${month}${year}`;
    }
  }
  
  // Handle DD/MM/YYYY
  if (cleaned.includes("/")) {
    const parts = cleaned.split("/");
    if (parts.length === 3) {
      const [day, month, year] = parts;
      return `${day}${month}${year}`;
    }
  }

  // Fallback: strip non-digits
  return cleaned.replace(/\D/g, "");
}

/**
 * Converts a hex string into an ArrayBuffer.
 * 
 * @param {string} hexString - Hex representation of bytes
 * @returns {ArrayBuffer} ArrayBuffer representing bytes
 */
function hexToBytes(hexString) {
  const bytes = new Uint8Array(hexString.length / 2);
  for (let i = 0; i < bytes.length; i++) {
    bytes[i] = parseInt(hexString.substring(i * 2, i * 2 + 2), 16);
  }
  return bytes.buffer;
}

/**
 * Converts a Base64 string into an ArrayBuffer.
 * 
 * @param {string} base64String - Base64 encoded string
 * @returns {ArrayBuffer} ArrayBuffer representing decoded bytes
 */
function base64ToBytes(base64String) {
  const binaryString = atob(base64String);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

/**
 * Decrypts a password-protected ZIP archive containing AIS, TIS, or Form 26AS JSON data.
 * 
 * @param {Blob|File} fileBlob - The uploaded ZIP file
 * @param {string} pan - Taxpayer PAN
 * @param {string} dob - Taxpayer DOB (e.g. "YYYY-MM-DD")
 * @returns {Promise<Object>} Decrypted JSON content parsed into an object
 */
async function decryptTaxZip(fileBlob, pan, dob) {
  if (!fileBlob) throw new Error("No file uploaded");
  if (!pan) throw new Error("PAN is required to unlock this file");
  if (!dob) throw new Error("Date of birth is required to unlock this file");

  // Derive password: lowercase(PAN) + DDMMYYYY(DOB)
  const cleanPan = pan.trim();
  const cleanDob = formatDobToDdMmYyyy(dob);
  const password = `${cleanPan.toLowerCase()}GQ39%*g${cleanDob}`;

  const reader = new zip.ZipReader(new zip.BlobReader(fileBlob), { password });
  try {
    const entries = await reader.getEntries();
    
    // Find the first JSON file inside the ZIP
    const jsonEntry = entries.find(entry => entry.filename.toLowerCase().endsWith(".json"));
    
    if (!jsonEntry) {
      throw new Error("No JSON file found inside the ZIP archive");
    }

    // Extract JSON contents as a string
    const textWriter = new zip.TextWriter();
    const jsonText = await jsonEntry.getData(textWriter);
    
    // Decryption was successful
    return JSON.parse(jsonText);
  } catch (error) {
    if (error.message?.includes("password") || error.message?.includes("decrypt") || error.message?.includes("AES")) {
      throw new Error("Incorrect Password. Please check your PAN and Date of Birth details.");
    }
    throw error;
  } finally {
    await reader.close();
  }
}

async function decryptAesCbcTaxJson(fileText, pan, dob) {
  // Extract IV (first 32 characters) and Salt (next 32 characters)
  const ivHex = fileText.substring(0, 32);
  const saltHex = fileText.substring(32, 64);
  const ciphertextBase64 = fileText.substring(64);

  const cleanPan = pan.trim();
  const cleanDob = formatDobToDdMmYyyy(dob);
  const password = `${cleanPan.toLowerCase()}GQ39%*g${cleanDob}`;

  const subtle = crypto?.subtle || (await import("crypto")).webcrypto.subtle;
  const enc = new TextEncoder();
  
  const saltBuffer = hexToBytes(saltHex);
  const ivBuffer = hexToBytes(ivHex);
  const ciphertextBuffer = base64ToBytes(ciphertextBase64);

  // Import base key
  const passwordKey = await subtle.importKey(
    "raw",
    enc.encode(password),
    "PBKDF2",
    false,
    ["deriveKey"]
  );

  // Derive AES decryption key (256-bit CBC) using PBKDF2
  const derivedKey = await subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: saltBuffer,
      iterations: 1000,
      hash: "SHA-256"
    },
    passwordKey,
    {
      name: "AES-CBC",
      length: 256
    },
    false,
    ["decrypt"]
  );

  // Decrypt cipher text
  const decryptedBuffer = await subtle.decrypt(
    {
      name: "AES-CBC",
      iv: ivBuffer
    },
    derivedKey,
    ciphertextBuffer
  );

  const decryptedText = new TextDecoder().decode(decryptedBuffer);
  return JSON.parse(decryptedText);
}

/**
 * Parses caret-separated Form 26AS text statements.
 * 
 * @param {string} fileText - Caret-separated Form 26AS text content
 * @returns {Object} Extracted data containing taxDeductedAtSource
 */
function parseForm26AsTxt(fileText) {
  const lines = fileText.split(/\r?\n/);
  const taxDeductedAtSource = [];
  
  let currentDeductor = null;
  let inPartI = false;
  let inPartII = false;
  
  for (let line of lines) {
    line = line.trim();
    if (!line) continue;
    
    // Detect section transitions
    if (line.includes("PART-I - Details of Tax Deducted at Source")) {
      inPartI = true;
      inPartII = false;
      continue;
    }
    if (line.includes("PART-II - Details of Tax Deducted at Source for 15G / 15H")) {
      inPartI = false;
      inPartII = true;
      continue;
    }
    if (line.startsWith("^PART-") || line.includes("PART-")) {
      // Any other part ends Part I & II
      inPartI = false;
      inPartII = false;
      continue;
    }
    
    if (inPartI || inPartII) {
      const parts = line.split("^");
      
      // A transaction row starts with empty element because line starts with ^ (e.g., ^1^194^...)
      if (line.startsWith("^")) {
        // Skip transaction headers or empty/announcement rows
        if (parts[1] === "Sr. No." || parts[1]?.includes("No Transactions Present") || !parts[1]) {
          continue;
        }
        
        // This is a transaction row
        if (currentDeductor && parts.length >= 10) {
          const section = parts[2]?.trim();
          const amtPaid = parseFloat(parts[7]?.replace(/,/g, "")) || 0;
          const tdsDep = parseFloat(parts[9]?.replace(/,/g, "")) || 0;
          
          taxDeductedAtSource.push({
            section: section,
            tanOfDeductor: currentDeductor.tan,
            deductorName: currentDeductor.name,
            totalAmountPaid: amtPaid,
            totalTaxDeposited: tdsDep
          });
        }
      } else {
        // This is a deductor header row
        // Format: Sr. No.^Name of Deductor^TAN of Deductor^^^^^Total Amount Paid / Credited(Rs.)^Total Tax Deducted(Rs.)^Total TDS Deposited(Rs.)
        // Skip the header row itself: "Sr. No.^Name of Deductor^TAN of Deductor..."
        if (parts[0] === "Sr. No." || !parts[1] || !parts[2]) {
          continue;
        }
        
        // Save the current deductor context
        currentDeductor = {
          name: parts[1]?.trim(),
          tan: parts[2]?.trim()
        };
      }
    }
  }
  
  return {
    documentType: "Form 26AS (Caret-separated Text)",
    taxDeductedAtSource
  };
}

/**
 * Parses a tax source document (ZIP, JSON, or PDF).
 * Detects encrypted ZIP files disguised with a .json extension by checking magic bytes.
 * Also decrypts custom AES-CBC encrypted JSON files when plain JSON parsing fails.
 * 
 * @param {File} file - Raw uploaded file object
 * @param {string} pan - Taxpayer PAN
 * @param {string} dob - Taxpayer DOB (YYYY-MM-DD)
 * @param {string} [formName] - The form/document type ID (e.g., "form26as", "ais", "tis")
 * @returns {Promise<Object>} Cleaned/decrypted tax data
 */
export async function parseTaxFile(file, pan, dob, formName) {
  if (!file) return null;

  // If formName is form26as, parse directly as caret-separated text
  if (formName === "form26as") {
    const text = await file.text();
    return parseForm26AsTxt(text);
  }

  // Read first 4 bytes to check for zip header magic bytes (PK\x03\x04)
  const buffer = await file.slice(0, 4).arrayBuffer();
  const arr = new Uint8Array(buffer);
  const isZip = arr[0] === 0x50 && arr[1] === 0x4B; // 'P' and 'K'

  // ZIP file decryption (either ends with .zip or has zip file signature)
  if (isZip) {
    if (!pan || !dob) {
      throw new Error(
        "Please fill in your PAN Card Number and Date of Birth in Section 2 first, so we can decrypt this password-protected ZIP file."
      );
    }
    return await decryptTaxZip(file, pan, dob);
  }

  // JSON file parsing
  const fileName = file.name.toLowerCase();
  if (file.type === "application/json" || fileName.endsWith(".json")) {
    const text = await file.text();
    try {
      return JSON.parse(text);
    } catch (err) {
      const cleanText = text.trim();
      // Check if it starts with 64-char hex header representing IV and salt
      const isHexHeader = /^[0-9a-fA-F]{64}/.test(cleanText);
      if (isHexHeader) {
        if (!pan || !dob) {
          throw new Error(
            "Please fill in your PAN Card Number and Date of Birth in Section 2 first, so we can decrypt this password-protected document."
          );
        }
        try {
          return await decryptAesCbcTaxJson(cleanText, pan, dob);
        } catch (decryptErr) {
          throw new Error("Incorrect Password or Invalid Encrypted JSON file. Please check your PAN and Date of Birth.");
        }
      }
      throw err;
    }
  }


  // PDF format fallback structure (returning only the arrays utilized by the generator)
  return {
    records: [],
    taxDeductedAtSource: []
  };
}
