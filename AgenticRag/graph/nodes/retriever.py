from typing import Any, Dict

from graph.state import GraphState
from ingestion import get_retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")
    question = state["question"]

    try:
        retriever = get_retriever()
        documents = retriever.invoke(question)
    except Exception:
        documents = []
    return {"documents": documents, "question": question}