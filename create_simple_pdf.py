#!/usr/bin/env python3
"""
Простой генератор PDF с организационной структурой
"""

def create_pdf_header():
    return """
%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Resources <<
/Font <<
/F1 4 0 R
/F2 5 0 R
>>
>>
/Contents 6 0 R
>>
endobj

4 0 obj
<<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica-Bold
>>
endobj

5 0 obj
<<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
endobj

6 0 obj
<<
/Length 7 0 R
>>
stream
BT
/F1 18 Tf
50 750 Td
(Организационная структура ООО «Эверест-Тех») Tj
0 -30 Td
/F2 12 Tf
(УПРАВЛЯЮЩИЙ ДИРЕКТОР) Tj
0 -20 Td
(├── ТЕХНИЧЕСКИЙ ДИРЕКТОР) Tj
0 -15 Td
(│   └── Главный инженер АХО и СтИК) Tj
0 -15 Td
(│       └── Технология ОТК) Tj
0 -20 Td
(└── ГЕНЕРАЛЬНЫЙ ДИРЕКТОР) Tj
0 -15 Td
(    ├── Охрана труда и техника безопасности) Tj
0 -15 Td
(    └── ИСПОЛНИТЕЛЬНЫЙ ДИРЕКТОР) Tj
0 -20 Td
(        ├── БУХГАЛТЕРИЯ) Tj
0 -15 Td
(        │   ├── Главбух) Tj
0 -15 Td
(        │   ├── Кадры) Tj
0 -15 Td
(        │   └── Казначейство) Tj
0 -20 Td
(        ├── КОНСТРУКТОРСКОЕ БЮРО) Tj
0 -15 Td
(        │   ├── Конструктора) Tj
0 -15 Td
(        │   └── Неокр) Tj
0 -20 Td
(        ├── КОММЕРЧЕСКИЙ ДИРЕКТОР) Tj
0 -15 Td
(        │   ├── Отдел продаж) Tj
0 -15 Td
(        │   ├── Клиентский сервис) Tj
0 -15 Td
(        │   ├── Сметный отдел) Tj
0 -15 Td
(        │   └── Снабжение) Tj
0 -20 Td
(        ├── ЮРИДИЧЕСКИЙ ОТДЕЛ) Tj
0 -15 Td
(        ├── ГРУППА ЛОГИСТИКИ) Tj
0 -20 Td
(        └── ДИРЕКТОР ПО ПРОИЗВОДСТВУ) Tj
0 -15 Td
(            ├── Склад сырья и готовой продукции) Tj
0 -15 Td
(            └── ПРОИЗВОДСТВЕННЫЙ БЛОК) Tj
0 -15 Td
(                └── Начальник производства) Tj
0 -15 Td
(                    └── Зам. начальника производства) Tj
0 -20 Td
(                        ├── ЗАГОТОВИТЕЛЬНЫЙ УЧАСТОК) Tj
0 -15 Td
(                        ├── ГИБОЧНЫЙ УЧАСТОК) Tj
0 -15 Td
(                        ├── СБОРОЧНЫЙ УЧАСТОК) Tj
0 -15 Td
(                        ├── СВАРОЧНЫЙ УЧАСТОК) Tj
0 -15 Td
(                        ├── ПОКРАСОЧНЫЙ УЧАСТОК) Tj
0 -15 Td
(                        └── УПАКОВКА-КОМПЛЕКТОВКА) Tj
ET
endstream
endobj

7 0 obj
2847
endobj

xref
0 8
0000000000 65535 f 
0000000010 00000 n 
0000000079 00000 n 
0000000138 00000 n 
0000000291 00000 n 
0000000379 00000 n 
0000000463 00000 n 
0000003362 00000 n 
trailer
<<
/Size 8
/Root 1 0 R
>>
startxref
3381
%%EOF
"""

# Создаем PDF
try:
    with open('/Users/bond/.openclaw/workspace/everest-org-structure.pdf', 'w', encoding='latin-1') as f:
        f.write(create_pdf_header().strip())
    print("PDF создан успешно!")
except Exception as e:
    print(f"Ошибка создания PDF: {e}")