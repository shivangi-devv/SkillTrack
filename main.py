import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# -----------------------------
# LOAD API KEY
# -----------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="SkillTrack",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 50%,
        #172554 100%
    );
}


/* Main content width */
.block-container {
    max-width: 1100px;
    padding-top: 45px;
}


/* Main title */
.stApp h1 {
    color: #f8fafc !important;
    font-size: 52px !important;
    font-weight: 800 !important;
    text-align: center;
    margin-bottom: 5px;
}


/* Subtitle */
.subtitle-text {
    color: #cbd5e1 !important;
    text-align: center;
    font-size: 19px;
    margin-bottom: 55px;
}


/* Section heading */
.stApp h2 {
    color: #ffffff !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

/* Normal text */
.stApp p {
    color: #cbd5e1;
}


/* Text area label */
[data-testid="stTextArea"] label {
    color: #e2e8f0 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}


/* Text area */
[data-testid="stTextArea"] textarea {
    background-color: #f8fafc !important;
    color: #1e293b !important;
    border: 2px solid #334155 !important;
    border-radius: 12px !important;
    font-size: 16px !important;
}


/* Placeholder */
[data-testid="stTextArea"] textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}


/* Analyze button */
.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );
    color: white !important;
    font-size: 17px;
    font-weight: 700;
    margin-top: 15px;
}


/* Button hover */
.stButton > button:hover {
    border: none;
    color: white !important;
    transform: translateY(-2px);
}


/* Success message */
[data-testid="stAlert"] {
    border-radius: 10px;
}


/* Caption / small text */
.stCaption {
    color: #cbd5e1 !important;
}


/* Divider */
hr {
    border-color: #334155;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #e2e8f0 !important;
    font-size: 17px !important;
    line-height: 1.7 !important;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #f8fafc !important;
}

[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol {
    color: #e2e8f0 !important;
}

[data-testid="stMarkdownContainer"] li::marker {
    color: #94a3b8 !important;
}

</style>


""", unsafe_allow_html=True)

st.title("🎯 SkillTrack")

st.markdown(
    '<div class="subtitle-text">'
    'career & skill analyzer'
    '</div>',
    unsafe_allow_html=True
)

# -----------------------------
# JOB ANALYZER
# -----------------------------

st.markdown(
    "## 📋 <span style='color:#ffffff;'>Analyze a Job Opportunity</span>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:#cbd5e1; font-size:16px;'>"
    "Paste a job or internship description below.<br>"
    "SkillTrack will help you understand what skills are required."
    "</p>",
    unsafe_allow_html=True
)


# -----------------------------
# JOB DESCRIPTION INPUT
# -----------------------------

job_description = st.text_area(
    "Job / Internship Description",
    height=300,
    placeholder="Paste the job description here..."
)
st.markdown("## 🧑‍💻 Your Skills")

st.write(
    "Enter the skills you already know. "
    "Separate multiple skills using commas."
)

user_skills = st.text_input(
    "Your Current Skills",
    placeholder="Example: Python, SQL, Git, Pandas"
)


# -----------------------------
# ANALYZE BUTTON
# -----------------------------

if st.button("🚀 Analyze Job"):

    if job_description.strip() == "":
        st.warning("⚠️ Please paste a job description first.")

    elif user_skills.strip() == "":
        st.warning("⚠️ Please enter your current skills.")
    
    else:
        with st.spinner("🤖 AI is analyzing the job description"):
            prompt= f"""
You are SkillTrack, an AI career and skill gap analyzer.
Analyze the following job description and compare it with
the user's current skills.
JOB DESCRIPTION:
{job_description}
USER'S CURRENT SKILLS:
{user_skills}
Give the result in this exact structure:
🎯 Role
Identify the main role.
🧠 Required Skills
List the important skills required for this job.
💻 Technologies
List the technologies, programming languages,
frameworks, libraries and tools required.
✅ Skills You Already Have
From the user's current skills, identify which skills
match the job requirements.
⚠️ Skill Gap
Identify the important skills required by the job
that the user does not currently have.
📚 What You Should Learn
Explain which missing skills the user should learn.
 🗺️ Personalized Learning Roadmap
Create a beginner-friendly step-by-step roadmap
based on the skill gap.
Keep the explanation practical and easy to understand.
Do not assume that the user knows a skill unless it
is mentioned in the user's current skills.
"""
            interaction = client.interactions.create(
                    model="gemini-3.5-flash-lite",
                    input=prompt
                )
            st.success("✅ Analysis Complete!")

            st.markdown("## 📊 SkillTrack Analysis")

            st.markdown(interaction.output_text)

             
else:
        st.success("✅ Job description received!")

        st.subheader("📄 Your Job Description")

        st.write(job_description)