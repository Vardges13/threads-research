#!/usr/bin/env node
/**
 * TourVisor Pro Scraper
 * Автоматический сбор горящих туров
 */

const { chromium } = require('playwright');

const LOGIN_URL = 'https://pro.tourvisor.ru/search';
const EMAIL = 'vardges13@mail.ru';
const PASSWORD = 'c424bd6o3v12';

async function scrapeTours() {
  console.log('🚀 Запуск браузера...');
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });
  
  const page = await context.newPage();
  
  try {
    console.log('📄 Открываю TourVisor Pro...');
    await page.goto(LOGIN_URL, { waitUntil: 'networkidle', timeout: 30000 });
    
    // Ждём форму логина
    await page.waitForTimeout(2000);
    
    // Проверяем есть ли форма логина
    const loginForm = await page.$('input[type="email"], input[name="email"], input[type="text"]');
    
    if (loginForm) {
      console.log('🔐 Выполняю вход...');
      
      // Ищем поля email и password
      const emailInput = await page.$('input[type="email"]') || await page.$('input[name="email"]') || await page.$('input[placeholder*="mail"]');
      const passwordInput = await page.$('input[type="password"]');
      
      if (emailInput && passwordInput) {
        await emailInput.fill(EMAIL);
        await passwordInput.fill(PASSWORD);
        
        // Ищем кнопку входа
        const submitBtn = await page.$('button[type="submit"]') || await page.$('input[type="submit"]') || await page.$('button:has-text("Вход")');
        if (submitBtn) {
          await submitBtn.click();
          await page.waitForTimeout(3000);
        }
      }
    }
    
    console.log('🔍 Ищу горящие туры...');
    
    // Делаем скриншот для отладки
    await page.screenshot({ path: '/Users/bond/.openclaw/workspace/tools/tourvisor-screenshot.png', fullPage: true });
    
    // Получаем HTML страницы
    const content = await page.content();
    
    // Пробуем найти блоки с турами
    const tours = await page.$$eval('.tour-item, .search-result, .offer, [class*="tour"], [class*="result"]', elements => {
      return elements.slice(0, 10).map(el => ({
        text: el.innerText.substring(0, 500),
        html: el.innerHTML.substring(0, 1000)
      }));
    }).catch(() => []);
    
    console.log(`✅ Найдено элементов: ${tours.length}`);
    
    // Выводим текст страницы
    const pageText = await page.evaluate(() => document.body.innerText);
    console.log('\n📋 Содержимое страницы:\n');
    console.log(pageText.substring(0, 5000));
    
    return { success: true, tours, pageText };
    
  } catch (error) {
    console.error('❌ Ошибка:', error.message);
    await page.screenshot({ path: '/Users/bond/.openclaw/workspace/tools/tourvisor-error.png' });
    return { success: false, error: error.message };
  } finally {
    await browser.close();
    console.log('\n🏁 Браузер закрыт');
  }
}

scrapeTours();
