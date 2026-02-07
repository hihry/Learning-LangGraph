from langchain_tavily import TavilySearch
from langchain_core.tools import  StructuredTool
from langchain.tools import tool_node
from schemas import AnswerQuestion, ReflectionFromAnswer

tavily_searc=TavilySearch(max_results=5)

def run_queries(search_queris : list[str], **kwargs):
    return tavily_searc.batch([{"query" :query} for query in search_queris])
# Example: Using TavilySearchResults as a tool
execute_tools = tool_node(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReflectionFromAnswer.__name__)
    ]
)
# search_tool = StructuredTool(
#     name="tavily_search",
#     description="Searches the web using Tavily and returns relevant results.",
#     func=TavilySearchResults().run,
#     args_schema=None  # TavilySearchResults may have its own schema, update if needed
# )



# Example ToolNode usage (for chaining tools)
# tool_node = ToolNode(
#     tool=search_tool,
#     next_tool=None  # You can chain more tools if needed
# )

# # Example function to use Tavily and format results into AnswerQuestion schema
# def search_and_format(query: str) -> AnswerQuestion:
#     results = TavilySearchResults().run(query)
#     # Format results into AnswerQuestion (customize as needed)
#     return AnswerQuestion(
#         answer=results,
#         reflection=None,
#         search_queries=[query]
#     )

# # Example usage
# if __name__ == "__main__":
#     query = "latest AI research papers"
#     answer = search_and_format(query)
#     print(answer)
