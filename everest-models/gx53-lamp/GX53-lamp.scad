/*
 * Встраиваемый светильник GX53
 * Модель: OGX-R1-001-GX53-DIY (ОНЛАЙТ DIY)
 * Для: Михаил Ковалев, ООО "Эверест-Тех"
 * Автор: Бонд (OpenClaw Agent)
 * Дата: 2026-02-09
 */

// === РАЗМЕРЫ (мм) ===
outer_dia = 106;           // Внешний диаметр фланца
cutout_dia = 90;           // Врезное отверстие
inner_dia = 53;            // Посадка под GX53
total_height = 23;         // Общая высота
flange_height = 4;         // Высота фланца (видимая часть)
body_height = 19;          // Высота корпуса (в потолке)
wall_thick = 1.5;          // Толщина стенки

// Пружины
spring_wire = 1.5;         // Диаметр проволоки
spring_width = 25;         // Ширина пружины
spring_length = 30;        // Длина пружины
spring_angle = 25;         // Угол отгиба

$fn = 64;  // Качество окружностей

// === ОСНОВНОЙ КОРПУС ===
module lamp_body() {
    difference() {
        union() {
            // Фланец (видимая часть сверху)
            translate([0, 0, body_height])
            cylinder(h=flange_height, d=outer_dia);
            
            // Корпус (в потолке)
            cylinder(h=body_height, d=cutout_dia - 2);
        }
        
        // Центральное отверстие под лампу
        translate([0, 0, -1])
        cylinder(h=total_height + 2, d=inner_dia);
        
        // Внутренняя полость корпуса
        translate([0, 0, wall_thick])
        cylinder(h=body_height, d=cutout_dia - 2 - wall_thick*2);
        
        // Скос на фланце (эстетика)
        translate([0, 0, body_height + flange_height - 0.5])
        difference() {
            cylinder(h=1, d=outer_dia + 1);
            cylinder(h=1, d1=inner_dia, d2=inner_dia + 3);
        }
    }
}

// === ПРУЖИННЫЙ ФИКСАТОР ===
module spring_clip() {
    // Основание (крепление к корпусу)
    translate([0, -spring_width/2, 0])
    cube([3, spring_width, 8]);
    
    // Пружина (отогнутая часть)
    translate([0, 0, 5])
    rotate([0, spring_angle, 0])
    translate([0, -spring_width/2, 0])
    cube([spring_length, spring_width, spring_wire]);
    
    // Загнутый конец
    translate([0, 0, 5])
    rotate([0, spring_angle, 0])
    translate([spring_length - 2, -spring_width/2, 0])
    rotate([0, -60, 0])
    cube([8, spring_width, spring_wire]);
}

// === СБОРКА ===
module gx53_lamp() {
    color("White")
    lamp_body();
    
    // Пружины (2 шт, напротив друг друга)
    color("Silver") {
        translate([cutout_dia/2 - 5, 0, 3])
        spring_clip();
        
        rotate([0, 0, 180])
        translate([cutout_dia/2 - 5, 0, 3])
        spring_clip();
    }
}

// Рендер
gx53_lamp();

// Информация
echo("=== GX53 Светильник ===");
echo(str("Внешний Ø: ", outer_dia, " мм"));
echo(str("Врезное Ø: ", cutout_dia, " мм"));
echo(str("Высота: ", total_height, " мм"));
