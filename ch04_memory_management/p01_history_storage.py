from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Get or create a chat message history for a session.
    """

    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()

    return session_store[session_id]


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0.9,
)
chain = prompt | llm

session_store: dict[str, InMemoryChatMessageHistory] = {}

conversational_chain = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "demo-session"}}


# === Interactions ===
response1 = conversational_chain.invoke(
    input={"input": "Hello, my name is Higor. how are you?"},
    config=config,  # type: ignore
)
print("Assistant: ", response1.content)
print("-" * 30)

response2 = conversational_chain.invoke(
    input={"input": "Can you repeat my name?"},
    config=config,  # type: ignore
)
print("Assistant: ", response2.content)
print("-" * 30)

response3 = conversational_chain.invoke(
    input={"input": "Can you repeat my name in a motivation phrase?"},
    config=config,  # type: ignore
)
print("Assistant: ", response3.content)
print("-" * 30)
