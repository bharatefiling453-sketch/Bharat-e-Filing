import { GoogleGenerativeAI } from "@google/generative-ai";

export const decodeAadhaar = (base64Str) => {
  if (!base64Str) return "";
  try {
    if (/^[A-Za-z0-9+/=]+$/.test(base64Str) && base64Str.length % 4 === 0) {
      return typeof window !== "undefined"
        ? window.atob(base64Str)
        : Buffer.from(base64Str, "base64").toString("utf-8");
    }
  } catch (e) {
    // fallback
  }
  return base64Str;
};

/**
 * Sends an Aadhaar card image to Gemini to extract all details.
 * 
 * @param {Buffer} imageBuffer - Buffer of the uploaded file
 * @param {string} mimeType - MIME type of the file
 * @returns {Promise<Object>} The extracted details
 */
export async function extractAadhaarFromImage(imageBuffer, mimeType) {
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

  const prompt = `You are an expert Indian Income Tax assistant. Extract the details from this Aadhaar card image.
Return a structured JSON object with the following fields:
- "name": Full name of the card holder.
- "aadhaarCardNo": The 12-digit Aadhaar Card number (do not include spaces, just the 12 digits).
- "dob": The date of birth formatted as YYYY-MM-DD.
- "email": Email address (if present).
- "phone": Mobile number (if present).
- "address": An object containing the address details:
  - "residenceNo": Flat, house, or apartment number.
  - "residenceName": Building or apartment complex name.
  - "roadOrStreet": Street, road, lane name.
  - "localityOrArea": Locality, area, sector name.
  - "cityOrTownOrDistrict": City, town, or district name.
  - "state": State name (e.g. "Karnataka", "Maharashtra", "Delhi").
  - "pinCode": 6-digit postal pin code.

If any field is missing or not visible in the image, return empty string ("") for that field or subfield. Do not use placeholders or guess.`;

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
    throw new Error("Failed to parse Aadhaar extraction response from Gemini: " + text);
  }
}

/**
 * Client-side helper to upload an Aadhaar card image/PDF to the backend API route.
 * 
 * @param {File} file - The uploaded file object
 * @returns {Promise<Object>} The extracted details
 */
export async function parseAadhaarImageClient(file) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("type", "aadhaar");

  const res = await fetch("/api/extract-document", {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText || "Failed to extract Aadhaar details.");
  }

  return await res.json();
}


