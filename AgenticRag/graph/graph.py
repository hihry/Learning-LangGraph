from graph.const import WEB_SEARCH, RETRIEVE, GENERATE, GRADE_DOCUMENTS, NODES

from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination import hallucination_grader
from graph.chains.router import question_router


def route_after_grading(state: GraphState) -> str:
	return WEB_SEARCH if state.get("web_search", False) else GENERATE


def route_question(state: GraphState) -> str:
	question = state["question"]
	result = question_router.invoke({"question": question})
	return result.datasource


def route_after_generation(state: GraphState) -> str:
	question = state["question"]
	documents = state["documents"]
	generation = state["generation"]

	hallucination_score = hallucination_grader.invoke(
		{"documents": documents, "generation": generation}
	)
	if not hallucination_score.binary_score:
		return WEB_SEARCH

	answer_score = answer_grader.invoke(
		{"question": question, "generation": generation}
	)
	return END if answer_score.binary_score else GENERATE


builder = StateGraph(GraphState)
builder.add_node(RETRIEVE, NODES[RETRIEVE])
builder.add_node(GRADE_DOCUMENTS, NODES[GRADE_DOCUMENTS])
builder.add_node(WEB_SEARCH, NODES[WEB_SEARCH])
builder.add_node(GENERATE, NODES[GENERATE])

builder.add_conditional_edges(
	START,
	route_question,
	{
		RETRIEVE: RETRIEVE,
		WEB_SEARCH: WEB_SEARCH,
	},
)
builder.add_edge(RETRIEVE, GRADE_DOCUMENTS)

builder.add_conditional_edges(
	GRADE_DOCUMENTS,
	route_after_grading,
	{
		WEB_SEARCH: WEB_SEARCH,
		GENERATE: GENERATE,
	},
)

builder.add_edge(WEB_SEARCH, GENERATE)
builder.add_conditional_edges(
	GENERATE,
	route_after_generation,
	{
		WEB_SEARCH: WEB_SEARCH,
		GENERATE: GENERATE,
		END: END,
	},
)

app = builder.compile()
