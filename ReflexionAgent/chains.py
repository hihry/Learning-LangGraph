from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser, PydanticToolsParser
from langchain_core.messages import HumanMessage, BaseMessage
import datetime
from schemas import AnswerQuestion, ReflectionFromAnswer
from model import llm

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
out_tools_parser = JsonOutputToolsParser()
final_output_parser = PydanticToolsParser(tools=[AnswerQuestion])

# Define the placeholder variable for messages
messages_placeholder = MessagesPlaceholder(variable_name="messages")


# Original instructions
first_instructions = "write a detailed report with 250 words"

# Revised instructions with required details and reference
revised_instructions = (
    "Revise your previous answer for clarity, depth, and accuracy. "
    "Ensure the report is well-structured, includes critical analysis, and provides actionable recommendations. "
    "Cite at least one reputable reference, such as www.example.com."
)


actor_systems_prompt = ChatPromptTemplate.from_messages(
    [
        'system',
        """
        You are an expert Researcher
        Current time : {time}
        1.{first_instructions}
        2.Reflect and critique your answer. Make sure for improvements
        3.Recommend search queries to research infromation
        """,
        messages_placeholder
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)
first_responder = actor_systems_prompt.partial(
    first_instructions="write a detailed report with 250 words"
)
second_responder = actor_systems_prompt.partial(
    first_instructions=revised_instructions
)
# Build the chain: prompt -> llm with tools -> pydantic parser
chain_extrat = first_responder | llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion') | final_output_parser
chain_reflect =second_responder | llm.bind_tools(tools=[ReflectionFromAnswer] , tool_choice='ReflectionFromAnswer') 

if __name__ == "__main__":
    human_message = HumanMessage(content="Generate a detailed report on football leagues.")
    parsed_output = chain_extrat.invoke({"messages": [human_message]})
    print(parsed_output)


