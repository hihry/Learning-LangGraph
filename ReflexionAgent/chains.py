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
revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""



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
    first_instructions=revise_instructions
)
# Build the chain: prompt -> llm with tools -> pydantic parser
chain_extrat = first_responder | llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion') 
chain_reflect =second_responder | llm.bind_tools(tools=[ReflectionFromAnswer] , tool_choice='ReflectionFromAnswer') 
chain_k = chain_extrat | final_output_parser

if __name__ == "__main__":
    human_message = HumanMessage(content="Generate a detailed report on football leagues.")
    parsed_output = chain_k.invoke({"messages": [human_message]})
    print(parsed_output)


