const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Загружаем данные
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'all_korpus_data.json'), 'utf8'));
const signatureBase64 = fs.readFileSync(path.join(__dirname, 'signature_base64.txt'), 'utf8').trim();

// Форматирование числа
function formatNumber(num) {
    return num.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Генерация HTML для КП
function generateKPHtml(korpusNum, korpusData) {
    const today = new Date();
    const dateStr = today.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
    
    // Группируем позиции по категориям
    const categories = {};
    for (const item of korpusData.items) {
        if (!categories[item.category]) {
            categories[item.category] = [];
        }
        categories[item.category].push(item);
    }
    
    // Порядок категорий
    const categoryOrder = [
        'Подшивные панели',
        'Вертикальные элементы',
        'Декоративные элементы',
        'Декоративные колонны',
        'Вертикальные пилоны',
        'Горизонтальные пояса',
        'Прочее'
    ];
    
    let itemsHtml = '';
    let rowNum = 1;
    
    for (const cat of categoryOrder) {
        if (categories[cat] && categories[cat].length > 0) {
            // Заголовок категории
            itemsHtml += `
                <tr class="category-row">
                    <td colspan="7" style="background: #f5f5f5; font-weight: bold; text-align: center; padding: 6px;">${cat}</td>
                </tr>
            `;
            
            for (const item of categories[cat]) {
                itemsHtml += `
                    <tr>
                        <td style="text-align: center;">${rowNum}</td>
                        <td>${item.name}</td>
                        <td style="text-align: center;">алюминий толщ. 2 мм</td>
                        <td style="text-align: center;">${item.color}</td>
                        <td style="text-align: center;">${item.unit}</td>
                        <td style="text-align: right;">${formatNumber(item.qty)}</td>
                        <td style="text-align: right;">${formatNumber(item.total)}</td>
                    </tr>
                `;
                rowNum++;
            }
        }
    }
    
    // Считаем общее кол-во
    const totalQty = korpusData.items.reduce((sum, i) => sum + i.qty, 0);
    
    return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: A4; margin: 12mm; }
        * { box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            font-size: 8.5pt; 
            line-height: 1.3;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .header { 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 10px;
            border-bottom: 3px solid #c5a000;
            padding-bottom: 8px;
        }
        .logo { font-size: 20pt; font-weight: bold; color: #333; }
        .logo-sub { font-size: 7pt; color: #666; letter-spacing: 2px; }
        .company-info { text-align: right; font-size: 7.5pt; line-height: 1.4; }
        .rekvizity { font-size: 6.5pt; color: #666; margin-bottom: 8px; }
        .info-block { 
            display: flex; 
            justify-content: space-between; 
            margin: 10px 0;
            font-size: 8.5pt;
        }
        .contact-block { text-align: right; }
        .contact-block strong { text-decoration: underline; }
        .intro { margin: 10px 0; font-size: 8pt; text-align: justify; }
        .intro-small { font-size: 7pt; color: #555; }
        table.main-table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 8px 0;
            font-size: 7.5pt;
        }
        .main-table th, .main-table td { 
            border: 1px solid #999; 
            padding: 4px 5px; 
            vertical-align: middle;
        }
        .main-table th { 
            background: #e8e8e8; 
            font-weight: bold;
            text-align: center;
        }
        .totals-table { 
            width: 45%; 
            margin-left: auto;
            border-collapse: collapse;
            font-size: 8pt;
        }
        .totals-table td { 
            padding: 3px 8px; 
            border: none;
        }
        .totals-table .label { text-align: right; font-weight: bold; }
        .totals-table .value { text-align: right; }
        .grand-total { 
            font-size: 9pt; 
            font-weight: bold; 
            background: #fffde7 !important; 
        }
        .conditions { margin-top: 12px; font-size: 7.5pt; }
        .conditions p { margin: 4px 0; }
        .conditions ul { margin: 4px 0; padding-left: 18px; }
        .conditions li { margin: 2px 0; }
        .signature-block { 
            margin-top: 25px; 
            display: flex; 
            justify-content: space-between;
            align-items: flex-end;
            page-break-inside: avoid;
        }
        .signature-left { font-size: 8.5pt; }
        .signature-right { text-align: right; }
        .signature-right img { height: 65px; }
        .signature-name { font-size: 9pt; margin-top: 5px; }
        .footer { 
            margin-top: 15px;
            padding-top: 8px;
            border-top: 1px solid #ccc;
            display: flex;
            justify-content: space-between;
            font-size: 7pt;
            color: #666;
        }
        .korpus-title {
            background: #c5a000;
            color: white;
            padding: 6px 12px;
            font-weight: bold;
            font-size: 10pt;
            margin: 12px 0 6px 0;
        }
        .title-center {
            text-align: center;
            margin: 15px 0;
        }
        .title-center h2 {
            margin: 0;
            font-size: 12pt;
            font-weight: normal;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="logo">
                <span style="color: #c5a000;">▲</span> ЭВЕРЕСТ
            </div>
            <div class="logo-sub">МЕТАЛЛООБРАБОТКА</div>
        </div>
        <div class="company-info">
            ООО «ЭВЕРЕСТ-ТЕХ»<br>
            127644, город Москва, улица Лобненская, дом 21, эт. 3, пом. II, ком. 13, 14<br>
            Тел.: 8 (495) 255-06-40<br>
            e-mail: info@everest-zavod.ru
        </div>
    </div>
    
    <div class="rekvizity">
        ИНН 7713766665 КПП 771301001 ОГРН 1137746305058 ОКПО 17416880 Р/С 40702810438040032500 К/С 30101810400000000225 БИК 044525225 ПАО СБЕРБАНК Г. МОСКВА
    </div>
    
    <div class="info-block">
        <div>
            <strong>Дата:</strong> ${dateStr}<br>
            <strong>Проект:</strong> 7139_Остров-7 Корпуса 1-7
        </div>
        <div class="contact-block">
            <strong>Контакт для связи:</strong><br>
            <em>должность:</em> коммерческий директор<br>
            <em>Ф.И.О.:</em> Ковалев Михаил Александрович<br>
            <em>тел.:</em> 89169018140<br>
            <em>e-mail:</em> ceo@everest-zavod.ru
        </div>
    </div>
    
    <div class="title-center">
        <h2>Уважаемый Клиент!</h2>
    </div>
    
    <div class="intro">
        Предлагаем Вам, рассмотреть наше коммерческое предложение на комплекс работ, связанных с производством в заводских условиях запрашиваемых Вами металлоизделий и металлоконструкций.
    </div>
    
    <div class="intro intro-small">
        Производство «EVEREST» специализируется на разработке и создании металлических конструкций для оформления фасадов и внутренних пространств. Компания имеет собственные производственные мощности, обрабатывающие листовой и профильный материал из алюминия, стали, меди, латуни и пр. Современное оборудование и опытные специалисты позволяют выполнять заказы оперативно и на высоком уровне как для фасадных/уличных архитектурных элементов (облицовка зданий и колонн, корзины для кондиционеров, вентиляционные решетки, ограждения), так и для интерьерных дизайнерских решений (потолочные системы, панельная облицовка стен, лифтовые порталы).
    </div>
    
    <div class="korpus-title">Корпус ${korpusNum}</div>
    
    <table class="main-table">
        <thead>
            <tr>
                <th style="width: 4%;">№ п/п</th>
                <th style="width: 28%;">Наименование</th>
                <th style="width: 14%;">Материал</th>
                <th style="width: 12%;">Цвет</th>
                <th style="width: 6%;">Ед. изм.</th>
                <th style="width: 10%;">Кол-во</th>
                <th style="width: 16%;">Цена за партию без НДС, руб.</th>
            </tr>
        </thead>
        <tbody>
            ${itemsHtml}
            <tr style="font-weight: bold; background: #f9f9f9;">
                <td colspan="5" style="text-align: right;">ИТОГО:</td>
                <td style="text-align: right;">${formatNumber(totalQty)}</td>
                <td></td>
            </tr>
        </tbody>
    </table>
    
    <table class="totals-table">
        <tr>
            <td class="label">ИТОГО без НДС:</td>
            <td class="value">${formatNumber(korpusData.total_no_vat)}</td>
        </tr>
        <tr>
            <td class="label">НДС 22%:</td>
            <td class="value">${formatNumber(korpusData.vat)}</td>
        </tr>
        <tr class="grand-total">
            <td class="label">ИТОГО с НДС 22%:</td>
            <td class="value">${formatNumber(korpusData.total_with_vat)}</td>
        </tr>
    </table>
    
    <div class="conditions">
        <p><em>Расчет стоимости произведен на основании предоставленных данных. Окончательный объем и стоимость определяется по результатам разработки конструкторской документации.</em></p>
        <p><em>Итоговая сумма указана с учетом доставки до объекта.</em></p>
        <p><em>Стоимость указана по ВИДИМОЙ части панели.</em></p>
        
        <p><strong>Коммерческие условия:</strong></p>
        <ul>
            <li>Разработка КМД, маркировка продукции и упаковка включены в стоимость продукции по условиям КП.</li>
            <li>Упаковка осуществляется в жесткую тару (деревянный ящик).</li>
            <li>Условия оплаты: аванс - 70%, остаток - 30% перед отгрузкой.</li>
            <li>Доставка осуществляется на объект.</li>
            <li>Персональное предложение действительно в течение 3 рабочих дней.</li>
        </ul>
    </div>
    
    <div class="signature-block">
        <div class="signature-left">
            Генеральный директор ООО «Эверест-Тех»
        </div>
        <div class="signature-right">
            <img src="${signatureBase64}" alt="Подпись и печать">
            <div class="signature-name">Рыбаков А.В.</div>
        </div>
    </div>
    
    <div class="footer">
        <div>WWW.EVEREST-ZAVOD.RU</div>
        <div>EVEREST МЕТАЛЛООБРАБОТКА</div>
    </div>
</body>
</html>`;
}

async function generatePDFs() {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    for (const [korpusNum, korpusData] of Object.entries(data)) {
        console.log(`Генерация КП для Корпуса ${korpusNum}...`);
        
        const html = generateKPHtml(korpusNum, korpusData);
        const htmlPath = path.join(__dirname, `kp_korpus_${korpusNum}.html`);
        fs.writeFileSync(htmlPath, html, 'utf8');
        
        await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
        
        const pdfPath = path.join(__dirname, `КП_Корпус_${korpusNum}.pdf`);
        await page.pdf({
            path: pdfPath,
            format: 'A4',
            printBackground: true,
            margin: { top: '8mm', bottom: '8mm', left: '8mm', right: '8mm' }
        });
        
        console.log(`  ✓ Сохранено: КП_Корпус_${korpusNum}.pdf`);
    }
    
    await browser.close();
    console.log('\n✅ Все 7 КП сгенерированы!');
}

generatePDFs().catch(console.error);
