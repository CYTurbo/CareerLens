# CareerLens

## Indian Job Market Intelligence & Skill-Gap Analyzer

> **Explore the job market. Understand the demand. Discover your next career move.**

CareerLens is an end-to-end data analytics product built to analyze the Indian job market using real job-posting data.

It combines data engineering, SQL analytics, Python, Power BI, and Streamlit to explore job demand, skills, salaries, locations, experience requirements, work arrangements, and career paths — and turns those insights into an interactive skill-gap analysis.

---

## 🚀 Project Overview

The job market contains thousands of postings with different combinations of:

- Job titles
- Skills
- Companies
- Salaries
- Experience requirements
- Locations
- Work arrangements

CareerLens transforms this fragmented information into a structured analytical system.

The project answers questions such as:

- Which jobs are in demand?
- Which skills are frequently requested?
- Which skills appear together?
- How do salary distributions vary across roles?
- How does salary vary with experience?
- Which locations have the most opportunities?
- How do requirements differ between career paths?
- Which skills are commonly requested for a target role?
- How does a user's current skill set compare with the market?

---

## 📊 Dataset

CareerLens uses the **Indian Job Market Dataset 2025–2026**.

### Dataset scale

| Metric | Value |
|---|---:|
| Job postings | **97,679** |
| Companies | **18,560** |
| Locations | **4,952** |
| Unique skills | **43,849** |
| Job-skill relationships | **752,930** |
| Job-location relationships | **129,675** |
| Jobs with salary data | **33,427** |

The dataset contains job postings from across India and includes information about job titles, companies, salaries, experience, locations, skills, and work arrangements.

---

# 🏗️ Data Architecture

CareerLens follows an end-to-end analytics pipeline:

```text
Raw Job Data
      ↓
Data Ingestion
      ↓
Data Cleaning & Standardization
      ↓
Skill / Salary / Experience / Location Normalization
      ↓
Data Warehouse
      ↓
SQL Analytics
      ↓
Analytical Marts
      ↓
Power BI
      ↓
Streamlit Application
