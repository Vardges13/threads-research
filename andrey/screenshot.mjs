import { chromium } from 'playwright';

const args = process.argv.slice(2);
const htmlFile = args[0];
const outputFile = args[1];

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setViewportSize({ width: 900, height: 1200 });
await page.goto(`file://${htmlFile}`, { waitUntil: 'load', timeout: 30000 });
await page.waitForTimeout(1000);
await page.screenshot({ path: outputFile, fullPage: false });
await browser.close();
console.log(`Screenshot saved: ${outputFile}`);
