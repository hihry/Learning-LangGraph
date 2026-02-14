try:
	from langchain import hub
except ImportError:
	from langchain_classic import hub

from model import llm
from langchain_core.output_parsers import StrOutputParser

prompt = hub.pull("rlm/rag-prompt")

generate_chain=prompt | llm | StrOutputParser()