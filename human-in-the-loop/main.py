# from typing import TypedDict

# from langgraph.graph import END, START, StateGraph
# from langgraph.checkpoint.memory import MemorySaver


# class State(TypedDict):
#     input: str
#     user_feedback: str


# def step1(state: State):
#     print("step1")
#     return state


# def step2(state: State):
#     print("step2")
#     return state


# def human_feedback(state: State):
#     print("human_feedback")
#     return state


# def step3(state: State):
#     print("step3")
#     return state


# workflow = StateGraph(State)

# workflow.add_node("step1", step1)
# workflow.add_node("step2", step2)
# workflow.add_node("human_feedback", human_feedback)
# workflow.add_node("step3", step3)

# workflow.add_edge(START, "step1")
# workflow.add_edge("step1", "step2")
# workflow.add_edge("step2", "human_feedback")
# workflow.add_edge("human_feedback", "step3")
# workflow.add_edge("step3", END)

# memory = MemorySaver()

# app = workflow.compile(checkpointer=memory, interrupt_before=["human_feedback"])

# # Print the mermaid diagram
# mermaid_str = app.get_graph().draw_mermaid()
# print(mermaid_str)

# # Save to file for PNG generation
# with open("workflow.mmd", "w") as f:
#     f.write(mermaid_str)

# print("\nMermaid diagram saved to workflow.mmd")

# from dotenv import load_dotenv
# load_dotenv()

# from langchain_core.tools import tool
# from langchain_tavily import TavilySearch
# from model import llm

# @tool
# def Triple(num: float) -> float:
#     """Return the input multiplied by three.

#     Args:
#         num (float): A numeric value (or value convertible to float).

#     Returns:
#         float: The input value times 3.

#     Raises:
#         TypeError: If `num` cannot be converted to float.
#         ValueError: If `num` conversion to float raises ValueError.
#     """
#     try:
#         return float(num) * 3
#     except (TypeError, ValueError) as e:
#         raise TypeError("num must be a number or convertible to float") from e


# tools=[TavilySearch(max_results=1) , Triple]

# llm = llm.bind_tools(tools)