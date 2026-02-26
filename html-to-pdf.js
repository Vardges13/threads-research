const fs = require('fs');
const path = require('path');

// Простой скрипт для создания PDF через browser automation
// Но у нас нет Puppeteer, поэтому создадим инструкцию

const htmlFile = '/Users/bond/.openclaw/workspace/everest-org-pdf.html';
const instructionsFile = '/Users/bond/.openclaw/workspace/pdf-instructions.txt';

const instructions = `
ИНСТРУКЦИЯ ПО СОЗДАНИЮ PDF:

1. Откройте файл в Safari:
   ${htmlFile}

2. Нажмите Cmd+P (печать)

3. В диалоге печати нажмите кнопку "PDF" (внизу слева)

4. Выберите "Сохранить как PDF..."

5. Введите имя файла: everest-org-structure

6. Нажмите "Сохранить"

PDF будет создан в папке Загрузки или выбранной директории.

АЛЬТЕРНАТИВНО:
Можете открыть файл в любом браузере и использовать функцию печати в PDF.
`;

fs.writeFileSync(instructionsFile, instructions);
console.log('Инструкции созданы в:', instructionsFile);