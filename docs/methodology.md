# CareerLens — Methodology

## Overview

CareerLens is an end-to-end job-market analytics project built from an Indian job-posting dataset.

The objective is to transform raw job-posting information into a structured analytical system that can answer questions about:

- Job demand
- Skills
- Salaries
- Experience
- Locations
- Companies
- Work arrangements
- Career roles

The project uses Python for data preparation, DuckDB for analytical storage and SQL, Power BI for business intelligence, and Streamlit for the interactive career-gap application.

---

# 1. Data Source

The project uses the Kaggle dataset:

`shivamshrivastava21/indian-job-market-dataset-2025-2026`

Source file:

`indian-job-market-dataset-2025.xlsx`

The original dataset contained:

**97,929 rows × 17 columns**

---

# 2. Data Cleaning

The cleaning process was performed before the data was loaded into the analytical warehouse.

## Duplicate job IDs

The source contained repeated job IDs.

The cleaning process:

1. Identified repeated job IDs.
2. Checked whether repeated rows were exact duplicates.
3. Removed exact duplicate rows.
4. Removed the remaining repeated job-ID groups where the same job ID appeared with conflicting information.

Final job count:

**97,679**

---

## Salary Cleaning

Salary values appeared in several formats, including:

- Annual salaries
- Monthly salaries
- Lacs per annum
- Salary ranges
- `Not disclosed`
- `Unpaid`

Salary values were standardized into annual salary values where possible.

Two main fields were created:

```text
minimum_salary_annual
maximum_salary_annual
```

Only jobs with usable minimum and maximum salary values were included in salary-range analysis.

This produced:

**33,427 jobs with salary information**

For these jobs:

```text
salary_midpoint =
(minimum_salary_annual + maximum_salary_annual) / 2
```

The midpoint is used as a representative value for comparing salary ranges.

It should not be interpreted as the actual salary paid to an employee.

---

# 3. Experience Cleaning

Experience information was standardized into minimum and maximum experience fields.

The project checked for invalid ranges such as:

```text
minimum experience > maximum experience
```

No such invalid ranges remained.

A small number of jobs had no usable experience information. These jobs were retained rather than artificially assigning an experience level.

---

# 4. Company Normalization

Company names contained variations and inconsistencies.

A normalized company dimension was created using a surrogate:

```text
company_key
```

This allows company-related analysis to use a consistent identifier while retaining the original company information.

---

# 5. Skill Cleaning

Skills were extracted from the source skill field and transformed into job-skill relationships.

Cleaning included:

- Removing duplicate job-skill pairs
- Removing obviously invalid or excessively long skill values
- Standardizing skill representations where possible

Final result:

**752,930 job-skill relationships**

and:

**43,849 unique skills**

The project intentionally does not manually redefine every unusual skill string because doing so could introduce subjective assumptions.

---

# 6. Location Cleaning

Location information was normalized into a location dimension and a job-location bridge.

The final model contains:

**4,952 unique locations**

and:

**129,675 job-location relationships**

Because a single job can contain multiple locations, location demand is calculated using:

```sql
COUNT(DISTINCT job_id)
```

rather than counting raw relationship rows.

---

# 7. Work Mode Classification

Job postings were classified into:

- `remote`
- `hybrid`
- `not_specified`

The project does not assume that a missing work-mode description means on-site work.

Final distribution:

| Work mode | Jobs |
|---|---:|
| Not specified | 89,975 |
| Hybrid | 5,752 |
| Remote | 1,952 |

---

# 8. Posting Age

The source provides relative posting information such as:

- Just Now
- Few Hours Ago
- Today
- 1 Day Ago
- 2 Days Ago

These values were converted into approximate posting-age categories.

Because the source does not provide reliable calendar dates, CareerLens does not perform monthly or yearly job-demand trend analysis.

The Trends dashboard therefore focuses on:

- Posting age
- Experience
- Work arrangement

rather than calendar-time trends.

---

# 9. Data Warehouse

The cleaned data was organized into a relational analytical model.

```text
fact_job_posting
       │
       ├── dim_company
       │
       ├── bridge_job_skill ─── dim_skill
       │
       └── bridge_job_location ─── dim_location
```

The design separates:

- Job-level information
- Company information
- Skills
- Locations
- Many-to-many relationships

This structure makes the data easier to query and reduces duplication during analysis.

---

# 10. Analytical Marts

SQL transformations were used to create purpose-built analytical marts.

Major marts include:

- `mart_market_overview`
- `mart_skill_demand`
- `mart_salary_analysis`
- `mart_role_analysis`
- `mart_location_demand`
- `mart_role_skill_demand`
- `mart_salary_by_title`
- `mart_salary_by_experience`

These marts provide the datasets used by Power BI and the downstream application.

---

# 11. Role Classification

The Career Path Explorer analyzes:

- Data Analyst
- Data Engineer
- Data Scientist

Role groups were created using job-title matching.

For example, titles containing the relevant role terms were grouped into the corresponding analytical role.

This approach is transparent and easy to reproduce, but it is not a perfect occupational classification system.

---

# 12. Salary Analysis

Salary analysis primarily uses:

**median salary midpoint**

rather than average salary.

Median values reduce the influence of unusually high or low observations.

Salary comparisons are also filtered using minimum observation thresholds to avoid presenting statistics based on very small samples.

---

# 13. Association vs Causation

CareerLens reports relationships observed in job-market data.

For example:

> A particular skill may appear more frequently in higher-paying jobs.

This does **not** prove that learning that skill causes a higher salary.

Other factors may explain the relationship, including:

- Experience
- Job title
- Industry
- Company
- Location
- Seniority
- Other technical skills

Therefore the project describes these relationships as associations rather than causal effects.

---

# 14. Power BI

Power BI is used as the primary business-intelligence layer.

The dashboard contains five pages:

1. Market Overview
2. Skills Explorer
3. Salary Explorer
4. Career Path Explorer
5. Market Trends

Each dashboard page uses analytical marts rather than directly querying the raw source dataset.

---

# 15. Streamlit Application

The Streamlit application provides the **My Career Gap** experience.

The user selects:

- Target job
- Experience level
- Current skills

CareerLens then compares the selected skills against skills requested in the relevant market segment.

The output includes:

- Market skill demand
- Skills already selected by the user
- Skills requested by the market
- Job counts
- Job-share percentages

The application does not produce an unexplained employability score.

Instead, the underlying methodology and market evidence are shown directly to the user.

---

# 16. Reproducibility

The project separates:

```text
Raw data
    ↓
Cleaning
    ↓
Warehouse
    ↓
Analytical marts
    ↓
Power BI / Streamlit
```

This separation makes the analytical workflow easier to understand, reproduce, and extend.

---

# 17. Limitations

CareerLens has several important limitations:

1. The dataset represents a particular source and time period rather than the entire Indian job market.
2. Salary information is missing from a large proportion of postings.
3. Posting dates are relative rather than reliable calendar dates.
4. Job-title matching is an approximation.
5. Skill names originate from source data and may contain unusual terminology.
6. Work-mode information is missing for many postings.
7. Salary midpoint represents the midpoint of an advertised range, not necessarily the salary ultimately received.

These limitations are intentionally documented so that the analysis is not presented as more precise than the source data allows.