from graph.chains.answer_grader import answer_grader
from graph.chains.retrival_grader import relevant_retrive_chain
from graph.chains.generate import generate_chain
from ingestion import get_retriever


def test_retrival_grader_model_binary_score_yes_or_no():
	question = "make a sandwich?"
	retriever = get_retriever(k=1)
	docs = retriever.invoke(question)

	result = relevant_retrive_chain.invoke(
		{"question": question, "document": docs[0].page_content}
	)

	assert result.binary_score.lower() in {"yes", "no"}


def test_hallcination_grader_model_binary_score_bool():
	question = "make a sandwich?"
	retriever = get_retriever(k=1)
	docs = retriever.invoke(question)

	generation = generate_chain.invoke(
		{"question": question, "context": docs[0].page_content}
	)
	result = answer_grader.invoke(
		{"question": question, "generation": generation}
	)

	assert isinstance(result.binary_score, bool)


