import os
import streamlit as st
from groq import Groq

# ----------------------------
# Streamlit UI setup
# ----------------------------
st.set_page_config(page_title="💼 AI Job Posting Generator", page_icon="💼")
st.title("💼 AI Job Posting Generator")

# ----------------------------
# Initialize Groq client
# ----------------------------
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    st.error("🚨 Missing Groq API Key! Please add it in Streamlit Cloud → Settings → Secrets → GROQ_API_KEY.")
    st.stop()

try:
    client = Groq(api_key=GROQ_KEY)
    st.success("✅ LLM initialized successfully with Groq.")
except Exception as e:
    st.error(f"❌ Failed to initialize Groq client: {e}")
    st.stop()

# ----------------------------
# User Inputs
# ----------------------------
job_title = st.text_input("Enter Job Title:", "Data Scientist")
skills = st.text_area("Required Skills:", "Python, SQL, Machine Learning")
company = st.text_input("Company Name:", "TechNova Analytics Pvt. Ltd.")
experience = st.text_input("Experience Level:", "2+ years")
job_type = st.selectbox("Job Type:", ["Full-time", "Part-time", "Internship", "Remote"])

# ----------------------------
# Generate Job Description
# ----------------------------
if st.button("Generate Job Description"):
    with st.spinner("Generating... Please wait..."):
        try:
            prompt = f"""
            Write a professional job description for the role of {job_title} at {company}.
            Include:
            - Company overview (short paragraph)
            - Key responsibilities
            - Required skills ({skills})
            - Experience level ({experience})
            - Job type ({job_type})
            - How to apply section
            """

            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",

                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            result = response.choices[0].message.content
            st.subheader("📝 Generated Job Description:")
            st.write(result)

        except Exception as e:
            st.error(f"❌ Error while generating description: {e}")
