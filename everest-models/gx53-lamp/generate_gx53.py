#!/usr/bin/env python3
"""
GX53 Встраиваемый светильник OGX-R1-001-GX53-DIY
3D модель для визуализации
Размеры по фото от Михаила (Эверест-Тех)
"""

import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')

import FreeCAD
import Part
import math

# === РАЗМЕРЫ (мм) ===
OUTER_DIAMETER = 106.0      # Внешний диаметр
CUTOUT_DIAMETER = 90.0      # Врезное отверстие  
INNER_DIAMETER = 53.0       # Посадка под GX53
TOTAL_HEIGHT = 23.0         # Общая высота
FLANGE_HEIGHT = 4.0         # Высота фланца (видимая часть)
BODY_HEIGHT = 19.0          # Высота корпуса (в потолке)
WALL_THICKNESS = 1.5        # Толщина стенки

# Пружины
SPRING_WIRE_DIA = 1.5       # Диаметр проволоки
SPRING_WIDTH = 25.0         # Ширина пружины
SPRING_LENGTH = 35.0        # Длина пружины

def create_lamp_body():
    """Создаёт корпус светильника"""
    doc = FreeCAD.newDocument("GX53_Lamp")
    
    # === ФЛАНЕЦ (видимая часть) ===
    # Внешнее кольцо фланца
    flange_outer = Part.makeCylinder(
        OUTER_DIAMETER / 2,  # радиус
        FLANGE_HEIGHT,       # высота
        FreeCAD.Vector(0, 0, BODY_HEIGHT)  # позиция (сверху)
    )
    
    # Вырез под лампу (центральное отверстие)
    flange_hole = Part.makeCylinder(
        INNER_DIAMETER / 2,
        FLANGE_HEIGHT + 1,
        FreeCAD.Vector(0, 0, BODY_HEIGHT - 0.5)
    )
    
    flange = flange_outer.cut(flange_hole)
    
    # === КОРПУС (в потолке) ===
    # Внешняя стенка корпуса
    body_outer = Part.makeCylinder(
        CUTOUT_DIAMETER / 2 - 1,  # чуть меньше врезного отверстия
        BODY_HEIGHT,
        FreeCAD.Vector(0, 0, 0)
    )
    
    # Внутренняя полость
    body_inner = Part.makeCylinder(
        CUTOUT_DIAMETER / 2 - 1 - WALL_THICKNESS,
        BODY_HEIGHT - WALL_THICKNESS,
        FreeCAD.Vector(0, 0, WALL_THICKNESS)
    )
    
    body = body_outer.cut(body_inner)
    
    # Центральное отверстие через весь корпус
    center_hole = Part.makeCylinder(
        INNER_DIAMETER / 2,
        TOTAL_HEIGHT + 1,
        FreeCAD.Vector(0, 0, -0.5)
    )
    
    body = body.cut(center_hole)
    
    # === ОБЪЕДИНЕНИЕ ===
    lamp = flange.fuse(body)
    
    # === ПРУЖИННЫЕ ФИКСАТОРЫ ===
    springs = []
    for angle in [0, 180]:  # две пружины напротив друг друга
        rad = math.radians(angle)
        
        # Базовая точка крепления
        base_x = (CUTOUT_DIAMETER / 2 - 5) * math.cos(rad)
        base_y = (CUTOUT_DIAMETER / 2 - 5) * math.sin(rad)
        
        # Создаём упрощённую пружину (прямоугольник)
        spring_profile = Part.makeBox(
            SPRING_WIDTH,
            SPRING_WIRE_DIA * 2,
            SPRING_LENGTH,
            FreeCAD.Vector(
                base_x - SPRING_WIDTH / 2,
                base_y - SPRING_WIRE_DIA,
                5
            )
        )
        springs.append(spring_profile)
    
    # Добавляем пружины
    for spring in springs:
        lamp = lamp.fuse(spring)
    
    # === СОХРАНЕНИЕ ===
    # Добавляем в документ
    part_obj = doc.addObject("Part::Feature", "GX53_Lamp")
    part_obj.Shape = lamp
    
    # Экспорт в разные форматы
    output_dir = "/Users/bond/.openclaw/workspace/everest-models/gx53-lamp"
    
    # STL для визуализации
    lamp.exportStl(f"{output_dir}/GX53-lamp-visual.stl")
    print(f"✅ STL сохранён: {output_dir}/GX53-lamp-visual.stl")
    
    # STEP для производства
    lamp.exportStep(f"{output_dir}/GX53-lamp.step")
    print(f"✅ STEP сохранён: {output_dir}/GX53-lamp.step")
    
    # Сохраняем FreeCAD документ
    doc.saveAs(f"{output_dir}/GX53-lamp.FCStd")
    print(f"✅ FreeCAD проект: {output_dir}/GX53-lamp.FCStd")
    
    return lamp

if __name__ == "__main__":
    print("🔧 Создаю 3D модель светильника GX53...")
    print(f"   Внешний Ø: {OUTER_DIAMETER} мм")
    print(f"   Врезное Ø: {CUTOUT_DIAMETER} мм")
    print(f"   Высота: {TOTAL_HEIGHT} мм")
    print()
    
    create_lamp_body()
    
    print()
    print("🎉 Готово!")
