import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD
import Part
import importDXF
from FreeCAD import Base
V = Base.Vector

doc = FreeCAD.newDocument("Full")
Part.insert("KLC-2-1.1-clean.step", "Full")
shape = doc.Objects[0].Shape

# Parameters  
t = 2.0
r = 2.0
k = 0.4
ba_90 = 3.14159 * (r + k*t) * 0.5

# Find ALL circular features (holes)
all_circles = []
for edge in shape.Edges:
    try:
        if edge.Curve.__class__.__name__ == 'Circle':
            c = edge.Curve
            # Check if it's on a horizontal plane (mounting holes on top/bottom)
            if abs(c.Axis.z) > 0.9:  # Z-axis oriented (horizontal hole)
                all_circles.append({
                    'x': c.Center.x,
                    'y': c.Center.y,  
                    'z': c.Center.z,
                    'r': c.Radius
                })
    except:
        pass

print(f"Found {len(all_circles)} circular edges")

# Group by radius
from collections import Counter
radii = Counter([round(c['r'], 1) for c in all_circles])
print("Hole radii distribution:")
for r_val, count in sorted(radii.items()):
    print(f"  D{r_val*2:.1f}mm: {count} pcs")

# Get unique holes (filter duplicates from top/bottom)
unique_holes = []
for c in all_circles:
    if abs(c['z']) < 1:  # Only top surface holes
        is_dup = False
        for uh in unique_holes:
            if abs(c['x'] - uh['x']) < 0.5 and abs(c['y'] - uh['y']) < 0.5:
                is_dup = True
                break
        if not is_dup:
            unique_holes.append(c)

print(f"Unique holes on top surface: {len(unique_holes)}")

# Unfold dimensions
main_w = 916.8
main_l = 2993.8  
flange_h = 305.9
unfold_w = main_w + flange_h + ba_90

# Create shapes for DXF
shapes = []

# Outer rectangle
p1, p2, p3, p4 = V(0,0,0), V(unfold_w,0,0), V(unfold_w,main_l,0), V(0,main_l,0)
outline = Part.makePolygon([p1, p2, p3, p4, p1])
shapes.append(outline)

# Bend line
bend_line = Part.makeLine(V(main_w, 0, 0), V(main_w, main_l, 0))
shapes.append(bend_line)

# Add holes - transform Y coordinate (model Y range: -1496.9 to 1496.9)
y_offset = main_l / 2  # shift to make all Y positive
for h in unique_holes:
    if h['x'] < main_w:  # holes on main panel
        cx = h['x']
        cy = h['y'] + y_offset
        if 0 < cx < unfold_w and 0 < cy < main_l:
            circle = Part.makeCircle(h['r'], V(cx, cy, 0))
            shapes.append(circle)

print(f"Added {len(shapes)-2} holes to DXF")

# Create compound and export
compound = Part.makeCompound(shapes)

doc2 = FreeCAD.newDocument("Export")
obj = doc2.addObject("Part::Feature", "Unfold")
obj.Shape = compound
doc2.recompute()

importDXF.export([obj], "KLC-2-1.1-full-unfold.dxf")
print(f"\nExported: KLC-2-1.1-full-unfold.dxf")
print(f"Unfold size: {unfold_w:.1f} x {main_l:.1f} mm")
