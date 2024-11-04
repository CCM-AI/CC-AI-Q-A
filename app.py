import streamlit as st

# Sample Q&A data with tags
qa_data = [
    {"tags": ["asthma"], "Q": "What is asthma?", "A": "Asthma is a chronic inflammatory disease of the airways that causes difficulty in breathing."},
    {"tags": ["blood pressure", "hypertension"], "Q": "What is considered high blood pressure?", "A": "High blood pressure (hypertension) is generally defined as a reading of 130/80 mm Hg or higher."},
    {"tags": ["diabetes"], "Q": "What is diabetes?", "A": "Diabetes is a chronic condition characterized by high blood sugar levels."},
    # Add more Q&A pairs as needed...
]

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

# Function to filter Q&A by tag
def filter_by_tag(tag):
    results = [item for item in qa_data if tag.lower() in (t.lower() for t in item['tags'])]
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
