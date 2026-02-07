from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
# Load environment variables
load_dotenv()

# List of URLs to load (populate with your own URLs)
URLS = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]
class SentenceTransformerEmbeddings:
    """
    Minimal LangChain-compatible wrapper around sentence-transformers.
    Provides embed_documents and embed_query used by Chroma.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode([text], convert_to_numpy=True)[0].tolist()

# Chroma persist directory
CHROMA_PERSIST_DIR = "chroma_db"


def ingest_web_pages_to_chroma(urls: list[str] = URLS) -> Chroma:
    """
    Load web pages, chunk them using RecursiveCharacterTextSplitter,
    and ingest into ChromaDB.
    """
    # 1. Load documents from URLs
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]
    print(f"Loaded {len(docs_list)} documents from {len(urls)} URLs")

    # 2. Split documents into chunks using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs_list)
    print(f"Split into {len(doc_splits)} chunks")

    # 3. Create embeddings
    embeddings = SentenceTransformerEmbeddings()

    # 4. Ingest into Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )
    vectorstore.persist()
    print(f"Ingested {len(doc_splits)} chunks into Chroma at '{CHROMA_PERSIST_DIR}'")

    return vectorstore


def get_retriever(k: int = 4):
    """
    Load existing Chroma vectorstore and return a retriever.
    """
    embeddings = SentenceTransformerEmbeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(search_kwargs={"k": k})


if __name__ == "__main__":
    # Run ingestion
    vectorstore = ingest_web_pages_to_chroma(URLS)

    # Test retriever
    retriever = get_retriever()
    results = retriever.invoke("What is prompt engineering?")
    print(f"\nRetrieved {len(results)} documents:")
    for i, doc in enumerate(results, 1):
        print(f"\n--- Document {i} ---")
        print(doc.page_content[:300])
