import json

import requests
import streamlit as st
from games_functions import load_games, search_games

from cloudfunctions.chunker.embedder import Embedder
from ragrules.vector_search.homemade_vector_search import find_nearest_neighbors, load_vectors

# from langchain.chains import RetrievalQA
# from langchain.embeddings.openai import OpenAIEmbeddings  # Use any embedding model for retrieval
# from langchain.vectorstores import FAISS


# Function to call Gemini API
def call_gemini(prompt):
    url = "https://api.gemini.cloud/v1/generate"  # Update to the actual Gemini API endpoint
    headers = {
        "Authorization": f"Bearer YOUR_GEMINI_API_KEY",  # Replace with your Gemini API Key
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "model": "gemini-model",  # Replace with the correct Gemini model name if needed
        "max_tokens": 500,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return "Error: Unable to generate a response from Gemini."


# Backend setup
# def initialize_rag():
#     # Initialize FAISS (or any other vector store you are using)
#     embeddings = OpenAIEmbeddings()  # You can use OpenAI embeddings or any other embedding model
#     vectorstore = FAISS.load_local("path_to_faiss_index", embeddings)

#     # Set up RAG (Retrieval-Augmented Generation) pipeline with Gemini for the LLM
#     rag_pipeline = RetrievalQA.from_chain_type(
#         llm=None,  # We'll handle the LLM call manually
#         chain_type="stuff",
#         retriever=vectorstore.as_retriever(),
#     )
#     return rag_pipeline


# Initialize the RAG model once
# rag_model = initialize_rag()

# Initialize Embedder
embedder = Embedder()

 # Load games
games = load_games()

poc_v = st.radio("Switch POC versions", ["Sans Autocomplete", "Avec Autocomplete"])

if poc_v=="Sans Autocomplete":
    st.title("Version 1 : sans autocomplete")

    # Search widget
    query = st.text_input("Enter board game name:")

    if query:
        results = search_games(games, query)
        if results:
            # Show results
            selected_game = st.selectbox("Select a game:", [game['name'] for game in results])

            # Get the ID of the selected game
            if selected_game:
                game_id = next(game['id'] for game in results if game['name'] == selected_game)
                st.write(f"Selected Game ID: {game_id}")
        else:
            st.write("No games found.")
else:
    st.title("Version 2 : autocomplete")

    game_names = [game['name'] for game in games]

    filtered_names = game_names  # Show all games if no query is entered

    # Display a selectbox with filtered results
    if filtered_names:
        selected_game_name = st.selectbox("Select a game:", filtered_names)
        # Find the game ID of the selected game
        if selected_game_name:
            selected_game = next((game for game in games if game['name'] == selected_game_name), None)
            if selected_game:
                st.write(f"Selected Game ID: {selected_game['id']}")
    else:
        st.write("No games found.")

# Streamlit UI
st.title("RAG-powered Chatbot with Gemini")

# Input box for user question
user_question = st.text_input("Ask me anything:")

if user_question:
    with st.spinner("Generating embedding..."):
        embedded = embedder.embed_content(user_question)
        st.write(f"{embedded[:10]} ...")
    with st.spinner("Calculating nearest neighbors"):
        nn = find_nearest_neighbors(embedded,load_vectors(), top_n=3)
        st.write(nn)
# if user_question:
#     # Show loading animation while processing
#     with st.spinner("Retrieving and generating response..."):
#         # Retrieve relevant sentences from RAG
#         relevant_docs = rag_model.retriever.get_relevant_documents(user_question)

#         # Display the top retrieved sentences
#         st.subheader("Top Retrieved Sentences:")
#         for idx, doc in enumerate(relevant_docs[:5]):  # Show top 5 sentences
#             st.write(f"{idx + 1}. {doc.page_content}")

#         # Combine retrieved content with the user question to send to Gemini
#         combined_prompt = f"User Question: {user_question}\n\nRelevant Info:\n"
#         combined_prompt += "\n".join([doc.page_content for doc in relevant_docs[:5]])

#         # Get the response from Gemini LLM
#         gemini_response = call_gemini(combined_prompt)

#     # Display Gemini's response
#     st.subheader("Answer from Gemini LLM:")
#     st.write(gemini_response)
