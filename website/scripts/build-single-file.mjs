// Builds ONE self-contained HTML file of a service page — CSS, JS, logo, favicon and fonts all embedded —
// so it looks identical anywhere (Discord attachment, email, offline), with no other files needed.
// Usage: node scripts/build-single-file.mjs [page-folder]   (default: gst-registration)
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const page = process.argv[2] || "gst-registration";
const read = (p) => readFileSync(resolve(root, p));
const dataUri = (p, mime) =>
  `data:${mime};base64,${read(p).toString("base64")}`;

const fonts = [
  // Inter (variable: weight + optical size). latin-ext carries the ₹ sign.
  [
    "Inter",
    "100 900",
    "@fontsource-variable/inter/files/inter-latin-opsz-normal.woff2",
    "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
  ],
  [
    "Inter",
    "100 900",
    "@fontsource-variable/inter/files/inter-latin-ext-opsz-normal.woff2",
    "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
  ],
  [
    "Noto Sans Devanagari",
    "400",
    "@fontsource/noto-sans-devanagari/files/noto-sans-devanagari-devanagari-400-normal.woff2",
    "U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20F0,U+25CC,U+A830-A839,U+A8E0-A8FF",
  ],
  [
    "Noto Sans Devanagari",
    "600",
    "@fontsource/noto-sans-devanagari/files/noto-sans-devanagari-devanagari-600-normal.woff2",
    "U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20F0,U+25CC,U+A830-A839,U+A8E0-A8FF",
  ],
];
const fontCss = fonts
  .map(
    ([family, weight, file, range]) =>
      `@font-face{font-family:"${family}";font-style:normal;font-weight:${weight};font-display:swap;` +
      `src:url(${dataUri("node_modules/" + file, "font/woff2")}) format("woff2");unicode-range:${range}}`,
  )
  .join("\n");

let html = read(`${page}/index.html`).toString();
const css = read("assets/css/bef-design-system.css").toString();
const js = read("assets/js/bef-page.js").toString();

const replaceOnce = (needle, value) => {
  if (!html.includes(needle))
    throw new Error("Not found in page: " + needle.slice(0, 80));
  html = html.split(needle).join(value);
};

// Google Fonts → embedded fonts (identical rendering offline)
html = html.replace(
  /\s*<link rel="preconnect" href="https:\/\/fonts\.(googleapis|gstatic)\.com"[^>]*\/>/g,
  "",
);
html = html.replace(
  /\s*<link\s+rel="stylesheet"\s+href="https:\/\/fonts\.googleapis\.com[^"]*"\s*\/>/,
  "",
);
replaceOnce(
  '<link rel="stylesheet" href="../assets/css/bef-design-system.css" />',
  `<style>\n${fontCss}\n${css}\n</style>`,
);
replaceOnce(
  '<script src="../assets/js/bef-page.js" defer></script>',
  `<script>\n${js}\n</script>`,
);
html = html.replace(/\s*<link rel="preload" as="image"[^>]*\/>/, "");
replaceOnce(
  "../assets/img/bef-logo@2x.webp",
  dataUri("assets/img/bef-logo@2x.webp", "image/webp"),
);
replaceOnce(
  "../assets/img/bef-logo.webp",
  dataUri("assets/img/bef-logo.webp", "image/webp"),
);
replaceOnce(
  "../assets/img/bef-mark.svg",
  dataUri("assets/img/bef-mark.svg", "image/svg+xml"),
);
if (/\.\.\/assets\//.test(html))
  throw new Error("A ../assets reference was left un-embedded");

mkdirSync(resolve(root, "dist"), { recursive: true });
const out = resolve(root, "dist", `bharat-efiling-${page}.html`);
writeFileSync(out, html);
console.log(`Built ${out} (${(Buffer.byteLength(html) / 1024).toFixed(0)} KB)`);
