# Dataset Notes: LinkedIn Job Postings (2023 - 2024)

| | |
|---|---|
| **Dataset** | LinkedIn Job Postings (2023 - 2024) |
| **Author** | Arsh Koneru (`arshkon/linkedin-job-postings`) |
| **Source** | https://www.kaggle.com/datasets/arshkon/linkedin-job-postings |
| **Total files** | 11 CSV files in 3 folders + 1 root file |
| **Prepared by** | Rija |
| **Purpose** | Dataset check: why 11 files, null values in main columns, and which files connect through which ID |

> **Note on figures:** Row counts, file sizes and null percentages below are approximate. Run the verification script in Section 7 on your downloaded copy to get exact values before presenting.

---

## 1. Why There Are 11 Files

The dataset is a **normalized relational structure** (like a small database), not one flat table. A single job can have many skills, many benefits and many industries, and a single company can post hundreds of jobs. Putting all of that in one file would repeat the same values over and over. Splitting it into tables stores each fact once and links tables through ID columns.

| Folder | Files | Count |
|---|---|---|
| root | `postings.csv` | 1 |
| `jobs/` | `benefits.csv`, `job_industries.csv`, `job_skills.csv`, `salaries.csv` | 4 |
| `companies/` | `companies.csv`, `company_industries.csv`, `company_specialities.csv`, `employee_counts.csv` | 4 |
| `mappings/` | `industries.csv`, `skills.csv` | 2 |
| | **Total** | **11** |

Benefits of this design:

- No duplicated company addresses or descriptions across thousands of job rows.
- Smaller storage footprint and cleaner data.
- Analysts join only the tables they need.

---

## 2. File Overview

| # | File | Columns | Approx. rows | Granularity (one row = ...) |
|---|---|---|---|---|
| 1 | `postings.csv` | 31 | ~124,000 | one job posting |
| 2 | `jobs/benefits.csv` | 3 | ~68,000 | one benefit of one job |
| 3 | `jobs/job_industries.csv` | 2 | ~165,000 | one industry tag of one job |
| 4 | `jobs/job_skills.csv` | 2 | ~214,000 | one skill category of one job |
| 5 | `jobs/salaries.csv` | 8 | ~41,000 | one salary record of one job |
| 6 | `companies/companies.csv` | 10 | ~24,000 | one company |
| 7 | `companies/company_industries.csv` | 2 | ~24,000 | one industry of one company |
| 8 | `companies/company_specialities.csv` | 2 | ~169,000 | one speciality of one company |
| 9 | `companies/employee_counts.csv` | 4 | ~36,000 | one employee/follower snapshot of one company |
| 10 | `mappings/industries.csv` | 2 | ~400 | one industry (lookup) |
| 11 | `mappings/skills.csv` | 2 | ~35 | one skill category (lookup) |

Approximate total size of the dataset: roughly **0.5 GB** uncompressed, with `postings.csv` being the largest file because of long job descriptions.

---

## 3. Main File: `postings.csv` (31 columns)

One row per job posting, about 124,000 rows.

