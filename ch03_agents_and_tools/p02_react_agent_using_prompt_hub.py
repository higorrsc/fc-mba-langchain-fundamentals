from dotenv import load_dotenv
from langchain.tools import tool
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

load_dotenv()


@tool("calculator", return_direct=True)
def calculator(expression: str) -> str:
    """
    Evaluate a simple mathematical expression and return the result.
    """

    try:
        result = eval(expression)
    except Exception as e:
        return f"Error: {e}"

    return str(result)


@tool("web_search_mock")
def web_search_mock(query: str) -> str:
    """
    Mocked web search tool. Returns a hardcoded result.
    """

    data = {
        "Brazil": "Brasília",
        "France": "Paris",
        "Germany": "Berlin",
        "Italy": "Rome",
        "Spain": "Madrid",
        "United States": "Washington, D.C.",
    }

    for country, capital in data.items():
        if country.lower() in query.lower():
            return f"The capital of {country} is {capital}."

    return "I don't know the capital of that country."


llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
)
tools = [calculator, web_search_mock]

prompt = hub.pull("hwchase17/react")

agent_chain = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    # stop_sequence=False,
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent_chain,
    tools=tools,
    verbose=True,
    # handle_parsing_errors="Invalid format. Either provide an "
    # "Action with Action Input, or a Final Answer only.",
    # max_iterations=3,
)

print(agent_executor.invoke({"input": "What is the capital of Iran?"}))
print(agent_executor.invoke({"input": "What is the capital of France?"}))
print(agent_executor.invoke({"input": "How much is 10+10?"}))
