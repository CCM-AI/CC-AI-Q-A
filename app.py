import streamlit as st
import json
from googletrans import Translator

# Load the Q&A data from JSON
def load_qa_data():
    with open('responses.json', 'r') as f:
        qa_data = json.load(f)
    return qa_data

# Load initial Q&A data
qa_data = load_qa_data()

# To store the list of favorites in the session
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Function to search questions by keyword, supporting all languages
def search_qa(query):
    translator = Translator()
    
    # Convert the query to lowercase for consistent searching
    query_lower = query.lower()

    results = []
    for item in qa_data:
        # Translate the question to the language of the query
        translated_question = translator.translate(item['Q'], src='en', dest='auto').text.lower()
        
        # Check if the query appears in the translated question text
        if query_lower in translated_question:
            results.append(item)

    return results

# Function to display questions and answers
def display_qa_for_selection(qa_list):
    if not qa_list:
        st.write("No results found.")
        return

    for idx, item in enumerate(qa_list):
        question_key = f"question_{idx}_{item['Q']}"  # Create a unique key for each question
        answer_key = f"answer_{idx}_{item['Q']}"  # Create a unique key for each answer

        # Show question with a button to toggle the answer
        show_answer = st.session_state.get(answer_key, False)
        if st.button(f"**{item['Q']}**", key=question_key, help="Click to toggle answer visibility"):
            # Toggle the answer visibility
            st.session_state[answer_key] = not show_answer
            show_answer = not show_answer

        # Show the answer if toggled
        if show_answer:
            st.write(f"**Answer**: {item['A']}")

        # Favorite functionality
        favorite_key = f"favorite_{idx}_{item['Q']}"  # Unique key for add/remove favorite
        if item in st.session_state.favorites:
            if st.button("❌ Remove from MY LIST", key=f"remove_{favorite_key}"):
                st.session_state.favorites.remove(item)
                st.success(f"Removed '{item['Q']}' from MY LIST.")
        else:
            if st.button("✔️ Add to MY LIST", key=f"add_{favorite_key}"):
                st.session_state.favorites.append(item)
                st.success(f"Added '{item['Q']}' to MY LIST.")

# Main Streamlit app
def main():
    st.title("Multilingual Q&A App")

    # Option to choose between search or selection
    option = st.radio("Choose an option to explore:", ["Search by Keywords", "Select from a List", "MY LIST"])

    # Handle Search by Keywords
    if option == "Search by Keywords":
        query = st.text_input("Search by Keywords")

        if query:
            # Search across all languages
            results = search_qa(query)

            if results:
                st.write(f"Found {len(results)} matching questions:")
                display_qa_for_selection(results)
            else:
                st.warning("No results found.")
    
    # Handle Select from a List
    elif option == "Select from a List":
        # Display a list of questions
        st.write("Select from a list of questions:")
        display_qa_for_selection(qa_data)
    
    # Handle MY LIST: Your Favorite Questions and Answers
    elif option == "MY LIST":
        if st.session_state.favorites:
            st.write("### MY LIST: Your Favorite Questions and Answers")
            display_qa_for_selection(st.session_state.favorites)
        else:
            st.write("You have no favorites saved.")

if __name__ == "__main__":
    main()
