const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Загружаем данные
const data = JSON.parse(fs.readFileSync('all_korpus_data.json', 'utf8'));

// Форматирование числа
function formatNumber(num) {
    return num.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Генерация HTML для КП
function generateKPHtml(korpusNum, korpusData) {
    const today = new Date();
    const dateStr = today.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
    
    // Группируем позиции по категориям
    const panels = korpusData.items.filter(i => i.type === 'panels');
    const decorative = korpusData.items.filter(i => i.type === 'decorative');
    const other = korpusData.items.filter(i => !['panels', 'decorative'].includes(i.type));
    
    // Все позиции в порядке
    const allItems = [...panels, ...decorative, ...other];
    
    let itemsHtml = '';
    let rowNum = 1;
    let currentCategory = '';
    
    for (const item of allItems) {
        // Определяем категорию для заголовка
        let category = '';
        if (item.type === 'panels') category = 'Подшивные панели';
        else if (item.type === 'decorative') category = 'Декоративные элементы';
        else category = 'Прочие элементы';
        
        if (category !== currentCategory) {
            currentCategory = category;
            itemsHtml += `
                <tr class="category-row">
                    <td colspan="7" style="background: #f5f5f5; font-weight: bold; text-align: center;">${category}</td>
                </tr>
            `;
        }
        
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
    
    // Считаем общее кол-во
    const totalQty = korpusData.items.reduce((sum, i) => sum + i.qty, 0);
    
    return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: A4; margin: 15mm; }
        body { 
            font-family: Arial, sans-serif; 
            font-size: 9pt; 
            line-height: 1.3;
            color: #333;
        }
        .header { 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 15px;
            border-bottom: 2px solid #c5a000;
            padding-bottom: 10px;
        }
        .logo { font-size: 18pt; font-weight: bold; color: #333; }
        .logo-sub { font-size: 8pt; color: #666; }
        .company-info { text-align: right; font-size: 8pt; }
        .title { text-align: center; margin: 20px 0; }
        .title h2 { margin: 0; font-size: 12pt; }
        .info-block { 
            display: flex; 
            justify-content: space-between; 
            margin: 15px 0;
            font-size: 9pt;
        }
        .contact-block { text-align: right; }
        .intro { margin: 15px 0; font-size: 9pt; text-align: justify; }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 10px 0;
            font-size: 8pt;
        }
        th, td { 
            border: 1px solid #ccc; 
            padding: 4px 6px; 
            vertical-align: middle;
        }
        th { 
            background: #f0f0f0; 
            font-weight: bold;
            text-align: center;
        }
        .totals { margin-top: 10px; }
        .totals td { border: none; padding: 2px 6px; }
        .totals .label { text-align: right; font-weight: bold; }
        .totals .value { text-align: right; }
        .grand-total { font-size: 10pt; font-weight: bold; background: #fffde7 !important; }
        .conditions { margin-top: 20px; font-size: 8pt; }
        .conditions ul { margin: 5px 0; padding-left: 20px; }
        .conditions li { margin: 3px 0; }
        .signature-block { 
            margin-top: 40px; 
            display: flex; 
            justify-content: space-between;
            align-items: flex-end;
        }
        .signature-left { font-size: 9pt; }
        .signature-right { text-align: right; }
        .signature-right img { height: 80px; }
        .footer { 
            margin-top: 30px;
            padding-top: 10px;
            border-top: 1px solid #ccc;
            display: flex;
            justify-content: space-between;
            font-size: 8pt;
            color: #666;
        }
        .korpus-title {
            background: #c5a000;
            color: white;
            padding: 5px 10px;
            font-weight: bold;
            margin: 15px 0 5px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="logo">
                <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAAAyCAYAAACqNX6+AAAACXBIWXMAAAsTAAALEwEAmpwYAAAF0WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4yLWMwMDAgNzkuMWI2NWE3OWI0LCAyMDIyLzA2LzEzLTIyOjAxOjAxICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjQuMCAoTWFjaW50b3NoKSIgeG1wOkNyZWF0ZURhdGU9IjIwMjQtMDEtMTVUMTA6MDA6MDArMDM6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjQtMDEtMTVUMTA6MDA6MDArMDM6MDAiIHhtcDpNb2RpZnlEYXRlPSIyMDI0LTAxLTE1VDEwOjAwOjAwKzAzOjAwIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjEyMzQ1Njc4LTEyMzQtMTIzNC0xMjM0LTEyMzQ1Njc4OTBhYiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkw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" style="height: 35px; vertical-align: middle; margin-right: 10px;">
                ЭВЕРЕСТ
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
    
    <div style="font-size: 7pt; color: #666; margin-bottom: 10px;">
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
    
    <div class="title">
        <h2>Уважаемый Клиент!</h2>
    </div>
    
    <div class="intro">
        Предлагаем Вам, рассмотреть наше коммерческое предложение на комплекс работ, связанных с производством в заводских условиях запрашиваемых Вами металлоизделий и металлоконструкций.
    </div>
    
    <div class="intro" style="font-size: 8pt;">
        Производство «EVEREST» специализируется на разработке и создании металлических конструкций для оформления фасадов и внутренних пространств. Компания имеет собственные производственные мощности, обрабатывающие листовой и профильный материал из алюминия, стали, меди, латуни и пр. Современное оборудование и опытные специалисты позволяют выполнять заказы оперативно и на высоком уровне как для фасадных/улочных архитектурных элементов (облицовка зданий и колонн, корзины для кондиционеров, вентиляционные решетки, ограждения), так и для интерьерных дизайнерских решений (потолочные системы, панельная облицовка стен, лифтовые порталы).
    </div>
    
    <div class="korpus-title">Корпус ${korpusNum}</div>
    
    <table>
        <thead>
            <tr>
                <th style="width: 5%;">№ п/п</th>
                <th style="width: 30%;">Наименование</th>
                <th style="width: 15%;">Материал</th>
                <th style="width: 12%;">Цвет</th>
                <th style="width: 8%;">Ед. изм.</th>
                <th style="width: 12%;">Кол-во</th>
                <th style="width: 18%;">Цена за партию без НДС, руб.</th>
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
    
    <table class="totals" style="width: 50%; margin-left: auto;">
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
        <p><em>Итоговая сумма указана с учетом доставки до объекта</em></p>
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
            <img src="signature_stamp.png" alt="Подпись и печать">
            <div>Рыбаков А.В.</div>
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
        fs.writeFileSync(htmlPath, html);
        
        await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
        
        const pdfPath = path.join(__dirname, `КП_Корпус_${korpusNum}.pdf`);
        await page.pdf({
            path: pdfPath,
            format: 'A4',
            printBackground: true,
            margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }
        });
        
        console.log(`Сохранено: ${pdfPath}`);
    }
    
    await browser.close();
    console.log('\nВсе КП сгенерированы!');
}

generatePDFs().catch(console.error);
