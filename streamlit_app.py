import os
import time
import streamlit as st
from crewai import Agent, Task, Crew, LLM

# ----------------------------
# App Title and Info
# ----------------------------
st.set_page_config(page_title="💼 AI Job Posting Generator", page_icon="💼")
st.title("💼 AI Job Posting Generator")
st.write(
    """
    This app uses **CrewAI** + **OpenAI GPT** to automatically generate 
    professional job descriptions based on your input.
    """
)

# ----------------------------
# Step 1: Safe LLM Initialization
# ----------------------------
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
    st.error("🚨 Missing OpenAI API Key! Please add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

try:
    # ✅ Do NOT include provider (CrewAI auto-detects OpenAI)
    llm = LLM(
        model="gpt-3.5-turbo",   # you can also use "gpt-3.5-turbo"
        api_key=OPENAI_KEY
    )
except Exception as e:
    st.error(f"❌ LLM initialization failed: {e}")
    st.stop()

# ----------------------------
# Step 2: User Inputs
# ----------------------------
st.header("🧾 Enter Job Details")

job_title = st.text_input("Enter Job Title:", "Data Scientist")
skills = st.text_area("Required Skills:", "Python, SQL, Machine Learning")
company = st.text_input("Company Name:", "TechNova Analytics Pvt. Ltd.")
experience = st.selectbox("Experience Level:", ["Fresher", "Mid-Level", "Senior"])
job_type = st.selectbox("Job Type:", ["Full-time", "Part-time", "Internship", "Contract"])

# ----------------------------
# Step 3: Generate Description Button
# ----------------------------
if st.button("🚀 Generate Job Description"):
    with st.spinner("Generating job description... Please wait."):
        try:
            # --- Define Agent ---
            agent = Agent(
                role="Job Description Writer",
                goal=f"Create a professional job description for {job_title} at {company}.",
                backstory="You are an HR assistant experienced in writing clear, detailed job postings.",
                llm=llm,
            )

            # --- Define Task ---
            task = Task(
                description=(
                    f"Write a detailed job description for a {job_title} role at {company}. "
                    f"The required skills are: {skills}. The position is {job_type} for {experience} candidates. "
                    "Include responsibilities, qualifications, and a closing note encouraging applicants."
                ),
                expected_output="A well-formatted job description in Markdown style.",
                agent=agent,
            )

            # --- Execute with CrewAI ---
            crew = Crew(agents=[agent], tasks=[task])

            # Retry logic (to avoid temporary rate limit issues)
            for attempt in range(3):
                try:
                    result = crew.kickoff()
                    break
                except Exception as e:
                    if "RateLimitError" in str(e):
                        st.warning("⚠️ Rate limit hit, retrying in 20 seconds...")
                        time.sleep(20)
                    else:
                        raise e

            # --- Display Output ---
            st.subheader("📝 Generated Job Description:")
            st.markdown(result)

        except Exception as e:
            st.error(f"❌ Error while generating description: {e}")

# ----------------------------
# Step 4: Footer
# ----------------------------
st.divider()
st.caption("Built with ❤️ using [CrewAI](https://github.com/joaomdmoura/crewai) and Streamlit.")
