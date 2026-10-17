# Dataset Notes: `postings.csv`

**Dataset:** [LinkedIn Job Postings (2023 - 2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) by arshkon on Kaggle
**Role:** Core / central table of the dataset

---

## 1. Overview

| Property | Value |
| :--- | :--- |
| File path | `postings.csv` (dataset root directory) |
| File size | ~516 MB |
| Rows | ~124,000 unique LinkedIn job postings (captured across 2023 and 2024) |
| Columns | 27 documented below (see note in Section 3) |
| Primary key | `job_id` |
| Foreign key | `company_id` |

---

## 2. Column Dictionary

### 2.1 Identifiers

| Column | Description |
| :--- | :--- |
| `job_id` | Unique LinkedIn job identifier. Primary key; links to the `jobs/` subfiles. |
| `company_id` | Unique company identifier. Foreign key; links to the `company_details/` subfiles. |

### 2.2 Job Content

| Column | Description |
| :--- | :--- |
| `title` | Official job position title. |
| `description` | Full text of the role's responsibilities and requirements. |
| `skills_desc` | Free-text skills or qualifications sought by the employer. |
| `location` | Geographical location of the job. |

### 2.3 Compensation

| Column | Description |
| :--- | :--- |
| `min_salary` | Lower bound of the compensation range. |
| `max_salary` | Upper bound of the compensation range. |
| `med_salary` | Median / mid-point salary value. |
| `pay_period` | Payout frequency (e.g., Hourly, Monthly, Yearly). |
| `currency` | ISO currency code (e.g., USD, EUR, GBP). |
| `compensation_type` | Structure of the package (e.g., base salary, range, fixed). |

### 2.4 Classification

| Column | Description |
| :--- | :--- |
| `formatted_work_type` | Employment type (e.g., Full-time, Part-time, Contract). |
| `work_type` | Alternative categorization of work type. |
| `formatted_experience_level` | Seniority requirement (e.g., Entry level, Mid-Senior, Executive). |
| `remote_allowed` | Whether remote work is permitted (`1/0` or `True/False`). |

### 2.5 Engagement & Promotion

| Column | Description |
| :--- | :--- |
| `views` | Number of views the posting accumulated. |
| `applies` | Number of applications submitted (when tracked). |
| `sponsored` | Whether the listing was a paid/promoted ad (`1/0`). |

### 2.6 Application Details

| Column | Description |
| :--- | :--- |
| `job_posting_url` | Direct URL to the live LinkedIn posting. |
| `application_url` | Destination link where candidates apply. |
| `application_type` | Application mechanism (offsite vs. onsite apply). |
| `posting_domain` | Web domain hosting the external application page (if applicable). |

### 2.7 Timestamps

| Column | Description |
| :--- | :--- |
| `original_listed_time` | Timestamp when the job was originally posted. |
| `listed_time` | Timestamp of the listing as observed by the dataset collector. |
| `expiry` | Timestamp / date when the listing expires. |
| `closed_time` | Timestamp when the recruiter closed the listing. |

---

## 3. Verification Note on Column Count

The source notes documented **27** columns. The published dataset may contain additional columns not covered above. Run the snippet below to confirm and compare against this dictionary:

```python
import pandas as pd

df = pd.read_csv("postings.csv", nrows=5)
print(len(df.columns))
print(df.columns.tolist())
```

Columns worth checking for (not in the notes above): `company_name`, `normalized_salary`, `zip_code`, `fips`.

---

## 4. Null Value Distribution

| Severity | Columns | Reason |
| :--- | :--- | :--- |
| **Near-zero (< 1%)** | `job_id`, `title`, `description`, `original_listed_time`, `company_id` | Mandatory core identifiers. |
| **Moderate (10% - 30%)** | `applies`, `views`, `expiry`, `skills_desc` | Depends on scraping visibility and tracking limits. |
| **High (60% - 80%)** | `min_salary`, `max_salary`, `med_salary`, `currency`, `compensation_type` | Salary disclosure is optional for recruiters on LinkedIn. |

> Percentages are approximate. Verify with `df.isna().mean().sort_values()`.

---

## 5. Relationships

`postings.csv` is the central anchor table of the 11-file dataset.

```
                       ┌── jobs/benefits.csv
                       ├── jobs/job_industries.csv
   job_id ────────────►├── jobs/job_skills.csv
                       └── jobs/salaries.csv

postings.csv
                       ┌── company_details/companies.csv
   company_id ────────►└── company_details/employee_counts.csv
```

| Join key | Related files |
| :--- | :--- |
| `job_id` | `jobs/benefits.csv`, `jobs/job_industries.csv`, `jobs/job_skills.csv`, `jobs/salaries.csv` |
| `company_id` | `company_details/companies.csv`, `company_details/employee_counts.csv` |

> Folder names above come from the source notes. Check them against the actual download, since Kaggle's layout may group these files differently.

---

## 6. Quick Start

```python
import pandas as pd

postings = pd.read_csv("postings.csv")

# Join with a jobs/ subfile
skills = pd.read_csv("jobs/job_skills.csv")
merged = postings.merge(skills, on="job_id", how="left")

# Join with a company file
companies = pd.read_csv("company_details/companies.csv")
merged = merged.merge(companies, on="company_id", how="left")
```

## 7. Usage Tips

- The file is large (~516 MB); use `usecols=` or `chunksize=` if memory is limited.
- Salary columns are mostly empty, so filter on `pay_period` and `currency` before comparing salaries.
- Normalize `remote_allowed` and `sponsored` to booleans, since they may mix `1/0` and `True/False`.
- Convert timestamp columns with `pd.to_datetime(..., unit="ms")` if values are epoch milliseconds; check first.
