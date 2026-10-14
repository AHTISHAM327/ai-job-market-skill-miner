# LinkedIn Job Postings (2023-2024): Data Mining Project Guide

Dataset: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings

This dataset has about 124,000 job postings plus company details, benefits, and skills. It works well for a Data Mining course.

> **Note on counts:** The numbers below come from the dataset notes and may be approximate. Different download versions can differ slightly. Always confirm the exact numbers in your own copy with `df.shape` and `df.columns` (code in Section 7) before putting them in your report.

---

## 1. Dataset Structure

The dataset is several linked CSV files. This lets you practice joining tables (relational data mining).

| File | Purpose | Approx. rows | Columns |
|---|---|---|---|
| `job_postings.csv` (main table) | Core details of each job | 124,000+ | 31 |
| `companies.csv` | Info about hiring companies | Tens of thousands (the notes say 72,521; verify) | ~10-11 |
| `benefits.csv` | Perks offered per job | Thousands (several rows per job) | 3 |
| `employee_counts.csv` | Company size and followers over time | Several snapshots per company | 4 |

Some download versions also include extra files such as company industries, company specialities, job industries, job skills, and salaries.

---

## 2. Columns in Each File

### 2.1 job_postings.csv (31 columns)

| Column | Meaning |
|---|---|
| `job_id` | Unique ID of the job |
| `company_id` | Links to `companies.csv` |
| `company_name` | Name of the company (in some versions) |
| `title` | Job title |
| `description` | Full job description text |
| `max_salary` | Maximum salary offered |
| `med_salary` | Median salary offered |
| `min_salary` | Minimum salary offered |
| `pay_period` | Hourly, Monthly, Yearly |
| `formatted_work_type` | Full-time, Part-time, Contract |
| `location` | Job city/state |
| `applies` | Number of applications |
| `original_listed_time` | When first posted |
| `remote_allowed` | Whether remote work is allowed |
| `views` | Number of views |
| `job_posting_url` | LinkedIn URL of the job |
| `application_url` | External application link |
| `application_type` | Offsite or onsite application |
| `expiry` | Expiry timestamp |
| `closed_time` | When the listing closed |
| `formatted_experience_level` | Entry, Associate, Mid-Senior, Executive |
| `skills_desc` | Text about required skills |
| `listed_time` | Time the job was listed |
| `posting_domain` | Domain of the application website |
| `sponsored` | Whether the post is promoted |
| `work_type` | Raw work type category |
| `currency` | Currency code (e.g. USD) |
| `compensation_type` | Type of pay |
| `normalized_salary` | Salary converted to a common yearly scale |
| `zip_code` | Postal code |
| `fips` | County code |

(Check the exact list in your file with `df.columns`.)

### 2.2 companies.csv

| Column | Meaning |
|---|---|
| `company_id` | Unique company ID (matches jobs table) |
| `name` | Company name |
| `description` | Company overview |
| `company_size` | Size group, coded 0 to 7 |
| `country`, `state`, `city` | Headquarters location |
| `zip_code` | Postal code |
| `address` | Street address |
| `url` | LinkedIn company page |

### 2.3 benefits.csv (3 columns)

| Column | Meaning |
|---|---|
| `job_id` | Links to the job |
| `type` | Benefit type (Medical Insurance, 401(k), Dental, Paid Time Off) |
| `inferred` | Whether the benefit was tagged explicitly or inferred by LinkedIn |

### 2.4 employee_counts.csv (4 columns)

| Column | Meaning |
|---|---|
| `company_id` | Links to companies |
| `employee_count` | Number of employees at that time |
| `follower_count` | LinkedIn followers |
| `time_recorded` | Unix timestamp of the snapshot |

---

## 3. Data Mining Tasks You Can Do

### A. Exploration and Preprocessing (the foundation)
- **Missing values:** Salary columns (`min_salary`, `max_salary`, `med_salary`) have many missing values because many companies don't show pay. Descriptions can also be missing.
- **Feature engineering:** Pull keywords from `description` or `skills_desc` to find the most requested programming languages, tools, and soft skills.

### B. Classification (predict a category)
- **Goal:** Predict experience level (Entry, Associate, Mid-Senior, Executive) or Remote vs On-site, using description text and salary.
- **Algorithms:** Decision Tree, Random Forest, Naive Bayes (with TF-IDF on text).

### C. Regression (predict a number)
- **Goal:** Predict salary from location, company size, experience level, and skills.
- **Algorithms:** Linear Regression, Support Vector Regression (SVR), Gradient Boosting (XGBoost).

### D. Clustering (group similar jobs, no labels)
- **Goal:** Find natural job market groups, e.g. "high-paying tech jobs" or "entry-level local admin jobs", using salary, location, and requirements.
- **Algorithms:** K-Means, Hierarchical Clustering.

### E. Association Rule Mining (market basket analysis)
- **Goal:** Find items that go together. Example: "Jobs offering Health Insurance and 401(k) are often Full-time." You can also find which skills appear together.
- **Algorithm:** Apriori.

### F. Text Mining and Sentiment Analysis
- **Goal:** Use NLP on job descriptions to find common buzzwords or compare tone across industries.

---

## 4. Suggested Project Workflow

1. **Introduction and objective:** State your question, e.g. "What factors most affect salary, and which skills are most in demand?"
2. **Load and clean data:** Load CSVs with Pandas, merge `job_postings` with `companies` on `company_id`, handle nulls.
3. **Visualize:** Charts (Matplotlib/Seaborn) of top job titles, locations, and salary distribution.
4. **Apply mining models:** Use at least two techniques, e.g. classification for remote work and clustering for job segments.
5. **Conclusion and insights:** Summarize what the models found and how it helps job seekers or recruiters.

---

## 5. Merge and Missing-Value Notes

- Merging `job_postings` and `companies` on `company_id` joins about 124,000 jobs to the company table. Many jobs share a company, and some jobs have no matching company, so check for unmatched rows after the merge.
- Run `df.isnull().sum()` to count missing values. Expect many in the salary columns. Mention this in your report as a data-cleaning issue.
- The jobs table has 31 columns, which gives you many features to choose from.

---

## 6. Common Data Issues to Mention in Your Report

- Many missing salaries
- Mixed pay periods (hourly, monthly, yearly), so salaries must be converted to one scale
- Long free-text fields that need cleaning
- Duplicate or near-duplicate postings
- Outliers in salary, views, and applies
- Inconsistent location formats
- Several benefit rows per job, which need grouping before joining

---

## 7. Starter Code

```python
import pandas as pd

jobs = pd.read_csv("job_postings.csv")
companies = pd.read_csv("companies.csv")
benefits = pd.read_csv("benefits.csv")
emp = pd.read_csv("employee_counts.csv")

# Confirm exact counts and column names
for name, df in [("jobs", jobs), ("companies", companies),
                 ("benefits", benefits), ("employee_counts", emp)]:
    print(name, df.shape)
    print(list(df.columns), "\n")

# Missing values
print(jobs.isnull().sum().sort_values(ascending=False).head(15))

# Merge jobs with companies
merged = jobs.merge(companies, on="company_id", how="left",
                    suffixes=("_job", "_company"))
print(merged.shape)
```

---

## 8. Summary

| Technique | Question it answers |
|---|---|
| Classification | Is this job remote? What experience level is it? |
| Regression | What salary can we expect? |
| Clustering | What job market segments exist? |
| Association rules | Which benefits or skills appear together? |
| Text mining | What words and skills do employers use most? |
