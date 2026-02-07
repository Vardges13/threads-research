const { chromium } = require('playwright');

const queries = [
  'бесит эксперт предприниматель',
  'раздражает инфобизнес',
  'заебало продвижение эксперт',
  'почему так сложно предприниматель',
  'вдохновляет бизнес эксперт'
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    locale: 'ru-RU',
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
  });
  
  const allResults = [];
  
  for (const query of queries) {
    console.error(`\n--- Searching: "${query}" ---`);
    const page = await context.newPage();
    try {
      const url = `https://www.threads.net/search?q=${encodeURIComponent(query)}&serp_type=default`;
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      
      // Wait for content to load
      await page.waitForTimeout(5000);
      
      // Try to get post content
      const posts = await page.evaluate(() => {
        const results = [];
        // Threads uses various selectors - try multiple
        const textElements = document.querySelectorAll('[data-pressable-container] span, [class*="BodyTextContainer"] span, div[dir="auto"] span');
        const seen = new Set();
        
        textElements.forEach(el => {
          const text = el.textContent?.trim();
          if (text && text.length > 30 && text.length < 1000 && !seen.has(text)) {
            seen.add(text);
            results.push(text);
          }
        });
        
        return results.slice(0, 10);
      });
      
      if (posts.length > 0) {
        console.error(`Found ${posts.length} posts`);
        allResults.push({ query, posts });
      } else {
        // Try alternative: grab all visible text
        const bodyText = await page.evaluate(() => {
          return document.body.innerText;
        });
        console.error(`No structured posts found. Page text length: ${bodyText.length}`);
        if (bodyText.length > 100) {
          allResults.push({ query, rawText: bodyText.substring(0, 3000) });
        }
      }
    } catch (e) {
      console.error(`Error for "${query}": ${e.message}`);
    }
    await page.close();
  }
  
  console.log(JSON.stringify(allResults, null, 2));
  await browser.close();
})();
