#!/usr/bin/env python3
"""
Extract flat pattern faces from STEP model using FreeCAD
"""
import sys
sys.path.insert(0, "/Applications/FreeCAD.app/Contents/Resources/lib")

import FreeCAD
import Part
import Import
import importDXF

# File paths
step_file = "/Users/bond/.openclaw/workspace/everest-models/KLC-2-1.1.step"
output_dir = "/Users/bond/.openclaw/workspace/everest-models"

# Create new document
doc = FreeCAD.newDocument("Extract")
Import.insert(step_file, doc.Name)

# Find main panel (Part__Feature002 - the largest one)
main_shape = None
max_volume = 0

for obj in doc.Objects:
    if hasattr(obj, 'Shape') and obj.Shape.Faces:
        vol = obj.Shape.Volume
        if vol > max_volume:
            max_volume = vol
            main_shape = obj.Shape
            print(f"Largest shape: {obj.Name}, Volume: {vol:.0f} mm3")

if main_shape:
    # Find all flat faces (planar with normal in Z direction)
    flat_faces = []
    top_faces = []
    
    for i, face in enumerate(main_shape.Faces):
        if face.Surface.TypeId == "Part::GeomPlane":
            normal = face.Surface.Axis
            # Check if face is horizontal (normal along Z)
            if abs(normal.z) > 0.99:
                area = face.Area
                if area > 1000:  # Skip small faces
                    flat_faces.append((i, face, area))
                    print(f"Flat face {i}: Area={area:.0f} mm2, Z-normal={normal.z:.2f}")
    
    # Sort by area descending
    flat_faces.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\nTotal flat faces: {len(flat_faces)}")
    
    # Export top 5 largest flat faces as DXF
    if flat_faces:
        # Create compound of flat faces edges
        edges = []
        for i, face, area in flat_faces[:5]:
            for edge in face.Edges:
                edges.append(edge)
        
        # Make compound
        compound = Part.makeCompound(edges)
        
        # Export as DXF
        dxf_file = f"{output_dir}/flat_faces.dxf"
        try:
            import importDXF
            importDXF.export([compound], dxf_file)
            print(f"\nExported DXF: {dxf_file}")
        except Exception as e:
            print(f"DXF export error: {e}")
            # Try SVG instead
            try:
                import importSVG
                svg_file = f"{output_dir}/flat_faces.svg"
                importSVG.export([compound], svg_file)
                print(f"Exported SVG: {svg_file}")
            except Exception as e2:
                print(f"SVG export error: {e2}")

    # Also export the bounding outline
    print("\nBounding box of main shape:")
    bb = main_shape.BoundBox
    print(f"  X: {bb.XMin:.1f} to {bb.XMax:.1f} ({bb.XLength:.1f} mm)")
    print(f"  Y: {bb.YMin:.1f} to {bb.YMax:.1f} ({bb.YLength:.1f} mm)")
    print(f"  Z: {bb.ZMin:.1f} to {bb.ZMax:.1f} ({bb.ZLength:.1f} mm)")

FreeCAD.closeDocument(doc.Name)
print("\nDone!")
