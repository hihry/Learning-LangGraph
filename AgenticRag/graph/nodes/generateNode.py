from typing import Any , Dict

from graph.chains.generate import generate_chain
from graph.state import GraphState


def _build_fallback_answer(question: str, context: str) -> str:
    snippet = context[:600].strip()
    return (
        "I could not call the language model right now (likely API rate limit). "
        f"Based on available context, here is a quick answer to '{question}':\n\n"
        f"{snippet if snippet else 'No context available.'}"
    )


def Generate(state: GraphState) -> Dict[str, Any]:
    """
    Generate an answer using the generate_chain, given the current graph state.
    Expects state to have 'question' and 'documents' (list of Document or str).
    Returns updated state with 'generation' field.
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    # Prepare context string from documents
    context = "\n".join([
        d.page_content if hasattr(d, "page_content") else str(d)
        for d in documents
    ])
    # Run the generation chain
    try:
        generation = generate_chain.invoke({"question": question, "context": context})
    except Exception:
        generation = _build_fallback_answer(question, context)
    # Update state
    state["generation"] = generation
    return {
        "question": question,
        "documents": documents,
        "generation": generation,
    }
    
