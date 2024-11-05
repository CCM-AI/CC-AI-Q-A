import streamlit as st
import json
from googletrans import Translator

# Load the Q&A data from JSON
@st.cache_data
def load_qa_data():
    with open('responses.json', 'r') as f:
        return json.load(f)

# Load initial Q&A data
qa_data = load_qa_data()

# Set up translator and cache translations
translator = Translator()

# Cache translations for questions and answers to avoid repetitive API calls
@st.cache_data
def translate_qa_data(qa_data, target_language):
    if target_language == 'en':
        return qa_data  # No translation needed for English
    
    translated_data = []
    for item in qa_data:
        translated_data.append({
            'Q': translator.translate(item['Q'], dest=target_language).text,
            'A': translator.translate(item['A'], dest=target_language).text
        })
    return translated_data

# Translate UI text for supported languages
translations = {
    'en': {
        "welcome": "Welcome! You can either search for questions, select from a list of topics, or view your saved favorites.",
        "search_prompt": "Enter a keyword to search for questions:",
        "choose_option": "Choose an option to explore:",
        "select_list": "Select from a List",
        "my_list": "MY LIST: Your Favorite Questions and Answers",
        "no_results": "No results found.",
        "answer_label": "Answer",
        "remove_favorite": "Remove from MY LIST",
        "add_favorite": "Add to MY LIST"
    },
    'ar': {
        "welcome": "مرحباً! يمكنك البحث عن الأسئلة، أو اختيار من قائمة المواضيع، أو عرض المفضلة المحفوظة.",
        "search_prompt": "أدخل كلمة رئيسية للبحث عن الأسئلة:",
        "choose_option": "اختر خيارًا للاستكشاف:",
        "select_list": "اختر من قائمة",
        "my_list": "قائمتي: أسئلتك وأجوبتك المفضلة",
        "no_results": "لم يتم العثور على نتائج.",
        "answer_label": "الإجابة",
        "remove_favorite": "إزالة من قائمتي",
        "add_favorite": "إضافة إلى قائمتي"
    }
}

# Function to search questions based on pre-translated data
def search_qa(query, qa_data):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

# Display function with optimized toggling and caching
def display_qa_for_selection(qa_list, language):
    if not qa_list:
        st.write(translations[language]["no_results"])
        return

    for idx, item in enumerate(qa_list):
        question_key = f"question_{idx}_{item['Q']}"
        answer_key = f"answer_{idx}_{item['Q']}"

        # Display each question as a button for toggling the answer visibility
        show_answer = st.session_state.get(answer_key, False)
        if st.button(f"**{item['Q']}**", key=question_key):
            st.session_state[answer_key] = not show_answer
            show_answer = not show_answer

        # Show the answer if toggled
        if show_answer:
            st.write(f"**{translations[language]['answer_label']}**: {item['A']}")

        # Add/Remove from favorites buttons
        favorite_key = f"favorite_{idx}_{item['Q']}"
        if item in st.session_state.favorites:
            if st.button(f"❌ {translations[language]['remove_favorite']}", key=f"remove_{favorite_key}"):
                st.session_state.favorites.remove(item)
                st.success(f"Removed '{item['Q']}' from {translations[language]['my_list']}.")
        else:
            if st.button(f"✔️ {translations[language]['add_favorite']}", key=f"add_{favorite_key}"):
                st.session_state.favorites.append(item)
                st.success(f"Added '{item['Q']}' to {translations[language]['my_list']}.")

# Main Streamlit app
def main():
    # Set default session state for favorites
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    # Language selection for translation
    target_language = st.selectbox(
        "Select Language", 
        ['en', 'ar'], 
        format_func=lambda x: 'English' if x == 'en' else 'العربية'
    )

    # Welcome message based on selected language
    st.write(translations[target_language]["welcome"])

    # Option to choose between search or selection
    option = st.radio(translations[target_language]["choose_option"],
                      [translations[target_language]["select_list"], 
                       translations[target_language]["my_list"]])

    # Translate Q&A data if needed
    translated_qa_data = translate_qa_data(qa_data, target_language)

    # Handle "Search by Keywords"
    if option == translations[target_language]["select_list"]:
        query = st.text_input(translations[target_language]["search_prompt"])
        if query:
            results = search_qa(query, translated_qa_data)
            if results:
                st.write(f"{len(results)} {translations[target_language]['answer_label']} found.")
                display_qa_for_selection(results, target_language)
            else:
                st.warning(translations[target_language]["no_results"])

    # Handle "MY LIST: Your Favorite Questions and Answers"
    elif option == translations[target_language]["my_list"]:
        if st.session_state.favorites:
            st.write("### " + translations[target_language]["my_list"] + ":")
            display_qa_for_selection(st.session_state.favorites, target_language)
        else:
            st.write(translations[target_language]["no_results"])

if __name__ == "__main__":
    main()
