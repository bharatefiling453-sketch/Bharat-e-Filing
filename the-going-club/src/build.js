// Inlines GSAP, ScrollTrigger, SplitText and Lenis into one self-contained index.html.
// Usage: npm i gsap@3 lenis@1 && node build.js
const fs = require("fs");
const path = require("path");

const nm = path.join(process.argv[2] || __dirname, "node_modules");
const read = p => fs.readFileSync(path.join(nm, p), "utf8").replace(/\/\/# sourceMappingURL=.*$/m, "");

let html = fs.readFileSync(path.join(__dirname, "index.src.html"), "utf8");
const parts = {
  "/* @@LENIS_CSS@@ */": read("lenis/dist/lenis.css"),
  "/* @@GSAP@@ */": read("gsap/dist/gsap.min.js"),
  "/* @@SCROLLTRIGGER@@ */": read("gsap/dist/ScrollTrigger.min.js"),
  "/* @@SPLITTEXT@@ */": read("gsap/dist/SplitText.min.js"),
  "/* @@LENIS@@ */": read("lenis/dist/lenis.min.js"),
};
for (const [k, v] of Object.entries(parts)) html = html.split(k).join(v.replace(/<\/script/gi, "<\\/script"));

fs.writeFileSync(path.join(__dirname, "..", "index.html"), html);
console.log("wrote index.html", (html.length / 1024).toFixed(0) + " KB");