| # | Column | Description | Why it exists |
|---|---|---|---|
| 1 | `job_id` | Unique LinkedIn job ID (maps to `linkedin.com/jobs/view/<job_id>`) | Primary key; joins to all `jobs/` files |
| 2 | `company_name` | Name of the hiring company | Quick readable reference without joining |
| 3 | `title` | Job title | Core searchable attribute |
| 4 | `description` | Full job description text | Source for text analysis / NLP |
| 5 | `max_salary` | Maximum pay for the position | Salary analysis |
| 6 | `pay_period` | Pay frequency (hourly, monthly, yearly) | Needed to interpret salary values |
| 7 | `location` | Job location | Geographic analysis |
| 8 | `company_id` | Company identifier | Foreign key to `companies/` files |
| 9 | `views` | Number of times the posting was viewed | Engagement metric |
| 10 | `med_salary` | Median pay | Salary analysis |
| 11 | `min_salary` | Minimum pay | Salary analysis |
| 12 | `formatted_work_type` | Full-time, part-time, contract, etc. | Employment type filter |
| 13 | `applies` | Number of applications submitted | Demand / competition metric |
| 14 | `original_listed_time` | When the job was first posted | Posting trend analysis |
| 15 | `remote_allowed` | Whether remote work is allowed | Remote-work analysis |
| 16 | `job_posting_url` | URL of the LinkedIn posting | Traceability |
| 17 | `application_url` | URL where candidates apply | Application routing |
| 18 | `application_type` | Offsite, simple onsite, or complex onsite apply | Application process analysis |
| 19 | `expiry` | Expiration date of the posting | Posting lifecycle |
| 20 | `closed_time` | When the posting was closed | Time-to-fill analysis |
| 21 | `formatted_experience_level` | Entry, associate, mid-senior, director, etc. | Seniority filter |
| 22 | `skills_desc` | Free-text skills required | Skills extraction |
| 23 | `listed_time` | Time the job was listed / observed | Recency tracking |
| 24 | `posting_domain` | Domain of the external application site | Source analysis |
| 25 | `sponsored` | Whether the posting is promoted (0/1) | Paid vs organic comparison |
| 26 | `work_type` | Work type category | Employment classification |
| 27 | `currency` | Currency of the compensation | Cross-country salary comparison |
| 28 | `compensation_type` | Type of compensation | Salary interpretation |
| 29 | `normalized_salary` | Salary normalized to a common (yearly) basis | Comparing hourly/monthly/yearly pay |
| 30 | `zip_code` | ZIP code of the location | Fine-grained geography |
| 31 | `fips` | FIPS county code | Joining with US census/geographic data |

---

## 4. Supporting Files and Columns

### `jobs/` folder (linked by `job_id`)

**`jobs/benefits.csv` (3 columns)**

| Column | Description | Why it exists |
|---|---|---|
| `job_id` | Job the benefit belongs to | Links to `postings.csv` |
| `inferred` | Whether the benefit was inferred by LinkedIn rather than explicitly listed | Data transparency |
| `type` | Benefit type (e.g. 401(k), medical insurance, dental, paid time off) | Lets seekers/analysts compare perks |

Many-to-one: one job can have several benefits, so one `job_id` appears in several rows.

**`jobs/job_industries.csv` (2 columns)**

| Column | Description | Why it exists |
|---|---|---|
| `job_id` | Job being tagged | Links to `postings.csv` |
| `industry_id` | Industry code | Links to `mappings/industries.csv` |

**`jobs/job_skills.csv` (2 columns)**

| Column | Description | Why it exists |
|---|---|---|
| `job_id` | Job being tagged | Links to `postings.csv` |
| `skill_abr` | Skill category abbreviation | Links to `mappings/skills.csv` |

**`jobs/salaries.csv` (8 columns)**

| Column | Description | Why it exists |
|---|---|---|
| `salary_id` | Unique ID of the salary record | Primary key of this table |
| `job_id` | Job the salary belongs to | Links to `postings.csv` |
| `max_salary` | Maximum pay | Salary range upper bound |
| `med_salary` | Median pay | Midpoint when given |
| `min_salary` | Minimum pay | Salary range lower bound |
| `pay_period` | Hourly, monthly, yearly, etc. | Interprets the amounts |
| `currency` | Currency code (e.g. USD) | Cross-currency comparison |
| `compensation_type` | Type of compensation (e.g. base salary) | Classifies the pay |

### `companies/` folder (linked by `company_id`)

**`companies/companies.csv` (10 columns)**

| Column | Description |
|---|---|
| `company_id` | Primary key, links to `postings.csv` |
| `name` | Company name |
| `description` | Company description |
| `company_size` | Size category, 0 (smallest) to 7 (largest) |
| `state` | State |
| `country` | Country |
| `city` | City |
| `zip_code` | ZIP code |
| `address` | Street address |
| `url` | Company LinkedIn URL |

**`companies/company_industries.csv` (2 columns):** `company_id`, `industry` (industry name as text).

**`companies/company_specialities.csv` (2 columns):** `company_id`, `speciality` (company specialities listed on LinkedIn).

**`companies/employee_counts.csv` (4 columns)**

| Column | Description | Why it exists |
|---|---|---|
| `company_id` | Company | Links to `companies.csv` |
| `employee_count` | Employees on LinkedIn at that time | Company size over time |
| `follower_count` | LinkedIn followers at that time | Brand popularity |
| `time_recorded` | Snapshot timestamp | Enables growth/shrink tracking |

