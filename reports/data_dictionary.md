Quratulain's task, done by Rija.

# Data dictionary: postings.csv (123,849 rows, 31 columns)

Source: Drive copy of Kaggle version 13 (`postings.csv`). Checked against `reports/data_quality_report.md` and `rija/dataset_notes.md`.

| Column | Type | % missing | Different values | Meaning | Keep or drop (reason) |
| :--- | :--- | ---: | ---: | :--- | :--- |
| job_id | int64 | 0 | 123849 | Unique ID of each posting | keep: joins the other files |
| company_name | object | 1.4 | 24428 | Name of the hiring company | keep: used to find repeats |
| title | object | 0 | 72521 | Job title text | keep: data/AI title filter |
| description | object | 0 | 107827 | Full job description text | keep: skills come from it |
| max_salary | float64 | 75.9 | 5321 | Maximum posted pay | drop: 75.9% missing; pay model uses normalized_salary |
| pay_period | object | 70.9 | 5 | Pay frequency (Hourly, Monthly, Yearly) | drop: normalized_salary already uses a common yearly scale |
| location | object | 0 | 8526 | City, state, or country of the job | keep: state chart |
| company_id | float64 | 1.4 | 24474 | Unique LinkedIn company ID | drop: company_name used for repeat checks; not needed for the 3 models |
| views | float64 | 1.4 | 684 | Number of views on the posting | drop: engagement metric not needed for our 3 questions |
| med_salary | float64 | 94.9 | 1417 | Median posted pay | drop: 94.9% missing; pay model uses normalized_salary |
| min_salary | float64 | 75.9 | 4612 | Minimum posted pay | drop: 75.9% missing; pay model uses normalized_salary |
| formatted_work_type | object | 0 | 7 | Standardized employment type (Full-time, Contract, etc.) | keep: salary model input |
| applies | float64 | 81.2 | 274 | Number of LinkedIn applications | drop: 81.2% missing |
| original_listed_time | float64 | 0 | 65036 | Timestamp when first posted | drop: timestamps not needed for our 3 questions |
| remote_allowed | float64 | 87.7 | 1 | Flag indicating remote work allowed | keep: salary model input (empty = not remote) |
| job_posting_url | object | 0 | 123849 | LinkedIn URL of the posting | drop: identifier link not needed for analysis |
| application_url | object | 29.6 | 84800 | External application URL | drop: URL not needed for analysis |
| application_type | object | 0 | 4 | Application method (onsite, offsite, etc.) | drop: application mechanics not needed for our 3 questions |
| expiry | float64 | 0 | 54851 | Timestamp when posting expires | drop: timestamps not needed for our 3 questions |
| closed_time | float64 | 99.1 | 698 | Timestamp when listing closed | drop: 99.1% missing |
| formatted_experience_level | object | 23.7 | 6 | Standardized seniority level (Entry, Mid-Senior, etc.) | keep: salary model input (empty = "Unknown") |
| skills_desc | object | 98 | 2212 | Raw text summary of required skills | drop: 98% missing; skills mined from description instead |
| listed_time | float64 | 0 | 53231 | Timestamp when job was listed | drop: timestamps not needed for our 3 questions |
| posting_domain | object | 32.3 | 4443 | Domain hosting the job application | drop: web domain not needed for our 3 questions |
| sponsored | int64 | 0 | 1 | Whether the post is promoted | drop: constant value (no variance) |
| work_type | object | 0 | 7 | Raw work type category | drop: same as formatted_work_type |
| currency | object | 70.9 | 6 | Currency code for the listed pay | keep: pay model filter (USD only) |
| compensation_type | object | 70.9 | 1 | Type of compensation (base salary) | drop: single value across all non-null rows |
| normalized_salary | float64 | 70.9 | 7259 | Salary converted to a common yearly scale | keep: pay model target bands (USD only) |
| zip_code | float64 | 16.9 | 6989 | Postal code of the job location | drop: location column used for state chart |
| fips | float64 | 22.1 | 2270 | County FIPS code | drop: location column used for state chart |
