// Turns a PDF or image into positioned text items: { str, x, y, w, h, page, conf, ocr }.
// Digital PDFs (TRACES / payroll exports) are read from the text layer — exact, no OCR errors.
// Scanned PDFs and photos fall back to OCR (Tesseract), and every OCR value is marked for the user to confirm.

const vendor = () => new URL("./vendor/", document.baseURI).href;
let pdfjsPromise, ocrWorkerPromise;

function pdfjs() {
  if (!pdfjsPromise)
    pdfjsPromise = import("pdfjs-dist/build/pdf.min.mjs").then((m) => {
      m.GlobalWorkerOptions.workerSrc = vendor() + "pdf.worker.min.mjs";
      return m;
    });
  return pdfjsPromise;
}

async function ocrWorker(onProgress) {
  if (!ocrWorkerPromise)
    ocrWorkerPromise = import("tesseract.js").then(async (mod) => {
      const createWorker = mod.createWorker || mod.default?.createWorker;
      const w = await createWorker("eng", 1, {
        workerPath: vendor() + "tesseract/worker.min.js",
        corePath: vendor() + "tesseract/",
        langPath: vendor() + "tesseract/lang/",
        logger: (m) => onProgress && m.status === "recognizing text" && onProgress(m.progress),
      });
      await w.setParameters({ preserve_interword_spaces: "1" });
      return w;
    });
  return ocrWorkerPromise;
}

export async function openPdf(file, passwords = []) {
  const lib = await pdfjs();
  const data = new Uint8Array(await file.arrayBuffer());
  const tries = [undefined, ...passwords];
  let lastErr;
  for (const password of tries) {
    try {
      return await lib.getDocument({ data: data.slice(), password, isEvalSupported: false }).promise;
    } catch (e) {
      lastErr = e;
      if (e?.name !== "PasswordException") throw e;
    }
  }
  const err = new Error("This PDF is password-protected. Enter its password.");
  err.code = "PASSWORD";
  err.cause = lastErr;
  throw err;
}

async function pdfTextItems(doc) {
  const items = [];
  for (let p = 1; p <= doc.numPages; p++) {
    const page = await doc.getPage(p);
    const vp = page.getViewport({ scale: 1 });
    const tc = await page.getTextContent();
    for (const it of tc.items) {
      const str = (it.str || "").trim();
      if (!str) continue;
      const [a, b, c, d, e, f] = it.transform;
      const h = Math.hypot(c, d) || it.height || 8;
      items.push({ str, x: e, y: vp.height - f, w: it.width, h, page: p, pageW: vp.width, conf: 100, ocr: false });
    }
  }
  return items;
}

/** Prepares a scan for OCR: greyscale, Otsu threshold, and removal of table ruling lines (they break Tesseract on forms). */
export function cleanForOcr(canvas) {
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const { width: W, height: H } = canvas;
  const img = ctx.getImageData(0, 0, W, H), d = img.data;
  const g = new Uint8Array(W * H), hist = new Array(256).fill(0);
  for (let i = 0, j = 0; i < d.length; i += 4, j++) { const v = (d[i] * 299 + d[i + 1] * 587 + d[i + 2] * 114) / 1000 | 0; g[j] = v; hist[v]++; }
  // Otsu threshold
  let sum = 0; for (let t = 0; t < 256; t++) sum += t * hist[t];
  let sumB = 0, wB = 0, best = 0, thr = 160;
  for (let t = 0; t < 256; t++) { wB += hist[t]; if (!wB) continue; const wF = W * H - wB; if (!wF) break; sumB += t * hist[t];
    const mB = sumB / wB, mF = (sum - sumB) / wF, between = wB * wF * (mB - mF) ** 2; if (between > best) { best = between; thr = t; } }
  const dark = new Uint8Array(W * H); for (let j = 0; j < g.length; j++) dark[j] = g[j] < thr ? 1 : 0;
  const minRun = Math.round(Math.min(W, H) * 0.06);
  const erase = new Uint8Array(W * H);
  for (let y = 0; y < H; y++) { let x = 0; while (x < W) { if (!dark[y * W + x]) { x++; continue; } let e = x; while (e < W && dark[y * W + e]) e++; if (e - x >= minRun) for (let k = x; k < e; k++) erase[y * W + k] = 1; x = e; } }
  for (let x = 0; x < W; x++) { let y = 0; while (y < H) { if (!dark[y * W + x]) { y++; continue; } let e = y; while (e < H && dark[e * W + x]) e++; if (e - y >= minRun) for (let k = y; k < e; k++) erase[k * W + x] = 1; y = e; } }
  for (let j = 0, i = 0; j < g.length; j++, i += 4) { const v = dark[j] && !erase[j] ? 0 : 255; d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255; }
  ctx.putImageData(img, 0, 0);
  return canvas;
}

