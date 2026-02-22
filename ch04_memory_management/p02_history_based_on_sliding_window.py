"""
Conversational LangChain Example (Python 3.13+)
-----------------------------------------------

Features:
- Modern typing (PEP 695)
- Clean separation of concerns
- Config constants
- Proper main() entrypoint
"""

from __future__ import annotations

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# =========================
# Configuration
# =========================

MODEL_NAME = "gpt-5-nano"
TEMPERATURE = 0.9
MAX_HISTORY_TOKENS = 2
SESSION_ID = "demo-session"


# =========================
# Type Aliases
# =========================

type SessionStore = dict[str, InMemoryChatMessageHistory]
type Payload = dict[str, object]


# =========================
# Session Store
# =========================

session_store: SessionStore = {}


# =========================
# History Management
# =========================


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Retrieve or create session history."""

    return session_store.setdefault(session_id, InMemoryChatMessageHistory())


# =========================
# Input Preparation
# =========================


def prepare_inputs(payload: Payload) -> dict[str, object]:
    """Trim conversation history before sending to model."""

    raw_history = payload.get("history", [])
    history: list[BaseMessage] = raw_history if isinstance(raw_history, list) else []

    trimmed_history = trim_messages(
        history,
        token_counter=len,
        max_tokens=MAX_HISTORY_TOKENS,
        strategy="last",
        start_on="human",
        include_system=True,
        allow_partial=False,
    )

    return {
        "input": payload.get("input", ""),
        "history": trimmed_history,
    }


# =========================
# Chain Builder
# =========================


def build_conversational_chain() -> RunnableWithMessageHistory:
    """Create conversational chain with memory support."""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a helpful assistant that answers "
                "with a short joke when possible.",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )

    llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    prepare = RunnableLambda(prepare_inputs)
    base_chain = prepare | prompt | llm

    return RunnableWithMessageHistory(
        runnable=base_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )


# =========================
# Demo Runner
# =========================


def run_demo(chain: RunnableWithMessageHistory) -> None:
    """Run example interactions."""

    config = {"configurable": {"session_id": SESSION_ID}}

    interactions = [
        "My name is Higor. Reply only with 'OK' and do not mention my name.",
        "Tell me a one-sentence fun fact. Do not mention my name.",
        "What is my name?",
    ]

    for user_input in interactions:
        response = chain.invoke(
            input={"input": user_input},
            config=config,  # type: ignore
        )
        print(f"Assistant: {response.content}")
        print("-" * 40)


# =========================
# Entrypoint
# =========================


def main() -> None:
    """Main entrypoint for the application."""

    load_dotenv()
    chain = build_conversational_chain()
    run_demo(chain)


if __name__ == "__main__":
    main()
