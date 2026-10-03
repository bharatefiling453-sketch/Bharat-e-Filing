import { GoogleGenerativeAI } from "@google/generative-ai";

/**
 * Extracts the PAN (Permanent Account Number) from parsed tax documents
 * (such as AIS, TIS, or Form 26AS) at the root level or nested records.
 * 
 * @param {Object} data - Parsed document JSON object
 * @returns {string|null} The extracted PAN or null if not found
 */
export function extractPan(data) {
  if (!data) return null;

  // 1. AIS JSON: PAN is in metadata.loggedInPan
  if (data.metadata?.loggedInPan && typeof data.metadata.loggedInPan === "string") {
    return data.metadata.loggedInPan.trim().toUpperCase();
  }

  // 2. AIS JSON: partA.columnData[0] is also the PAN
  if (Array.isArray(data.partA?.columnData) && typeof data.partA.columnData[0] === "string") {
    return data.partA.columnData[0].trim().toUpperCase();
  }

  // 3. Check for root level pan key
  if (data.pan && typeof data.pan === "string") {
    return data.pan.trim().toUpperCase();
  }

  // 4. Check nested records list (e.g. from legacy formats)
  if (Array.isArray(data.records)) {
    for (const record of data.records) {
      if (record?.pan && typeof record.pan === "string") {
        return record.pan.trim().toUpperCase();
      }
    }
  }

  return null;
}

/**
 * Sends a PAN card image to Gemini to extract all details.
 * 
 * @param {Buffer} imageBuffer - Buffer of the uploaded file
 * @param {string} mimeType - MIME type of the file
 * @returns {Promise<Object>} The extracted details
 */
export async function extractPanFromImage(imageBuffer, mimeType) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY environment variable is not configured.");
  }

  const genAI = new GoogleGenerativeAI(apiKey);
  const model = genAI.getGenerativeModel({
    model: "gemini-2.5-flash",
    generationConfig: {
      responseMimeType: "application/json",
    }
  });

  const prompt = `You are an expert Indian Income Tax assistant. Extract the taxpayer's details from this PAN card.
Return a structured JSON object with the following fields:
- "name": Full name of the card holder.
- "pan": The 10-character alphanumeric PAN number.
- "dob": The date of birth formatted as YYYY-MM-DD.
- "fatherName": The father's name of the card holder (if present).

If any information is not present in the image, return empty string ("") for that field. Do not use placeholders or guess.`;

  const response = await model.generateContent([
    prompt,
    {
      inlineData: {
        data: Buffer.from(imageBuffer).toString("base64"),
        mimeType: mimeType
      }
    }
  ]);

  const text = response.response.text();
  try {
    return JSON.parse(text);
  } catch (e) {
    throw new Error("Failed to parse PAN extraction response from Gemini: " + text);
  }
}

/**
 * Client-side helper to upload a PAN card image/PDF to the backend API route.
 * 
 * @param {File} file - The uploaded file object
 * @returns {Promise<Object>} The extracted details
 */
export async function parsePanImageClient(file) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("type", "pan");

  const res = await fetch("/api/extract-document", {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText || "Failed to extract PAN details.");
  }

  return await res.json();
}


