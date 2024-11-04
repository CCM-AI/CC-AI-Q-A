import streamlit as st
import json

# Load Q&A data from JSON file
def load_qa_data():
    with open('responses.json', 'r') as f:
        qa_data = json.load(f)
    return qa_data

# Load the initial Q&A data
qa_data = load_qa_data()
favorites = []

# Function to display Q&A for selection
def display_qa_for_selection(qa_list):
    if not qa_list:
        st.write("No results found.")
        return
    for i, item in enumerate(qa_list, start=1):
        st.write(f"{i}. **Q:** {item['Q']}")

# Function to search Q&A
def search_qa(query):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

# Main Streamlit app
def main():
    st.title("Q&A Tool")

    # Sidebar options
    option = st.sidebar.selectbox("Choose an option", [
        "Search for a question",
        "View favorite questions",
        "Add a question to favorites",
        "Exit"
    ])

    if option == "Search for a question":
        query = st.text_input("Enter a search term:")
        if query:
            results = search_qa(query)
            display_qa_for_selection(results)
            question_number = st.number_input("Select the question number to add to favorites:", min_value=1, max_value=len(results), step=1)
            if st.button("Add to Favorites"):
                if 1 <= question_number <= len(results):
                    favorites.append(results[question_number - 1])
                    st.write("Added to favorites!")
                else:
                    st.write("Invalid question number.")

    elif option == "View favorite questions":
        if not favorites:
            st.write("No favorite questions saved.")
        else:
            display_qa_for_selection(favorites)

    elif option == "Exit":
        st.write("Exiting the Q&A Tool. Goodbye!")

if __name__ == "__main__":
    main()
