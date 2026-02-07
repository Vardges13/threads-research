#!/usr/bin/env python3
"""
Convert extracted faces to DXF using ezdxf
"""
import sys
sys.path.insert(0, "/Applications/FreeCAD.app/Contents/Resources/lib")

import FreeCAD
import Part
import math

# Load the top faces
brep_file = "/Users/bond/.openclaw/workspace/everest-models/top_faces.brep"
output_dxf = "/Users/bond/.openclaw/workspace/everest-models/top_faces.dxf"

# Read BREP
shape = Part.Shape()
shape.read(brep_file)

print(f"Loaded shape: {len(shape.Edges)} edges")

# Get all edge coordinates
edges_data = []
for edge in shape.Edges:
    try:
        # Get edge type
        curve = edge.Curve
        curve_type = curve.TypeId
        
        if "Line" in curve_type:
            # Straight line
            p1 = edge.Vertexes[0].Point
            p2 = edge.Vertexes[1].Point
            edges_data.append(("LINE", (p1.x, p1.y), (p2.x, p2.y)))
        elif "Circle" in curve_type or "Arc" in curve_type:
            # Arc or circle
            center = curve.Center
            radius = curve.Radius
            # Get start/end angles
            fp = edge.FirstParameter
            lp = edge.LastParameter
            start_angle = math.degrees(fp)
            end_angle = math.degrees(lp)
            edges_data.append(("ARC", (center.x, center.y), radius, start_angle, end_angle))
        elif "BSpline" in curve_type:
            # Approximate as polyline
            points = []
            for i in range(21):  # 20 segments
                param = edge.FirstParameter + (edge.LastParameter - edge.FirstParameter) * i / 20
                pt = edge.valueAt(param)
                points.append((pt.x, pt.y))
            edges_data.append(("POLYLINE", points))
        else:
            print(f"Unknown curve type: {curve_type}")
    except Exception as e:
        print(f"Edge error: {e}")

print(f"Processed {len(edges_data)} edges")

# Now use ezdxf to create DXF
try:
    import ezdxf
    print("ezdxf loaded")
    
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    for item in edges_data:
        if item[0] == "LINE":
            msp.add_line(item[1], item[2])
        elif item[0] == "ARC":
            _, center, radius, start, end = item
            msp.add_arc(center, radius, start, end)
        elif item[0] == "POLYLINE":
            points = item[1]
            msp.add_lwpolyline(points)
    
    doc.saveas(output_dxf)
    print(f"Saved: {output_dxf}")
    
except ImportError:
    print("ezdxf not available in FreeCAD environment")
    # Export coordinates as text
    with open("/Users/bond/.openclaw/workspace/everest-models/edges.txt", "w") as f:
        for item in edges_data:
            f.write(str(item) + "\n")
    print("Exported edge data to edges.txt")

print("Done!")
