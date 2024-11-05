import streamlit as st
import json

# Load the Q&A data from JSON
def load_qa_data():
    with open('responses.json', 'r') as f:
        qa_data = json.load(f)
    return qa_data

# Load initial Q&A data
qa_data = load_qa_data()

# Initialize session state for favorites if not already initialized
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Function to search questions by keyword
def search_qa(query, qa_list):
    results = [item for item in qa_list if query.lower() in item['Q'].lower()]
    return results

# Function to display questions and allow checkbox selection
def display_qa_for_selection(qa_list, source="main"):
    if not qa_list:
        st.write("No results found.")
        return

    # List the questions with buttons for selection
    for idx, item in enumerate(qa_list):
        # Show question with checkbox to show/hide answer
        if st.checkbox(f"**{item['Q']}**", key=f"checkbox_{item['Q']}_{idx}"):
            st.write(f"**Answer**: {item['A']}")
            
            # Add or Remove from MY LIST based on whether the question is in the list
            if item in st.session_state.favorites:
                # If the item is already in favorites, show "Remove from MY LIST"
                if st.button(f"Remove '{item['Q']}' from MY LIST", key=f"remove_{item['Q']}_{idx}"):
                    st.session_state.favorites.remove(item)
                    st.success(f"Removed '{item['Q']}' from your favorites!")
            else:
                # If the item is not in favorites, show "Add to MY LIST"
                if st.button(f"Add '{item['Q']}' to MY LIST", key=f"add_{item['Q']}_{idx}"):
                    st.session_state.favorites.append(item)
                    st.success(f"Added '{item['Q']}' to your favorites!")

# Function to display MY LIST
def display_my_list():
    if not st.session_state.favorites:
        st.write("You haven't added any questions to your list yet. Try selecting or searching one.")
        return

    st.write("### MY LIST: Your Favorite Questions and Answers:")

    # Display all the questions in MY LIST with the same format as Search by Keywords
    for idx, item in enumerate(st.session_state.favorites):
        # Show question with checkbox to show/hide answer
        if st.checkbox(f"**{item['Q']}**", key=f"checkbox_fav_{item['Q']}_{idx}"):
            st.write(f"**Answer**: {item['A']}")

        # Allow user to remove questions from MY LIST
        if st.button(f"Remove '{item['Q']}' from MY LIST", key=f"remove_fav_{item['Q']}_{idx}"):
            st.session_state.favorites.remove(item)
            st.success(f"Removed '{item['Q']}' from your favorites!")

# Main Streamlit app
def main():
    st.title("Health Q&A Tool")
    st.write("Welcome! You can either search for questions, select from the list of questions, or manage your favorites.")

    # Option to choose between search or selection
    option = st.radio("Choose how you want to explore:", ["Search by Keywords", "Select from a List", "MY LIST"])

    if option == "Search by Keywords":
        query = st.text_input("Enter a keyword to search for questions:")
        
        if query:
            results = search_qa(query, qa_data)
            
            if results:
                st.write(f"Found {len(results)} matching question(s):")
                display_qa_for_selection(results)
            else:
                st.warning("No questions found matching your search. Please try a different keyword.")

    elif option == "Select from a List":
        # Display all questions from qa_data if no categories
        st.write("Here are all the questions available:")
        display_qa_for_selection(qa_data)

    elif option == "MY LIST":
        st.write("### MY LIST: Your Favorite Questions and Answers:")
        
        # Search functionality for MY LIST
        query = st.text_input("Search your favorite questions:")
        
        # Filter the favorites list based on the search query
        filtered_favorites = search_qa(query, st.session_state.favorites)
        
        if filtered_favorites:
            st.write(f"Found {len(filtered_favorites)} matching question(s) in your list:")
            display_qa_for_selection(filtered_favorites, source="my_list")
        else:
            if query:
                st.warning("No questions found matching your search in MY LIST.")
            else:
                st.write("No favorites added yet. Try selecting some questions to add to your favorites.")
                
        # Display all the questions in MY LIST
        display_my_list()

if __name__ == "__main__":
    main()
