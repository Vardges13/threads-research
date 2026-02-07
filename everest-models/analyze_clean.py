import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD
import Part

doc = FreeCAD.newDocument("Clean")
Part.insert("KLC-2-1.1-clean.step", "Clean")

print("=== FILE STRUCTURE ===")
for obj in doc.Objects:
    print(f"\nObject: {obj.Name}")
    if hasattr(obj, 'Shape'):
        shape = obj.Shape
        print(f"  Type: {shape.ShapeType}")
        bb = shape.BoundBox
        print(f"  BoundBox: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm")
        
        if shape.ShapeType == 'Compound':
            solids = shape.Solids
            print(f"  Solids: {len(solids)}")
            for i, solid in enumerate(solids):
                sbb = solid.BoundBox
                print(f"    [{i}] {sbb.XLength:.1f} x {sbb.YLength:.1f} x {sbb.ZLength:.1f} mm")
                print(f"        Faces: {len(solid.Faces)}, Edges: {len(solid.Edges)}")
        elif shape.ShapeType == 'Solid':
            print(f"  Faces: {len(shape.Faces)}")
            print(f"  Edges: {len(shape.Edges)}")
        
        # Analyze bends (cylindrical faces)
        faces = shape.Faces if hasattr(shape, 'Faces') else []
        bends = []
        for f in faces:
            surf_type = f.Surface.__class__.__name__
            if surf_type == 'Cylinder':
                r = f.Surface.Radius
                bends.append(r)
        
        if bends:
            from collections import Counter
            bend_counts = Counter([round(r, 2) for r in bends])
            print(f"\n  BENDS (cylinders): {len(bends)} total")
            for radius, count in sorted(bend_counts.items()):
                print(f"    R{radius} mm: {count} pcs")
