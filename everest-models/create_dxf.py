import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD
import Part
import importDXF

doc = FreeCAD.newDocument("DXF")
Part.insert("KLC-2-1.1-clean.step", "DXF")
shape = doc.Objects[0].Shape

# Parameters
t = 2.0  # thickness
r = 2.0  # bend radius  
k = 0.4  # k-factor
ba_90 = 3.14159 * (r + k*t) * 0.5  # 90 deg bend allowance

# Dimensions from analysis
main_w = 916.8
main_l = 2993.8
flange_h = 305.9

# Create unfold as simple rectangle (main + flange)
unfold_w = main_w + flange_h + ba_90
unfold_l = main_l

print(f"Creating unfold: {unfold_w:.1f} x {unfold_l:.1f} mm")

# Create outline edges
from FreeCAD import Base
V = Base.Vector

# Unfold outline (origin at corner, X = width, Y = length)
p1 = V(0, 0, 0)
p2 = V(unfold_w, 0, 0)
p3 = V(unfold_w, unfold_l, 0)
p4 = V(0, unfold_l, 0)

outline = Part.makePolygon([p1, p2, p3, p4, p1])

# Bend line position
bend_x = main_w  # bend at edge of main panel
bend_line = Part.makeLine(V(bend_x, 0, 0), V(bend_x, unfold_l, 0))

print(f"Bend line at X = {bend_x:.1f} mm")

# Extract mounting holes from original
# Find small circular edges on top faces
holes = []
for edge in shape.Edges:
    if hasattr(edge, 'Curve'):
        curve_type = edge.Curve.__class__.__name__
        if curve_type == 'Circle':
            r_hole = edge.Curve.Radius
            center = edge.Curve.Center
            # Only holes on top surface (Z near 0 or near -3.1)
            if abs(center.z) < 5 or abs(center.z + 3.1) < 1:
                if r_hole > 1 and r_hole < 20:  # reasonable hole size
                    holes.append({
                        'center': (center.x, center.y),
                        'radius': r_hole
                    })

# Remove duplicates (holes appear twice - top and bottom of sheet)
unique_holes = []
for h in holes:
    is_dup = False
    for uh in unique_holes:
        if abs(h['center'][0] - uh['center'][0]) < 0.1 and abs(h['center'][1] - uh['center'][1]) < 0.1:
            is_dup = True
            break
    if not is_dup:
        unique_holes.append(h)

print(f"Found {len(unique_holes)} unique mounting holes")

# Create hole circles for DXF
hole_shapes = []
for h in unique_holes:
    cx, cy = h['center']
    # Transform coordinates: Y in model = Y in unfold, X depends on which panel
    if cx < main_w:  # on main panel
        circle = Part.makeCircle(h['radius'], V(cx, cy + main_l/2, 0))  # shift Y to center
        hole_shapes.append(circle)
    
# Compound all shapes
all_shapes = [outline, bend_line] + hole_shapes
compound = Part.makeCompound(all_shapes)

# Export DXF
compound.exportStep("unfold.step")
print("Exported unfold.step")

# For DXF we need to use importDXF
doc2 = FreeCAD.newDocument("Export")
obj = doc2.addObject("Part::Feature", "Unfold")
obj.Shape = compound
doc2.recompute()

try:
    importDXF.export([obj], "KLC-2-1.1-unfold.dxf")
    print("Exported KLC-2-1.1-unfold.dxf")
except Exception as e:
    print(f"DXF export error: {e}")
    # Fallback - export as STEP
    compound.exportStep("KLC-2-1.1-unfold.step")
    print("Exported as STEP instead")
