# KD-Tree Spatial-Vector Matching Algorithm

## Overview

The inter-slice gap bridging algorithm is the core methodological contribution of this thesis. It solves the problem of connecting vessel segments across the 50 µm gaps between consecutive histological sections — a step where naive approaches fail due to vessel orientation changes between slices.

---

## The Problem in Detail

After 3-D U-Net segmentation, each histological section yields a set of detected vessel cross-sections. To reconstruct a continuous 3-D network, corresponding cross-sections in adjacent slices must be matched and connected.

**Why nearest-neighbour fails:**
- Vessels are not always perpendicular to the cutting plane — oblique vessels shift laterally between slices
- Dense capillary beds create many nearby candidates — proximity alone is ambiguous
- Branching points create one-to-many relationships that nearest-neighbour cannot handle

---

## Algorithm Design

### Step 1: Endpoint Extraction
For each segmented vessel region in slice *n*, compute:
- Centroid position `(x, y, z)`
- Local orientation vector `v` from the principal axis of the region

### Step 2: Candidate Search via KD-Tree
Build a KD-Tree from all vessel centroids in slice *n+1*.  
For each centroid in slice *n*, query the KD-Tree for all candidates within radius `r`:

```
r = base_radius + orientation_correction_factor × |sin(θ)|
```

where `θ` is the estimated vessel angle to the cutting plane.  
This adaptive radius compensates for lateral displacement in oblique vessels.

### Step 3: Orientation Consistency Filtering
For each candidate pair `(A in slice n, B in slice n+1)`:

```
score = α × spatial_score + β × orientation_score

spatial_score    = 1 - (dist(A,B) / r)
orientation_score = |dot(v_A, v_B)|   # cosine similarity of direction vectors
```

Pairs below a combined threshold are rejected.

### Step 4: Global Assignment
Build a bipartite graph of (slice n endpoints) vs (slice n+1 endpoints) with edge weights = match scores.  
Solve the assignment problem to find the globally optimal non-conflicting matching — preventing one vessel from being connected to multiple candidates.

### Step 5: Graph Integration
Accepted matches become edges in the growing 3-D vascular graph.  
Unmatched endpoints (vessel starts/ends, branching points at tissue edges) are flagged as terminal nodes.

---

## Validation

The resulting graph was validated by:
- **Integration rate:** proportion of segments successfully matched (achieved: **92.4 %**)
- **Branching degree distribution:** compared against known histological reference values (result: **3.26**, consistent with literature)
- **Connectivity analysis:** no isolated subgraphs in the main network body
- **Visual inspection:** random sample of 200 matched pairs confirmed by manual review

---

## Parameters

| Parameter | Value | Description |
|---|---|---|
| `base_radius` | 45 µm | Spatial search radius |
| `α` (spatial weight) | 0.4 | Weight for distance score |
| `β` (orientation weight) | 0.6 | Weight for vector alignment |
| `min_score` | 0.55 | Rejection threshold |

Parameters were tuned on a held-out validation set of manually annotated tissue sections.
