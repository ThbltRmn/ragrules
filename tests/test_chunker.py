from ragrules.offline.chunker.chunker import Chunker  # Assuming the Chunker class is saved in a file called chunker.py

def test_chunk_size_exact_division():
    text = "abcdefghij"  # Length is 10
    chunk_size = 2
    chunker = Chunker(chunk_size)
    expected_chunks = ["ab", "cd", "ef", "gh", "ij"]
    assert chunker.get_chunks(text) == expected_chunks

def test_chunk_size_larger_than_text():
    text = "abc"
    chunk_size = 10
    chunker = Chunker(chunk_size)
    expected_chunks = ["abc"]
    assert chunker.get_chunks(text) == expected_chunks

def test_chunk_size_not_exact_division():
    text = "abcdefghijk"  # Length is 11
    chunk_size = 3
    chunker = Chunker(chunk_size)
    expected_chunks = ["abc", "def", "ghi", "jk"]
    assert chunker.get_chunks(text) == expected_chunks

def test_empty_text():
    text = ""
    chunk_size = 5
    chunker = Chunker(chunk_size)
    expected_chunks = []
    assert chunker.get_chunks(text) == expected_chunks

def test_chunk_size_one():
    text = "abcd"
    chunk_size = 1
    chunker = Chunker(chunk_size)
    expected_chunks = ["a", "b", "c", "d"]
    assert chunker.get_chunks(text) == expected_chunks

def test_repr_method():
    chunk_size = 3
    chunker = Chunker(chunk_size)
    expected_repr = "Chunker(chunk_size=3)"
    assert repr(chunker) == expected_repr
