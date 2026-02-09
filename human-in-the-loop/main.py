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

