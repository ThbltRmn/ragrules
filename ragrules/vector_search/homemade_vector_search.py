import json
import os

import numpy as np
from scipy.spatial.distance import cosine


# Load vectors from file
def load_vectors(file_path: str = "tests/datas/crack_list_embedded.json") -> list:
    vectors: list = []
    with open(file_path) as f:
        for line in f:
            # Parse the line as JSON
            vector_data = json.loads(line)
            vector_id: str = vector_data["id"]
            vector = np.array(vector_data["embedding"])
            vectors.append((vector_id, vector))
    return vectors

def load_full_sentences(file_path: str = "tests/datas/crack_list_sentences.json") -> list:
    sentences: list = []
    with open(file_path) as f:
        for line in f:
            # Parse the line as JSON
            data = json.loads(line)
            sentence_id: str = data["id"]
            sentence = np.array(data["sentence"])
            sentences.append((sentence_id, sentence))
    return sentences


# Function to find top N nearest neighbors using cosine similarity
def find_nearest_neighbors(target_vector: list, vectors: list, top_n: int = 5) -> list:
    np_target_vector = np.array(target_vector)
    similarities: list = []
    for vec_id, vector in vectors:
        # Calculate cosine similarity (1 - cosine distance)
        similarity: float = 1 - cosine(np_target_vector, vector)
        similarities.append((vec_id, similarity))
    # Sort by similarity in descending order and get the top N
    top_neighbors: list = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]
    return top_neighbors

# Function to find top N nearest neighbors using cosine similarity
def find_nearest_neighbors_ids(target_vector: list, vectors: list, top_n: int = 5) -> list:
    np_target_vector = np.array(target_vector)
    similarities: list = []
    for vec_id, vector in vectors:
        # Calculate cosine similarity (1 - cosine distance)
        similarity: float = 1 - cosine(np_target_vector, vector)
        similarities.append((vec_id, similarity))
    # Sort by similarity in descending order and get the top N
    top_neighbors: list = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]
    top_neighbors_ids = [i[0] for i in top_neighbors]
    return top_neighbors_ids

# if __name__ == "__main__":
#     print(os.listdir())
#     file_path: str = "tests/datas/crack_list_embedded.json"
#     vector_path = "tests/datas/test_base_vector.txt"
#     target_vector = [
#         float(line.strip().strip(",")) for line in open(vector_path)
#     ]  # Replace with the target vector you want to query
#     print(target_vector)
#     # Load vectors from file
#     vectors: list = load_vectors(file_path)

#     # Find top 5 nearest neighbors
#     top_neighbors: list = find_nearest_neighbors(target_vector, vectors, top_n=2)

#     # Print results
#     print("Top 5 Nearest Neighbors:")
#     for neighbor_id, similarity in top_neighbors:
#         print(f"ID: {neighbor_id}, Similarity: {similarity:.4f}")
