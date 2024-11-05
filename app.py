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

# Display the questions and answers for the user to select as favorites
def display_qa_for_selection(qa_list):
    if not qa_list:
        st.write("No results found.")
        return

    selected_questions = []

    # List the questions with checkboxes for selection
    for idx, item in enumerate(qa_list):
        # Provide a unique key by using the question text and its index
        if st.checkbox(f"**{item['Q']}**", key=f"{item['Q']}_{idx}"):
            selected_questions.append(item)
    
    # Add selected questions to favorites
    if selected_questions:
        for selected in selected_questions:
            if selected not in favorites:
                favorites.append(selected)
                st.success(f"Added '{selected['Q']}' to your favorites!")

    # Display answers for selected questions
    if selected_questions:
        st.write("### Answers to Your Selected Questions:")
        for selected in selected_questions:
            st.write(f"**{selected['Q']}**")
            st.write(f"**Answer**: {selected['A']}")
    else:
        st.write("No questions selected yet.")

# Main Streamlit app
def main():
    st.title("Health Q&A Tool")
    st.write("Welcome! You can either search for questions or select from the list of questions to add to your favorites.")

    # Option to choose between search or selection
    option = st.radio("Choose how you want to explore:", ["Search by Keywords", "Select from a List"])

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
        # Display all questions if no categories
        st.write("Here are all the questions available:")
        display_qa_for_selection(qa_data)

    # Display the user's favorites
    if favorites:
        st.write("### Your Favorite Questions:")
        for item in favorites:
            st.write(f"- **{item['Q']}**")

    # If no favorites, guide the user to add one
    if not favorites:
        st.write("You haven't added any questions to your favorites yet. Try selecting or searching one.")

if __name__ == "__main__":
    main()
