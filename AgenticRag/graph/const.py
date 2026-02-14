from graph.nodes import Generate, grade_documents, retrieve, web_search

RETRIEVE = "retrieve"
GRADE_DOCUMENTS = "grade_documents"
GENERATE = "generate"
WEB_SEARCH = "web_search"

NODES = {
	RETRIEVE: retrieve,
	GRADE_DOCUMENTS: grade_documents,
	GENERATE: Generate,
	WEB_SEARCH: web_search,
}

__all__ = [
	"RETRIEVE",
	"GRADE_DOCUMENTS",
	"GENERATE",
	"WEB_SEARCH",
	"NODES",
]