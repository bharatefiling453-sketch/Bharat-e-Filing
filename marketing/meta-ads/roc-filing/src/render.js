// Renders each ad-XX.html to ../final/*.png at 1080x1350
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const only = process.argv[2];
  const files = fs.readdirSync(__dirname).filter(f => /^ad-\d+.*\.html$/.test(f) && (!only || f.includes(only)));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const f of files) {
    await page.goto('file://' + path.join(__dirname, f));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const out = path.join(__dirname, '..', 'final', f.replace('.html', '.png'));
    await page.screenshot({ path: out });
    console.log('rendered', out);
  }
  await browser.close();
})();
