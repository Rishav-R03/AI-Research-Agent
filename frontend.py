import streamlit as st
import requests
import json

# --- Configuration ---
FASTAPI_URL = "http://localhost:8000/research" # Replace with your server URL if different

st.set_page_config(page_title="Gemini Research Assistant", layout="wide")

st.title("📚 Gemini Research Assistant")
st.markdown("Enter a query below and let the AI assistant research it for you!")

# --- User Input ---
user_query = st.text_input("Enter your research query here:", placeholder="e.g., 'Latest advancements in quantum computing'")

# --- Research Button ---
if st.button("Start Research"):
    if not user_query:
        st.warning("Please enter a research query.")
    else:
        st.info(f"Researching: '{user_query}'...")
        with st.spinner("Processing your request... This might take a moment as the AI agent works..."):
            try:
                # Make a POST request to your FastAPI backend
                response = requests.post(FASTAPI_URL, json={"query": user_query})
                response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

                research_data = response.json()

                st.success("Research Complete!")

                # Display the structured response
                st.subheader("Research Summary")
                st.write(f"**Topic:** {research_data.get('topic', 'N/A')}")
                st.write(f"**Summary:**")
                st.markdown(research_data.get('summary', 'N/A'))

                st.subheader("Sources")
                sources = research_data.get('sources', [])
                if sources:
                    for source in sources:
                        st.markdown(f"- {source}")
                else:
                    st.write("No specific sources provided.")

                st.subheader("Tools Used")
                tools_used = research_data.get('tools_used', [])
                if tools_used:
                    st.write(", ".join(tools_used))
                else:
                    st.write("No tools explicitly reported by the agent.")

            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to the FastAPI server at {FASTAPI_URL}. "
                         "Please ensure the server is running.")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred during the request: {e}")
                if response.status_code == 500:
                    st.error(f"Server Error Details: {response.json().get('detail', 'No additional details.')}")
            except json.JSONDecodeError:
                st.error("Failed to decode JSON response from the server. Unexpected server response.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

st.markdown("---")
st.caption("Powered by Google Gemini and LangChain")