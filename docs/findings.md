# CareerLens — Key Findings

## Overview

The CareerLens analysis examines 97,679 Indian job postings across job titles, companies, skills, salaries, experience, locations, and work arrangements.

The findings below describe patterns observed in the dataset. They should be interpreted as characteristics of the dataset rather than as a complete representation of the Indian job market.

---

# 1. Job Market Size

The cleaned dataset contains:

- **97,679 job postings**
- **18,560 companies**
- **4,952 locations**
- **43,849 unique skills**
- **752,930 job-skill relationships**
- **129,675 job-location relationships**

This provides a large enough dataset to examine job-market patterns across multiple dimensions.

---

# 2. Job Titles

The most frequently occurring job titles include:

| Job title | Job postings |
|---|---:|
| Application Developer | 2,033 |
| Application Lead | 1,346 |
| Sales Executive | 583 |
| Software Development Engineer | 497 |
| Business Development Executive | 457 |
| Trust & Safety New Associate | 348 |
| Data Engineer | 339 |
| Business Development Manager | 325 |
| Sales Manager | 322 |
| Java Full Stack Developer | 285 |

The dataset therefore covers a broad range of occupations rather than only technical or data roles.

---

# 3. Companies

The companies with the largest number of postings in the dataset include:

| Company | Job postings |
|---|---:|
| Accenture | 8,193 |
| IDESLABS PRIVATE LIMITED | 2,294 |
| Wipro | 1,494 |
| Krazy Mantra HR Solutions Pvt Ltd | 1,026 |
| PRO Hr Complete Solutions | 981 |
| Kotak Mahindra Bank | 980 |
| Infosys | 937 |
| Capgemini | 698 |
| IBM | 687 |
| PRADEEPIT CONSULTING SERVICES PVT LTD | 615 |

These counts describe the number of postings in this dataset and should not be interpreted as total hiring activity by those companies.

---

# 4. Skill Demand

The most frequently requested skills include:

| Skill | Job postings |
|---|---:|
| Sales | 9,178 |
| Python | 5,846 |
| Project Management | 5,543 |
| Customer Service | 5,122 |
| SAP | 5,043 |
| Management | 4,849 |
| CSS | 4,186 |
| Java | 4,088 |
| SQL | 3,983 |
| Business Development | 3,738 |

The skill distribution also demonstrates that the dataset extends well beyond traditional data and software roles.

This is one reason CareerLens was designed as a broader job-market intelligence product rather than only a data-career dashboard.

---

# 5. Salary Coverage

Salary information is incomplete.

Out of 97,679 job postings:

**33,427** contain usable minimum and maximum salary values.

The remaining postings do not provide a usable salary range for the salary analysis.

This means salary findings should always be interpreted separately from overall job-volume findings.

---

# 6. Salary by Role

For selected data-related roles, the analysis produced the following results:

| Role | Job postings | Jobs with salary data | Median salary midpoint |
|---|---:|---:|---:|
| Data Engineer | 1,082 | 319 | ₹20.0L |
| Data Scientist | 317 | 48 | ₹21.375L |
| Data Analyst | 267 | 59 | ₹7.5L |

These figures are based on the project's title-matching methodology.

The salary figures represent the median midpoint of advertised salary ranges, not guaranteed compensation.

---

# 7. Salary and Work Arrangement

Among jobs with usable salary information:

| Work mode | Salary jobs | Median salary midpoint |
|---|---:|---:|
| Hybrid | 1,944 | ₹15L |
| Remote | 797 | ₹5.5L |
| Not specified | 30,686 | ₹4L |

These differences should **not** be interpreted as evidence that work arrangement causes differences in salary.

The groups differ substantially in size and may also differ in:

- Job roles
- Experience
- Companies
- Locations
- Industries
- Salary disclosure behavior

Therefore this finding is an observed association in the dataset.

---

# 8. Location Demand

The largest granular location strings by job-location relationships include:

| Location | Job-location relationships |
|---|---:|
| Bengaluru | 24,188 |
| Hyderabad | 12,340 |
| Pune | 10,028 |
| Chennai | 8,605 |
| Gurugram | 6,362 |
| Mumbai | 5,935 |
| Noida | 4,562 |
| Nawabganj | 2,828 |
| Ahmedabad | 2,795 |

Because a job can be associated with multiple locations, CareerLens uses distinct job IDs when interpreting unique job demand by location.

---

# 9. Data Career Profiles

CareerLens includes a role comparison for three selected data careers.

## Data Engineer

- 1,082 job postings
- 319 postings with salary information
- Median salary midpoint: ₹20L
- Median minimum experience: 5 years

## Data Scientist

- 317 job postings
- 48 postings with salary information
- Median salary midpoint: ₹21.375L
- Median minimum experience: 4 years

## Data Analyst

- 267 job postings
- 59 postings with salary information
- Median salary midpoint: ₹7.5L
- Median minimum experience: 4 years

These figures describe the selected dataset and role-classification method.

---

# 10. Work Arrangement

The dataset contains:

| Work mode | Job postings |
|---|---:|
| Not specified | 89,975 |
| Hybrid | 5,752 |
| Remote | 1,952 |

The large `not_specified` category is important.

It means that the dataset cannot reliably be interpreted as an on-site-versus-remote comparison because many postings simply do not provide enough information.

---

# 11. Posting Age

The source provides relative posting information rather than reliable calendar dates.

CareerLens therefore analyzes posting recency using approximate posting-age categories.

The Trends dashboard examines:

- Recent postings
- 8–20 day postings
- Posting age
- Experience
- Work arrangement

The project does not claim monthly or yearly job-demand trends.

---

# 12. What These Findings Demonstrate

The main purpose of CareerLens is not to produce a list of "best" careers or skills.

Instead, the project demonstrates how raw job-market data can be transformed into measurable evidence.

The analysis can answer questions such as:

- What skills appear frequently in job postings?
- Which roles have more salary observations?
- How do advertised salaries differ across roles?
- Which locations contain large numbers of postings?
- How much work-mode information is actually available?
- How do selected career profiles differ?

---

# 13. Key Analytical Takeaways

### Job demand is broad

The dataset contains technical, sales, business, customer-service, management, finance, and many other roles.

### Skills are highly diverse

More than 43,000 distinct skill values were identified after cleaning.

### Salary data is incomplete

Only 33,427 postings contain usable salary ranges, so salary analysis represents a subset of the total market.

### Role comparisons require context

Job-title classification is an analytical approximation, so role-level results should not be treated as exact occupational categories.

### Work-mode comparisons require caution

Most postings do not explicitly specify remote or hybrid status.

### Relative posting age is not the same as historical trend data

The source does not provide reliable calendar dates, so CareerLens avoids unsupported monthly or yearly trend claims.

---

# Conclusion

CareerLens shows how a large, messy job-posting dataset can be transformed into a structured analytics product.

The project combines:

```text
Python
   ↓
Data Cleaning
   ↓
DuckDB + SQL
   ↓
Analytical Marts
   ↓
Power BI
   ↓
Streamlit
```

The final product focuses on evidence from job postings while clearly documenting the limitations of the underlying data.

The goal is not to tell users what career they should choose.

The goal is to give them a structured view of what the job market is actually asking for.