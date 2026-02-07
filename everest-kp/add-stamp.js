const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');

async function addStampToPdf(inputPath, outputPath, stampImagePath) {
    // Читаем PDF
    const pdfBytes = fs.readFileSync(inputPath);
    const pdfDoc = await PDFDocument.load(pdfBytes);
    
    // Читаем изображение печати
    const stampBytes = fs.readFileSync(stampImagePath);
    const stampImage = await pdfDoc.embedPng(stampBytes);
    
    // Получаем последнюю страницу
    const pages = pdfDoc.getPages();
    const lastPage = pages[pages.length - 1];
    const { width, height } = lastPage.getSize();
    
    // Размер печати (масштабируем) — увеличиваем
    const stampWidth = 280;
    const stampHeight = (stampImage.height / stampImage.width) * stampWidth;
    
    // Позиция: внизу справа с отступом
    const x = width - stampWidth - 30;
    const y = 25;
    
    // Добавляем печать на последнюю страницу
    lastPage.drawImage(stampImage, {
        x: x,
        y: y,
        width: stampWidth,
        height: stampHeight,
    });
    
    // Сохраняем
    const modifiedPdfBytes = await pdfDoc.save();
    fs.writeFileSync(outputPath, modifiedPdfBytes);
    console.log(`✓ ${path.basename(outputPath)}`);
}

async function main() {
    const sheetsDir = path.join(__dirname, 'excel_pdfs/sheets');
    const outputDir = path.join(__dirname, 'final_pdfs');
    const stampPath = path.join(__dirname, 'stamp_signature_v3.png');
    
    // Создаём выходную папку
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Список файлов для обработки
    const files = [
        { input: 'ВОР_ЭВЕРЕСТ.pdf', output: 'ВОР_ЭВЕРЕСТ.pdf' },
        { input: 'K1.pdf', output: 'Корпус_1.pdf' },
        { input: 'К2.pdf', output: 'Корпус_2.pdf' },
        { input: 'К3.pdf', output: 'Корпус_3.pdf' },
        { input: 'К4.pdf', output: 'Корпус_4.pdf' },
        { input: 'К5.pdf', output: 'Корпус_5.pdf' },
        { input: 'К6.pdf', output: 'Корпус_6.pdf' },
        { input: 'К7.pdf', output: 'Корпус_7.pdf' },
    ];
    
    console.log('Добавление печати и подписи...\n');
    
    for (const file of files) {
        const inputPath = path.join(sheetsDir, file.input);
        const outputPath = path.join(outputDir, file.output);
        
        if (fs.existsSync(inputPath)) {
            await addStampToPdf(inputPath, outputPath, stampPath);
        } else {
            console.log(`⚠ Файл не найден: ${file.input}`);
        }
    }
    
    console.log('\n✅ Готово! Файлы в папке final_pdfs/');
}

main().catch(console.error);
