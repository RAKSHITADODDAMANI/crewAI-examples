import streamlit as st
from crewai import Agent, Task, Crew
from crewai.llm import LLM

st.title("💼 AI Job Posting Generator")

# Define the LLM used by the agent
from crewai import LLM
import os
import streamlit as st

# Make sure OpenAI API key exists
if "OPENAI_API_KEY" not in os.environ:
    st.error("🚨 Missing OpenAI API Key! Please add it under Streamlit Cloud Secrets.")
else:
    # Explicitly tell CrewAI to use OpenAI provider
    llm = LLM(
        provider="openai",
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"]
    )


# Create the job posting agent
agent = Agent(
    name="JobPostingAgent",
    role="Job Description Writer",
    goal="Write professional and attractive job postings.",
    backstory=(
        "You are an experienced HR specialist skilled at writing engaging and "
        "detailed job descriptions that attract qualified candidates."
    ),
    llm=llm
)

# Input fields
job_title = st.text_input("Enter Job Title:")
skills = st.text_area("Required Skills:")
company = st.text_input("Company Name:")

if st.button("Generate Job Description"):
    if job_title and skills and company:
        task = Task(
            description=f"Write a professional job posting for {job_title} at {company}. "
                        f"Required skills: {skills}",
            expected_output="A detailed, formatted, and engaging job posting.",
            agent=agent
        )

        crew = Crew(agents=[agent], tasks=[task])

        # ✅ Updated run method for latest CrewAI
        try:
            result = crew.kickoff()  # works in CrewAI >=0.40
        except AttributeError:
            # fallback for older versions
            result = crew.run()

        st.subheader("📝 Generated Job Description:")
        st.write(result)
    else:
        st.warning("Please fill all fields before generating.")
