from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import sys
import io

# Temporarily capture stdout to prevent LangChain's verbose output from appearing in the server logs directly,
# unless it's a specific error. You can adjust this based on your logging needs.
# For production, consider proper logging configuration.
original_stdout = sys.stdout
sys.stdout = io.StringIO()

try:
    from main import get_research_agent_executor_and_parser
    # Restore stdout after importing, as it's often verbose during import
    sys.stdout = original_stdout
except Exception as e:
    sys.stdout = original_stdout # Ensure stdout is restored even on import error
    print(f"Error importing agent from main.py: {e}")
    print("Please ensure main.py is correctly set up and free of errors.")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="Research Agent API",
    description="API for a LangChain-powered research assistant using Google Gemini.",
    version="1.0.0"
)

# Initialize the agent executor and parser globally when the server starts
# This avoids re-initializing for every request
agent_executor, parser, ResearchResponse = get_research_agent_executor_and_parser()

# Request model for the API endpoint
class ResearchRequest(BaseModel):
    query: str

# API endpoint for research
@app.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    """
    Processes a research query using the LangChain agent and returns structured data.
    """
    print(f"Received research query: {request.query}")
    try:
        # Invoke the LangChain agent with the user's query
        raw_response = await agent_executor.ainvoke({"query": request.query})

        # The agent's raw output (should be the Pydantic-formatted string)
        llm_output_text = raw_response.get('output', '')

        try:
            # Parse the LLM's output into the Pydantic model
            parsed_response = parser.parse(llm_output_text)

            # Note: The `save_tool` is designed to be called by the agent.
            # If the agent decides to use it, it will execute.
            # If you want to ensure it's saved every time, you could call save_tool.run() here
            # For example:
            # data_to_save = f"Topic: {parsed_response.topic}\nSummary: {parsed_response.summary}\nSources: {', '.join(parsed_response.sources)}\nTools Used: {', '.join(parsed_response.tools_used)}"
            # save_tool.run(data_to_save) # This would require importing save_tool here from tools.py

            print("Research successful, returning parsed response.")
            return parsed_response

        except Exception as parse_error:
            print(f"Error parsing LLM output: {parse_error}")
            print(f"Raw LLM Output: {llm_output_text}")
            raise HTTPException(status_code=500, detail=f"Failed to parse research output: {parse_error}")

    except Exception as e:
        print(f"Error during agent execution: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during research: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("FastAPI server started on http://0.0.0.0:8000")