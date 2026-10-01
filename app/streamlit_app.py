import duckdb
import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerLens",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# HIDE STREAMLIT CHROME
# ============================================================

st.markdown(
    """
    <style>
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PARQUET FILES
# ============================================================

JOBS_FILE = "app_jobs.parquet"
SKILLS_FILE = "app_job_skills.parquet"

con = duckdb.connect(":memory:")


# ============================================================
# GET JOB TITLES
# ============================================================

@st.cache_data
def get_job_titles():

    query = f"""
        SELECT
            title_clean,
            COUNT(*) AS job_count

        FROM read_parquet('{JOBS_FILE}')

        WHERE title_clean IS NOT NULL

        GROUP BY
            title_clean

        HAVING COUNT(*) >= 20

        ORDER BY
            title_clean
    """

    return con.execute(query).df()


# ============================================================
# GET SKILLS
# ============================================================

@st.cache_data
def get_skills():

    query = f"""
        SELECT DISTINCT
            skill_name

        FROM read_parquet('{SKILLS_FILE}')

        WHERE skill_name IS NOT NULL

        ORDER BY
            skill_name
    """

    return con.execute(query).df()


# ============================================================
# GET MARKET SKILLS
# ============================================================

@st.cache_data
def get_market_skills(
    target_job,
    experience_level
):

    experience_conditions = {

        "0–2 years":
            "minimum_experience_years <= 2",

        "3–5 years":
            "minimum_experience_years BETWEEN 3 AND 5",

        "6–10 years":
            "minimum_experience_years BETWEEN 6 AND 10",

        "10+ years":
            "minimum_experience_years >= 10"
    }

    experience_filter = experience_conditions[
        experience_level
    ]


    # --------------------------------------------------------
    # Find matching jobs
    # --------------------------------------------------------

    matching_jobs_query = f"""
        SELECT
            job_id

        FROM read_parquet('{JOBS_FILE}')

        WHERE LOWER(title_clean) LIKE LOWER(?)

        AND {experience_filter}
    """

    matching_jobs = con.execute(
        matching_jobs_query,
        [f"%{target_job}%"]
    ).df()

    total_jobs = len(matching_jobs)


    # --------------------------------------------------------
    # No matching jobs
    # --------------------------------------------------------

    if total_jobs == 0:

        return (
            pd.DataFrame(
                columns=[
                    "skill_name",
                    "job_count",
                    "job_share_pct"
                ]
            ),
            0
        )


    # --------------------------------------------------------
    # Calculate skill demand
    # --------------------------------------------------------

    con.register(
        "matching_jobs",
        matching_jobs
    )

    skill_query = f"""

        SELECT

            s.skill_name,

            COUNT(
                DISTINCT mj.job_id
            ) AS job_count,

            ROUND(
                100.0 *
                COUNT(DISTINCT mj.job_id)
                / ?,
                2
            ) AS job_share_pct

        FROM matching_jobs AS mj

        INNER JOIN read_parquet(
            '{SKILLS_FILE}'
        ) AS s

            ON mj.job_id = s.job_id

        GROUP BY
            s.skill_name

        ORDER BY
            job_count DESC

        LIMIT 20
    """

    market_skills = con.execute(
        skill_query,
        [total_jobs]
    ).df()

    con.unregister(
        "matching_jobs"
    )

    return (
        market_skills,
        total_jobs
    )


# ============================================================
# LOAD DATA
# ============================================================

job_titles_df = get_job_titles()

skills_df = get_skills()


# ============================================================
# HEADER
# ============================================================

st.title("CareerLens")

st.subheader(
    "My Career Gap"
)

st.caption(
    "Compare your current skills with the skills "
    "requested in the job market."
)


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander(
    "How does CareerLens calculate the skill gap?"
):

    st.write(
        """
        CareerLens compares your selected skills with skills
        requested in job postings matching your selected
        job-title keyword and experience level.

        **Matching Job Postings**

        Job postings whose title contains your selected
        job title keyword and whose minimum experience falls
        within your selected experience range.

        **Job Count**

        The number of matching job postings that mention
        a particular skill.

        **Job Share**

        The percentage of matching job postings that mention
        that skill.

        **Your Skill Gap**

        CareerLens compares your selected skills with the
        top 20 skills requested by the selected market segment.

        CareerLens shows market evidence rather than an overall
        employability score. A skill being frequently requested
        does not mean that learning it guarantees employment.
        """
    )


# ============================================================
# BUILD CAREER PROFILE
# ============================================================

st.header(
    "Build Your Career Profile"
)


# ============================================================
# TARGET JOB
# ============================================================

target_job = st.selectbox(
    "Target Job Title",
    job_titles_df[
        "title_clean"
    ].tolist()
)


# ============================================================
# EXPERIENCE
# ============================================================

experience_level = st.selectbox(
    "Experience Level",
    [
        "0–2 years",
        "3–5 years",
        "6–10 years",
        "10+ years"
    ]
)


# ============================================================
# CURRENT SKILLS
# ============================================================

st.markdown(
    "**Current Skills**"
)

st.caption(
    "Search for the skills you already know "
    "and select them below."
)


# ------------------------------------------------------------
# SEARCH SKILLS
# ------------------------------------------------------------

skill_search = st.text_input(
    "Search for a skill",
    placeholder="Type a skill you know, e.g. SQL or Python",
    label_visibility="visible"
)


# ------------------------------------------------------------
# FIND MATCHING SKILLS
# ------------------------------------------------------------

if skill_search.strip():

    search_term = (
        skill_search
        .strip()
        .lower()
    )

    matching_skills = skills_df[
        skills_df["skill_name"]
        .str.lower()
        .str.contains(
            search_term,
            regex=False,
            na=False
        )
    ]["skill_name"].tolist()

    # Prevent the dropdown from becoming too large

    matching_skills = matching_skills[:100]

else:

    matching_skills = []


# ------------------------------------------------------------
# SELECT MATCHING SKILLS
# ------------------------------------------------------------

selected_from_search = st.multiselect(
    "Select the skills you know",

    options=matching_skills,

    placeholder=(
        "Type above to search for skills"
        if not skill_search.strip()
        else "Select the skills you know"
    ),

    label_visibility="visible"
)


# ------------------------------------------------------------
# STORE SELECTED SKILLS
# ------------------------------------------------------------

if "current_skills" not in st.session_state:

    st.session_state.current_skills = []


for skill in selected_from_search:

    if skill not in st.session_state.current_skills:

        st.session_state.current_skills.append(
            skill
        )


current_skills = (
    st.session_state.current_skills
)


# ------------------------------------------------------------
# SHOW SELECTED SKILLS
# ------------------------------------------------------------

if current_skills:

    st.caption(
        f"{len(current_skills)} skill(s) selected"
    )

    st.write(
        ", ".join(current_skills)
    )


# ============================================================
# MARKET ANALYSIS
# ============================================================

market_skills_df, total_jobs = get_market_skills(
    target_job,
    experience_level
)


# ============================================================
# HANDLE NO MATCHING JOBS
# ============================================================

if total_jobs == 0:

    st.warning(
        "No matching job postings were found for this "
        "job-title keyword and experience level."
    )

    st.stop()


# ============================================================
# SKILL GAP CALCULATION
# ============================================================

market_skill_set = set(
    market_skills_df[
        "skill_name"
    ].str.lower()
)


user_skill_set = set(
    skill.lower()
    for skill in current_skills
)


matched_skills = sorted(
    user_skill_set.intersection(
        market_skill_set
    )
)


missing_skills = market_skills_df[
    ~market_skills_df[
        "skill_name"
    ]
    .str.lower()
    .isin(user_skill_set)
].copy()


matched_count = len(
    matched_skills
)


total_market_skills = len(
    market_skills_df
)


missing_count = len(
    missing_skills
)


# ============================================================
# TOP MARKET SKILL
# ============================================================

if not market_skills_df.empty:

    top_market_skill = (
        market_skills_df
        .iloc[0]["skill_name"]
    )

    top_market_skill_share = (
        market_skills_df
        .iloc[0]["job_share_pct"]
    )

else:

    top_market_skill = "N/A"

    top_market_skill_share = 0


# ============================================================
# MARKET SNAPSHOT
# ============================================================

st.header(
    "Your Market Snapshot"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Matching Job Postings",
        f"{total_jobs:,}"
    )


with col2:

    st.metric(
        "Your Skills Matched",
        f"{matched_count}/{total_market_skills}"
    )


with col3:

    st.metric(
        "Market Skills Missing",
        f"{missing_count}"
    )


with col4:

    st.metric(
        "Top Market Skill",
        top_market_skill
    )


# ============================================================
# MARKET SKILL DEMAND
# ============================================================

st.header(
    "Market Skill Demand"
)

st.caption(
    "Top skills requested across the matching job postings. "
    "Green bars indicate skills already in your profile."
)


for _, row in market_skills_df.iterrows():

    skill = row[
        "skill_name"
    ]

    share = float(
        row["job_share_pct"]
    )

    job_count = int(
        row["job_count"]
    )

    is_user_skill = (
        skill.lower()
        in user_skill_set
    )


    # --------------------------------------------------------
    # Skill name
    # --------------------------------------------------------

    st.markdown(
        f"**{skill}**"
    )


    # --------------------------------------------------------
    # Progress bar
    # --------------------------------------------------------

    if is_user_skill:

        st.markdown(
            f"""
            <div style="
                background-color: #e6e6e6;
                border-radius: 10px;
                height: 10px;
                width: 100%;
                margin-top: 4px;
                margin-bottom: 4px;
            ">

                <div style="
                    background-color: #22c55e;
                    width: {min(share, 100)}%;
                    height: 10px;
                    border-radius: 10px;
                "></div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.progress(
            min(
                share / 100,
                1.0
            )
        )


    st.caption(
        f"{share:.2f}% of matching jobs · "
        f"{job_count:,} job postings"
    )


