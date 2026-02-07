const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');

async function addStampToPdf(inputPath, outputPath, stampImagePath) {
    const pdfBytes = fs.readFileSync(inputPath);
    const pdfDoc = await PDFDocument.load(pdfBytes);
    
    const stampBytes = fs.readFileSync(stampImagePath);
    const stampImage = await pdfDoc.embedPng(stampBytes);
    
    const pages = pdfDoc.getPages();
    const lastPage = pages[pages.length - 1];
    const { width, height } = lastPage.getSize();
    
    const stampWidth = 220;
    const stampHeight = (stampImage.height / stampImage.width) * stampWidth;
    
    // Позиция: 0.42 от низа (немного ниже середины)
    const y = height * 0.42;
    
    lastPage.drawImage(stampImage, {
        x: width - stampWidth - 40,
        y: y,
        width: stampWidth,
        height: stampHeight,
    });
    
    const modifiedPdfBytes = await pdfDoc.save();
    fs.writeFileSync(outputPath, modifiedPdfBytes);
}

async function main() {
    const inputDir = path.join(__dirname, 'excel_pdfs/all_sheets');
    const outputDir = path.join(__dirname, 'final_signed');
    const stampPath = path.join(__dirname, 'stamp_signature_v3.png');
    
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const files = [
        'ВОР_ЭВЕРЕСТ.pdf',
        'Корпус_1.pdf',
        'Корпус_2.pdf',
        'Корпус_3.pdf',
        'Корпус_4.pdf',
        'Корпус_5.pdf',
        'Корпус_6.pdf',
        'Корпус_7.pdf',
    ];
    
    console.log('Добавление печати...');
    
    for (const file of files) {
        const inputPath = path.join(inputDir, file);
        const outputPath = path.join(outputDir, file);
        await addStampToPdf(inputPath, outputPath, stampPath);
        console.log('✓', file);
    }
    
    console.log('\n✅ Все файлы готовы!');
}

main().catch(console.error);
