# HPC Environment & Slurm Configuration

## Cluster

**System:** Pleiades HPC Cluster — Forschungszentrum Jülich  
**Architecture:** Multi-node, multi-GPU setup  
**Scheduler:** Slurm Workload Manager

---

## GPU Training Setup

- **Framework:** PyTorch with DistributedDataParallel (DDP)
- **Parallelisation:** Data-parallel training across multiple GPUs on multiple nodes
- **Precision:** Mixed precision (FP16) training for memory efficiency
- **Batch strategy:** Patch-based training on 3-D image volumes to handle gigapixel data

---

## Typical Slurm Job Configuration

```bash
#!/bin/bash
#SBATCH --job-name=unet3d_train
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --gres=gpu:4
#SBATCH --time=24:00:00
#SBATCH --partition=gpus
#SBATCH --output=logs/train_%j.out

module load Python/3.10
module load CUDA/11.8
module load PyTorch/2.0

srun python train.py \
    --data_path /path/to/data \
    --output_path /path/to/output \
    --batch_size 4 \
    --epochs 100
```

---

## Memory Management Strategy

Gigapixel images cannot be loaded into GPU memory directly. The pipeline uses:

1. **Tiled loading** — images are divided into overlapping tiles at ingestion
2. **Overlap handling** — tile borders include a margin to avoid edge artefacts in segmentation
3. **Streaming inference** — tiles are processed sequentially with result stitching
4. **Checkpoint saving** — intermediate results saved to disk after each section to allow resumption

---

## Scaling Notes

| Dataset size | Wall time | Nodes used |
|---|---|---|
| Single tissue section (1 slide) | ~15 min | 1 node, 1 GPU |
| Full tissue block (50 sections) | ~3 hrs | 2 nodes, 8 GPUs |
| Large cohort (200+ sections) | ~12 hrs | 4 nodes, 16 GPUs |

*Times are approximate and depend on image resolution and cluster load.*
