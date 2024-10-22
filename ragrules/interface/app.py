import json

import requests
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings  # Use any embedding model for retrieval
from langchain.vectorstores import FAISS


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
def initialize_rag():
    # Initialize FAISS (or any other vector store you are using)
    embeddings = OpenAIEmbeddings()  # You can use OpenAI embeddings or any other embedding model
    vectorstore = FAISS.load_local("path_to_faiss_index", embeddings)

    # Set up RAG (Retrieval-Augmented Generation) pipeline with Gemini for the LLM
    rag_pipeline = RetrievalQA.from_chain_type(
        llm=None,  # We'll handle the LLM call manually
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
    )
    return rag_pipeline


# Initialize the RAG model once
rag_model = initialize_rag()

# Streamlit UI
st.title("RAG-powered Chatbot with Gemini")

# Input box for user question
user_question = st.text_input("Ask me anything:")

if user_question:
    # Show loading animation while processing
    with st.spinner("Retrieving and generating response..."):
        # Retrieve relevant sentences from RAG
        relevant_docs = rag_model.retriever.get_relevant_documents(user_question)

        # Display the top retrieved sentences
        st.subheader("Top Retrieved Sentences:")
        for idx, doc in enumerate(relevant_docs[:5]):  # Show top 5 sentences
            st.write(f"{idx + 1}. {doc.page_content}")

        # Combine retrieved content with the user question to send to Gemini
        combined_prompt = f"User Question: {user_question}\n\nRelevant Info:\n"
        combined_prompt += "\n".join([doc.page_content for doc in relevant_docs[:5]])

        # Get the response from Gemini LLM
        gemini_response = call_gemini(combined_prompt)

    # Display Gemini's response
    st.subheader("Answer from Gemini LLM:")
    st.write(gemini_response)
