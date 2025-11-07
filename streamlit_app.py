import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM

os.environ["CREWAI_LLM_PROVIDER"] = "groq"

st.set_page_config(page_title="💼 AI Job Posting Generator", page_icon="💼")

# ----------------------------
# Step 1: Initialize LLM safely
# ----------------------------
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    st.error("🚨 Missing Groq API Key! Please add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()
else:
    try:
        # ✅ Initialize Groq LLM
        llm = LLM(
            model="mixtral-8x7b",
            api_key=GROQ_KEY
        )
        st.success("✅ LLM initialized successfully with Groq.")
    except Exception as e:
        st.error(f"❌ LLM initialization failed: {e}")
        st.stop()

# ----------------------------
# Step 2: App UI
# ----------------------------
st.title("💼 AI Job Posting Generator")

job_title = st.text_input("Enter Job Title:", "Data Scientist")
skills = st.text_area("Required Skills:", "Python, SQL, Machine Learning")
company = st.text_input("Company Name:", "TechNova Analytics Pvt. Ltd.")
experience = st.selectbox("Experience Level:", ["Fresher", "Mid-level", "Senior"])
job_type = st.selectbox("Job Type:", ["Full-time", "Part-time", "Internship"])

if st.button("🚀 Generate Job Description"):
    with st.spinner("Generating... Please wait..."):
        try:
            # Step 3: Define Agent and Task
            agent = Agent(
                role="HR Assistant",
                goal=f"Create a professional job description for {job_title} at {company}.",
                backstory="You are an HR expert experienced in crafting clear and attractive job descriptions.",
                llm=llm,
            )

            task = Task(
                description=(
                    f"Write a job description for the role '{job_title}' at {company}. "
                    f"Required skills: {skills}. Experience level: {experience}. Job type: {job_type}. "
                    "Include sections for Responsibilities, Requirements, and Benefits."
                ),
                expected_output="A clear, formatted job description with bullet points and structure.",
                agent=agent,
            )

            crew = Crew(agents=[agent], tasks=[task])
            result = crew.kickoff()

            st.subheader("📝 Generated Job Description:")
            st.write(result)

        except Exception as e:
            st.error(f"❌ Error while generating description: {e}")
