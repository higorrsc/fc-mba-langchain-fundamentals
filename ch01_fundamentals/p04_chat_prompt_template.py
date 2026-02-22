from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

load_dotenv()

prompt_system = (
    "system",
    "you are an assistant that answers questions in a {style} style",
)
prompt_user = (
    "user",
    "{question}",
)

chat_prompt = ChatPromptTemplate([prompt_system, prompt_user])

messages = chat_prompt.format_messages(
    style="funny",
    question="Who is Alan Turing?",
)

for m in messages:
    print(f"{m.type}: {m.content}")

# model = ChatOpenAI(
#     model="gpt-5-nano",
#     temperature=0.5,
# )
# answer = model.invoke(messages)
# print(answer.content)


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)
answer = model.invoke(messages)
print(answer.content)
