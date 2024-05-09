import os
from src.engine import AssistantEngine

openai_api_key = os.getenv("OPENAI_API_KEY")
engine = AssistantEngine(openai_api_key, model_name="gpt-3.5-turbo", pdf_path="/home/hl3352/Downloads/2301.10226.pdf")
print("------"*10)
engine.get_user_input("Who are the authors?")
print("------"*10)
engine.get_user_input("What is the title of this paper?")
print("------"*10)
engine.get_user_input("What was proposed in this paper?")
