import streamlit as st
import json

# Load the Q&A data from JSON
def load_qa_data():
    with open('responses.json', 'r') as f:
        qa_data = json.load(f)
    return qa_data

# Load initial Q&A data
qa_data = load_qa_data()
favorites = []

# Function to search questions by keyword
def search_qa(query):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

# Display all questions in a FAQ-style format
def display_faq(qa_list):
    if not qa_list:
        st.write("No results found.")
        return

    # List the questions as a FAQ
    for index, item in enumerate(qa_list):
        with st.expander(f"**{item['Q']}**", expanded=False):  # Makes it expandable like a FAQ
            # Display the answer when clicked
            st.write(f"**Answer**
