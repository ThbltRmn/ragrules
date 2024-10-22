from google.cloud.aiplatform_v1 import FindNeighborsRequest, FindNeighborsResponse, IndexDatapoint, MatchServiceClient


class VectorSearchClient:
    def __init__(self, api_endpoint: str, index_endpoint: str, deployed_index_id: str) -> None:
        self.api_endpoint = api_endpoint
        self.index_endpoint = index_endpoint
        self.deployed_index_id = deployed_index_id
        self.client = MatchServiceClient(client_options={"api_endpoint": self.api_endpoint})

    def build_query(self, feature_vector: list, neighbor_count: int = 10) -> FindNeighborsRequest.Query:
        datapoint = IndexDatapoint(feature_vector=feature_vector)
        query = FindNeighborsRequest.Query(datapoint=datapoint, neighbor_count=neighbor_count)
        return query

    def find_neighbors(
        self, feature_vector: list, neighbor_count: int = 10, return_full_datapoint: bool = False
    ) -> FindNeighborsResponse:
        query = self.build_query(feature_vector, neighbor_count)
        request = FindNeighborsRequest(
            index_endpoint=self.index_endpoint,
            deployed_index_id=self.deployed_index_id,
            queries=[query],
            return_full_datapoint=return_full_datapoint,
        )
        response = self.client.find_neighbors(request)
        return response


# # Usage
# API_ENDPOINT = "236921330.europe-west1-425866744273.vdb.vertexai.goog"
# INDEX_ENDPOINT = "projects/425866744273/locations/europe-west1/indexEndpoints/1270973869057900544"
# DEPLOYED_INDEX_ID = "embeddings_deploy_1729335715273"

# # Initialize the VectorSearchClient
# vector_search = VectorSearchClient(API_ENDPOINT, INDEX_ENDPOINT, DEPLOYED_INDEX_ID)

# # Feature vector for the query
# feature_vector = [...]  # Define your feature vector here

# # Find neighbors
# response = vector_search.find_neighbors(feature_vector, neighbor_count=10)

# # Handle the response
# print(response)
