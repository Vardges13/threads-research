#!/usr/bin/env node
/**
 * Горящие туры с onlineturplus.ru
 */

const { chromium } = require('playwright');

async function getHotTours() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  try {
    console.log('📄 Открываю onlineturplus.ru/goryashchie-tury...');
    await page.goto('https://onlineturplus.ru/goryashchie-tury', { 
      waitUntil: 'networkidle', 
      timeout: 30000 
    });
    
    // Ждём загрузки виджета
    console.log('⏳ Жду загрузки туров...');
    await page.waitForTimeout(8000);
    
    // Скриншот
    await page.screenshot({ 
      path: '/Users/bond/.openclaw/workspace/tools/hot-tours-screenshot.png', 
      fullPage: true 
    });
    console.log('📸 Скриншот сохранён');
    
    // Получаем весь текст
    const pageText = await page.evaluate(() => document.body.innerText);
    console.log('\n🔥 ГОРЯЩИЕ ТУРЫ:\n');
    console.log(pageText);
    
  } catch (error) {
    console.error('❌ Ошибка:', error.message);
  } finally {
    await browser.close();
  }
}

getHotTours();
