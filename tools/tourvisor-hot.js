#!/usr/bin/env node
/**
 * TourVisor Pro - Горящие туры
 */

const { chromium } = require('playwright');

const LOGIN_URL = 'https://pro.tourvisor.ru/search';
const EMAIL = 'vardges13@mail.ru';
const PASSWORD = 'c424bd6o3v12';

async function getHotTours() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log('📄 Открываю TourVisor Pro...');
    await page.goto(LOGIN_URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    // Логин
    const emailInput = await page.$('input[type="email"]') || await page.$('input[name="email"]');
    const passwordInput = await page.$('input[type="password"]');
    
    if (emailInput && passwordInput) {
      console.log('🔐 Вход...');
      await emailInput.fill(EMAIL);
      await passwordInput.fill(PASSWORD);
      const submitBtn = await page.$('button[type="submit"]');
      if (submitBtn) {
        await submitBtn.click();
        await page.waitForTimeout(3000);
      }
    }
    
    // Переходим на горящие туры
    console.log('🔥 Открываю горящие туры...');
    
    // Кликаем на "Лента горящих туров" или "Горящие"
    const hotLink = await page.$('a:has-text("Горящие")') || await page.$('text=Лента горящих туров');
    if (hotLink) {
      await hotLink.click();
      await page.waitForTimeout(3000);
    } else {
      // Пробуем прямой URL
      await page.goto('https://pro.tourvisor.ru/hot', { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000);
    }
    
    // Скриншот горящих туров
    await page.screenshot({ path: '/Users/bond/.openclaw/workspace/tools/tourvisor-hot.png', fullPage: true });
    
    // Получаем текст страницы
    const pageText = await page.evaluate(() => document.body.innerText);
    console.log('\n🔥 ГОРЯЩИЕ ТУРЫ:\n');
    console.log(pageText.substring(0, 8000));
    
  } catch (error) {
    console.error('❌ Ошибка:', error.message);
  } finally {
    await browser.close();
  }
}

getHotTours();
