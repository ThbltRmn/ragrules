import json

test_embedding = ""

# run query
response = my_index_endpoint.find_neighbors(
    deployed_index_id = DEPLOYED_INDEX_ID,
    queries = [query_emb],
    num_neighbors = 10
)

# show the results
for idx, neighbor in enumerate(response[0]):
    print(f"{neighbor.distance:.2f} {product_names[neighbor.id]}")