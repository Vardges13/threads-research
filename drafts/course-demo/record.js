const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, 'frames');
const HTML_FILE = path.join(__dirname, 'index.html');
const WIDTH = 1280;
const HEIGHT = 720;
const FPS = 30;

async function main() {
  // Clean output
  if (fs.existsSync(OUTPUT_DIR)) {
    fs.rmSync(OUTPUT_DIR, { recursive: true });
  }
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  console.log('Launching browser...');
  const browser = await chromium.launch({
    headless: true,
  });

  const context = await browser.newContext({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 2,
  });

  const page = await context.newPage();

  // Navigate to the HTML file
  console.log('Loading page...');
  await page.goto(`file://${HTML_FILE}`, { waitUntil: 'networkidle' });

  // Wait for fonts to load
  await page.waitForTimeout(2000);

  let frameCount = 0;

  async function captureFrame() {
    const framePath = path.join(OUTPUT_DIR, `frame_${String(frameCount).padStart(5, '0')}.jpg`);
    await page.screenshot({ path: framePath, type: 'jpeg', quality: 92 });
    frameCount++;
  }

  // Helper: capture N frames at current position (hold)
  async function hold(seconds) {
    const frames = Math.round(seconds * FPS);
    for (let i = 0; i < frames; i++) {
      await captureFrame();
    }
  }

  // Helper: smooth scroll
  async function smoothScroll(pixels, durationSec) {
    const totalFrames = Math.round(durationSec * FPS);
    const pixelsPerFrame = pixels / totalFrames;
    for (let i = 0; i < totalFrames; i++) {
      await page.evaluate((px) => window.scrollBy(0, px), pixelsPerFrame);
      await page.waitForTimeout(10);
      await captureFrame();
    }
  }

  console.log('Recording hero section...');
  // Scene 1: Hero section - hold
  await hold(3);

  console.log('Scrolling to UTP...');
  // Scene 2: Scroll to UTP section
  await smoothScroll(900, 2.5);
  await hold(2.5);

  console.log('Scrolling to modules...');
  // Scene 3: Scroll to modules
  await smoothScroll(800, 2);
  await hold(2);

  // Scene 4: Scroll through module cards
  await smoothScroll(600, 2);
  await hold(1.5);

  // Scene 5: Continue to module 7
  await smoothScroll(400, 1.5);
  await hold(1.5);

  console.log('Scrolling to agents grid...');
  // Scene 6: Scroll to agents section
  await smoothScroll(600, 2);
  await hold(2);

  // Scene 7: Scroll through agents grid
  await smoothScroll(700, 3);
  await hold(2);

  console.log('Scrolling to results...');
  // Scene 8: Results section
  await smoothScroll(500, 1.5);
  await hold(2);

  console.log('Scrolling to audience...');
  // Scene 9: Who is this for
  await smoothScroll(600, 2);
  await hold(2);

  console.log('Scrolling to quote and CTA...');
  // Scene 10: Quote
  await smoothScroll(500, 1.5);
  await hold(2);

  // Scene 11: CTA
  await smoothScroll(400, 1.5);
  await hold(3);

  console.log(`Done! Captured ${frameCount} frames.`);
  await browser.close();
}

main().catch(console.error);
