from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from model import llm

@tool
def Triple(num: float) -> float:
    """Return the input multiplied by three.

    Args:
        num (float): A numeric value (or value convertible to float).

    Returns:
        float: The input value times 3.

    Raises:
        TypeError: If `num` cannot be converted to float.
        ValueError: If `num` conversion to float raises ValueError.
    """
    try:
        return float(num) * 3
    except (TypeError, ValueError) as e:
        raise TypeError("num must be a number or convertible to float") from e

tools=[TavilySearch(max_results=1) , Triple]

llm = llm.bind_tools(tools)