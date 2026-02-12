#!/usr/bin/env python3
# Создаем PDF только с ASCII символами

def create_ascii_pdf():
    pdf_content = """%PDF-1.4
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
/Contents 4 0 R
/Resources <<
/Font <<
/F1 5 0 R
>>
>>
>>
endobj

4 0 obj
<<
/Length 1200
>>
stream
BT
/F1 16 Tf
50 750 Td
(EVEREST-TECH LLC ORGANIZATIONAL STRUCTURE) Tj
0 -30 Td
/F1 10 Tf
(MANAGING DIRECTOR) Tj
0 -15 Td
(+-- TECHNICAL DIRECTOR) Tj
0 -15 Td
(|   +-- Chief Engineer AHO and StIK) Tj
0 -15 Td
(|       +-- Technology QC) Tj
0 -20 Td
(+-- GENERAL DIRECTOR) Tj
0 -15 Td
(    +-- Safety and Security) Tj
0 -15 Td
(    +-- EXECUTIVE DIRECTOR) Tj
0 -20 Td
(        +-- ACCOUNTING) Tj
0 -15 Td
(        |   +-- Chief Accountant) Tj
0 -15 Td
(        |   +-- HR Department) Tj
0 -15 Td
(        |   +-- Treasury) Tj
0 -20 Td
(        +-- DESIGN BUREAU) Tj
0 -15 Td
(        |   +-- Designers) Tj
0 -20 Td
(        +-- COMMERCIAL DIRECTOR) Tj
0 -15 Td
(        |   +-- Sales Department) Tj
0 -15 Td
(        |   +-- Customer Service) Tj
0 -15 Td
(        |   +-- Estimation Department) Tj
0 -15 Td
(        |   +-- Procurement) Tj
0 -20 Td
(        +-- LEGAL DEPARTMENT) Tj
0 -15 Td
(        +-- LOGISTICS GROUP) Tj
0 -20 Td
(        +-- PRODUCTION DIRECTOR) Tj
0 -15 Td
(            +-- Raw Materials & Finished Goods Warehouse) Tj
0 -15 Td
(            +-- PRODUCTION BLOCK) Tj
0 -15 Td
(                +-- Production Manager) Tj
0 -15 Td
(                    +-- Deputy Production Manager) Tj
0 -20 Td
(                        +-- PREPARATION SECTION) Tj
0 -15 Td
(                        |   +-- Laser Cutting) Tj
0 -15 Td
(                        |   +-- Guillotine) Tj
0 -15 Td
(                        |   +-- CNC Punching) Tj
0 -20 Td
(                        +-- BENDING SECTION) Tj
0 -15 Td
(                        |   +-- Panel Benders) Tj
0 -15 Td
(                        |   +-- Press Brakes) Tj
0 -15 Td
(                        |   +-- Rolling) Tj
0 -20 Td
(                        +-- ASSEMBLY SECTION) Tj
0 -15 Td
(                        +-- WELDING SECTION) Tj
0 -15 Td
(                        +-- PAINTING SECTION) Tj
0 -15 Td
(                        +-- PACKAGING & COMPLETION) Tj
ET
endstream
endobj

5 0 obj
<<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
endobj

xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000079 00000 n 
0000000137 00000 n 
0000000325 00000 n 
0000001577 00000 n 
trailer
<<
/Size 6
/Root 1 0 R
>>
startxref
1650
%%EOF"""

    try:
        with open('/Users/bond/.openclaw/workspace/everest-org-structure.pdf', 'wb') as f:
            f.write(pdf_content.encode('ascii'))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if create_ascii_pdf():
        print("✅ PDF created successfully!")
        import os
        size = os.path.getsize('/Users/bond/.openclaw/workspace/everest-org-structure.pdf')
        print(f"File size: {size} bytes")
    else:
        print("❌ Failed to create PDF")