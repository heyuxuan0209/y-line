const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const ctx = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    recordVideo: { dir: '/tmp/ylrec', size: { width: 1280, height: 800 } },
  });
  const page = await ctx.newPage();
  await page.goto('file:///Users/heyuxuan/opencity-haidian/prototypes/yline-walkthrough.html');
  await page.waitForTimeout(4500); // hero: logo draw + year counter

  const n = await page.evaluate(() => document.querySelectorAll('section').length);
  for (let i = 1; i < n; i++) {
    await page.evaluate((idx) => {
      document.querySelectorAll('section')[idx].scrollIntoView({ behavior: 'smooth' });
    }, i);
    await page.waitForTimeout(i === n - 1 ? 4200 : 3400);
  }
  await ctx.close();
  await browser.close();
  console.log('recorded');
})();
