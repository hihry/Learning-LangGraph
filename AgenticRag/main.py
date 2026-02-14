import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from graph.graph import app

def main():
    print("AgenticRag project boilerplate is ready!")
    # Add your main logic here

if __name__ == "__main__":
    question = "how to make a sandwhich "
    result = app.invoke({"question": question})
    print(result)


    