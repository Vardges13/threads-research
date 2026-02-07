#!/usr/bin/env python3
"""
FreeCAD script to import STEP and attempt to unfold sheet metal
"""
import sys
import os

# Add FreeCAD to path
freecad_path = "/Applications/FreeCAD.app/Contents/Resources/lib"
sys.path.insert(0, freecad_path)

try:
    import FreeCAD
    import Part
    import Import
    print("FreeCAD loaded successfully")
    print(f"Version: {FreeCAD.Version()}")
except ImportError as e:
    print(f"Failed to import FreeCAD: {e}")
    sys.exit(1)

# File paths
step_file = "/Users/bond/.openclaw/workspace/everest-models/KLC-2-1.1.step"
output_dir = "/Users/bond/.openclaw/workspace/everest-models"

# Create new document
doc = FreeCAD.newDocument("Unfold")

# Import STEP
print(f"Importing: {step_file}")
Import.insert(step_file, doc.Name)

# Get shapes
shapes = []
for obj in doc.Objects:
    if hasattr(obj, 'Shape'):
        shapes.append(obj)
        print(f"Found shape: {obj.Name}, Type: {obj.TypeId}")

print(f"\nTotal shapes: {len(shapes)}")

# Print bounding box
for obj in shapes[:5]:
    bb = obj.Shape.BoundBox
    print(f"{obj.Name}: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm")

# Try to find sheet metal body
for obj in shapes:
    shape = obj.Shape
    print(f"\n{obj.Name}:")
    print(f"  Faces: {len(shape.Faces)}")
    print(f"  Edges: {len(shape.Edges)}")
    
# Save as BREP for further analysis
brep_file = os.path.join(output_dir, "model.brep")
if shapes:
    shapes[0].Shape.exportBrep(brep_file)
    print(f"\nExported BREP: {brep_file}")

FreeCAD.closeDocument(doc.Name)
print("\nDone!")
