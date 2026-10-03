// Runs axe-core (WCAG 2.2 AA) in Chromium and saves desktop + mobile screenshots.
// Usage: node scripts/a11y-check.mjs path/to/page.html
import { chromium } from "playwright";
import { AxeBuilder } from "@axe-core/playwright";
import { mkdirSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const file = resolve(process.argv[2]);
// Use a pre-installed Chromium when present (CI containers); otherwise Playwright's own download.
const exe =
  process.env.CHROME_PATH ||
  (existsSync("/opt/pw-browsers/chromium")
    ? "/opt/pw-browsers/chromium"
    : undefined);
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
mkdirSync("reports", { recursive: true });
let failed = 0;

for (const [name, viewport] of [
  ["desktop", { width: 1366, height: 900 }],
  ["mobile", { width: 390, height: 844 }],
]) {
  const context = await browser.newContext({ viewport, reducedMotion: "reduce" });
  const page = await context.newPage();
  await page.route(/googletagmanager|fonts\.g/, (r) => r.abort());
  await page.goto("file://" + file);
  await page.screenshot({ path: `reports/${name}.png`, fullPage: true });
  const res = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
    .analyze();
  console.log(`\n[${name}] axe violations: ${res.violations.length}`);
  for (const v of res.violations) {
    failed++;
    console.log(`✖ ${v.id} (${v.impact}) – ${v.help}`);
    v.nodes.slice(0, 3).forEach((n) => console.log("   " + n.target.join(" ")));
  }
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > window.innerWidth,
  );
  if (overflow) {
    failed++;
    console.log("✖ horizontal scroll at " + viewport.width + "px");
  }
}
await browser.close();
process.exit(failed ? 1 : 0);
