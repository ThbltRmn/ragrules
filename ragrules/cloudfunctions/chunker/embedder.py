import json
import os
import uuid

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class Embedder:
    def __init__(self, model: str = "models/text-embedding-004", task_type: str = "retrieval_document"):
        """
        Initialize the Embedder object with default model and task type.

        Args:
            model (str): The embedding model to be used.
            task_type (str): The type of task for the embedding (e.g., 'retrieval_document').
        """
        self.model = model
        self.task_type = task_type

    def embed_content(self, content: str, title: str = "") -> list:
        """
        Embeds the provided content and returns the embedding vector.

        Args:
            content (str): The text content to be embedded.
            title (str): An optional title for the embedding task.

        Returns:
            dict: A dictionary containing the embedding vector.
        """
        result = genai.embed_content(
            model=self.model,
            content=content,
            task_type=self.task_type,
            title=title if title else "Embedding of content",
        )

        self.result = result

        # Return the embedding part of the result
        return result.get("embedding", [])

    def print_trimmed_embedding(self, embedding: list, length: int = 50) -> None:
        """
        Prints the first `length` characters of the embedding for inspection.

        Args:
            embedding (list): The embedding vector.
            length (int): Number of characters to print before trimming.
        """
        print(str(embedding)[:length] + "... TRIMMED]")

    # Save to two files : one listing the embeddings and one listing the sentences
    def save_embedding(self, embedding: list, sentence: str, local_embed_path: str, local_sentences_path: str) -> None:
        with open(local_embed_path, "a") as embed_file, open(local_sentences_path, "a") as sentence_file:
            # for sentence, embedding in zip(sentences, embeddings):
            created_id = str(uuid.uuid4())

            embed_item = {"id": created_id, "embedding": embedding}
            sentence_item = {"id": created_id, "sentence": sentence}

            json.dump(sentence_item, sentence_file)
            sentence_file.write("\n")
            json.dump(embed_item, embed_file)
            embed_file.write("\n")

    # def embed_batch_contents(self, content, title=None):
    #     """
    #     Embeds the provided content and returns the embedding vector.

    #     Args:
    #         content (str): The text content to be embedded.
    #         title (str): An optional title for the embedding task.

    #     Returns:
    #         dict: A dictionary containing the embedding vector.
    #     """
    #     result = genai.embed_content(
    #         model=self.model,
    #         content=content,
    #         task_type=self.task_type,
    #         title=title if title else "Embedding of content"
    #     )

    #     self.result = result

    #     # Return the embedding part of the result
    #     return result.get('embedding', None)

    # def print_batch_trimmed_embedding(self, embedding, length=50):
    #     """
    #     Prints the first `length` characters of the embedding for inspection.

    #     Args:
    #         embedding (list): The embedding vector.
    #         length (int): Number of characters to print before trimming.
    #     """
    #     print(str(embedding)[:length] + '... TRIMMED]')

    # # Save to two files : one listing the embeddings and one listing the sentences
    # def save_batch_embedding(self, embedding, sentence, local_embed_path, local_sentences_path):
    #     with open(local_embed_path, 'w') as embed_file, open(local_sentences_path, 'w') as sentence_file:
    #         #for sentence, embedding in zip(sentences, embeddings):
    #         created_id = str(uuid.uuid4())

    #         embed_item = {"id": created_id, "embedding": embedding}
    #         sentence_item = {"id": created_id, "sentence": sentence}

    #         json.dump(sentence_item, sentence_file)
    #         sentence_file.write('\n')
    #         json.dump(embed_item, embed_file)
    #         embed_file.write('\n')


if __name__ == "__main__":
    embedder = Embedder()

    content = "What is the meaning of life?"

    # Embed content
    result = embedder.embed_content(content="What is the meaning of life?", title="Embedding of single string")

    # Print the first 50 characters of the embedding
    if result:
        embedder.print_trimmed_embedding(result)
    else:
        print("No embedding returned.")

    if result:
        embedder.save_embedding(result, content, "./embeded.txt", "./sentences.txt")
