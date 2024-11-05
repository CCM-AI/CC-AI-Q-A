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

# Predefined keywords in English (can add more for variety)
keyword_list_en = ["Python", "JavaScript", "Data Science", "Machine Learning", "Streamlit", "API"]

# Translate keywords based on selected language
def get_translated_keywords(lang):
    translator = Translator()
    return [translator.translate(keyword, dest=lang).text for keyword in keyword_list_en]

# Function to search questions by keyword
def search_qa(query, lang='en'):
    translator = Translator()
    translated_query = translator.translate(query, dest='en').text.lower()  # Always translate to English for dataset matching
    results = [item for item in qa_data if translated_query in item['Q'].lower()]
    return results

# Function to toggle answers and add/remove favorites
def display_qa_for_selection(qa_list, translate=False, lang='en', strings=None):
    if not qa_list:
        st.write(strings['no_results_found'])
        return

    for idx, item in enumerate(qa_list):
        question_key = f"question_{idx}_{item['Q']}"
        answer_key = f"answer_{idx}_{item['Q']}"

        if translate:
            translator = Translator()
            translated_question = translator.translate(item['Q'], dest=lang).text
            translated_answer = translator.translate(item['A'], dest=lang).text
        else:
            translated_question = item['Q']
            translated_answer = item['A']

        show_answer = st.session_state.get(answer_key, False)
        if st.button(f"**{translated_question}**", key=question_key, help=strings['click_to_toggle_answer']):
            st.session_state[answer_key] = not show_answer
            show_answer = not show_answer

        if show_answer:
            st.write(f"**{strings['answer']}**: {translated_answer}")

        favorite_key = f"favorite_{idx}_{item['Q']}"
        if item in st.session_state.favorites:
            if st.button(f"❌ {strings['remove_from_my_list']}", key=f"remove_{favorite_key}", help=strings['remove_from_favorites'], use_container_width=True):
                st.session_state.favorites.remove(item)
                st.success(f"{strings['removed']} '{translated_question}' {strings['from_my_list']}.")
        else:
            if st.button(f"✔️ {strings['add_to_my_list']}", key=f"add_{favorite_key}", help=strings['add_to_favorites'], use_container_width=True):
                st.session_state.favorites.append(item)
                st.success(f"{strings['added']} '{translated_question}' {strings['to_my_list']}.")

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

# Translate UI strings for each language
def get_translated_strings(lang):
    strings = {
        'en': {'search_by_keywords': "Search by Keywords", 'no_results_found': "No results found.", 'answer': "Answer"},
        'es': {'search_by_keywords': "Buscar por palabras clave", 'no_results_found': "No se encontraron resultados.", 'answer': "Respuesta"},
        'fr': {'search_by_keywords': "Recherche par mots-clés", 'no_results_found': "Aucun résultat trouvé.", 'answer': "Réponse"},
        # Add other languages here
    }
    return strings.get(lang, strings['en'])

# Main Streamlit app
def main():
    language_dict = translate_language_options()
    target_language = st.selectbox("Select your language:", list(language_dict.keys()), format_func=lambda x: language_dict[x])
    translate = target_language != 'en'
    strings = get_translated_strings(target_language)

    st.write(strings['search_by_keywords'])

    # Display predefined keywords in the selected language
    translated_keywords = get_translated_keywords(target_language)
    keyword = st.selectbox("Choose a keyword:", translated_keywords)

    # Input field for custom keyword search
    custom_keyword = st.text_input("Or enter your own keyword:")

    # Determine search query based on user choice
    if custom_keyword:
        search_query = custom_keyword
    else:
        search_query = keyword

    if search_query:
        results = search_qa(search_query, target_language)
        if results:
            st.write(f"Found {len(results)} matching questions:")
            display_qa_for_selection(results, translate, target_language, strings)
        else:
            st.warning(strings['no_results_found'])

if __name__ == "__main__":
    main()
