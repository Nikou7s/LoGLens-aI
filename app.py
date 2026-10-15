import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# Page setup
st.set_page_config(
    page_title="LogLens AI | SysAdmin & Security Copilot",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ LogLens AI — SysAdmin & Security Copilot")
st.markdown("Powered by **Google Gemma 4** via Gemini API")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input("Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
    model_choice = st.selectbox("Model", ["gemma-4-26b-a4b-it", "gemma-4-31b-it"])
    st.divider()
    st.markdown("### Hacktoberfest 2026")
    st.caption("Built for Hack Day Pune x Poona College")

# Main inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. System / Terminal Logs")
    log_input = st.text_area(
        "Paste error logs or console traces:",
        height=250,
        placeholder="e.g. systemd[1]: Failed to start nginx.service (Address already in use)"
    )

with col2:
    st.subheader("2. Terminal Screenshot (Optional)")
    uploaded_image = st.file_uploader("Upload screenshot of terminal/error output:", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Screenshot Preview", use_column_width=True)

# Run Analysis Button
if st.button("🚀 Analyze with Gemma 4", type="primary"):
    if not api_key_input:
        st.error("Please provide a valid Gemini API Key in the sidebar or .env file.")
    elif not log_input and not uploaded_image:
        st.warning("Please provide either log text or upload a screenshot to analyze.")
    else:
        with st.spinner("Gemma 4 is inspecting system logs and visual output..."):
            try:
                # Initialize GenAI Client
                client = genai.Client(api_key=api_key_input)
                
                system_prompt = (
                    "You are an expert Linux System Administrator and Security Auditor. "
                    "Analyze the provided terminal logs and terminal/dashboard screenshot. "
                    "Identify the root cause, flag security or configuration risks, "
                    "and output step-by-step Bash commands to fix the issue."
                )
                
                contents = []
                if uploaded_image:
                    img = Image.open(uploaded_image)
                    contents.append(img)
                
                if log_input:
                    contents.append(f"--- TERMINAL LOGS ---\n{log_input}\n---------------------")
                
                contents.append("Please provide: 1. Executive Summary & Root Cause, 2. Risk Assessment, 3. Step-by-step Remediation Commands.")

                response = client.models.generate_content(
                    model=model_choice,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.2,
                    )
                )

                st.success("Analysis Complete!")
                st.markdown("### 📋 Gemma 4 Audit Report")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
