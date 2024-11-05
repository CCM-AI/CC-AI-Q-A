import streamlit as st
import json

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

# Function to search questions by keyword
def search_qa(query):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

# Function to toggle answers and add/remove favorites
def display_qa_for_selection(qa_list):
    if not qa_list:
        st.write("No results found.")
        return

    for item in qa_list:
        # Show question with a button to toggle the answer
        show_answer = st.session_state.get(f"show_answer_{item['Q']}", False)
        if st.button(f"**{item['Q']}**", key=item['Q']):
            # Toggle the answer visibility
            st.session_state[f"show_answer_{item['Q']}"] = not show_answer
            show_answer = not show_answer

        # Show the answer if toggled
        if show_answer:
            st.write(f"**Answer**: {item['A']}")
        
        # Add to favorites or remove from favorites
        if item in st.session_state.favorites:
            if st.button(f"Remove from MY LIST: {item['Q']}", key=f"remove_{item['Q']}"):
                st.session_state.favorites.remove(item)
                st.success(f"Removed '{item['Q']}' from MY LIST.")
        else:
            if st.button(f"Add to MY LIST: {item['Q']}", key=f"add_{item['Q']}"):
                st.session_state.favorites.append(item)
                st.success(f"Added '{item['Q']}' to MY LIST.")

# Main Streamlit app
def main():
    st.title("Health Q&A Tool")
    st.write("Welcome! You can either search for questions or select from a list of topics, or view your saved favorites.")

    # Option to choose between search or selection
    option = st.radio("Choose an option to explore:", ["Search by Keywords", "Select from a List", "MY LIST: Your Favorite Questions and Answers"])

    if option == "Search by Keywords":
        query = st.text_input("Enter a keyword to search for questions:")

        if query:
            results = search_qa(query)

            if results:
                st.write(f"Found {len(results)} matching question(s):")
                display_qa_for_selection(results)
            else:
                st.warning("No questions found matching your search. Please try a different keyword.")
    
    elif option == "Select from a List":
        # Display a list of questions
        st.write("Here are the available questions:")
        display_qa_for_selection(qa_data)
    
    elif option == "MY LIST: Your Favorite Questions and Answers":
        if st.session_state.favorites:
            st.write("### Your Favorite Questions and Answers:")
            display_qa_for_selection(st.session_state.favorites)
        else:
            st.write("You don't have any questions in your favorites yet. Try adding some from the other sections.")

if __name__ == "__main__":
    main()
