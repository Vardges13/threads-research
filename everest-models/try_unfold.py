#!/usr/bin/env python3
"""
Try to unfold sheet metal using FreeCAD Sheet Metal workbench
"""
import sys
sys.path.insert(0, "/Applications/FreeCAD.app/Contents/Resources/lib")

import FreeCAD
import Part
import Import

# Check if SheetMetal workbench is available
try:
    import SheetMetalUnfoldCmd
    print("SheetMetal workbench available!")
    HAS_SHEETMETAL = True
except ImportError:
    print("SheetMetal workbench NOT available")
    print("Install it via: Tools > Addon Manager > Sheet Metal")
    HAS_SHEETMETAL = False

# Load main panel
step_file = "/Users/bond/.openclaw/workspace/everest-models/main_panel.step"
output_dir = "/Users/bond/.openclaw/workspace/everest-models"

doc = FreeCAD.newDocument("Unfold")
Import.insert(step_file, doc.Name)

# Get the shape
main_shape = None
for obj in doc.Objects:
    if hasattr(obj, 'Shape') and obj.Shape.Faces:
        main_shape = obj
        break

if main_shape:
    shape = main_shape.Shape
    print(f"Shape: {len(shape.Faces)} faces, {len(shape.Edges)} edges")
    
    # Find the largest flat face (likely the main surface)
    largest_face = None
    max_area = 0
    
    for i, face in enumerate(shape.Faces):
        if "Plane" in face.Surface.TypeId:
            area = face.Area
            if area > max_area:
                max_area = area
                largest_face = face
                largest_idx = i
    
    if largest_face:
        print(f"Largest flat face: #{largest_idx}, Area: {max_area:.0f} mm2")
        
        # Export this face as reference
        face_shape = Part.makeCompound([largest_face])
        face_step = f"{output_dir}/largest_face.step"
        face_shape.exportStep(face_step)
        print(f"Exported: {face_step}")
        
        # Get outline
        wires = largest_face.Wires
        print(f"Wires (outlines): {len(wires)}")
        
        # Export outline edges
        edges = []
        for wire in wires:
            for edge in wire.Edges:
                edges.append(edge)
        
        outline = Part.makeCompound(edges)
        outline_step = f"{output_dir}/outline.step"
        outline.exportStep(outline_step)
        print(f"Exported outline: {outline_step}")
        
        # Get bounding box of the face
        bb = largest_face.BoundBox
        print(f"Face bounds: {bb.XLength:.1f} x {bb.YLength:.1f} mm")

if HAS_SHEETMETAL:
    # Try actual unfolding
    print("\nAttempting unfold...")
    # This would require proper setup of the SheetMetal workbench
    pass

FreeCAD.closeDocument(doc.Name)
print("\nDone!")
