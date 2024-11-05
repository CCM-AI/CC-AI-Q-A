import streamlit as st
import json
from googletrans import Translator

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
def display_qa_for_selection(qa_list, translate=False, lang='en'):
    if not qa_list:
        st.write("No results found.")
        return

    for idx, item in enumerate(qa_list):
        question_key = f"question_{idx}_{item['Q']}"  # Create a unique key for each question
        answer_key = f"answer_{idx}_{item['Q']}"  # Create a unique key for each answer
        
        # Show question with a button to toggle the answer
        show_answer = st.session_state.get(answer_key, False)
        if st.button(f"**{item['Q']}**", key=question_key, help="Click to toggle answer visibility"):
            # Toggle the answer visibility
            st.session_state[answer_key] = not show_answer
            show_answer = not show_answer

        # Translate the content if needed
        if translate:
            translator = Translator()
            translated_question = translator.translate(item['Q'], dest=lang).text
            translated_answer = translator.translate(item['A'], dest=lang).text
        else:
            translated_question = item['Q']
            translated_answer = item['A']

        # Show the translated answer if toggled
        if show_answer:
            st.write(f"**Answer**: {translated_answer}")

        # Distinguish the "Add to MY LIST" and "Remove from MY LIST" buttons by styling
        favorite_key = f"favorite_{idx}_{item['Q']}"  # Unique key for add/remove favorite
        if item in st.session_state.favorites:
            # Styled 'Remove from MY LIST' button
            if st.button(f"❌ Remove from MY LIST", key=f"remove_{favorite_key}", help="Click to remove from favorites", use_container_width=True):
                st.session_state.favorites.remove(item)
                st.success(f"Removed '{translated_question}' from MY LIST.")
        else:
            # Styled 'Add to MY LIST' button
            if st.button(f"✔️ Add to MY LIST", key=f"add_{favorite_key}", help="Click to add to favorites", use_container_width=True):
                st.session_state.favorites.append(item)
                st.success(f"Added '{translated_question}' to MY LIST.")

# Translate language options dynamically
def translate_language_options():
    language_dict = {
        'en': 'English',
        'es': 'Español',
        'fr': 'Français',
        'de': 'Deutsch',
        'it': 'Italiano',
        'pt': 'Português',
        'zh-cn': '中文',
        'ar': 'اللغة العربية'
    }
    return language_dict

# Main Streamlit app
def main():
    st.title("Health Q&A Tool")
    st.write("Welcome! You can either search for questions, select from a list of topics, or view your saved favorites.")

    # Language selection for translation
    language_dict = translate_language_options()
    target_language = st.selectbox(
        "What does this mean in your own language?",  # Prompt dynamically translated
        list(language_dict.keys()), 
        format_func=lambda x: language_dict[x]
    )

    # Handle Search by Keywords
    option = st.radio("Choose an option to explore:", ["Search by Keywords", "Select from a List", "MY LIST: Your Favorite Questions and Answers"])

    # Translate the "What does this mean in your own language?" label dynamically based on selection
    translate = target_language != 'en'  # Only translate if language is not 'en' (default)

    # Handle Search by Keywords
    if option == "Search by Keywords":
        query = st.text_input("Enter a keyword to search for questions:")

        if query:
            results = search_qa(query)

            if results:
                st.write(f"Found {len(results)} matching question(s):")
                display_qa_for_selection(results, translate, target_language)
            else:
                st.warning("No questions found matching your search. Please try a different keyword.")
    
    # Handle Select from a List
    elif option == "Select from a List":
        # Display a list of questions
        st.write("Here are the available questions:")
        display_qa_for_selection(qa_data, translate, target_language)
    
    # Handle MY LIST: Your Favorite Questions and Answers
    elif option == "MY LIST: Your Favorite Questions and Answers":
        if st.session_state.favorites:
            st.write("### Your Favorite Questions and Answers:")
            display_qa_for_selection(st.session_state.favorites, translate, target_language)
        else:
            st.write("You don't have any questions in your favorites yet. Try adding some from the other sections.")

if __name__ == "__main__":
    main()
