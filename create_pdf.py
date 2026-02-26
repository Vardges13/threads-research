#!/usr/bin/env python3

import subprocess
import sys
import os

# Проверяем, есть ли текстовый файл
if not os.path.exists('everest-org-simple.txt'):
    print("Файл everest-org-simple.txt не найден")
    sys.exit(1)

# Пытаемся создать PDF через различные способы
content = open('everest-org-simple.txt', 'r', encoding='utf-8').read()

# Создаём HTML версию с лучшим форматированием
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Организационная структура ООО «Эверест-Тех»</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 12px;
            line-height: 1.4;
            margin: 20px;
            color: #333;
        }}
        h1 {{
            font-size: 16px;
            text-align: center;
            margin-bottom: 30px;
        }}
        pre {{
            white-space: pre-wrap;
            font-family: "SF Mono", Monaco, monospace;
            font-size: 10px;
            line-height: 1.3;
        }}
    </style>
</head>
<body>
    <h1>Организационная структура ООО «Эверест-Тех»</h1>
    <pre>{content}</pre>
</body>
</html>
"""

with open('everest-org-structure-formatted.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML файл создан: everest-org-structure-formatted.html")

# Пытаемся конвертировать через Safari (если доступно)
try:
    # Используем osascript для печати в PDF через Safari
    script = '''
tell application "Safari"
    open POSIX file "/Users/bond/.openclaw/workspace/everest-org-structure-formatted.html"
    delay 2
    tell application "System Events"
        keystroke "p" using command down
        delay 1
        keystroke return
    end tell
end tell
'''
    print("Попытка печати через Safari...")
    subprocess.run(['osascript', '-e', script])
except Exception as e:
    print(f"Ошибка при печати через Safari: {e}")