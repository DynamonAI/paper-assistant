from .base_interface import BaseInterface
from tqdm import tqdm
import openai

system_prompt = "You are an assistant dedicated to helping users understand and analyze research papers. I will provide the text and specify the task you need assistance with. Please help we address these questions."

class OpenAIInterface(BaseInterface):
    def __init__(self, api_key, model_name="gpt-3.5-turbo", **kwargs):
        self.init_interface(api_key)
        self.model_name = model_name
        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

    def init_interface(self, api_key):
        openai.api_key = api_key

    def completion(self,
        prompt, decoding_config=None,
        model_name=None,
        sleep_time=2,
        return_text=True,
        **kwargs
    ):
        if model_name is None:
            model_name = self.model_name

        self.messages.append(
            {"role": "user", "content": prompt}
        )
        while True:
            try:
                completion = openai.chat.completions.create(
                    messages=self.messages,
                    model=model_name,
                    **kwargs,
                )
                break
            except openai.OpenAIError as e:
                logging.warning(f"OpenAIError: {e}.")
                if "Please reduce your prompt" in str(e):
                    batch_decoding_args.max_tokens = int(batch_decoding_args.max_tokens * 0.8)
                    logging.warning(f"Reducing target length to {batch_decoding_args.max_tokens}, Retrying...")
                else:
                    logging.warning("Hit request rate limit; retrying...")
                    time.sleep(sleep_time)  # Annoying rate limit on requests.
        assistant_text = completion.choices[0].message.content.strip()
        self.messages.append(
            {"role": "assistant", "content": assistant_text}
        )

        if return_text == True:
            return assistant_text

        return completion
    
    def construct_section_prompt(self, sections):
        for title, content in tqdm(sections.items()):
            self.messages.append(
                {"role": "user", "content": f"The following section is {title}: {content}"}
            )
