from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from core.tools import search_vdb, search_JSON
from langchain.agents import create_react_agent, AgentExecutor

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Almacén de sesión en memoria
store = {}


# Function to create and configure ReactAgent with the required prompt and tools
def create_agent_with_prompt(llm, tools):
    # Create a prompt for the ReactAgent
    prompt = PromptTemplate(
        input_variables=["input", "tool_names", "agent_scratchpad"],
        template=""""
        You are an intelligent assistant that always thinks in English, capable of providing funny responses using the tools: {tool_names}.
        Here are the available tools: {tools}

        If you need to call a tool, respond using this exact format:

        Thought: [Explain your reasoning]
        Action: Tool to call
        Action Input: Tool input in JSON format with no additional quotes around the entire input

        If a tool response is received:
        - Extract all the relevant information to give a proper answer to user query.
        - Provide a final answer in the following format:

        Final Answer: [Your final response to the query: {input}. Include all relevant information with details.Answer always in spanish]

        Query: {input}

        {agent_scratchpad}
        """,
    )

    # Create the ReactAgent with the prompt and tools
    react_agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor.from_agent_and_tools(
        react_agent, tools=tools, handle_parsing_errors=True
    )


# Función principal para procesar la entrada del usuario
def ProcessUserInput(user_input, temperature):
    # Inicializa el modelo
    llm = ChatOpenAI(
        model_name="gpt-4o", temperature=temperature, openai_api_key=api_key
    )

    tools = [search_vdb, search_JSON]

    agent_executor = create_agent_with_prompt(llm, tools)

    # Call the agent with user input to process the query
    try:
        agent_response = agent_executor.invoke({"input": user_input})
        response_content = (
            agent_response["output"]
            if "output" in agent_response
            else str(agent_response)
        )
    except Exception as e:
        response_content = f"Error processing query: {str(e)}"


    return {"response": response_content, "documents": []}

