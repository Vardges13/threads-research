import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD
import Part
import importDXF
from FreeCAD import Base
V = Base.Vector

# Parameters
t = 2.0
r_bend = 2.0
k = 0.4
ba = 3.14159 * (r_bend + k*t) * 0.5  # 4.4 mm

# Dimensions
main_w = 916.8  # main panel width (X)
main_l = 2993.8  # length (Y in model is -1496.9 to +1496.9)
flange_h = 305.9  # side flange height
total_w = main_w + ba + flange_h  # 1227 mm

y_offset = main_l / 2  # shift model Y to make all positive

shapes = []

# OUTLINE
outline = Part.makePolygon([
    V(0, 0, 0), V(total_w, 0, 0), V(total_w, main_l, 0), V(0, main_l, 0), V(0, 0, 0)
])
shapes.append(outline)

# BEND LINE (main bend)
bend = Part.makeLine(V(main_w, 0, 0), V(main_w, main_l, 0))
shapes.append(bend)

# MOUNTING SLOTS on ends (Y=0 and Y=main_l edges)
# Model coords: X=159,179,549,569, Y=±1498.5/±1500 (oval slots 5mm)
slot_x = [159, 179, 549, 569]
slot_r = 2.5
for x in slot_x:
    # Bottom edge (Y=0)
    shapes.append(Part.makeCircle(slot_r, V(x, slot_r, 0)))  # semi-circle at edge
    # Top edge (Y=main_l)
    shapes.append(Part.makeCircle(slot_r, V(x, main_l - slot_r, 0)))

# MOUNTING HOLES on side edge (X=921.5-923, Z=-20 -> on flange)
# Model Y coords: ±258.5, ±281.5, ±798.5, ±821.5, ±1338.5, ±1361.5
side_holes_y = [-1361.5, -1338.5, -821.5, -798.5, -281.5, -258.5, 258.5, 281.5, 798.5, 821.5, 1338.5, 1361.5]
hole_r = 2.0
# These holes are on the side flange, which unfolds to X > main_w
flange_mid_x = main_w + ba + flange_h/2  # center of flange in unfold
for y_model in side_holes_y:
    y_unfold = y_model + y_offset
    shapes.append(Part.makeCircle(hole_r, V(flange_mid_x, y_unfold, 0)))

# HOLES on opposite side (X=0-1.5 in model, on main panel edge)
# Model Y: 358.5, 381.5, 848.5, 871.5, 1338.5, 1361.5 (only positive Y in model)
edge_holes_y = [358.5, 381.5, 848.5, 871.5, 1338.5, 1361.5]
for y_model in edge_holes_y:
    y_unfold = y_model + y_offset
    shapes.append(Part.makeCircle(hole_r, V(1.5, y_unfold, 0)))

# CORNER RADIUS at main bend corners (R3.1)
corner_r = 3.1
# Bottom-left corner of bend area
shapes.append(Part.makeCircle(corner_r, V(main_w - corner_r, corner_r, 0)))
# Top-left corner of bend area
shapes.append(Part.makeCircle(corner_r, V(main_w - corner_r, main_l - corner_r, 0)))

# Create compound
compound = Part.makeCompound(shapes)

# Export
doc = FreeCAD.newDocument("DetailedUnfold")
obj = doc.addObject("Part::Feature", "Unfold")
obj.Shape = compound
doc.recompute()

importDXF.export([obj], "KLC-2-1.1-detailed-unfold.dxf")

print("=== DETAILED UNFOLD ===")
print(f"Size: {total_w:.0f} x {main_l:.0f} mm")
print(f"Bend line at X = {main_w:.0f} mm")
print(f"Slots on ends: {len(slot_x)*2} pcs (D{slot_r*2:.0f})")
print(f"Side flange holes: {len(side_holes_y)} pcs (D{hole_r*2:.0f})")
print(f"Edge holes: {len(edge_holes_y)} pcs (D{hole_r*2:.0f})")
print(f"Corner radii: 4 pcs (R{corner_r:.0f})")
print(f"\nExported: KLC-2-1.1-detailed-unfold.dxf")
