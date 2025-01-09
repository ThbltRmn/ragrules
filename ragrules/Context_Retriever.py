from ragrules.cloudfunctions.chunker.embedder import Embedder
from ragrules.vector_search.homemade_vector_search import find_nearest_neighbors_ids, load_full_sentences_dict, load_vectors, find_nearest_neighbors


class ContextRetriever:
    def __init__(self, context_file: str, question: str):
        """
        Initializes the ContextRetriever with a context file and a question.
        """
        self.context_file = context_file
        self.question = question
        self.context = None  # Placeholder for the retrieved context
        self.context_full = None
        self.context_scores = None

    def get_context_scores(self):
        return(self.context_scores)

    def retrieve_context(self, top_n: int = 3) -> str:
        embedded = Embedder().embed_content(self.question)
        #nn = find_nearest_neighbors_ids(embedded, load_vectors("tests/datas/langchain_sw_embedded.json"), top_n=5)
        #nn_ids = [i[0] for i in nn]
        #nn_scores = [i[1] for i in nn]


        # nn_dict = find_nearest_neighbors(embedded, load_vectors("tests/datas/langchain_sw_embedded.json"), top_n = top_n)
        # full_sentences = load_full_sentences("tests/datas/langchain_sw_sentences.json")
        # #top_sentences = [str(s[1]) for s in full_sentences if s[0] in nn_ids]
        # top_sentences = [(str(s[1]), nn_dict[s[0]]) for s in full_sentences if s[0] in nn_dict]
        # top_sentences_only = [str(s[1]) for s in full_sentences if s[0] in nn_dict]
        # self.context = "-----\n".join(top_sentences_only)
        # self.context_scores = top_sentences



        nn = find_nearest_neighbors_ids(embedded, load_vectors("tests/datas/langchain_sw_embedded.json"), top_n = top_n)
        full_sentences = load_full_sentences_dict("tests/datas/langchain_sw_sentences.json")
        #top_sentences = [str(s[1]) for s in full_sentences if s[0] in nn_ids]
        top_sentences_ids_ordered = [i[0] for i in nn]
        top_sentences_ordered = [full_sentences[id] for id in top_sentences_ids_ordered]
        top_sentences_and_scores_ordered = [(full_sentences[i[0]],i[1])for i in nn]
        self.context = "-----\n".join(top_sentences_ordered)
        self.context_scores = top_sentences_and_scores_ordered
        return self.context

    def describe_context(self) -> str:
        context_with_scores = self.context_scores
        return "\n\n".join([f"Sentence : {i[0]} ; Simi Score : {i[1]}" for i in context_with_scores])

# if __name__ == "__main__":
#     cr = ContextRetriever("", "La carte Swap")
#     cr.retrieve_context()
