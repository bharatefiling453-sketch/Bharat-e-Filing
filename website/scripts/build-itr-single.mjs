// Builds the ITR-1 self-filing app as ONE self-contained HTML file: dist/bef-itr1-self-filing.html
// Everything is embedded (app code, CSS, logo, pdf.js worker, Tesseract OCR engine + English model, demo samples),
// so the file works offline, from a double-click, or uploaded anywhere as a single page.
// Embedded files are gzip+base64 and turned into blob URLs on demand by window.__befAsset(name).
// Run `npm run build:itr` first (it fills itr-self-filing/vendor/). Usage: node scripts/build-itr-single.mjs
import { build } from "esbuild";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { gzipSync } from "node:zlib";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const app = resolve(root, "itr-self-filing");
const read = (p) => readFileSync(resolve(root, p));

const js = await build({
  entryPoints: [resolve(app, "src/main.js")],
  bundle: true, format: "esm", write: false, minify: true, target: ["es2020"], legalComments: "none",
  define: { "process.env.NODE_ENV": '"production"' },
});

// name → [bytes, mime, alreadyCompressed]
const assets = {
  "app.js": [Buffer.from(js.outputFiles[0].contents), "text/javascript"],
  "pdf.worker.min.mjs": [read("itr-self-filing/vendor/pdf.worker.min.mjs"), "text/javascript"],
  "tesseract-worker.src.js": [read("itr-self-filing/vendor/tesseract/worker.min.js"), "text/javascript"],
  "tesseract-core.js": [read("itr-self-filing/vendor/tesseract/tesseract-core-simd-lstm.wasm.js"), "text/javascript"],
  "eng.traineddata.gz": [read("itr-self-filing/vendor/tesseract/lang/eng.traineddata.gz"), "application/gzip", true],
  "sample-form16.pdf": [read("itr-self-filing/samples/sample-form16.pdf"), "application/pdf"],
  "sample-form16-scanned.pdf": [read("itr-self-filing/samples/sample-form16-scanned.pdf"), "application/pdf"],
  "sample-salary-slip.png": [read("itr-self-filing/samples/sample-salary-slip.png"), "image/png", true],
  "sample-broker-tax-pnl.csv": [read("itr-self-filing/samples/sample-broker-tax-pnl.csv"), "text/csv"],
};

const blocks = Object.entries(assets).map(([name, [buf, mime, raw]]) => {
  const data = raw ? buf : gzipSync(buf, { level: 9 });
  return `<script type="application/octet-stream" data-bef-asset="${name}" data-mime="${mime}"${raw ? "" : ' data-gz="1"'}>${data.toString("base64")}</script>`;
});

// Runtime loader. The Tesseract worker gets a small prefix that redirects its core and language downloads to the embedded copies.
const loader = `<script>
(function () {
  var cache = {};
  function bytes(el) {
    var bin = atob(el.textContent.trim()), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  function blobOf(name) {
    var el = document.querySelector('script[data-bef-asset="' + name + '"]');
    if (!el) return Promise.reject(new Error("Missing embedded file: " + name));
    var b = new Blob([bytes(el)]);
    if (el.dataset.gz) b = new Response(b.stream().pipeThrough(new DecompressionStream("gzip"))).blob();
    return Promise.resolve(b).then(function (x) { return new Blob([x], { type: el.dataset.mime }); });
  }
  function url(name) { return blobOf(name).then(function (b) { return URL.createObjectURL(b); }); }
  window.__befAsset = function (name) {
    if (cache[name]) return cache[name];
    if (name === "tesseract-worker.js") {
      // One self-contained worker (prefix + OCR core + Tesseract worker): nested blob URLs are refused on file:// pages.
      var lang = document.querySelector('script[data-bef-asset="eng.traineddata.gz"]').textContent.trim();
      cache[name] = Promise.all([blobOf("tesseract-core.js"), blobOf("tesseract-worker.src.js")]).then(function (r) {
        var prefix = "(function(){var B=" + JSON.stringify(lang) + ";" +
          "var i=self.importScripts;self.importScripts=function(){var a=[].slice.call(arguments).filter(function(u){return !/tesseract-core/.test(String(u))});return a.length?i.apply(self,a):undefined};" +
          "var f=self.fetch;self.fetch=function(u,o){if(!/bef\\\\.embedded\\\\/lang\\\\//.test(String(u)))return f(u,o);var s=atob(B),b=new Uint8Array(s.length);for(var k=0;k<s.length;k++)b[k]=s.charCodeAt(k);return Promise.resolve(new Response(b))};})();\\n";
        return URL.createObjectURL(new Blob([prefix, r[0], "\\n", r[1]], { type: "text/javascript" }));
      });
    } else cache[name] = url(name);
    return cache[name];
  };
  window.__befAsset("app.js").then(function (u) { return import(u); }).catch(function (e) {
    document.getElementById("app").innerHTML = '<p style="padding:24px">Could not start the app: ' + String(e && e.message || e) + '. Please use a recent Chrome, Edge, Firefox or Safari.</p>';
  });
})();
</script>`;

const css = read("assets/css/bef-design-system.css").toString() + "\n" + read("itr-self-filing/app.css").toString();
if (/<\/style/i.test(css)) throw new Error("CSS contains </style");
const dataUri = (p, mime) => `data:${mime};base64,${read(p).toString("base64")}`;
const logo1 = dataUri("assets/img/bef-logo.webp", "image/webp"), logo2 = dataUri("assets/img/bef-logo@2x.webp", "image/webp");

let html = read("itr-self-filing/index.html").toString();
const swap = (from, to) => { if (!html.includes(from)) throw new Error("index.html changed, not found: " + from); html = html.replace(from, to); };
swap(`<link rel="stylesheet" href="../assets/css/bef-design-system.css" />\n    <link rel="stylesheet" href="app.css" />`, `<style>\n${css}\n</style>`);
swap(`href="../assets/img/bef-mark.svg"`, `href="${dataUri("assets/img/bef-mark.svg", "image/svg+xml")}"`);
swap(`src="../assets/img/bef-logo.webp" srcset="../assets/img/bef-logo.webp 1x, ../assets/img/bef-logo@2x.webp 2x"`, `src="${logo1}" srcset="${logo1} 1x, ${logo2} 2x"`);
swap(`<script type="module" src="app.js"></script>`, blocks.join("\n") + "\n" + loader);

mkdirSync(resolve(root, "dist"), { recursive: true });
const out = resolve(root, "dist/bef-itr1-self-filing.html");
writeFileSync(out, html);
console.log(`built dist/bef-itr1-self-filing.html (${(html.length / 1048576).toFixed(1)} MB)`);
