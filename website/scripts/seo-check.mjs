// Bharat eFiling product-page SEO / AEO gate.
// Usage: node scripts/seo-check.mjs path/to/page.html
// Fails (exit 1) on any rule in the Product Page Standard that a machine can check.
import { readFileSync } from "node:fs";
import * as cheerio from "cheerio";

const file = process.argv[2];
const $ = cheerio.load(readFileSync(file, "utf8"));
const errors = [];
const warns = [];
const ok = [];
const check = (cond, msg, level = "error") =>
  cond ? ok.push(msg) : (level === "error" ? errors : warns).push(msg);

const title = $("head > title").text().trim();
check(
  title.length >= 30 && title.length <= 60,
  `title 30–60 chars (got ${title.length})`,
);
check(/bharat efiling/i.test(title), "title ends with brand");

const desc = $('meta[name="description"]').attr("content") || "";
check(
  desc.length >= 120 && desc.length <= 160,
  `meta description 120–160 chars (got ${desc.length})`,
);

const canonical = $('link[rel="canonical"]').attr("href") || "";
check(
  /^https:\/\/bharatefiling\.com\/[a-z0-9-]+\/$/.test(canonical),
  "canonical is absolute, lowercase, hyphenated, trailing slash",
);
check($('meta[property="og:image"]').length === 1, "og:image present");
check($("html").attr("lang"), "html lang set");

check($("h1").length === 1, `exactly one <h1> (got ${$("h1").length})`);
let prev = 1;
let skip = false;
$("main h2, main h3, main h4").each((_, el) => {
  const lvl = Number(el.tagName[1]);
  if (lvl > prev + 1) skip = true;
  prev = lvl;
});
check(!skip, "no skipped heading levels inside <main>");

const answer = $(".answer").text().trim().split(/\s+/).length;
check(
  answer >= 35 && answer <= 70,
  `AEO answer box 35–70 words (got ${answer})`,
);

$("img").each((_, el) =>
  check($(el).attr("alt") !== undefined, `img alt: ${$(el).attr("src")}`),
);
$('a[target="_blank"]').each((_, el) =>
  check(
    /noopener/.test($(el).attr("rel") || ""),
    `noopener on ${$(el).attr("href")}`,
  ),
);

// JSON-LD
let graph = [];
$('script[type="application/ld+json"]').each((_, el) => {
  try {
    const data = JSON.parse($(el).text());
    graph = graph.concat(data["@graph"] || [data]);
  } catch (e) {
    errors.push("JSON-LD does not parse: " + e.message);
  }
});
const types = graph.flatMap((n) => [].concat(n["@type"]));
for (const t of [
  "Organization",
  "WebPage",
  "BreadcrumbList",
  "Service",
  "FAQPage",
])
  check(types.includes(t), `schema ${t}`);

const faq = graph.find((n) => n["@type"] === "FAQPage");
if (faq) {
  const visible = $(".faq details")
    .map((_, d) => ({
      q: $(d).find("summary").text().trim(),
      a: $(d).find(".faq__a").text().trim(),
    }))
    .get();
  check(
    visible.length === faq.mainEntity.length,
    `FAQ count visible (${visible.length}) = schema (${faq.mainEntity.length})`,
  );
  faq.mainEntity.forEach((q, i) => {
    check(
      visible[i] && visible[i].q === q.name,
      `FAQ ${i + 1} question matches schema`,
    );
    check(
      visible[i] && visible[i].a === q.acceptedAnswer.text,
      `FAQ ${i + 1} answer matches schema`,
    );
  });
  check(faq.mainEntity.length >= 8, "at least 8 FAQs", "warn");
}

const internal = $('main a[href^="https://bharatefiling.com/"]').length;
const external = $(
  'main a[href^="http"]:not([href^="https://bharatefiling.com/"])',
).length;
check(internal >= 8, `≥ 8 internal links in main (got ${internal})`);
check(external >= 3, `≥ 3 authoritative external links (got ${external})`);
check($("time[datetime]").length >= 1, "visible last-updated date");

const placeholders = (
  $.html().match(/REPLACE[_A-Z]*|GTM-XXXXXXX|00000 00000/g) || []
).length;
check(
  placeholders === 0,
  `no launch placeholders left (found ${placeholders})`,
  "warn",
);

const words = $("main").text().trim().split(/\s+/).length;
check(words >= 1500, `main content ≥ 1500 words (got ${words})`, "warn");

console.log(`\n✔ ${ok.length} passed`);
warns.forEach((w) => console.log("⚠ " + w));
errors.forEach((e) => console.log("✖ " + e));
process.exit(errors.length ? 1 : 0);
