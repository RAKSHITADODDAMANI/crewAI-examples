import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM

st.set_page_config(page_title="💼 AI Job Posting Generator", page_icon="💼")

# ----------------------------
# Safe LLM initialization
# ----------------------------
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    st.error("🚨 Missing Groq API Key! Please add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()
else:
    try:
        # ✅ No 'provider' argument for CrewAI ≥0.41
        llm = LLM(
            model="mixtral-8x7b",
            api_key=GROQ_KEY
        )
        st.success("✅ LLM initialized successfully with Groq.")
    except Exception as e:
        st.error(f"❌ LLM initialization failed: {e}")
        st.stop()
