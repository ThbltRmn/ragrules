from ragrules.cloudfunctions.chunker.embedder import Embedder
from ragrules.vector_search.homemade_vector_search import find_nearest_neighbors_ids, load_full_sentences, load_vectors


class ContextRetriever:
    def __init__(self, context_file: str, question: str):
        """
        Initializes the ContextRetriever with a context file and a question.
        """
        self.context_file = context_file
        self.question = question
        self.context = None  # Placeholder for the retrieved context

    def retrieve_context(self) -> str:
        embedded = Embedder().embed_content(self.question)
        nn = find_nearest_neighbors_ids(embedded, load_vectors("tests/datas/langchain_sw_embedded.json"), top_n=5)

        full_sentences = load_full_sentences("tests/datas/langchain_sw_sentences.json")
        top_sentences = [str(s[1]) for s in full_sentences if s[0] in nn]
        self.context = "-----\n".join(top_sentences)
        return self.context

# if __name__ == "__main__":
#     cr = ContextRetriever("", "La carte Swap")
#     cr.retrieve_context()
