import { NextResponse } from "next/server";
import { extractPanFromImage } from "@/utils/panExtractor";
import { extractAadhaarFromImage } from "@/utils/aadhaarDecoder";

export async function POST(request) {
  try {
    const formData = await request.formData();
    const file = formData.get("file");
    const docType = formData.get("type"); // "pan" or "aadhaar"

    if (!file) {
      return new NextResponse("No file uploaded", { status: 400 });
    }
    if (!docType || (docType !== "pan" && docType !== "aadhaar")) {
      return new NextResponse("Invalid document type. Must be 'pan' or 'aadhaar'", { status: 400 });
    }

    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    const mimeType = file.type;

    let result;
    if (docType === "pan") {
      result = await extractPanFromImage(buffer, mimeType);
    } else {
      result = await extractAadhaarFromImage(buffer, mimeType);
    }

    return NextResponse.json(result);
  } catch (error) {
    console.error("Error extracting document:", error);
    return new NextResponse(error.message || "Failed to process document", { status: 500 });
  }
}
