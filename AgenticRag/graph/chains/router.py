import re
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

from model import llm


class RouteQuery(BaseModel):
	datasource: Literal["retrieve", "web_search"] = Field(
		description="Route question to 'retrieve' for vectorstore lookup or 'web_search' for fresh/external information."
	)


structured_router = llm.with_structured_output(RouteQuery)

system = """You are a routing assistant for a RAG system.
Choose exactly one datasource for the user question:
- retrieve: use this only for AI/LLM/agent/RAG/vector-db/chains/langgraph/langchain topics that are likely covered by the internal ChromaDB.
- web_search: when the question needs up-to-date, external, or broad web information.
If the question is not clearly AI-related, prefer web_search.
Return only one choice."""

router_prompt = ChatPromptTemplate.from_messages(
	[
		("system", system),
		("human", "Question: {question}"),
	]
)


AI_DOMAIN_PATTERNS = [
	r"\b(llm|gpt|agent|rag|langgraph|langchain|vector\s?db|embedding|prompt)\b",
	r"\b(hallucination|retrieval|chroma|chain[- ]?of[- ]?thought)\b",
]

WEB_SEARCH_HINTS = [
	r"\b(today|latest|current|news|weather|price|stock|cricket|football)\b",
	r"\b(who is|where is|when did|population|capital of|recipe|sandwich)\b",
]


def _heuristic_route(question: str) -> str | None:
	question_lower = question.lower()
	if any(re.search(pattern, question_lower) for pattern in AI_DOMAIN_PATTERNS):
		return "retrieve"
	if any(re.search(pattern, question_lower) for pattern in WEB_SEARCH_HINTS):
		return "web_search"
	return None


def _route_query(payload: dict) -> RouteQuery:
	question = payload["question"]

	heuristic = _heuristic_route(question)
	if heuristic is not None:
		return RouteQuery(datasource=heuristic)

	try:
		result = (router_prompt | structured_router).invoke({"question": question})
		return RouteQuery(datasource=result.datasource)
	except Exception:
		return RouteQuery(datasource="web_search")


question_router = RunnableLambda(_route_query)

