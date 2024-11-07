import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiClient:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        Initializes the GeminiClient with the specified model name.

        Args:
            model_name (str): The name of the generative model to use.
        """
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    def call_model(self, prompt: str = "Write a story about a magic backpack.") -> str:
        response = self.model.generate_content(prompt)
        return response.text
