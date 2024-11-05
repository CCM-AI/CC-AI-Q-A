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
            st.write(f"**Answer**: {item['A']}")

            # Add to favorites button
            if st.button(f"Add '{item['Q']}' to Favorites", key=f"favorite_{index}"):
                if item not in favorites:
                    favorites.append(item)
                    st.success(f"Added '{item['Q']}' to your favorites!")
                else:
                    st.warning(f"'{item['Q']}' is already in your favorites.")

# Display the user's favorites with both question and answer
def display_favorites():
    if favorites:
        st.write("### Your Favorite Questions:")
        for index, item in enumerate(favorites):
            st.write(f"- **{item['Q']}**")
            st.write(f"  **Answer**: {item['A']}")
            st.markdown("---")  # Adds a separator between favorites
    else:
        st.write("You haven't added any questions to your favorites yet. Try selecting or searching one.")

# Main Streamlit app
def main():
    st.title("Health Q&A Tool")
    st.write("Welcome! You can either search for questions or explore all available questions.")

    # Option to choose between search or view all questions
    option = st.radio("Choose how you want to explore:", ["Search by Keywords", "View All Questions"])

    if option == "Search by Keywords":
        query = st.text_input("Enter a keyword to search for questions:")

        if query:
            results = search_qa(query)

            if results:
                st.write(f"Found {len(results)} matching question(s):")
                display_faq(results)
            else:
                st.warning("No questions found matching your search. Please try a different keyword.")

    elif option == "View All Questions":
        st.write("Here are all the available questions:")
        display_faq(qa_data)

    # Display the user's favorites section
    display_favorites()

if __name__ == "__main__":
    main()
