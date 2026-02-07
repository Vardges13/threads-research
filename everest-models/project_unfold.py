import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD
import Part
import importDXF
from FreeCAD import Base
V = Base.Vector

doc = FreeCAD.newDocument("Project")
Part.insert("KLC-2-1.1-clean.step", "Project")
shape = doc.Objects[0].Shape

# Check all circles
print("=== ALL CIRCLES ===")
for i, edge in enumerate(shape.Edges):
    try:
        if edge.Curve.__class__.__name__ == 'Circle':
            c = edge.Curve
            print(f"Edge {i}: center ({c.Center.x:.1f}, {c.Center.y:.1f}, {c.Center.z:.1f}), R={c.Radius:.1f}, axis=({c.Axis.x:.2f},{c.Axis.y:.2f},{c.Axis.z:.2f})")
    except:
        pass

# Get top faces and project them
print("\n=== PROJECTING TOP FACES ===")

# Collect all faces with Z+ normal
top_face_shapes = []
for f in shape.Faces:
    if f.Surface.__class__.__name__ == 'Plane':
        normal = f.Surface.Axis
        if abs(normal.z - 1.0) < 0.01:  # Z+ normal
            # Get all wires (outer + inner holes)
            for wire in f.Wires:
                top_face_shapes.append(wire)

print(f"Found {len(top_face_shapes)} wires on top faces")

# Also get side face outline (for flange)
side_face_shapes = []
for f in shape.Faces:
    if f.Surface.__class__.__name__ == 'Plane':
        normal = f.Surface.Axis
        if abs(normal.x + 1.0) < 0.01:  # X- normal (side)
            for wire in f.Wires:
                side_face_shapes.append(wire)

print(f"Found {len(side_face_shapes)} wires on side faces")

# Create compound of top wires
if top_face_shapes:
    top_compound = Part.makeCompound(top_face_shapes)
    
    # Export top projection as DXF
    doc2 = FreeCAD.newDocument("TopDXF")
    obj = doc2.addObject("Part::Feature", "TopProjection")
    obj.Shape = top_compound
    doc2.recompute()
    
    importDXF.export([obj], "KLC-2-1.1-top-projection.dxf")
    print("Exported: KLC-2-1.1-top-projection.dxf")

# Create simple unfold
t = 2.0
r = 2.0
k = 0.4
ba = 3.14159 * (r + k*t) * 0.5

main_w = 916.8
main_l = 2993.8
flange_h = 305.9
total_w = main_w + flange_h + ba

# Simple outline + bend line
outline = Part.makePolygon([V(0,0,0), V(total_w,0,0), V(total_w,main_l,0), V(0,main_l,0), V(0,0,0)])
bend = Part.makeLine(V(main_w, 0, 0), V(main_w, main_l, 0))

doc3 = FreeCAD.newDocument("SimpleUnfold")
obj3 = doc3.addObject("Part::Feature", "Unfold")
obj3.Shape = Part.makeCompound([outline, bend])
doc3.recompute()

importDXF.export([obj3], "KLC-2-1.1-simple-unfold.dxf")
print(f"Exported: KLC-2-1.1-simple-unfold.dxf ({total_w:.0f} x {main_l:.0f} mm)")
