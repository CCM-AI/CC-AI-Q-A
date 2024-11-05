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

# Function to detect language and search questions by keyword
def search_qa(query):
    translator = Translator()
    
    # Convert the query to lowercase for consistent searching
    query_lower = query.lower()
    results = []

    # Check if the query is in English or Arabic
    if translator.detect(query).lang == 'ar':
        # If the query is in Arabic, translate the questions to Arabic and search
        for item in qa_data:
            translated_question = translator.translate(item['Q'], src='en', dest='ar').text.lower()
            if query_lower in translated_question:
                results.append(item)
    else:
        # Assume English if not Arabic
        for item in qa_data:
            translated_question = translator.translate(item['Q'], src='ar', dest='en').text.lower()
            if query_lower in translated_question:
                results.append(item)

    return results

# Function to display questions and answers
def display_qa_for_selection(qa_list, translate=False, lang='en', strings=None):
    if not qa_list:
        st.write(strings['no_results_found'])
        return

    for idx, item in enumerate(qa_list):
        question_key = f"question_{idx}_{item['Q']}"  # Create a unique key for each question
        answer_key = f"answer_{idx}_{item['Q']}"  # Create a unique key for each answer
        
        # Translate the question and answer if needed
        if translate:
            translator = Translator()
            translated_question = translator.translate(item['Q'], dest=lang).text
            translated_answer = translator.translate(item['A'], dest=lang).text
        else:
            translated_question = item['Q']
            translated_answer = item['A']
        
        # Show question with a button to toggle the answer
        show_answer = st.session_state.get(answer_key, False)
        if st.button(f"**{translated_question}**", key=question_key, help=strings['click_to_toggle_answer']):
            # Toggle the answer visibility
            st.session_state[answer_key] = not show_answer
            show_answer = not show_answer

        # Show the translated answer if toggled
        if show_answer:
            st.write(f"**{strings['answer']}**: {translated_answer}")

        # Favorite functionality
        favorite_key = f"favorite_{idx}_{item['Q']}"  # Unique key for add/remove favorite
        if item in st.session_state.favorites:
            if st.button(f"❌ {strings['remove_from_my_list']}", key=f"remove_{favorite_key}"):
                st.session_state.favorites.remove(item)
                st.success(f"{strings['removed']} '{translated_question}' {strings['from_my_list']}.")
        else:
            if st.button(f"✔️ {strings['add_to_my_list']}", key=f"add_{favorite_key}"):
                st.session_state.favorites.append(item)
                st.success(f"{strings['added']} '{translated_question}' {strings['to_my_list']}.")

# Translate language options dynamically
def translate_language_options():
    language_dict = {
        'en': 'English',
        'ar': 'اللغة العربية'
    }
    return language_dict

# Translate UI strings for each language
def get_translated_strings(lang):
    strings = {
        'en': {
            'welcome': "Welcome! You can either search for questions, select from a list of topics, or view your saved favorites.",
            'choose_option': "Choose an option to explore:",
            'search_by_keywords': "Search by Keywords",
            'select_from_list': "Select from a List",
            'my_list': "MY LIST: Your Favorite Questions and Answers",
            'no_results_found': "No results found.",
            'answer': "Answer",
            'click_to_toggle_answer': "Click to toggle answer visibility",
            'remove_from_my_list': "Remove from MY LIST",
            'add_to_my_list': "Add to MY LIST",
            'removed': "Removed",
            'from_my_list': "from MY LIST.",
            'added': "Added",
            'to_my_list': "to MY LIST."
        },
        'ar': {
            'welcome': "مرحباً! يمكنك البحث عن الأسئلة، أو اختيار من قائمة المواضيع، أو عرض المفضلة المحفوظة.",
            'choose_option': "اختر خيارًا للاستكشاف:",
            'search_by_keywords': "البحث بالكلمات الرئيسية",
            'select_from_list': "اختيار من قائمة",
            'my_list': "قائمتي: الأسئلة والأجوبة المفضلة لديك",
            'no_results_found': "لم يتم العثور على نتائج.",
            'answer': "إجابة",
            'click_to_toggle_answer': "انقر للتبديل بين عرض الإجابة",
            'remove_from_my_list': "إزالة من قائمتي",
            'add_to_my_list': "إضافة إلى قائمتي",
            'removed': "تم الإزالة",
            'from_my_list': "من قائمتي.",
            'added': "تم الإضافة",
            'to_my_list': "إلى قائمتي."
        }
    }
    return strings.get(lang, strings['en'])  # Default to English if language not found

# Main Streamlit app
def main():
    language_dict = translate_language_options()
    target_language = st.selectbox(
        "What does this mean in your own language?",  # Prompt dynamically translated
        list(language_dict.keys()), 
        format_func=lambda x: language_dict[x]
    )

    # Get translated UI strings
    strings = get_translated_strings(target_language)

    # Translate the "Welcome" message dynamically based on the selected language
    st.write(strings['welcome'])

    # Option to choose between search or selection
    option = st.radio(strings['choose_option'], [strings['search_by_keywords'], strings['select_from_list'], strings['my_list']])

    # Handle Search by Keywords
    if option == strings['search_by_keywords']:
        query = st.text_input(strings['search_by_keywords'])

        if query:
            # Search only in English and Arabic
            results = search_qa(query)

            if results:
                st.write(f"{strings['found']} {len(results)} {strings['matching_question']}:")

                display_qa_for_selection(results, translate=True, lang=target_language, strings=strings)
            else:
                st.warning(strings['no_results_found'])
    
    # Handle Select from a List
    elif option == strings['select_from_list']:
        # Display a list of questions
        st.write(strings['select_from_list'])
        display_qa_for_selection(qa_data, translate=True, lang=target_language, strings=strings)
    
    # Handle MY LIST: Your Favorite Questions and Answers
    elif option == strings['my_list']:
        if st.session_state.favorites:
            st.write(f"### {strings['my_list']}:")
            display_qa_for_selection(st.session_state.favorites, translate=True, lang=target_language, strings=strings)
        else:
            st.write(strings['no_favorites'])

if __name__ == "__main__":
    main()
