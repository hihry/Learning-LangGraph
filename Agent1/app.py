
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from chain import gen_chain, refl_chain

gen = 'gen'
ref = 'ref'

class GraphState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]

def generate(state : GraphState):
    return {'messages' : gen_chain.invoke({'messages' : state["messages"]})}

def reflect(state : GraphState):
    res = refl_chain.invoke({'messages' : state["messages"]})
    return {'messages' : [HumanMessage(content=res.content)]}

def counter(state : GraphState):
    if len(state['messages']) > 6:
        return END
    return ref

graph = StateGraph(state_schema=GraphState)
graph.add_node(gen , generate)
graph.add_node(ref , reflect)
graph.add_edge(START , gen)
graph.add_conditional_edges(gen , counter, path_map={END:END , ref:ref})
graph.add_edge(ref , gen)

build = graph.compile()
print(build.get_graph().draw_mermaid())

if __name__ == '__main__':
    print('hi')
    input = HumanMessage(content="I want to make this tweet look professional"
                         "Bruh this is hilarious how trump is the US president, He hella is super funny and so stupid of scheming to occuping GreendLand by force I am laughing my ass off")
    build.invoke(input)
