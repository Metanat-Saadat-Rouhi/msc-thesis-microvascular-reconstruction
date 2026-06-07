"""
decimate_mesh.py
================
Run this script on YOUR OWN COMPUTER (where your .obj file is) to:
  1. Decimate your 10GB mesh to a web-friendly size
  2. Export it as vascular_data.json for the 3D viewer

Requirements (install once):
    pip install trimesh numpy

Usage:
    python decimate_mesh.py --input your_mesh.obj --output vascular_data.json

Options:
    --input       Path to your .obj / .ply / .stl file
    --output      Output JSON path (default: vascular_data.json)
    --target_mb   Target file size in MB (default: 5)
    --mode        'skeleton' for graph/skeleton data, 'mesh' for surface mesh
                  Use 'skeleton' if your mesh IS the vessel centreline graph.
                  Use 'mesh' if your mesh is the vessel surface.
"""

import argparse
import json
import numpy as np
import sys
import os

def estimate_target_faces(target_mb, bytes_per_face=80):
    return int((target_mb * 1024 * 1024) / bytes_per_face)

def decimate_and_export_mesh(input_path, output_path, target_mb=5):
    """
    For surface meshes (.obj with triangulated vessel walls).
    Decimates geometry and samples vertices/edges for the viewer.
    """
    try:
        import trimesh
    except ImportError:
        print("ERROR: trimesh not installed. Run: pip install trimesh")
        sys.exit(1)

    print(f"Loading mesh from: {input_path}")
    print("(This may take a few minutes for a 10GB file...)")

    mesh = trimesh.load(input_path, process=False)
    print(f"Loaded: {len(mesh.vertices):,} vertices, {len(mesh.faces):,} faces")

    # Estimate decimation ratio
    current_faces = len(mesh.faces)
    target_faces  = estimate_target_faces(target_mb)
    ratio = min(0.99, target_faces / max(1, current_faces))
    print(f"Decimating to {ratio*100:.1f}% of faces ({target_faces:,} target)...")

    decimated = mesh.simplify_quadric_decimation(target_faces)
    print(f"Decimated: {len(decimated.vertices):,} vertices, {len(decimated.faces):,} faces")

    # Extract skeleton-like structure from mesh:
    # sample vertices and build edges from face adjacency
    verts = decimated.vertices
    edges_raw = set()
    for face in decimated.faces:
        for i in range(3):
            a, b = int(face[i]), int(face[(i+1)%3])
            edges_raw.add((min(a,b), max(a,b)))

    # Estimate radius from local mesh density
    from scipy.spatial import cKDTree
    tree = cKDTree(verts)
    dists, _ = tree.query(verts, k=6)
    radii = dists[:, 1:].mean(axis=1)
    # normalise
    radii = radii / radii.max() * 2.0

    # Centre and normalise to [-5, 5] box
    verts = verts - verts.mean(axis=0)
    scale = np.abs(verts).max()
    verts = verts / scale * 5.0

    nodes = [{"id": int(i), "x": float(v[0]), "y": float(v[1]),
               "z": float(v[2]), "r": float(radii[i])}
             for i, v in enumerate(verts)]
    edges = [{"source": int(a), "target": int(b),
               "r": float((radii[a]+radii[b])/2)}
             for a, b in edges_raw]

    out = {
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "source": os.path.basename(input_path),
            "original_faces": current_faces,
            "decimated_faces": len(decimated.faces),
            "nodes": len(nodes),
            "edges": len(edges),
            "note": "Decimated surface mesh exported for web viewer"
        }
    }

    with open(output_path, 'w') as f:
        json.dump(out, f, separators=(',', ':'))

    size_mb = os.path.getsize(output_path) / (1024*1024)
    print(f"\nDone! Saved to: {output_path} ({size_mb:.1f} MB)")
    print(f"Nodes: {len(nodes):,} | Edges: {len(edges):,}")
    return size_mb


def export_skeleton(input_path, output_path, target_mb=5):
    """
    If your mesh IS already a skeleton/centreline (thin tubes representing
    vessel centre lines), use this mode for better results.
    Extracts the centreline graph directly.
    """
    try:
        import trimesh
    except ImportError:
        print("ERROR: trimesh not installed.")
        sys.exit(1)

    print(f"Loading skeleton mesh: {input_path}")
    mesh = trimesh.load(input_path, process=False)
    print(f"Vertices: {len(mesh.vertices):,}")

    # For skeleton: subsample vertices evenly
    max_nodes = estimate_target_faces(target_mb) // 3
    n = len(mesh.vertices)
    if n > max_nodes:
        idx = np.random.choice(n, max_nodes, replace=False)
        idx.sort()
        verts = mesh.vertices[idx]
        print(f"Subsampled to {len(verts):,} nodes")
    else:
        verts = mesh.vertices
        idx = np.arange(n)

    # Rebuild edges from original face structure
    old_to_new = {old: new for new, old in enumerate(idx)}
    edges_raw = set()
    for face in mesh.faces:
        mapped = [old_to_new.get(int(v)) for v in face]
        if all(m is not None for m in mapped):
            for i in range(3):
                a, b = mapped[i], mapped[(i+1)%3]
                edges_raw.add((min(a,b), max(a,b)))

    # Normalise
    verts = verts - verts.mean(axis=0)
    verts = verts / (np.abs(verts).max() + 1e-9) * 5.0

    nodes = [{"id": int(i), "x": float(v[0]), "y": float(v[1]),
              "z": float(v[2]), "r": 1.0}
             for i, v in enumerate(verts)]
    edges = [{"source": int(a), "target": int(b), "r": 1.0}
             for a, b in edges_raw]

    out = {"nodes": nodes, "edges": edges,
           "meta": {"source": os.path.basename(input_path),
                    "nodes": len(nodes), "edges": len(edges)}}

    with open(output_path, 'w') as f:
        json.dump(out, f, separators=(',', ':'))

    size_mb = os.path.getsize(output_path) / (1024*1024)
    print(f"Done! {output_path} ({size_mb:.1f} MB)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decimate mesh for web viewer')
    parser.add_argument('--input',  required=True, help='Input .obj/.ply/.stl file')
    parser.add_argument('--output', default='vascular_data.json', help='Output JSON')
    parser.add_argument('--target_mb', type=float, default=5.0,
                        help='Target JSON size in MB (default 5)')
    parser.add_argument('--mode', choices=['mesh', 'skeleton'], default='mesh',
                        help='mesh=surface mesh, skeleton=centreline graph')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: File not found: {args.input}")
        sys.exit(1)

    if args.mode == 'skeleton':
        export_skeleton(args.input, args.output, args.target_mb)
    else:
        decimate_and_export_mesh(args.input, args.output, args.target_mb)

    print("\nNext step: copy the output JSON to your viewer/ folder")
    print("Then open index.html in a browser to verify, then push to GitHub Pages.")
