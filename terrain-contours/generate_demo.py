#!/usr/bin/env python3
"""Generate demo terrain points."""
import numpy as np
import csv

np.random.seed(42)
n = 500
x = np.random.uniform(0, 500, n)
y = np.random.uniform(0, 500, n)

# Hilly terrain 100-150m
z = (120
     + 15 * np.sin(x / 80) * np.cos(y / 100)
     + 10 * np.sin((x + y) / 60)
     + 5 * np.cos(x / 40) * np.sin(y / 50)
     + np.random.normal(0, 0.5, n))

z = np.clip(z, 100, 150)

with open('/Users/bond/.openclaw/workspace/terrain-contours/demo_points.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['X', 'Y', 'Z'])
    for i in range(n):
        w.writerow([f'{x[i]:.2f}', f'{y[i]:.2f}', f'{z[i]:.2f}'])

print(f"Generated {n} points, Z range: {z.min():.1f} - {z.max():.1f}")
