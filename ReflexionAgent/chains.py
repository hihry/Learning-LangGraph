from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser, PydanticToolsParser
from langchain_core.messages import HumanMessage, BaseMessage
import datetime
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

actor_systems_prompt = ChatPromptTemplate.from_messages(
    [
        'system',
        """
        You are an expert Researcher
        Current time : {time}
        1.{first_instructions}
        2.Reflect and critique your answer. Make sure for improvements
        3.Recommend search queries to research infromatoin
        """
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)