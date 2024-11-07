from ragrules.GeminiClient import GeminiClient
from ragrules.prompts import RAG_PROMPT


class MainQuestion:
    def __init__(self, game_name: str, question: str, context: str, gemini_client: GeminiClient):
        self.game_name = game_name
        self.question = question
        self.context = context
        self.gemini_client = gemini_client

    def ask_question(self) -> str:
        # messages = [
        #     {
        #         "role": "system",
        #         "content": SYSTEM_PROMPT,
        #     },
        # ]
        #context = retrieve_context(self.question)
        context = self.context
        prompt = f"""
                {RAG_PROMPT}
                The name of the game is {self.game_name}.
                Use the following informations:

                ```
                {context}
                ```

                to answer the question:
                {self.question}
                        """
        print(prompt)
        return self.gemini_client.call_model(prompt), self.context

    def __repr__(self):
        return f"MainQuestion(GameName='{self.game_name}', Question='{self.question}', Context='{self.context}')"

    def __str__(self):
        return f"Game: {self.game_name}\nQuestion: {self.question}\nContext: {self.context}"
