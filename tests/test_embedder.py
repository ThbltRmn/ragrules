from cloudfunctions.chunker.embedder import Embedder


def full_test():
    embedder = Embedder()

    content = "What is the meaning of life?"

    # Embed content
    result = embedder.embed_content(
        content="What is the meaning of life?",
        title="Embedding of single string"
    )

    # Print the first 50 characters of the embedding
    if result:
        embedder.print_trimmed_embedding(result)
    else:
        print("No embedding returned.")

    if result:
        embedder.save_embedding(content, result, "ragrules/tests/datas/embeded.txt", "ragrules/tests/datas/sentences.txt")