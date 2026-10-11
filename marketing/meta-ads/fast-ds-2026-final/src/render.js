// Renders each ad-*.html as 4:5 feed (1080x1350) and 9:16 story (1080x1920) at 2x
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const only = process.argv[2];
  const files = fs.readdirSync(__dirname).filter(f => /^ad-.*\.html$/.test(f) && (!only || f.includes(only)));
  const browser = await chromium.launch();
  for (const [fmt, h] of [['feed-4x5', 1350], ['story-9x16', 1920]]) {
    const page = await browser.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 2 });
    for (const f of files) {
      await page.goto('file://' + path.join(__dirname, f) + '?fmt=' + fmt);
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(300);
      const out = path.join(__dirname, '..', 'final', f.replace('.html', `-${fmt}.png`));
      await page.screenshot({ path: out });
      console.log('rendered', path.basename(out));
    }
    await page.close();
  }
  await browser.close();
})();
