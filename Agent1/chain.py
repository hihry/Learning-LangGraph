from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app import llm

reflection_template = ChatPromptTemplate.from_messages(
    [
        ('system',
         "You are a great X's post grader, reading and recommending changes to the twitter posts"
         "Always provide details recommendations"
         
        ),
        MessagesPlaceholder(variable_name='messages')
    ]
)
generator_template = ChatPromptTemplate.from_messages(
    [
        ('system',
         "You are a great Narrator or story teller for twitter"
         "You generate best twitter posts"
         "You recieve recommendations and you work on it to enhance the content of the posts"
        ),
    ]
)
