import os
import streamlit as st
from crewai import Agent, Task, Crew
from crewai.llms import Groq

# --- Streamlit App Title ---
st.set_page_config(page_title="Agentic AI Portfolio Generator", page_icon="🤖", layout="centered")
st.title("🤖 Agentic AI Portfolio Generator")

# --- Sidebar Configuration ---
st.sidebar.header("🔑 API Key Setup")
groq_api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key

# --- Initialize LLM (GROQ) ---
try:
    llm = Groq(api_key=groq_api_key, model="mixtral-8x7b-32768")
    st.success("✅ LLM initialized successfully with Groq.")
except Exception as e:
    st.error(f"❌ LLM initialization failed: {e}")
    st.stop()

# --- Input Section ---
st.subheader("🧠 Enter Your Project Information")

project_title = st.text_input("Project Title:")
project_description = st.text_area("Project Description:")
project_tech = st.text_input("Technologies Used (comma-separated):")
generate_button = st.button("🚀 Generate Portfolio Summary")

# --- Generate Portfolio Section ---
if generate_button:
    if not project_title or not project_description or not project_tech:
        st.warning("⚠️ Please fill in all fields before generating the portfolio.")
    else:
        try:
            # Define an AI Agent
            generator_agent = Agent(
                role="AI Portfolio Generator",
                goal="Generate a professional and human-like project portfolio section.",
                backstory="You are an expert AI agent skilled in creating detailed, realistic project descriptions for technical portfolios.",
                llm=llm
            )

            # Create Task for the Agent
            task = Task(
                description=f"Generate a polished project portfolio entry for the following project:\n\n"
                            f"Title: {project_title}\n"
                            f"Description: {project_description}\n"
                            f"Technologies: {project_tech}\n\n"
                            f"Format the response with subheadings: Overview, Features, Tools Used, and Outcome.",
                agent=generator_agent
            )

            # Create Crew and Execute
            crew = Crew(agents=[generator_agent], tasks=[task])
            result = crew.kickoff()

            # Display Result
            st.subheader("📘 Generated Portfolio Summary")
            st.write(result)

        except Exception as e:
            st.error(f"❌ Error while generating description: {e}")
