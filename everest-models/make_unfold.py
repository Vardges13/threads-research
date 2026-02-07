import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD
import Part

doc = FreeCAD.newDocument("Unfold")
Part.insert("KLC-2-1.1-clean.step", "Unfold")

shape = doc.Objects[0].Shape

# Find all planar faces and their normals
planar_faces = []
for i, f in enumerate(shape.Faces):
    if f.Surface.__class__.__name__ == 'Plane':
        normal = f.Surface.Axis
        area = f.Area
        center = f.CenterOfMass
        planar_faces.append({
            'index': i,
            'area': area,
            'normal': (round(normal.x, 3), round(normal.y, 3), round(normal.z, 3)),
            'center': center
        })

# Group by normal direction
from collections import defaultdict
by_normal = defaultdict(list)
for pf in planar_faces:
    by_normal[pf['normal']].append(pf)

print("=== PLANAR FACES BY NORMAL ===")
for normal, faces in sorted(by_normal.items(), key=lambda x: -sum(f['area'] for f in x[1])):
    total_area = sum(f['area'] for f in faces)
    print(f"\nNormal {normal}: {len(faces)} faces, total area {total_area/1e6:.4f} m2")
    # Show top 3 largest
    top_faces = sorted(faces, key=lambda x: -x['area'])[:3]
    for f in top_faces:
        print(f"  Face {f['index']}: {f['area']/1e6:.6f} m2")

# Export largest flat face for each main direction
print("\n=== EXPORTING MAIN FACES ===")

# Find the largest face (main panel)
largest = max(planar_faces, key=lambda x: x['area'])
print(f"Largest face: index {largest['index']}, area {largest['area']/1e6:.4f} m2")
print(f"  Normal: {largest['normal']}")

# Export outline of the solid projected onto XY plane
from FreeCAD import Base
projection_dir = Base.Vector(0, 0, 1)

# Get bounding box outline
bb = shape.BoundBox
print(f"\nBounding box: X[{bb.XMin:.1f}, {bb.XMax:.1f}], Y[{bb.YMin:.1f}, {bb.YMax:.1f}], Z[{bb.ZMin:.1f}, {bb.ZMax:.1f}]")
