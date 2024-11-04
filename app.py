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

# Function to display Q&A
def display_qa(qa_list):
    if not qa_list:
        st.write("No results found.")
        return
    for item in qa_list:
        st.write(f"**Q:** {item['Q']}")
        st.write(f"**A:** {item['A']}")

# Function to search Q&A
def search_qa(query):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

# Function to filter Q&A by tag (you can implement this if your data has tags)
def filter_by_tag(tag):
    results = [item for item in qa_data if tag.lower() in item.get('tags', [])]
    return results

# Main Streamlit app
def main():
    st.title("Q&A Tool")

    # Sidebar options
    option = st.sidebar.selectbox("Choose an option", [
        "View all questions",
        "Search for a question",
        "Filter by tag",
        "View favorite questions",
        "Add a question to favorites",
        "Exit"
    ])

    if option == "View all questions":
        display_qa(qa_data)
    
    elif option == "Search for a question":
        query = st.text_input("Enter a search term:")
        if query:
            results = search_qa(query)
            display_qa(results)

    elif option == "Filter by tag":
        tag = st.text_input("Enter a tag (e.g., asthma, diabetes):")
        if tag:
            results = filter_by_tag(tag)
            display_qa(results)

    elif option == "View favorite questions":
        if not favorites:
            st.write("No favorite questions saved.")
        else:
            display_qa(favorites)

    elif option == "Add a question to favorites":
        question_number = st.number_input("Enter the question number you want to add to favorites:", min_value=1, max_value=len(qa_data), step=1)
        if st.button("Add to Favorites"):
            if 1 <= question_number <= len(qa_data):
                favorites.append(qa_data[question_number - 1])
                st.write("Added to favorites!")
            else:
                st.write("Invalid question number.")

    elif option == "Exit":
        st.write("Exiting the Q&A Tool. Goodbye!")

if __name__ == "__main__":
    main()