### `mappings/` folder (lookup tables)

| File | Columns | Purpose |
|---|---|---|
| `mappings/industries.csv` | `industry_id`, `industry_name` | Converts `industry_id` into a readable industry name |
| `mappings/skills.csv` | `skill_abr`, `skill_name` | Converts `skill_abr` into a readable skill category name |

---

## 5. Null Values in Main Columns (`postings.csv`)

Approximate pattern. Exact counts come from the script in Section 7.

| Group | Columns | Expected null level | Reason |
|---|---|---|---|
| Core identifiers | `job_id`, `title`, `description`, `company_id`, `listed_time` | Near zero (a few rows may be missing) | Required when a job is posted |
| Salary fields | `min_salary`, `med_salary`, `max_salary`, `pay_period`, `compensation_type`, `normalized_salary` | Very high (roughly 60 - 90%) | Most employers do not publish pay |
| Engagement | `applies`, `views` | Moderate to high | Depends on what the scraper captured |
| Lifecycle | `expiry`, `closed_time` | Varies; `closed_time` is mostly null | Many postings were still open at scrape time |
| Optional text/location | `skills_desc`, `zip_code`, `fips`, `posting_domain`, `application_url` | Moderate to high | Optional or not applicable (e.g. onsite apply) |
| Flags | `remote_allowed` | High | Only set when the poster specified it |

**Takeaway:** missing data is mostly structural (optional fields), so salary analysis should be done on the subset of jobs that actually disclose pay.

---

## 6. Which Files Connect Through Which ID

```
                          mappings/industries.csv
                                  ^ industry_id
                                  |
 jobs/job_industries.csv ---------+
 jobs/job_skills.csv ---skill_abr--> mappings/skills.csv
 jobs/benefits.csv  \
 jobs/salaries.csv   >-- job_id --> postings.csv -- company_id --> companies/companies.csv
 jobs/job_industries.csv /                                         companies/company_industries.csv
 jobs/job_skills.csv    /                                          companies/company_specialities.csv
                                                                   companies/employee_counts.csv
```

| Key | Connects | Relationship |
|---|---|---|
| `job_id` | `postings.csv` <-> `jobs/benefits.csv`, `jobs/job_industries.csv`, `jobs/job_skills.csv`, `jobs/salaries.csv` | One job to many rows |
| `company_id` | `postings.csv` <-> `companies/companies.csv`, `companies/company_industries.csv`, `companies/company_specialities.csv`, `companies/employee_counts.csv` | One company to many rows |
| `industry_id` | `jobs/job_industries.csv` <-> `mappings/industries.csv` | Code to name lookup |
| `skill_abr` | `jobs/job_skills.csv` <-> `mappings/skills.csv` | Code to name lookup |

---

## 7. Verification Script (exact rows, sizes, nulls)

```python
import os
import pandas as pd

BASE = "linkedin-job-postings"  # path to the extracted dataset folder

files = [
    "postings.csv",
    "jobs/benefits.csv", "jobs/job_industries.csv",
    "jobs/job_skills.csv", "jobs/salaries.csv",
    "companies/companies.csv", "companies/company_industries.csv",
    "companies/company_specialities.csv", "companies/employee_counts.csv",
    "mappings/industries.csv", "mappings/skills.csv",
]

for f in files:
    path = os.path.join(BASE, f)
    df = pd.read_csv(path)
    mb = os.path.getsize(path) / 1024**2
    print(f"{f}: {len(df):,} rows | {df.shape[1]} cols | {mb:.1f} MB")

postings = pd.read_csv(os.path.join(BASE, "postings.csv"))
nulls = postings.isna().sum().to_frame("null_count")
nulls["null_pct"] = (nulls["null_count"] / len(postings) * 100).round(2)
print(nulls.sort_values("null_pct", ascending=False))
```

---

## 8. Summary

- The dataset has **11 files** because it is normalized: one main table, four job detail tables, four company tables and two lookup tables.
- `postings.csv` is the hub: **31 columns**, about 124,000 job postings.
- Missing values are concentrated in optional fields, especially salary.
- **`job_id`** links job files to `postings.csv`; **`company_id`** links company files to `postings.csv`; **`industry_id`** and **`skill_abr`** link to lookup tables.
