from dotenv import load_dotenv
from langchain.tools import tool

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
