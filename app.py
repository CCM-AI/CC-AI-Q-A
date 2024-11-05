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
def display_qa_for_selection(qa_list):
    if not qa_list:
        st.write("No results found.")
        return

    # List the questions with checkboxes for selection
    for idx, item in enumerate(qa_list):
        if st.checkbox(f"**{item['Q']}**", key=f"checkbox_{item['Q']}_{idx}"):
            # Add the question to favorites if checked
            if item not in st.session_state.favorites:
                st.session_state.favorites.append(item)
                st.success(f"Added '{item['Q']}' to your favorites!")

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
            display_qa_for_selection(filtered_favorites)
        else:
            if query:
                st.warning("No questions found matching your search in MY LIST.")
            else:
                st.write("No favorites added yet. Try selecting some questions to add to your favorites.")
                
        # Display all the questions in MY LIST
        if st.session_state.favorites:
            for item in st.session_state.favorites:
                st.write(f"**{item['Q']}**")
                st.write(f"**Answer**: {item['A']}")
        else:
            st.write("You haven't added any questions to your list yet. Try selecting or searching one.")

if __name__ == "__main__":
    main()
