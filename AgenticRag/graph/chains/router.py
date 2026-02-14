from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from model import llm


class RouteQuery(BaseModel):
	datasource: Literal["retrieve", "web_search"] = Field(
		description="Route question to 'retrieve' for vectorstore lookup or 'web_search' for fresh/external information."
	)


structured_router = llm.with_structured_output(RouteQuery)

system = """You are a routing assistant for a RAG system.
Choose exactly one datasource for the user question:
- retrieve: when the question is likely answerable from internal/vectorstore knowledge.
- web_search: when the question needs up-to-date, external, or broad web information.
Return only one choice."""

router_prompt = ChatPromptTemplate.from_messages(
	[
		("system", system),
		("human", "Question: {question}"),
	]
)

question_router = router_prompt | structured_router

