from typing import Any , Dict

from graph.chains.generate import generate_chain
from graph.state import GraphState

def Generate(state: GraphState) -> Dict[str, Any]:
    """
    Generate an answer using the generate_chain, given the current graph state.
    Expects state to have 'question' and 'documents' (list of Document or str).
    Returns updated state with 'generation' field.
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state("documents")
    # Prepare context string from documents
    context = "\n".join([
        d.page_content if hasattr(d, "page_content") else str(d)
        for d in documents
    ])
    # Run the generation chain
    generation = generate_chain.invoke({"question": question, "context": context})
    # Update state
    state["generation"] = generation
    return state
    
