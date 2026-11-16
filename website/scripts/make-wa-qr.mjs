// Generates assets/img/wa-qr.svg — the WhatsApp QR code used by the floating chat card on v3 pages.
// Re-run after changing the number: node scripts/make-wa-qr.mjs
import { writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import QRCode from "qrcode";

const WHATSAPP_NUMBER = "910000000000"; // REPLACE with the real WhatsApp Business number (country code, no +)
const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent("Hi, I need help from a Bharat e-Filing expert")}`;

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
// High error correction so the WhatsApp logo can sit in the centre without breaking the scan
const svg = await QRCode.toString(url, { type: "svg", margin: 0, errorCorrectionLevel: "H", color: { dark: "#1d1d1f", light: "#ffffff" } });
writeFileSync(resolve(root, "assets/img/wa-qr.svg"), svg);
console.log("Wrote assets/img/wa-qr.svg for " + url);
