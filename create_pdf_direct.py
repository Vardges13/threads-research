#!/usr/bin/env python3
import os
import subprocess

# Попытка создать PDF через различные системные утилиты macOS

print("Попытка 1: Через lp (line printer)")
try:
    # Создаем PostScript файл
    ps_content = """%!PS-Adobe-3.0
%%Title: Everest Tech Organizational Structure
%%PageBoundingBox: 0 0 612 792
%%Pages: 1

/Times-Bold findfont 18 scalefont setfont
50 750 moveto
(ОРГАНИЗАЦИОННАЯ СТРУКТУРА ООО «ЭВЕРЕСТ-ТЕХ») show

/Courier findfont 10 scalefont setfont
50 720 moveto (УПРАВЛЯЮЩИЙ ДИРЕКТОР) show
50 705 moveto (├── ТЕХНИЧЕСКИЙ ДИРЕКТОР) show
50 690 moveto (│   └── Главный инженер АХО и СтИК) show
50 675 moveto (│       └── Технология ОТК) show
50 655 moveto (└── ГЕНЕРАЛЬНЫЙ ДИРЕКТОР) show
50 640 moveto (    ├── Охрана труда и техника безопасности) show
50 625 moveto (    └── ИСПОЛНИТЕЛЬНЫЙ ДИРЕКТОР) show
50 605 moveto (        ├── БУХГАЛТЕРИЯ) show
50 590 moveto (        │   ├── Главбух) show
50 575 moveto (        │   ├── Кадры) show
50 560 moveto (        │   └── Казначейство) show
50 540 moveto (        ├── КОНСТРУКТОРСКОЕ БЮРО) show
50 525 moveto (        │   ├── Конструктора) show
50 510 moveto (        │   └── Неокр) show
50 490 moveto (        ├── КОММЕРЧЕСКИЙ ДИРЕКТОР) show
50 475 moveto (        │   ├── Отдел продаж) show
50 460 moveto (        │   ├── Клиентский сервис) show
50 445 moveto (        │   ├── Сметный отдел) show
50 430 moveto (        │   └── Снабжение) show
50 410 moveto (        ├── ЮРИДИЧЕСКИЙ ОТДЕЛ) show
50 395 moveto (        ├── ГРУППА ЛОГИСТИКИ) show
50 375 moveto (        └── ДИРЕКТОР ПО ПРОИЗВОДСТВУ) show
50 360 moveto (            ├── Склад сырья и готовой продукции) show
50 345 moveto (            └── ПРОИЗВОДСТВЕННЫЙ БЛОК) show
50 330 moveto (                └── Начальник производства) show
50 315 moveto (                    └── Зам. начальника производства) show
50 295 moveto (                        ├── ЗАГОТОВИТЕЛЬНЫЙ УЧАСТОК) show
50 280 moveto (                        ├── ГИБОЧНЫЙ УЧАСТОК) show
50 265 moveto (                        ├── СБОРОЧНЫЙ УЧАСТОК) show
50 250 moveto (                        ├── СВАРОЧНЫЙ УЧАСТОК) show
50 235 moveto (                        ├── ПОКРАСОЧНЫЙ УЧАСТОК) show
50 220 moveto (                        └── УПАКОВКА-КОМПЛЕКТОВКА) show

showpage
%%EOF"""

    with open('everest.ps', 'w', encoding='utf-8') as f:
        f.write(ps_content)
    
    print("PostScript файл создан")
    
    # Конвертируем PS в PDF через ps2pdf
    result = subprocess.run(['ps2pdf', 'everest.ps', 'everest-org-structure.pdf'], 
                          capture_output=True, text=True, cwd='/Users/bond/.openclaw/workspace')
    
    if result.returncode == 0:
        print("PDF создан через ps2pdf!")
    else:
        print(f"ps2pdf failed: {result.stderr}")
        
except Exception as e:
    print(f"Ошибка PostScript: {e}")

print("\\nПопытка 2: Простая конвертация")
# Проверим размер созданного файла
if os.path.exists('/Users/bond/.openclaw/workspace/everest-org-structure.pdf'):
    size = os.path.getsize('/Users/bond/.openclaw/workspace/everest-org-structure.pdf')
    print(f"PDF файл создан! Размер: {size} байт")
else:
    print("PDF файл не создан")