#!/usr/bin/env node
/**
 * TourVisor Pro - Поиск туров с результатами
 */

const { chromium } = require('playwright');

const EMAIL = 'vardges13@mail.ru';
const PASSWORD = 'c424bd6o3v12';

async function searchTours() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log('📄 Открываю TourVisor Pro...');
    await page.goto('https://pro.tourvisor.ru/search', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    // Логин
    const emailInput = await page.$('input[type="email"]');
    const passwordInput = await page.$('input[type="password"]');
    
    if (emailInput && passwordInput) {
      console.log('🔐 Вход...');
      await emailInput.fill(EMAIL);
      await passwordInput.fill(PASSWORD);
      const submitBtn = await page.$('button[type="submit"]');
      if (submitBtn) {
        await submitBtn.click();
        await page.waitForTimeout(4000);
      }
    }
    
    console.log('🔍 Запускаю поиск туров...');
    
    // Кликаем "Найти туры"
    const searchBtn = await page.$('button:has-text("Найти туры")') || await page.$('text=Найти туры');
    if (searchBtn) {
      await searchBtn.click();
      console.log('⏳ Ожидаю результаты...');
      await page.waitForTimeout(10000); // Ждём загрузки результатов
    }
    
    // Скриншот
    await page.screenshot({ path: '/Users/bond/.openclaw/workspace/tools/tourvisor-results.png', fullPage: true });
    
    // Получаем текст
    const pageText = await page.evaluate(() => document.body.innerText);
    console.log('\n📋 РЕЗУЛЬТАТЫ ПОИСКА:\n');
    console.log(pageText.substring(0, 10000));
    
  } catch (error) {
    console.error('❌ Ошибка:', error.message);
  } finally {
    await browser.close();
  }
}

searchTours();
