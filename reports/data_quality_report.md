# Data-quality report (M1)

Every number comes from our notebooks; the file is named in each section.

**Data:** LinkedIn Job Postings 2023-24, Kaggle version 13: `postings.csv` with 123,849 postings and 31 columns, plus 10 linked files.
**Our subset:** data and AI job titles -> 1,753 postings (579 with pay, 281 entry level). Filter and 50-title hand check (47 of 50 correct): `rija/rija_m1_joins_demand (3).ipynb`.

## 1. Missing values
Source: `quratulaain/Quratulain_m1_missing_duplicates (1).ipynb`, section 2.

| Column | % missing | Decision | Reason |
| --- | --- | --- | --- |
| `closed_time` | 99.1 | not used | |
| `skills_desc` | 98.0 | not used; skills come from `description` | |
| `med_salary` | 94.9 | not used; we use `normalized_salary` | |
| `remote_allowed` | 87.7 | empty counted as "not remote" | |
| `applies` | 81.2 | not used | |
| `min_salary`, `max_salary` | 75.9 | not used; we use `normalized_salary` | |
| `normalized_salary`, `currency`, `pay_period` | 70.9 | the salary model uses only postings with pay | |
| `formatted_experience_level` | 23.7 | filled with "Unknown" inside the model | |
| `description` | 0.0 (7 rows) | postings with an empty description dropped | |

## 2. Duplicates
Source: same notebook, section 4.
- Repeated `job_id`: 0. Fully identical rows: 0.
- Same title + company + description: 12,650 of 123,849 postings; 175 of our 1,753; 22 of the 574 pay rows.
- **Decision:** drop the repeats, keep the first one. **Reason:**

## 3. Inconsistent values
Source: same notebook, section 5.
- `work_type` and `formatted_work_type` hold the same 7 categories in two spellings. **Decision:** use `formatted_work_type` only. **Reason:**
- Titles: 1,977 have spaces at the ends and 450 have double spaces; 72,521 different titles become 71,580 after lower-casing and trimming. **Decision:** the title filter lower-cases every title before matching. **Reason:**
- Locations: 13,365 have no comma (for example "United States"). **Decision:** locations are used only for the state chart; postings without a state code stay out of that chart. **Reason:**

## 4. Outliers in pay
Source: `ahtisham/ahtisham_m1_salary_quality.ipynb`, section 2 (first filter) and `ahtisham/ahtisham_m2_baseline.ipynb`, section 3 (final filter).
- Every posting with pay in our subset is in USD. Yearly pay (`normalized_salary`) ranged from 45 to 6,900,400 USD.
- The lowest values (45, 60, 63.5, 75) are marked yearly but look like hourly numbers; the highest (6,900,400) comes from an hourly post with a typo (65 to 6,570 per hour).
- **Decision:** keep yearly pay between 15,000 and 500,000 USD. With the final filter this removes 5 rows: 579 postings with pay -> 574. **Reason:**

## 5. Cleaning rules in our M2 and M3 notebooks
1. Data/AI title filter (Rija's final word lists) -> 1,753 postings.
2. Drop repeated postings (same title + company + description), keep the first -> 1,578.
3. Rules and clusters: drop postings with an empty description (none in our subset).
4. Salary model only: USD yearly pay between 15,000 and 500,000, repeats dropped (552 postings), then 3 equal bands of 184.

## 6. Hypothesis test
Source: `ahtisham/ahtisham_m1_salary_quality.ipynb`, section 3 (first filter, 578 postings with pay).
- Remote against not remote data/AI jobs: median 138,150 against 140,000 USD, Mann-Whitney p = 0.34. **What it means:**
