import numpy as np

from ragrules.vector_search.homemade_vector_search import find_nearest_neighbors, load_vectors


def load_sample_data():
    with open("./datas/test_base_vector.txt") as f:
        for l in f.readlines:
            print(l)
load_sample_data()

def test_load_vectors(sample_vector_file):
    vectors = load_vectors(sample_vector_file)
    assert len(vectors) == len(SAMPLE_DATA)
    for i, (vector_id, vector) in enumerate(vectors):
        assert vector_id == SAMPLE_DATA[i]["id"]
        np.testing.assert_array_equal(vector, np.array(SAMPLE_DATA[i]["vector"]))

def test_find_nearest_neighbors(sample_vector_file):
    target_vector = [1.0, 0.0, 0.0]  # Should be closest to "id1"
    vectors = load_vectors(sample_vector_file)

    top_neighbors = find_nearest_neighbors(target_vector, vectors, top_n=3)

    assert len(top_neighbors) == 3
    assert top_neighbors[0][0] == "id1"  # Closest neighbor
    assert top_neighbors[1][0] == "id4"  # Second closest neighbor
    assert top_neighbors[2][0] == "id5"  # Third closest neighbor

    # Check similarities
    similarities = [similarity for _, similarity in top_neighbors]
    assert all(similarities[i] >= similarities[i + 1] for i in range(len(similarities) - 1))  # Ensure sorted
