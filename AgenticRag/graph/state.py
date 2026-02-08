from typing import TypedDict, List

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
    web_search : str
    generation : str
    documents : List[str]