class BaseInterface:
    def __init__(self, api_key, model_name, **kwargs):
        self.api_key = api_key
        self.model_name = model_name

    def init_interface(self, *args, **kwargs):
        pass

    def completion(self, prompt, decoding_config, model_name, **kwargs):
        pass
