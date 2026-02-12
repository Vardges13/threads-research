/*
 * GX53 Светильник - упрощённая модель
 * Для визуализации
 */

$fn = 48;

// Размеры
outer_d = 106;
inner_d = 53;
cutout_d = 90;
h_flange = 4;
h_body = 19;

// Корпус
difference() {
    union() {
        // Фланец
        translate([0,0,h_body])
        cylinder(h=h_flange, d=outer_d);
        
        // Тело
        cylinder(h=h_body, d=cutout_d-2);
    }
    
    // Отверстие
    translate([0,0,-1])
    cylinder(h=h_body+h_flange+2, d=inner_d);
    
    // Полость
    translate([0,0,1.5])
    cylinder(h=h_body, d=cutout_d-5);
}

// Пружины (упрощённо)
for(a=[0,180]) {
    rotate([0,0,a])
    translate([cutout_d/2-3, -12, 5])
    rotate([0,30,0])
    cube([25, 24, 1.5]);
}
