import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD
import Part
import DraftGeomUtils

doc = FreeCAD.newDocument("Unfold")
Part.insert("KLC-2-1.1-clean.step", "Unfold")
shape = doc.Objects[0].Shape

# Get the two largest top faces (normal Z+)
top_faces = []
for i, f in enumerate(shape.Faces):
    if f.Surface.__class__.__name__ == 'Plane':
        normal = f.Surface.Axis
        if abs(normal.z - 1.0) < 0.01:  # Z+ normal
            top_faces.append((i, f, f.Area))

top_faces.sort(key=lambda x: -x[2])
print(f"Top 2 faces: {top_faces[0][0]} ({top_faces[0][2]/1e6:.4f} m2), {top_faces[1][0]} ({top_faces[1][2]/1e6:.4f} m2)")

# Get outer wires of main faces
face1 = shape.Faces[top_faces[0][0]]
face2 = shape.Faces[top_faces[1][0]]

wire1 = face1.OuterWire
wire2 = face2.OuterWire

print(f"Face1 outer wire: {len(wire1.Edges)} edges")
print(f"Face2 outer wire: {len(wire2.Edges)} edges")

# Export as compound
compound = Part.makeCompound([wire1, wire2])
compound.exportStep("top_wires.step")
print("Exported top_wires.step")

# Get side faces (normal X-)
side_faces = []
for i, f in enumerate(shape.Faces):
    if f.Surface.__class__.__name__ == 'Plane':
        normal = f.Surface.Axis
        if abs(normal.x + 1.0) < 0.01:  # X- normal
            side_faces.append((i, f, f.Area))

side_faces.sort(key=lambda x: -x[2])
print(f"\nTop 2 side faces: {side_faces[0][0]} ({side_faces[0][2]/1e6:.4f} m2), {side_faces[1][0]} ({side_faces[1][2]/1e6:.4f} m2)")

# Calculate unfold dimensions
# For L-shaped cassette: main panel + side flange
# Thickness = 2mm, main bend radius = 2.0mm

# Neutral axis for bending: k * t where k ~ 0.4 for sheet metal
t = 2.0  # thickness mm
k = 0.4
r = 2.0  # main bend radius

# Bend allowance = pi * (r + k*t) * (angle/180)
# For 90 degree bend:
ba_90 = 3.14159 * (r + k*t) * (90/180)
print(f"\nBend allowance for 90 deg (R{r}, t{t}): {ba_90:.2f} mm")

# Get bounding boxes
bb1 = face1.BoundBox
bb2 = face2.BoundBox
side_bb = shape.Faces[side_faces[0][0]].BoundBox

print(f"\nFace1 BB: X[{bb1.XMin:.1f}, {bb1.XMax:.1f}], Y[{bb1.YMin:.1f}, {bb1.YMax:.1f}]")
print(f"Face2 BB: X[{bb2.XMin:.1f}, {bb2.XMax:.1f}], Y[{bb2.YMin:.1f}, {bb2.YMax:.1f}]")
print(f"Side BB: Y[{side_bb.YMin:.1f}, {side_bb.YMax:.1f}], Z[{side_bb.ZMin:.1f}, {side_bb.ZMax:.1f}]")

# Estimate unfold size
# Main panel width (X direction)
main_width = bb1.XMax - bb1.XMin
# Main panel length (Y direction) 
main_length = max(bb1.YMax, bb2.YMax) - min(bb1.YMin, bb2.YMin)
# Side flange height (Z direction)
side_height = side_bb.ZMax - side_bb.ZMin

print(f"\n=== ESTIMATED UNFOLD ===")
print(f"Main panel: {main_width:.1f} x {main_length:.1f} mm")
print(f"Side flange: {side_height:.1f} mm height")
print(f"Total unfold width (with bend allowance): {main_width + side_height + ba_90:.1f} mm")
print(f"Total unfold length: {main_length:.1f} mm")
