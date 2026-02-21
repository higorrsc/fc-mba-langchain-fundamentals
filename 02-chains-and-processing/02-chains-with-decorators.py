from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import chain
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


@chain
def square(number: int) -> dict[str, int]:
    """
    Square a number.
    """

    return {"square_result": number**2}


question_template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell me a joke with my name!",
)

question_template_2 = PromptTemplate(
    input_variables=["square_result"],
    template="Tell me about the number {square_result}",
)

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)

chain = question_template | model

answer = chain.invoke({"name": "Higor"})
print(answer.content)

chain_2 = square | question_template_2 | model

answer_2 = chain_2.invoke(10)
print(answer_2.content)
