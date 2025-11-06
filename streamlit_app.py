import streamlit as st
from crewai import Agent, Task, Crew
from crewai.llm import LLM

st.title("💼 AI Job Posting Generator")

# Define the LLM used by the agent
llm = LLM(model="gpt-4o-mini")  # You can also use "gpt-4-turbo"

# Create an AI agent
agent = Agent(
    name="JobPostingAgent",
    role="Job Description Writer",
    goal="Create professional job postings based on user input",
    backstory=(
        "You are an expert HR professional with years of experience crafting "
        "clear, engaging, and persuasive job postings that attract top talent. "
        "You understand tone, inclusivity, and clarity in writing."
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
            description=f"Write a professional job posting for the position of {job_title} at {company}. "
                        f"The required skills are: {skills}.",
            expected_output="A detailed and attractive job posting text.",
            agent=agent  # ✅ must attach agent to the task
        )

        # Create a crew with this single agent and task
        crew = Crew(tasks=[task], agents=[agent])

        # Run the crew
        result = crew.run()

        # Display output
        st.subheader("📝 Generated Job Description:")
        st.write(result)
    else:
        st.warning("Please fill all fields before generating.")
