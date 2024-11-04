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

# Display Q&A for user selection with answers
def display_qa_for_selection(qa_list):
    if not qa_list:
        st.write("No results found.")
        return
    
    for i, item in enumerate(qa_list, start=1):
        if st.button(f"**{i}.** {item['Q']}"):
            # When the button is clicked, show the answer
            st.write(f"**Answer**: {item['A']}")
            
            # Add to favorites button
            if st.button(f"Add '{item['Q']}' to Favorites"):
                favorites.append(item)
                st.success(f"Added '{item['Q']}' to your favorites!")

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
