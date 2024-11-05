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
    
    # Translate the query to the target language
    translated_query = translator.translate(query, dest=lang).text.lower()

    # Search in the dataset for questions that match the translated query
    results = [item for item in qa_data if translated_query in translator.translate(item['Q'], dest=lang).text.lower()]
    return results

# Function to toggle answers and add/remove favorites
def display_qa_for_selection(qa_list, translate=False, lang='en', strings=None):
    if not qa_list:
        st.write(strings['no_results_found'])
        return

    for idx, item in enumerate(qa_list):
        question_key = f"question_{idx}_{item['Q']}"  # Create a unique key for each question
        answer_key = f"answer_{idx}_{item['Q']}"  # Create a unique key for each answer
        
        # Translate the question and answer
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

        # Distinguish the "Add to MY LIST" and "Remove from MY LIST" buttons by styling
        favorite_key = f"favorite_{idx}_{item['Q']}"  # Unique key for add/remove favorite
        if item in st.session_state.favorites:
            # Styled 'Remove from MY LIST' button
            if st.button(f"❌ {strings['remove_from_my_list']}", key=f"remove_{favorite_key}", help=strings['remove_from_favorites'], use_container_width=True):
                st.session_state.favorites.remove(item)
                st.success(f"{strings['removed']} '{translated_question}' {strings['from_my_list']}.")
        else:
            # Styled 'Add to MY LIST' button
            if st.button(f"✔️ {strings['add_to_my_list']}", key=f"add_{favorite_key}", help=strings['add_to_favorites'], use_container_width=True):
                st.session_state.favorites.append(item)
                st.success(f"{strings['added']} '{translated_question}' {strings['to_my_list']}.")

# Translate language options dynamically
def translate_language_options():
    language_dict = {
        'en': 'English',
        'zh-cn': '中文 (Chinese)',
        'ar': 'اللغة العربية'
    }
    return language_dict

# Translate the label "What does this mean in your own language?" dynamically
def translate_label_text(lang):
    translator = Translator()
    text = "What does this mean in your own language?"
    return translator.translate(text, dest=lang).text

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
            'remove_from_favorites': "Click to remove from favorites",
            'add_to_my_list': "Add to MY LIST",
            'add_to_favorites': "Click to add to favorites",
            'removed': "Removed",
            'from_my_list': "from MY LIST.",
            'added': "Added",
            'to_my_list': "to MY LIST.",
            'found': "Found",
            'matching_question': "matching question(s):"
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
            'remove_from_favorites': "انقر لإزالة من المفضلة",
            'add_to_my_list': "إضافة إلى قائمتي",
            'add_to_favorites': "انقر لإضافة إلى المفضلة",
            'removed': "تم الإزالة",
            'from_my_list': "من قائمتي.",
            'added': "تم الإضافة",
            'to_my_list': "إلى قائمتي.",
            'found': "تم العثور على",
            'matching_question': "سؤال (ق) مطابق:"
        },
        'zh-cn': {
            'welcome': "欢迎！你可以搜索问题，选择一个话题列表，或查看你保存的收藏。",
            'choose_option': "选择一个选项进行探索：",
            'search_by_keywords': "按关键字搜索",
            'select_from_list': "从列表中选择",
            'my_list': "我的列表：你喜欢的问答",
            'no_results_found': "未找到结果。",
            'answer': "回答",
            'click_to_toggle_answer': "点击以切换答案可见性",
            'remove_from_my_list': "从我的列表中删除",
            'remove_from_favorites': "点击以从收藏夹中删除",
            'add_to_my_list': "添加到我的列表",
            'add_to_favorites': "点击以添加到收藏夹",
            'removed': "已删除",
            'from_my_list': "从我的列表中。",
            'added': "已添加",
            'to_my_list': "到我的列表。",
            'found': "找到",
            'matching_question': "匹配的问题:"
        }
    }
    return strings.get(lang, strings['en'])  # Default to English if language not found

# Main Streamlit app
def main():
    # Language selection for translation (only Arabic, English, Chinese)
    language_dict = translate_language_options()
    target_language = st.selectbox(
        "What does this mean in your own language?",  # Prompt dynamically translated
        list(language_dict.keys()), 
        format_func=lambda x: language_dict[x]
    )

    # Translate the "What does this mean in your own language?" label dynamically
    translate = target_language != 'en'  # Only translate if language is not 'en' (default)

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
            # Search in the selected language
            results = search_qa(query, target_language)

            if results:
                st.write(f"{strings['found']} {len(results)} {strings['matching_question']}:")

                display_qa_for_selection(results, translate, target_language, strings)
            else:
                st.warning(strings['no_results_found'])
    
    # Handle Select from a List
    elif option == strings['select_from_list']:
        # Display a list of questions
        st.write(strings['select_from_list'])
        display_qa_for_selection(qa_data, translate, target_language, strings)
    
    # Handle MY LIST: Your Favorite Questions and Answers
    elif option == strings['my_list']:
        if st.session_state.favorites:
            st.write(f"### {strings['my_list']}:")
            display_qa_for_selection(st.session_state.favorites, translate, target_language, strings)
        else:
            st.write(strings['no_favorites'])

if __name__ == "__main__":
    main()
