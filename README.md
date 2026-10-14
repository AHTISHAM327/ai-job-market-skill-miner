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
Open [`notebooks/01_data_start.ipynb`](notebooks/01_data_start.ipynb) in Colab and choose Runtime → Run all. It downloads the pinned version 13 and prints the file list and first checks.

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