export const OCR_OPTS = { psm: "6" };
async function ocrCanvas(canvas, page, onProgress) {
  const w = await ocrWorker(onProgress);
  cleanForOcr(canvas);
  await w.setParameters({ tessedit_pageseg_mode: OCR_OPTS.psm, preserve_interword_spaces: "1" });
  const { data } = await w.recognize(canvas);
  const scale = canvas.__scale || 1;
  return (data.words || [])
    .filter((wd) => wd.text.trim())
    .map((wd) => ({
      str: wd.text.trim(),
      x: wd.bbox.x0 / scale,
      y: wd.bbox.y1 / scale,
      w: (wd.bbox.x1 - wd.bbox.x0) / scale,
      h: (wd.bbox.y1 - wd.bbox.y0) / scale,
      page,
      pageW: canvas.width / scale,
      conf: wd.confidence,
      ocr: true,
    }));
}

async function renderPage(doc, p, scale = 3.5) {
  const page = await doc.getPage(p);
  const vp = page.getViewport({ scale });
  const canvas = document.createElement("canvas");
  canvas.width = vp.width;
  canvas.height = vp.height;
  await page.render({ canvasContext: canvas.getContext("2d"), viewport: vp }).promise;
  canvas.__scale = scale;
  return canvas;
}

async function imageToCanvas(file) {
  const bmp = await createImageBitmap(file);
  const scale = Math.max(1, 2000 / Math.max(bmp.width, bmp.height));
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(bmp.width * scale);
  canvas.height = Math.round(bmp.height * scale);
  const ctx = canvas.getContext("2d");
  ctx.drawImage(bmp, 0, 0, canvas.width, canvas.height);
  canvas.__scale = scale;
  return canvas;
}

/** Returns { items, source: "text" | "ocr", pages } */
export async function extractItems(file, { passwords = [], onStatus } = {}) {
  const isPdf = file.type === "application/pdf" || /\.pdf$/i.test(file.name);
  if (!isPdf) {
    onStatus && onStatus("Reading the image (OCR)…");
    const canvas = await imageToCanvas(file);
    const items = await ocrCanvas(canvas, 1, (p) => onStatus && onStatus(`Reading the image (OCR) ${Math.round(p * 100)}%`));
    return { items, source: "ocr", pages: 1 };
  }
  onStatus && onStatus("Opening the PDF…");
  const doc = await openPdf(file, passwords);
  const items = await pdfTextItems(doc);
  const digits = items.filter((i) => /\d/.test(i.str)).length;
  if (digits >= 15) return { items, source: "text", pages: doc.numPages };
  // scanned PDF → OCR every page
  const out = [];
  for (let p = 1; p <= doc.numPages; p++) {
    onStatus && onStatus(`Scanned PDF: reading page ${p} of ${doc.numPages} (OCR)…`);
    const canvas = await renderPage(doc, p);
    out.push(...(await ocrCanvas(canvas, p, (pr) => onStatus && onStatus(`Scanned PDF: page ${p}/${doc.numPages} ${Math.round(pr * 100)}%`))));
  }
  return { items: out, source: "ocr", pages: doc.numPages };
}

// ---------------------------------------------------------------- layout helpers shared by all parsers
export function toLines(items) {
  const sorted = [...items].sort((a, b) => a.page - b.page || a.y - b.y || a.x - b.x);
  const lines = [];
  for (const it of sorted) {
    const last = lines[lines.length - 1];
    const tol = Math.max(2.5, Math.min(it.h, last?.h || it.h) * 0.45);
    if (last && last.page === it.page && Math.abs(last.y - it.y) <= tol) {
      last.items.push(it);
      last.h = Math.max(last.h, it.h);
    } else lines.push({ page: it.page, y: it.y, h: it.h, pageW: it.pageW, items: [it] });
  }
  for (const l of lines) {
    l.items.sort((a, b) => a.x - b.x);
    l.text = l.items.map((i) => i.str).join(" ");
    l.norm = normalize(l.text);
    l.labelNorm = normalize(l.items.filter((i) => parseAmount(i.str) === null).map((i) => i.str).join(" "));
  }
  return lines;
}

export function normalize(s) {
  return s
    .toLowerCase()
    .replace(/[“”"]/g, "")
    .replace(/[‐-―]/g, "-")
    .replace(/\s+/g, " ")
    .replace(/\s*([()])\s*/g, "$1")
    .trim();
}

const AMOUNT_RE = /^\(?-?(?:rs\.?|₹)?\s*(\d{1,3}(?:,\d{2,3})+|\d+)(\.\d{1,2})?\)?$/i;
/** Parses an amount token, returns null when the token is not an amount. */
export function parseAmount(str) {
  const s = str.replace(/\s/g, "");
  const m = s.match(AMOUNT_RE);
  if (!m) return null;
  // "(2)", "(1B)" etc. are section references, not negative amounts: brackets need a comma or decimals
  if (/^\(.*\)$/.test(s) && !/[,.]/.test(s)) return null;
  let v = Number((m[1] + (m[2] || "")).replace(/,/g, ""));
  if (/^\(.*\)$/.test(s) || s.startsWith("-")) v = -v;
  return v;
}

/** Amount items in a line that sit to the right of x (labels are on the left, amounts on the right). */
export function amountsRightOf(line, x, { minFrac = 0.4 } = {}) {
  return line.items
    .filter((i) => i.x >= x - 1)
    .map((i) => ({ item: i, v: parseAmount(i.str) }))
    .filter(({ item, v }) => v !== null && (item.str.includes(",") || item.str.includes(".") || item.x > (item.pageW || 600) * minFrac));
}