# ============================================================
# YOUR SKILLS
# ============================================================

st.header(
    "Skills You Already Have"
)


if matched_skills:

    st.success(
        f"{matched_count} of the top "
        f"{total_market_skills} market skills "
        f"match your current profile."
    )


    matched_display = market_skills_df[
        market_skills_df[
            "skill_name"
        ]
        .str.lower()
        .isin(user_skill_set)
    ].copy()


    matched_display = matched_display[
        [
            "skill_name",
            "job_count",
            "job_share_pct"
        ]
    ].rename(
        columns={
            "skill_name": "Skill",
            "job_count": "Job Count",
            "job_share_pct": "Job Share (%)"
        }
    )


    st.dataframe(
        matched_display,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "None of your selected skills appear in the "
        "top market skills for this segment."
    )


# ============================================================
# SKILL GAP
# ============================================================

st.header(
    "Skills Requested by the Market"
)


if not missing_skills.empty:

    st.warning(
        f"{missing_count} of the top "
        f"{total_market_skills} market skills "
        f"are not currently in your selected skills."
    )


    missing_display = missing_skills[
        [
            "skill_name",
            "job_count",
            "job_share_pct"
        ]
    ].rename(
        columns={
            "skill_name": "Skill",
            "job_count": "Job Count",
            "job_share_pct": "Job Share (%)"
        }
    )


    st.dataframe(
        missing_display,
        use_container_width=True,
        hide_index=True
    )


else:

    st.success(
        "All of the top market skills are already "
        "included in your selected skills."
    )


# ============================================================
# INTERPRETING THE RESULTS
# ============================================================

st.header(
    "How to Interpret Your Results"
)


st.info(
    f"""
    CareerLens found **{total_jobs:,} matching job postings**
    for the selected job-title keyword and experience level.

    The most frequently requested skill in this market segment
    is **{top_market_skill}**, appearing in approximately
    **{top_market_skill_share:.2f}%** of matching postings.

    These percentages describe how frequently skills appear
    in job postings. They are market-demand signals, not
    guarantees that a skill is required for every job or that
    learning a skill will guarantee employment.
    """
)


# ============================================================
# FOOTNOTE
# ============================================================

st.caption(
    "CareerLens uses job-posting data as market evidence. "
    "Skill frequency represents job-posting demand and does "
    "not guarantee employment outcomes."
)