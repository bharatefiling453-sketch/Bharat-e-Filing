// Builds the ITR-1 self-filing app: bundles src/ with esbuild (code-split so PDF/OCR/Excel/PDF-export libraries
// load only when used) and copies the pdf.js worker, Tesseract worker/core and English OCR model into vendor/.
// Usage: node scripts/build-itr-app.mjs
import { build } from "esbuild";
import { cpSync, mkdirSync, rmSync, readdirSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const app = resolve(root, "itr-self-filing");
const nm = (p) => resolve(root, "node_modules", p);

rmSync(resolve(app, "chunks"), { recursive: true, force: true });
await build({
  entryPoints: { app: resolve(app, "src/main.js") },
  bundle: true, splitting: true, format: "esm", outdir: app, chunkNames: "chunks/[name]-[hash]",
  minify: true, sourcemap: false, target: ["es2020"], legalComments: "none",
  define: { "process.env.NODE_ENV": '"production"' },
});

const vendor = resolve(app, "vendor");
rmSync(vendor, { recursive: true, force: true });
mkdirSync(resolve(vendor, "tesseract/lang"), { recursive: true });
cpSync(nm("pdfjs-dist/build/pdf.worker.min.mjs"), resolve(vendor, "pdf.worker.min.mjs"));
cpSync(nm("tesseract.js/dist/worker.min.js"), resolve(vendor, "tesseract/worker.min.js"));
for (const f of readdirSync(nm("tesseract.js-core"))) if (/^tesseract-core(-simd)?-lstm\.wasm\.js$/.test(f)) cpSync(nm("tesseract.js-core/" + f), resolve(vendor, "tesseract/" + f));
cpSync(nm("@tesseract.js-data/eng/4.0.0_best_int/eng.traineddata.gz"), resolve(vendor, "tesseract/lang/eng.traineddata.gz"));
console.log("built itr-self-filing/app.js + chunks/ + vendor/");
