#!/usr/bin/env python3
"""
Extract flat pattern faces from STEP model using FreeCAD - v2
"""
import sys
sys.path.insert(0, "/Applications/FreeCAD.app/Contents/Resources/lib")

import FreeCAD
import Part
import Import

# File paths
step_file = "/Users/bond/.openclaw/workspace/everest-models/KLC-2-1.1.step"
output_dir = "/Users/bond/.openclaw/workspace/everest-models"

# Create new document
doc = FreeCAD.newDocument("Extract")
Import.insert(step_file, doc.Name)

# Find Part__Feature002 (the main panel 923x3030x309)
main_obj = None
for obj in doc.Objects:
    if obj.Name == "Part__Feature002":
        main_obj = obj
        break

if not main_obj:
    print("Part__Feature002 not found!")
    # List all shapes
    for obj in doc.Objects:
        if hasattr(obj, 'Shape') and obj.TypeId == "Part::Feature":
            bb = obj.Shape.BoundBox
            print(f"{obj.Name}: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm")
    sys.exit(1)

main_shape = main_obj.Shape
print(f"Selected: {main_obj.Name}")
print(f"Faces: {len(main_shape.Faces)}")
print(f"Volume: {main_shape.Volume:.0f} mm3")

bb = main_shape.BoundBox
print(f"Bounding box: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm")

# Find all planar faces
planar_faces = []
curved_faces = []

for i, face in enumerate(main_shape.Faces):
    surface_type = face.Surface.TypeId
    area = face.Area
    
    if "Plane" in surface_type:
        normal = face.Surface.Axis
        planar_faces.append((i, face, area, normal))
    elif "Cylinder" in surface_type:
        radius = face.Surface.Radius
        curved_faces.append((i, face, area, radius))

print(f"\nPlanar faces: {len(planar_faces)}")
print(f"Cylindrical faces (bends): {len(curved_faces)}")

# Categorize by normal direction
top_faces = []  # Z+ normal
bottom_faces = []  # Z- normal
side_faces = []  # X or Y normal

for i, face, area, normal in planar_faces:
    if abs(normal.z) > 0.9:
        if normal.z > 0:
            top_faces.append((i, face, area))
        else:
            bottom_faces.append((i, face, area))
    else:
        side_faces.append((i, face, area))

print(f"\nTop faces (Z+): {len(top_faces)}, Total area: {sum(a for _,_,a in top_faces):.0f} mm2")
print(f"Bottom faces (Z-): {len(bottom_faces)}, Total area: {sum(a for _,_,a in bottom_faces):.0f} mm2")
print(f"Side faces: {len(side_faces)}")

# Get bend radii
bend_radii = {}
for i, face, area, radius in curved_faces:
    r = round(radius, 1)
    bend_radii[r] = bend_radii.get(r, 0) + 1

print(f"\nBend radii:")
for r, count in sorted(bend_radii.items()):
    print(f"  R{r:.1f}: {count//2} bends")

# Export outline of all top faces
print(f"\nExporting outlines...")

# Collect outer edges
all_edges = []
for i, face, area in top_faces:
    if area > 100:  # Skip tiny faces
        for wire in face.Wires:
            for edge in wire.Edges:
                all_edges.append(edge)

print(f"Collected {len(all_edges)} edges from top faces")

# Make compound and export
if all_edges:
    compound = Part.makeCompound(all_edges)
    
    # Export BREP
    brep_file = f"{output_dir}/top_faces.brep"
    compound.exportBrep(brep_file)
    print(f"Exported: {brep_file}")
    
    # Export STEP
    step_out = f"{output_dir}/top_faces.step"
    compound.exportStep(step_out)
    print(f"Exported: {step_out}")

# Also export the whole main shape for reference
main_brep = f"{output_dir}/main_panel.brep"
main_shape.exportBrep(main_brep)
print(f"Exported: {main_brep}")

main_step = f"{output_dir}/main_panel.step"
main_shape.exportStep(main_step)
print(f"Exported: {main_step}")

FreeCAD.closeDocument(doc.Name)
print("\nDone!")
