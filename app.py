import streamlit as st
import json

# Load the Q&A data from JSON
def load_qa_data():
    with open('responses.json', 'r') as f:
        qa_data = json.load(f)
    return qa_data

# Load the initial Q&A data
qa_data = load_qa_data()
favorites = []

# Display Q&A for user selection
def display_qa_for_selection(qa_list):
    if not qa_list:
        st.write("No results found.")
        return
    for i, item in enumerate(qa_list, start=1):
        st.write(f"**{i}.** {item['Q']}")

# Search function to filter questions based on query
def search_qa(query):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

# Main Streamlit app
def main():
    st.title("Health Q&A Tool")
    st.write("Welcome! Search for health-related questions and add them to your favorites.")

    # Input field for search query
    query = st.text_input("Search for a health-related question:")
    
    if query:
        results = search_qa(query)
        
        if results:
            st.write(f"Found {len(results)} matching question(s):")
            display_qa_for_selection(results)

            # Select a question to add to favorites
            question_number = st.number_input("Select a question number to add to your favorites:", min_value=1, max_value=len(results), step=1)
            if st.button("Add to Favorites"):
                selected_question = results[question_number - 1]
                favorites.append(selected_question)
                st.success(f"Question added to favorites: {selected_question['Q']}")
        else:
            st.warning("No questions found matching your search. Please try a different keyword.")

    # Display the user's favorites
    if favorites:
        st.write("### Your Favorite Questions:")
        for item in favorites:
            st.write(f"- **{item['Q']}**")

    # If no favorites, guide the user to add one
    if not favorites and query:
        st.write("You haven't added any questions to your favorites yet. Try selecting one.")

if __name__ == "__main__":
    main()
