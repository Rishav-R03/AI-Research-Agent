## AI-Powered Research Assistant
### Project Overview
The AI-Powered Research Assistant is an intelligent web application designed to automate and streamline the research process. Built on cutting-edge Large Language Model (LLM) technology, this tool acts as your personal research aide, capable of dynamically gathering, synthesizing, and structuring information from various web sources based on your queries.

Forget spending hours sifting through search results. This assistant quickly provides concise summaries, highlights key sources, and maintains a searchable history of your past inquiries, boosting efficiency and insight.

### Features
Intelligent Agent Core: Powered by LangChain and Google Gemini 1.5 Flash, the agent dynamically selects and orchestrates specialized tools (Web Search via DuckDuckGo, Wikipedia) to fulfill complex research queries.
Structured & Actionable Output: Delivers research results in a consistently structured format, including topic, summary, sources, and tools_used, thanks to Pydantic validation, ensuring clarity and downstream compatibility.
Persistent Research History: Integrates with a SQLite database via SQLAlchemy to securely store all past research queries and their structured outputs, enabling easy retrieval and review.
Scalable API Backend: A robust FastAPI application serves as the project's backbone, providing a clean, efficient, and scalable API for interacting with the AI agent.
Intuitive Web Interface: Features a user-friendly frontend built with Streamlit, offering a clean, real-time interface for submitting queries and visualizing detailed research summaries.
Automated Information Gathering: Significantly reduces manual research time by automating data collection and synthesis from disparate web sources.
### Technologies Used
Python: The core programming language.
LangChain: Framework for developing LLM-powered applications.
Google Gemini API: State-of-the-art Large Language Model for advanced reasoning and generation.
FastAPI: High-performance web framework for the backend API.
Streamlit: For creating the interactive web user interface.
Pydantic: For data validation and structured output.
SQLAlchemy: Python SQL toolkit and Object-Relational Mapper (ORM) for database interaction.
SQLite: Lightweight, file-based database for persistent storage.
python-dotenv: For managing environment variables (API keys).
DuckDuckGoSearchRun, WikipediaQueryRun: LangChain community tools for web scraping and information retrieval.
### Getting Started
Follow these steps to set up and run the AI-Powered Research Assistant locally.

Prerequisites
Python 3.9+
An API key from Google AI Studio for Gemini access.
(Optional, but recommended for more advanced search): API keys for services like Google Search API or SerpAPI if you extend tools.py beyond DuckDuckGo/Wikipedia.
Installation
Clone the repository:

git clone [repolink](https://github.com/Rishav-R03/AI-Research-Agent)
cd AI-Research-Agent
Create a virtual environment (recommended):

Bash

python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
Install dependencies:

Bash

pip install -r requirements.txt
(If you don't have a requirements.txt yet, you can generate one after installing everything with pip freeze > requirements.txt)

Minimum required packages:

langchain-google-genai
langchain-community
fastapi
uvicorn
streamlit
requests
python-dotenv
pydantic~=2.0
sqlalchemy
greenlet # often needed for SQLAlchemy
Configuration
Create a .env file: In the root directory of your project, create a file named .env and add your Google Gemini API key:
Code snippet

GOOGLE_API_KEY="<Enter_your_key>"
Replace "YOUR_GOOGLE_GEMINI_API_KEY" with your actual key.
Running the Application
This project consists of two main components: a FastAPI backend (API server) and a Streamlit frontend (web interface).

Start the FastAPI Backend:
Open your terminal and run:

Bash

uvicorn server:app --reload --port 8000
This will start the API server, typically accessible at http://localhost:8000. Keep this terminal open.

Start the Streamlit Frontend:
Open a new terminal, navigate to your project directory (and activate your venv if you closed it), and run:

Bash

streamlit run frontend.py
This will open the Streamlit application in your web browser.

Demo
Check out a quick demonstration of the AI-Powered Research Assistant in action!

Video Demonstration
(Replace YOUR_VIDEO_ID with the actual ID of your YouTube demo video. You can also use a GIF if preferred.)

Screenshots
![image](https://github.com/user-attachments/assets/c64bbd08-8343-4085-8e49-f25b397473f8)


1. Initial Query Input(Replace assets/screenshot-query.png with the actual path to your screenshot.)
![image](https://github.com/user-attachments/assets/883ef9f8-d6be-4d68-a0f6-948746288c7a)

2. Research Results Display(Replace assets/screenshot-results.png with the actual path to your screenshot.)

![image](https://github.com/user-attachments/assets/05abd413-d4ff-4610-a6f3-789623d6a7d8)


# Future Enhancements
Advanced Tooling: Integration with more specialized tools like Google Search API, ArXiv API, or PDF document analysis (RAG).
User Authentication: Implement user accounts and personalized research history.
Configurable Agent Behavior: Allow users to customize agent persona, tool usage, and output constraints.
Iterative Research: Enable multi-turn conversations for refining research results or exploring sub-topics.
Enhanced Output Formats: Options to export research to Markdown, PDF, or other structured documents.
Cost Optimization: Implement token usage tracking and caching mechanisms.
# Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

# License
This project is licensed under the MIT License - see the LICENSE file for details.(Create a LICENSE file in your repository if you haven't already.)

# Contact
Rishav Raj https://www.linkedin.com/in/rishav-raj-15b077249/  | rishav042023@gmail.com
Project Link: [project_repo](https://github.com/Rishav-R03/AI-Research-Agent)
