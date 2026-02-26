#!/usr/bin/env python3
"""
Terrain Contour Generator
Reads XYZ point cloud from CSV, builds TIN, generates contour lines,
exports to DXF and PNG.
"""

import argparse
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
import ezdxf


def read_csv(path):
    """Read X, Y, Z from CSV."""
    x, y, z = [], [], []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            x.append(float(row['X']))
            y.append(float(row['Y']))
            z.append(float(row['Z']))
    return np.array(x), np.array(y), np.array(z)


def build_contours(x, y, z, step):
    """Build contour lines using matplotlib triangulation."""
    triang = mtri.Triangulation(x, y)
    
    # Also build scipy Delaunay for stats
    points = np.column_stack([x, y])
    delaunay = Delaunay(points)
    
    z_min = np.floor(z.min() / step) * step
    z_max = np.ceil(z.max() / step) * step
    levels = np.arange(z_min, z_max + step, step)
    
    fig_tmp, ax_tmp = plt.subplots()
    cs = ax_tmp.tricontour(triang, z, levels=levels)
    plt.close(fig_tmp)
    
    contours = []
    for i, level in enumerate(cs.levels):
        for seg in cs.allsegs[i]:
            if len(seg) >= 2:
                contours.append((float(level), seg))
    
    return contours, triang, delaunay, levels


def export_dxf(contours, output_path):
    """Export contour lines to DXF."""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Create layers
    doc.layers.add('CONTOURS', color=3)  # green
    doc.layers.add('LABELS', color=7)    # white
    
    for level, seg in contours:
        points = [(p[0], p[1]) for p in seg]
        msp.add_lwpolyline(points, dxfattribs={'layer': 'CONTOURS'})
        
        # Add height label at midpoint
        mid = len(seg) // 2
        mx, my = seg[mid]
        msp.add_text(
            f'{level:.1f}',
            height=2.0,
            dxfattribs={
                'layer': 'LABELS',
                'insert': (mx, my),
            }
        )
    
    doc.saveas(output_path)


def export_png(x, y, z, triang, levels, contours, png_path):
    """Save PNG visualization."""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Filled contours
    tcf = ax.tricontourf(triang, z, levels=levels, cmap='terrain')
    plt.colorbar(tcf, ax=ax, label='Высота, м')
    
    # Contour lines
    tc = ax.tricontour(triang, z, levels=levels, colors='black', linewidths=0.5)
    ax.clabel(tc, inline=True, fontsize=7, fmt='%.1f')
    
    # Points
    ax.scatter(x, y, s=1, c='red', alpha=0.3, zorder=5)
    
    ax.set_xlabel('X, м')
    ax.set_ylabel('Y, м')
    ax.set_title('Горизонтали рельефа')
    ax.set_aspect('equal')
    
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Terrain contour generator')
    parser.add_argument('--input', required=True, help='CSV file (X,Y,Z)')
    parser.add_argument('--output', default='output.dxf', help='Output DXF')
    parser.add_argument('--step', type=float, default=1.0, help='Contour interval (m)')
    parser.add_argument('--png', default='preview.png', help='PNG preview')
    args = parser.parse_args()
    
    print(f'Reading {args.input}...')
    x, y, z = read_csv(args.input)
    print(f'  Points: {len(x)}')
    print(f'  Z range: {z.min():.1f} — {z.max():.1f} m')
    
    print(f'Building contours (step={args.step}m)...')
    contours, triang, delaunay, levels = build_contours(x, y, z, args.step)
    print(f'  Triangles: {len(delaunay.simplices)}')
    print(f'  Contour levels: {len(levels)}')
    print(f'  Contour lines: {len(contours)}')
    
    print(f'Exporting DXF → {args.output}')
    export_dxf(contours, args.output)
    
    print(f'Exporting PNG → {args.png}')
    export_png(x, y, z, triang, levels, contours, args.png)
    
    # Validate DXF
    doc = ezdxf.readfile(args.output)
    entities = list(doc.modelspace())
    print(f'  DXF entities: {len(entities)} (valid ✓)')
    
    print('Done! ✅')


if __name__ == '__main__':
    main()
