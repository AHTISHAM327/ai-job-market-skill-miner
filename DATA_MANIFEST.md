# DATA_MANIFEST

## Source
- Dataset: LinkedIn Job Postings (2023 - 2024), "A Snapshot Into the Current Job Market"
- Kaggle link: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
- Owner: Arsh Koneru (arshkon) and 1 collaborator
- License: CC BY-SA 4.0 (sharing and adapting allowed with credit; shared copies keep the same license)
- Last updated on Kaggle: about 2 years ago (page says "Expected update frequency: Monthly")
- Limits noticed: LinkedIn only; about 95% U.S. locations; postings first listed Dec 2023 to Apr 2024; pay disclosed for 29.1% of postings; skills_desc empty for 98% of postings; the data card's file names (job_postings.csv, job_details/, company_details/) are outdated, the real files are listed below

## Version pinned in loader
- Version: 13 (556.5 MB) (Ahtisham, 12 Oct 2026)
- Checked against Kaggle by Quratulain:

## Files
| File | Rows | Columns | What it holds |
| --- | --- | --- | --- |
| postings.csv | 123849 | 31 | One row per job posting: title, description, salary, location, experience level, work type |
| jobs/job_skills.csv | 213768 | 2 | job_id to skill code (35 broad job functions) |
| jobs/salaries.csv | 40785 | 8 | Salary records per job |
| jobs/benefits.csv | 67943 | 3 | Benefits per job |
| jobs/job_industries.csv | 164808 | 2 | job_id to industry id |
| companies/companies.csv | 24473 | 10 | Company details |
| companies/company_industries.csv | 24375 | 2 | Company to industry |
| companies/company_specialities.csv | 169387 | 2 | Company specialities |
| companies/employee_counts.csv | 35787 | 4 | Employee and follower counts |
| mappings/skills.csv | 35 | 2 | Skill code to name |
| mappings/industries.csv | 422 | 2 | Industry id to name |

postings.csv columns (31): job_id, company_name, title, description, max_salary, pay_period, location, company_id, views, med_salary, min_salary, formatted_work_type, applies, original_listed_time, remote_allowed, job_posting_url, application_url, application_type, expiry, closed_time, formatted_experience_level, skills_desc, listed_time, posting_domain, sponsored, work_type, currency, compensation_type, normalized_salary, zip_code, fips

First checks (12 Oct 2026, Colab, version 13): 0 duplicate job_id; description missing in 7 rows; pay columns filled for 36073 postings (29.1%): yearly 20628, hourly 14741, monthly 518, weekly 177, biweekly 9; normalized_salary filled for the same 36073.

## Sharing decision
- Can we keep a copy in our Drive? Yes. CC BY-SA 4.0 allows it with credit to the dataset authors; any data we share keeps CC BY-SA 4.0. (To be confirmed by Quratulain against the Kaggle page.)

## Current accepted version
- none yet

## Version history
| Version | Date | Made by | Notebook | Rows | What changed |
| --- | --- | --- | --- | --- | --- |

## Reload checks
| Who | Date | Result |
| --- | --- | --- |
