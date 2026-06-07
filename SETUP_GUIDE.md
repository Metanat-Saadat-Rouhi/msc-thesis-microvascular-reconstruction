# GitHub Repository Setup Guide
## Step-by-step: how to publish your thesis repo

---

### Step 1 — Create the repository on GitHub

1. Go to **github.com** and log in
2. Click the **+** button (top right) → **New repository**
3. Fill in:
   - **Repository name:** `msc-thesis-microvascular-reconstruction`
   - **Description:** `HPC-accelerated 3-D reconstruction of large-scale microvascular networks from gigapixel histological data — M.Sc. Thesis`
   - **Visibility:** ✅ **Public**
   - Do NOT initialise with README (you already have one)
4. Click **Create repository**

---

### Step 2 — Upload the files

You have two options:

#### Option A — Upload via GitHub website (easiest, no terminal needed)

1. On your new empty repo page, click **uploading an existing file**
2. Drag and drop ALL files from the folder you downloaded
3. Keep the folder structure:
   ```
   README.md
   assets/pipeline_diagram.png
   assets/pipeline_diagram.svg
   assets/results_overview.png
   results/metrics_summary.md
   docs/algorithm_description.md
   docs/hpc_setup.md
   ```
4. Write commit message: `Initial upload — thesis results and pipeline documentation`
5. Click **Commit changes**

> ⚠️ GitHub's web uploader cannot create subfolders automatically.  
> Upload files in each subfolder separately:  
> - First upload `README.md` to the root  
> - Then go into `assets/` folder (create it by typing `assets/` before the filename)  
> - Repeat for `results/` and `docs/`

#### Option B — via Git terminal (cleaner)

```bash
# In terminal, navigate to the folder containing these files
cd path/to/thesis_repo

git init
git add .
git commit -m "Initial upload — thesis results and pipeline documentation"
git branch -M main
git remote add origin https://github.com/Metanat-Saadat-Rouhi/msc-thesis-microvascular-reconstruction.git
git push -u origin main
```

---

### Step 3 — Pin the repo to your GitHub profile

1. Go to your GitHub profile page: **github.com/Metanat-Saadat-Rouhi**
2. Click **Customize your pins**
3. Check **msc-thesis-microvascular-reconstruction**
4. Click **Save pins**

This makes the thesis repo the first thing anyone sees when they visit your profile.

---

### Step 4 — Add a profile README (optional but recommended)

1. Create a new repo named exactly **Metanat-Saadat-Rouhi** (same as your username)
2. Create a `README.md` inside it with a short bio:

```markdown
## Matanat Saadat Rouhi

ML Engineer · Medical Imaging · Computer Vision · HPC

- 🔬 M.Sc. Computer Simulation in Science (Bergische Universität Wuppertal, Sep 2026)
- 🏥 Python Developer @ Forschungszentrum Jülich, INM-1
- 🧠 Thesis: HPC-accelerated 3-D microvascular reconstruction from gigapixel histological data
- 📍 Wuppertal, Germany · Available immediately
- 📧 metanat.saadat@gmail.com
```

---

### Step 5 — Update your CV and LinkedIn

Once the repo is live, update:

**In your LaTeX CV** — change the thesis GitHub link from the general profile URL to the direct repo:
```
https://github.com/Metanat-Saadat-Rouhi/msc-thesis-microvascular-reconstruction
```

**On LinkedIn** — go to your profile → Add section → Projects → Add the thesis as a project with the GitHub link and key results numbers.

---

### Step 6 — Add your result images (when ready)

When your thesis is submitted (September 2026), replace the placeholder note in the README with actual result images. To add an image:

1. Save your figure as `results_3d_network.png` in the `assets/` folder
2. In `README.md`, change:
   ```markdown
   > **Note on visualisations:** result images will be added upon thesis submission
   ```
   to:
   ```markdown
   ![3D Network Result](assets/results_3d_network.png)
   *Figure: Reconstructed 3-D vascular network — 100,000+ connections*
   ```

---

### What the repo looks like to a recruiter

When a recruiter or PhD supervisor clicks your GitHub link they will see:

1. ✅ A clear, professional README with the problem/solution/results framing
2. ✅ A pipeline diagram showing you understand system design
3. ✅ Quantitative results front and centre (92.4%, 100k+)
4. ✅ Clinical relevance explained in plain language
5. ✅ Detailed algorithm description showing depth of contribution
6. ✅ HPC setup notes showing real infrastructure experience
7. ✅ Code available on request — no IP issues, no risk

This is the difference between a repo that gets ignored and one that gets you an interview.
