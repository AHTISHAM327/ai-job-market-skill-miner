LinkedIn Job Postings (2023-2024): Data Mining Project Guide
Dataset: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
This dataset has 123,849 job postings plus company details, benefits, and skills. It works well for a Data Mining course.
> **Note on counts:** The row and column counts in Section 1 were checked on our real data (by Ahtisham, 12 Oct; also in `DATA_MANIFEST.md`). Any other number that was not checked is marked "not checked". Always confirm the exact numbers in your own copy with `df.shape` and `df.columns` (code in Section 7) before putting them in your report. The Kaggle page lists old file names (`job_postings.csv`, `job_details/`, `company_details/`). They are outdated: use the names below.
---
1. Dataset Structure
The dataset is several linked CSV files. This lets you practice joining tables (relational data mining).
File (inside the data folder)	Purpose	Rows	Columns
`postings.csv` (main table)	Core details of each job	123,849	31
`jobs/job_skills.csv`	Skills linked to each job	213,768	2
`jobs/salaries.csv`	Salary details per job	40,785	8
`jobs/benefits.csv`	Perks offered per job (several rows per job)	67,943	3
`jobs/job_industries.csv`	Industries linked to each job	164,808	2
`companies/companies.csv`	Info about hiring companies	24,473	10
`companies/company_industries.csv`	Industries linked to each company	24,375	2
`companies/company_specialities.csv`	Specialities linked to each company	169,387	2
`companies/employee_counts.csv`	Company size and followers over time	35,787	4
`mappings/skills.csv`	Skill code to skill name	35	2
`mappings/industries.csv`	Industry code to industry name	422	2
Other checked facts:
0 repeated `job_id`. `description` is empty in 7 rows.
Pay is given in only 36,073 postings (29.1%).
`skills_desc` is empty in about 98% of postings.
---
2. Columns in Each File
2.1 postings.csv (31 columns)
Column	Meaning
`job_id`	Unique ID of the job
`company_id`	Links to `companies/companies.csv`
`company_name`	Name of the company
`title`	Job title
`description`	Full job description text
`max_salary`	Maximum salary offered
`med_salary`	Median salary offered
`min_salary`	Minimum salary offered
`pay_period`	Hourly, Monthly, Yearly
`formatted_work_type`	Full-time, Part-time, Contract
`location`	Job city/state
`applies`	Number of applications
`original_listed_time`	When first posted
`remote_allowed`	Whether remote work is allowed
`views`	Number of views
`job_posting_url`	LinkedIn URL of the job
`application_url`	External application link
`application_type`	Offsite or onsite application
`expiry`	Expiry timestamp
`closed_time`	When the listing closed
`formatted_experience_level`	Entry, Associate, Mid-Senior, Executive
`skills_desc`	Text about required skills
`listed_time`	Time the job was listed
`posting_domain`	Domain of the application website
`sponsored`	Whether the post is promoted
`work_type`	Raw work type category
`currency`	Currency code (e.g. USD)
`compensation_type`	Type of pay
`normalized_salary`	Salary converted to a common yearly scale
`zip_code`	Postal code
`fips`	County code
(The 31 column names match `df.columns` on our data. The meanings come from the Kaggle page: not checked in detail.)
2.2 companies/companies.csv (10 columns)
Column	Meaning
`company_id`	Unique company ID (matches jobs table)
`name`	Company name
`description`	Company overview
`company_size`	Size group, coded 0 to 7
`country`, `state`, `city`	Headquarters location
`zip_code`	Postal code
`address`	Street address
`url`	LinkedIn company page
(Column names and meanings: not checked.)
2.3 jobs/benefits.csv (3 columns)
Column	Meaning
`job_id`	Links to the job
`type`	Benefit type (Medical Insurance, 401(k), Dental, Paid Time Off)
`inferred`	Whether the benefit was tagged explicitly or inferred by LinkedIn
(Column names and meanings: not checked.)
2.4 companies/employee_counts.csv (4 columns)
Column	Meaning
`company_id`	Links to companies
`employee_count`	Number of employees at that time
`follower_count`	LinkedIn followers
`time_recorded`	Unix timestamp of the snapshot
(Column names and meanings: not checked.)
---
3. Data Mining Tasks You Can Do
A. Exploration and Preprocessing (the foundation)
Missing values: Salary columns (`min_salary`, `max_salary`, `med_salary`) have many missing values because many companies don't show pay (pay is given in only 29.1% of postings). `description` is empty in 7 rows.
Feature engineering: Pull keywords from `description` or `skills_desc` to find the most requested programming languages, tools, and soft skills.
Our 3 project questions
Question 1. Which skills appear together in data/AI jobs?
Goal: Find skills that go together in the same job posting.
Algorithms: Association rules, FP-Growth.
Question 2. What job families exist?
Goal: Find natural groups of similar jobs, using the job text, with no labels.
Algorithms: TF-IDF + k-means clustering.
Question 3. Can we predict a salary band?
Goal: Predict the salary band of a job from its other details.
Algorithms: Decision tree, random forest.
F. Text Mining
Goal: Use NLP on job descriptions to find common buzzwords. This supports Question 1 and Question 2.
---
4. Suggested Project Workflow
Introduction and objective: State our 3 questions (skills together, job families, salary band).
Load and clean data: Load CSVs with Pandas, merge `postings` with `companies` on `company_id`, handle nulls and duplicates.
Visualize: Charts (Matplotlib/Seaborn) of experience level, work type, and salary.
Apply mining models: FP-Growth for skills, TF-IDF + k-means for job families, decision tree / random forest for salary band.
Conclusion and insights: Summarize what the models found and how it helps job seekers or recruiters.
---
5. Merge and Missing-Value Notes
Merging `postings` and `companies` on `company_id` joins 123,849 postings to the company table. Many jobs share a company, and some jobs have no matching company, so check for unmatched rows after the merge (not checked yet).
Run `df.isnull().sum()` to count missing values. Expect many in the salary columns. Mention this in your report as a data-cleaning issue.
The postings table has 31 columns, which gives you many features to choose from.
---
6. Common Data Issues to Mention in Your Report
Many missing salaries (checked: pay is given in only 29.1% of postings)
`skills_desc` empty in about 98% of postings (checked)
Mixed pay periods (hourly, monthly, yearly), so salaries must be converted to one scale (not checked)
Long free-text fields that need cleaning (not checked)
Duplicate or near-duplicate postings (to be checked in the notebook, section 4)
Outliers in salary, views, and applies (not checked)
Inconsistent location formats (to be checked in the notebook, section 5)
Several benefit rows per job, which need grouping before joining (not checked)
---
7. Starter Code
```python
import pandas as pd

# Paths are relative to the data folder
postings = pd.read_csv("postings.csv")
companies = pd.read_csv("companies/companies.csv")
benefits = pd.read_csv("jobs/benefits.csv")
emp = pd.read_csv("companies/employee_counts.csv")

# Confirm exact counts and column names
for name, df in [("postings", postings), ("companies", companies),
                 ("benefits", benefits), ("employee_counts", emp)]:
    print(name, df.shape)
    print(list(df.columns), "\n")

# Missing values
print(postings.isnull().sum().sort_values(ascending=False).head(15))

# Merge postings with companies
merged = postings.merge(companies, on="company_id", how="left",
                        suffixes=("_job", "_company"))
print(merged.shape)
```
---
8. Summary
Technique	Question it answers
Association rules (FP-Growth)	Which skills appear together in data/AI jobs?
Clustering (TF-IDF + k-means)	What job families exist?
Classification (decision tree / random forest)	Can we predict a salary band?
Text mining	What words and skills do employers use most?
