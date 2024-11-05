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
def search_qa(query, lang='en'):
    translator = Translator()
    translated_query = translator.translate(query, dest=lang).text

    # Match with original English questions
    results = []
    for item in qa_data:
        translated_question = translator.translate(item['Q'], dest=lang).text
        if translated_query.lower() in translated_question.lower():
            results.append(item)
    
    return results

# Function to toggle answers and add/remove favorites
def display_qa_for_selection(qa_list, translate=False, lang='en'):
    if not qa_list:
        st.write(translations[lang]["no_results"])
        return

    for idx, item in enumerate(qa_list):
        question_key = f"question_{idx}_{item['Q']}"
        answer_key = f"answer_{idx}_{item['Q']}"

        # Show question with a button to toggle the answer
        show_answer = st.session_state.get(answer_key, False)
        if st.button(f"**{item['Q']}**", key=question_key):
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
            st.write(f"**{translations[lang]['answer_label']}**: {translated_answer}")

        # Favorite buttons
        favorite_key = f"favorite_{idx}_{item['Q']}"
        if item in st.session_state.favorites:
            if st.button(f"❌ {translations[lang]['remove_favorite']}", key=f"remove_{favorite_key}"):
                st.session_state.favorites.remove(item)
                st.success(f"Removed '{translated_question}' from {translations[lang]['my_list']}.")
        else:
            if st.button(f"✔️ {translations[lang]['add_favorite']}", key=f"add_{favorite_key}"):
                st.session_state.favorites.append(item)
                st.success(f"Added '{translated_question}' to {translations[lang]['my_list']}.")

# Translation dictionary for UI text
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

# Main Streamlit app
def main():
    # Language selection for translation
    target_language = st.selectbox(
        translations['en']['search_prompt'],
        ['en', 'ar'],
        format_func=lambda x: 'English' if x == 'en' else 'العربية'
    )

    translate = target_language != 'en'

    # Welcome message based on selected language
    st.write(translations[target_language]['welcome'])

    # Option to choose between search or selection
    option = st.radio(translations[target_language]['choose_option'], 
                      [translations[target_language]['select_list'], 
                       translations[target_language]['my_list']])

    # Handle Search by Keywords
    if option == translations[target_language]['select_list']:
        query = st.text_input(translations[target_language]['search_prompt'])

        if query:
            results = search_qa(query, target_language)

            if results:
                st.write(f"Found {len(results)} matching question(s):")
                display_qa_for_selection(results, translate, target_language)
            else:
                st.warning(translations[target_language]['no_results'])
    
    # Handle MY LIST: Your Favorite Questions and Answers
    elif option == translations[target_language]['my_list']:
        if st.session_state.favorites:
            st.write("### " + translations[target_language]['my_list'] + ":")
            display_qa_for_selection(st.session_state.favorites, translate, target_language)
        else:
            st.write(translations[target_language]['no_results'])

if __name__ == "__main__":
    main()
