import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool # Assuming these are defined correctly in tools.py

# Load environment variables from .env file
load_dotenv()

# --- API Key Setup ---
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError(
        "GOOGLE_API_KEY environment variable not set. "
        "Please ensure it's in your .env file or system environment."
    )

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_api_key)

# Tools definition
tools = [search_tool, wiki_tool, save_tool]

### Output Schema Definition
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

### Prompt Template Definition
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate research papers.
            Answer the user query and use necessary tools.
            After generating the response in the specified format, you should also consider if the information
            should be saved. If so, use the 'save_txt' tool.
            Wrap the output in this format and provide no other text in your final answer to the user:
            \n{format_instructions}
            """,
        ),
        (
            "placeholder", "{chat_history}"
        ),
        (
            "human", "{query}"
        ),
        (
            "placeholder", "{agent_scratchpad}"
        ),
    ]
).partial(format_instructions=parser.get_format_instructions())

# --- Function to create and return the agent executor and parser ---
def get_research_agent_executor_and_parser():
    """
    Initializes and returns the LangChain agent executor and the Pydantic parser.
    This function encapsulates the agent setup logic for reusability.
    """
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor, parser, ResearchResponse # Return ResearchResponse for type hinting in FastAPI

# --- Original local CLI execution (now under a guard) ---
if __name__ == "__main__":
    agent_executor, parser, _ = get_research_agent_executor_and_parser() # We don't need ResearchResponse here

    print("\n--- Local Agent Execution (CLI) ---")
    try:
        user_query = input("Enter a query to run! ")
        raw_response = agent_executor.invoke({"query": user_query})

        llm_output_text = raw_response.get('output', '')

        try:
            parsed_response = parser.parse(llm_output_text)
            print("\n--- Parsed Research Response ---")
            print(f"Topic: {parsed_response.topic}")
            print(f"Summary: {parsed_response.summary}")
            print(f"Sources: {parsed_response.sources}")
            print(f"Tools Used: {parsed_response.tools_used}")

            data_to_save = f"Topic: {parsed_response.topic}\nSummary: {parsed_response.summary}\nSources: {', '.join(parsed_response.sources)}\nTools Used: {', '.join(parsed_response.tools_used)}"
            save_tool.run(data_to_save) # Call the save_tool directly

        except Exception as parse_error:
            print(f"Error parsing LLM output: {parse_error}")
            print(f"Raw LLM Output: {llm_output_text}")

    except Exception as e:
        print(f"An error occurred during agent execution: {e}")
        print("Ensure your LangChain setup is correct and your API keys are valid.")