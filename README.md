# AI Job-Market Skill Miner (P08)

Data Mining course project, Fall 2026.

## Question
What skills do data and AI job postings ask for, how do they group into job families, and how do they relate to disclosed pay? Each question also reports entry-level postings separately.

| Question | Owner | Method |
| --- | --- | --- |
| Which skills appear together, and which are most common? | Quratulain Afzal | Association rules (FP-Growth) |
| What job families exist? | Rija Faisal | Clustering (TF-IDF + k-means) |
| Can job details predict a disclosed salary band? | Ahtisham Ul Hassan (lead) | Classification (decision tree, random forest) |

## Data
LinkedIn Job Postings (2023 - 2024) by Arsh Koneru on Kaggle, **version 13**, license **CC BY-SA 4.0**:
https://www.kaggle.com/datasets/arshkon/linkedin-job-postings

123,849 postings, 31 columns in `postings.csv`, plus 10 related files. Source details, file list and the current accepted data version are in [`DATA_MANIFEST.md`](DATA_MANIFEST.md).

📁 **Team Google Drive workspace:** [Access Google Drive Folder](https://drive.google.com/drive/folders/181-Vo21XPKPlllpRPqDeAvGqK6fnKV3Y?usp=share_link)

## How to start
1. In Google Drive, open "Shared with me", right-click the team folder, and choose Organize → Add shortcut → My Drive (once per person).
2. [Open the loader in Colab](https://colab.research.google.com/github/AHTISHAM327/ai-job-market-skill-miner/blob/main/ahtisham/ahtisham_00_load_drive.ipynb) and choose Runtime → Run all. It loads the pinned version 13 from the team Drive copy and prints the first checks.

`notebooks/01_data_start.ipynb` is only the Kaggle backup. It downloads version 13 again from Kaggle and needs a Kaggle key in Colab Secrets. Use it only if the Drive copy is damaged.
## Rules
- No raw data, processed data, passwords or Kaggle keys in this repo. Data lives in the shared Drive (`data/raw`, `data/processed`).
- Raw data is never edited; cleaned data is saved as a new numbered version (v001, v002, ...).
- Everyone works from the version marked current in `DATA_MANIFEST.md`.

## Structure
- `notebooks/`: Colab notebooks
- `reports/`: proposal, question-to-column map, field profile, data dictionary, cleaning log, meeting notes
- `ahtisham/`, `quratulaain/`, `rija/`: personal workspaces
- `data/`: folder layout only; data files are blocked by `.gitignore`

## Dates
M0 proposal 14 Oct · M1 21 Oct · M2 28 Oct · internal finish 10 Dec
