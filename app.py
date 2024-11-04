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
        st.write(f"**{i}. Q:** {item['Q']}")

# Function to search Q&A
def search_qa(query):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

# Main Streamlit app
def main():
    st.title("Q&A Tool - Your Personal Assistant")
    st.write("Welcome to the Q&A Tool! This tool helps you search for health-related questions and answers. Let's get started!")

    # Sidebar options with more friendly guidance
    option = st.sidebar.selectbox("Choose what you'd like to do:", [
        "Search for a question",
        "View favorite questions",
        "Add a question to favorites",
        "Exit"
    ])
    
    if option == "Search for a question":
        st.header("Step 1: Search for a Question")
        query = st.text_input("Enter a search term or a question (e.g., 'What is asthma?', 'hypertension'):")
        
        if query:
            results = search_qa(query)
            if results:
                st.write(f"Found {len(results)} matching question(s):")
                display_qa_for_selection(results)
                question_number = st.number_input("Select the question number to add to favorites:", min_value=1, max_value=len(results), step=1)
                
                if st.button("Add this question to Favorites"):
                    if 1 <= question_number <= len(results):
                        favorites.append(results[question_number - 1])
                        st.success("The question has been added to your favorites!")
                    else:
                        st.error("Invalid question number. Please select a valid number from the list.")
            else:
                st.warning("No questions found matching your search. Try a different keyword.")
        
        st.write("---")
        st.write("Tip: You can search for any health-related question, and we'll find the best matches for you!")

    elif option == "View favorite questions":
        st.header("Step 2: View Your Favorite Questions")
        if not favorites:
            st.write("You haven't added any questions to your favorites yet.")
            st.write("Go back and search for a question, then click 'Add to Favorites'.")
        else:
            st.write("Here are your favorite questions:")
            display_qa_for_selection(favorites)

    elif option == "Add a question to favorites":
        st.header("Step 3: Add a Question to Your Favorites")
        question_number = st.number_input("Enter the question number you want to add to your favorites:", min_value=1, max_value=len(qa_data), step=1)
        if st.button("Add to Favorites"):
            if 1 <= question_number <= len(qa_data):
                favorites.append(qa_data[question_number - 1])
                st.success("This question has been added to your favorites!")
            else:
                st.error("Invalid question number. Please select a valid number.")

    elif option == "Exit":
        st.write("Thank you for using the Q&A Tool! Have a great day!")
        st.stop()

if __name__ == "__main__":
    main()
