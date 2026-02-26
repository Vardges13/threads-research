import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function convertHtmlToPdf() {
    console.log('🚀 Запуск Puppeteer...');
    
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    const htmlPath = path.join(__dirname, 'everest-v2-professional.html');
    const pdfPath = path.join(__dirname, 'everest-v2-beautiful.pdf');
    
    console.log('📄 Открываю HTML файл...');
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
    
    console.log('🖨️ Создаю PDF...');
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true,
        margin: {
            top: '10mm',
            bottom: '10mm',
            left: '10mm',
            right: '10mm'
        }
    });
    
    await browser.close();
    
    console.log(`✅ PDF создан: ${pdfPath}`);
}

convertHtmlToPdf().catch(console.error);