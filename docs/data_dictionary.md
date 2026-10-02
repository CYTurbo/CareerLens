# CareerLens — Data Dictionary

## Overview

CareerLens uses a cleaned Indian job-market dataset containing 97,679 job postings.

The data is organized into a small analytical warehouse consisting of fact, dimension, and bridge tables.

## Warehouse Structure

```text
fact_job_posting
       │
       ├── dim_company
       │
       ├── bridge_job_skill ─── dim_skill
       │
       └── bridge_job_location ─── dim_location
```

---

# 1. fact_job_posting

One row represents one job posting.

| Column | Description |
|---|---|
| `job_id` | Unique identifier for the job posting |
| `company_key` | Internal normalized company identifier |
| `company_name` | Company name associated with the posting |
| `title_clean` | Cleaned job title |
| `currency` | Currency reported by the source |
| `salary_type` | Classification of the salary information |
| `minimum_salary_annual` | Minimum salary converted to annual value |
| `maximum_salary_annual` | Maximum salary converted to annual value |
| `minimum_experience` | Minimum required experience |
| `maximum_experience` | Maximum required experience |
| `work_mode` | Remote, hybrid, or not specified |
| `location_raw` | Original location associated with the posting |
| `posting_age_days` | Approximate age of the posting based on the source's relative posting label |
| `start_timing` | Original posting-time category |

### Salary midpoint

For jobs containing both minimum and maximum annual salary values:

```text
salary_midpoint =
(minimum_salary_annual + maximum_salary_annual) / 2
```

This value is used for salary-distribution analysis.

---

# 2. dim_company

One row represents a normalized company.

| Column | Description |
|---|---|
| `company_key` | Surrogate identifier for the normalized company |
| `company_id` | Original company identifier from the source |
| `company_name` | Normalized company name |

The company dimension was created because the source contained cases where the same company ID appeared with different company-name variations.

---

# 3. dim_skill

One row represents a normalized skill.

| Column | Description |
|---|---|
| `skill_key` | Identifier for the skill |
| `skill_name` | Normalized skill name |

The final skill dimension contains 43,849 unique skills.

---

# 4. bridge_job_skill

This table connects jobs with the skills mentioned in their postings.

One row represents one job-skill relationship.

| Column | Description |
|---|---|
| `job_id` | Job posting identifier |
| `skill_key` | Skill identifier |

Final size:

**752,930 job-skill relationships**

Duplicate job-skill pairs were removed during cleaning.

---

# 5. dim_location

One row represents a normalized job location.

| Column | Description |
|---|---|
| `location_key` | Location identifier |
| `location_name` | Normalized location |
| `location_raw` | Source location representation |

The final location dimension contains 4,952 unique granular locations.

---

# 6. bridge_job_location

This table connects jobs with their locations.

One row represents one job-location relationship.

| Column | Description |
|---|---|
| `job_id` | Job posting identifier |
| `location_key` | Location identifier |

Final size:

**129,675 job-location relationships**

Because one job can be associated with multiple locations, job-location analysis uses:

```sql
COUNT(DISTINCT job_id)
```

when measuring the number of unique jobs.

---

# 7. Analytical Marts

CareerLens also contains analytical marts used by Power BI and analysis.

## mart_market_overview

One row per job posting.

Used for:

- Total job postings
- Companies
- Work arrangements
- Posting age
- Job titles
- Market overview

---

## mart_skill_demand

One row per skill.

Used for:

- Skill demand
- Job count by skill
- Skill share of job postings
- Top skills

Important fields:

- `skill_name`
- `job_count`
- `job_share_pct`

---

## mart_salary_analysis

One row per job containing usable salary information.

Used for:

- Salary distributions
- Median salary
- Salary analysis

Important fields:

- `job_id`
- `title_clean`
- `work_mode`
- `salary_midpoint`

Contains **33,427 jobs with usable salary ranges**.

---

## mart_role_analysis

Contains role-level analysis for selected data-related roles.

Used for:

- Career Path Explorer
- Role comparison
- Job counts
- Salary comparison
- Experience comparison

Roles analyzed include:

- Data Analyst
- Data Engineer
- Data Scientist

---

## mart_location_demand

Contains job demand by location.

Used for:

- Location analysis
- Top job markets

---

## mart_role_skill_demand

Connects selected job roles with their requested skills.

Used for:

- Skills by role
- Career Path Explorer
- Role-specific skill analysis

---

## mart_salary_by_title

Contains salary statistics by job title and work mode.

Used for:

- Salary Explorer
- Median salary by title

Only titles meeting the minimum observation threshold are included.

---

## mart_salary_by_experience

Contains salary statistics by minimum experience and work mode.

Used for:

- Salary Explorer
- Salary by experience analysis

Only groups meeting the minimum observation threshold are included.

---

# Dataset Summary

| Metric | Value |
|---|---:|
| Job postings | 97,679 |
| Companies | 18,560 |
| Locations | 4,952 |
| Unique skills | 43,849 |
| Job-skill relationships | 752,930 |
| Job-location relationships | 129,675 |
| Jobs with salary data | 33,427 |

---

# Important Data Notes

### Salary

Salary information is incomplete. Many job postings do not disclose salary.

### Posting dates

The source provides relative posting labels such as "Today", "1 Day Ago", and "Few Hours Ago" rather than reliable calendar dates.

Therefore CareerLens does not claim to provide true monthly or yearly job-demand trends.

### Job roles

Role classification for the Career Path Explorer is based on title matching and should be interpreted as an analytical classification rather than a perfect occupational taxonomy.

### Skills

Skills originate from job-posting data and may contain inconsistent or unusual source terminology. Cleaning removes obvious invalid values and duplicates but does not attempt to manually redefine every skill.

### Work arrangement

Many postings do not explicitly specify remote or hybrid work. These are classified as `not_specified` rather than assumed to be on-site.