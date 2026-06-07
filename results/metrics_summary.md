# Quantitative Results Summary

## Primary Metrics

| Metric | Value | Notes |
|---|---|---|
| Network integration rate | **92.4 %** | Proportion of vessel segments successfully connected into the 3-D graph |
| Total vascular connections | **100,000+** | Edges in the reconstructed graph |
| Mean branching degree | **3.26** | Average number of connections per vessel node |
| Topological continuity | **Validated** | No isolated subgraphs in the main network body |

---

## Algorithm Performance vs. Baseline

| Method | Integration Rate |
|---|---|
| Naive nearest-neighbour matching | ~60 % |
| **KD-Tree Spatial-Vector Matching (this work)** | **92.4 %** |
| Manual annotation (reference) | ~98 % (estimated) |

The novel KD-Tree spatial-vector matching algorithm improves integration rate by ~32 percentage points over the naive baseline, approaching manual annotation quality while being fully automated and scalable.

---

## Segmentation Performance

| Metric | Value |
|---|---|
| 3-D U-Net Dice coefficient | to be reported at submission |
| Precision | to be reported at submission |
| Recall | to be reported at submission |

*Full segmentation metrics will be added upon thesis submission (September 2026).*

---

## Computational Performance

| Stage | Time (single tissue block, ~50 sections) |
|---|---|
| Image ingestion + tiling | ~20 min |
| 3-D U-Net segmentation (multi-GPU) | ~90 min |
| KD-Tree matching | ~10 min |
| Graph construction + validation | ~15 min |
| **Total** | **~2.5 hrs** |

*vs. estimated 4–6 months for equivalent manual annotation.*

---

## Graph-Theoretic Validation

The reconstructed network was validated as a biologically plausible vascular graph:

- **Branching degree 3.26** — consistent with histological literature values for cortical microvasculature (expected range: 3.0–3.5)
- **Degree distribution** — follows expected power-law-like distribution for biological vascular networks
- **No self-loops** — graph is a valid directed acyclic structure in the main network body
- **Connectivity** — single connected component accounts for > 95 % of all nodes
