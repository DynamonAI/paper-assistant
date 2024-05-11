from .interfaces.openai import OpenAIInterface
from .reader import PdfReader

class AssistantEngine:
    def __init__(self, api_key, model_name, pdf_path):
        self.interface = OpenAIInterface(api_key, model_name)
        self.reader = PdfReader(pdf_path, interface=self.interface)

    def get_completion(self, query, **kwargs):
        prompt = f"Here is a question, please answer it carefully: {query}"
        answer = self.interface.completion(prompt, **kwargs)
        return answer
