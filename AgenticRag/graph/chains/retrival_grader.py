import re

from pydantic import Field, BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from model import llm

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Binary relevance score for the document. Expected values: 'Yes' (relevant) or 'No' (not relevant)."
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

final = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)


def _extract_binary_score(text: str) -> str:
    match = re.search(r"\b(yes|no)\b", text, flags=re.IGNORECASE)
    return match.group(1).lower() if match else "no"


def _grade_with_fallback(payload: dict) -> GradeDocuments:
    question = payload["question"]
    document = payload["document"]

    try:
        result = (final | structured_llm_grader).invoke(
            {"question": question, "document": document}
        )
        if isinstance(result, GradeDocuments):
            return result
        return GradeDocuments(binary_score=str(result.binary_score).lower())
    except Exception:
        return GradeDocuments(binary_score="no")


relevant_retrive_chain = RunnableLambda(_grade_with_fallback)

