from typing import Any, List, TypedDict

class GraphState(TypedDict):
    """
    State of the Graph for the nodes

    Attributtes : 
    question : question,
    web_search : to serach through web,
    documents : list of documents,
    generation : LLM generation
    """

    question : str
    web_search : bool
    generation : str
    documents : List[Any]