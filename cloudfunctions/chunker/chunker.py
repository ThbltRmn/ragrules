class Chunker:
    def __init__(self, chunk_size):
        """
        Initializes the Chunker with the chunk size.

        Args:
            chunk_size (int): The maximum size of each chunk.
        """
        self.chunk_size = chunk_size

    def get_chunks(self, text):
        """
        Splits the text into chunks of specified size.

        Args:
            text (str): The text to be chunked.

        Returns:
            list: A list of text chunks.
        """
        return [text[i : i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]

    def __repr__(self):
        """
        Returns a string representation of the Chunker class.

        Returns:
            str: A string representation of the object.
        """
        return f"Chunker(chunk_size={self.chunk_size})"


# if __name__ == "__main__":
#     text = "This is an example text that we want to split into multiple chunks of a specified size."
#     chunk_size = 20

#     chunker = Chunker(chunk_size)
#     chunks = chunker.get_chunks(text=text)

#     for idx, chunk in enumerate(chunks):
#         print(f"Chunk {idx + 1}: {chunk}")
