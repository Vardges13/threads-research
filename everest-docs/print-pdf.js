const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function printPDF(htmlFile, pdfFile) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  const htmlPath = path.resolve(htmlFile);
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: pdfFile,
    format: 'A4',
    margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' },
    printBackground: true
  });
  await browser.close();
  console.log('Created:', pdfFile);
}

(async () => {
  await printPDF('01-marshrutnaya-karta.html', '01-marshrutnaya-karta.pdf');
  await printPDF('02-proizvodstvenniy-uchet.html', '02-proizvodstvenniy-uchet.pdf');
  await printPDF('03-smenniy-otchet-uchastka.html', '03-smenniy-otchet-uchastka.pdf');
})();
