import streamlit as st
import json
from googletrans import Translator

# Load the Q&A data from JSON (ensure this is the right format)
def load_qa_data():
    with open('responses.json', 'r') as f:
        qa_data = json.load(f)
    return qa_data

# Function to translate text to selected language
def translate_text(text, lang_code):
    translator = Translator()
    try:
        translated_text = translator.translate(text, dest=lang_code).text
        return translated_text
    except Exception as e:
        st.error(f"Error in translation: {str(e)}")
        return text

# Load initial Q&A data
qa_data = load_qa_data()

# Translate content based on the selected language
def translate_qa_data(language):
    translated_data = []
    for item in qa_data:
        translated_question = translate_text(item['Q'], language)
        translated_answer = translate_text(item['A'], language)
        translated_data.append({"Q": translated_question, "A": translated_answer})
    return translated_data

# App instructions and labels in English and Arabic
translations = {
    "title": {
        "en": "Health Q&A Tool",
        "ar": "أداة الأسئلة والأجوبة الصحية"
    },
    "welcome": {
        "en": "Welcome! You can either search for questions or select from a list of topics.",
        "ar": "مرحبًا! يمكنك البحث عن الأسئلة أو الاختيار من قائمة الموضوعات."
    },
    "search": {
        "en": "Search by Keywords",
        "ar": "البحث باستخدام الكلمات الرئيسية"
    },
    "select": {
        "en": "Select from a List",
        "ar": "اختيار من قائمة"
    },
    "my_list": {
        "en": "MY LIST: Your Favorite Questions and Answers",
        "ar": "قائمتي: أسئلتي وأجوبتي المفضلة"
    },
    "no_results": {
        "en": "No results found.",
        "ar": "لم يتم العثور على نتائج."
    },
    "no_favorites": {
        "en": "You haven't added any questions to your favorites yet. Try selecting or searching one.",
        "ar": "لم تقم بإضافة أي أسئلة إلى المفضلة بعد. جرب تحديد أو البحث عن أحدها."
    },
    "remove_from_list": {
        "en": "Remove from MY LIST",
        "ar": "إزالة من قائمتي"
    },
    "add_to_list": {
        "en": "Add to MY LIST",
        "ar": "أضف إلى قائمتي"
    }
}

# Function to apply the selected language
def apply_language(selected_language):
    return translations[selected_language]

# Main Streamlit app
def main():
    # Language selection (English or Arabic)
    lang = st.selectbox("Select Language", ["en", "ar"])

    # Translate UI based on selected language
    labels = apply_language(lang)

    # Set the title and welcome message based on the selected language
    st.title(labels["title"])
    st.write(labels["welcome"])

    # Option to choose between search or selection
    option = st.radio("Choose how you want to explore:", [labels["search"], labels["select"]])

    # Load translated Q&A data based on the selected language
    translated_qa_data = translate_qa_data(lang)

    # Display questions for the user to select or search from
    if option == labels["search"]:
        query = st.text_input(labels["search"])

        if query:
            results = [item for item in translated_qa_data if query.lower() in item['Q'].lower()]

            if results:
                st.write(f"Found {len(results)} matching question(s):")
                for item in results:
                    if st.button(f"**{item['Q']}**", key=item['Q']):
                        st.write(f"**Answer**: {item['A']}")
                        if st.button(f"{labels['add_to_list']}", key=f"add_{item['Q']}"):
                            # Add to favorites functionality
                            st.success(f"Added '{item['Q']}' to your favorites!")

            else:
                st.warning(labels["no_results"])

    elif option == labels["select"]:
        # Here, display all questions for selection
        st.write(f"{labels['my_list']}:")
        for item in translated_qa_data:
            if st.button(f"**{item['Q']}**", key=f"button_{item['Q']}"):
                st.write(f"**Answer**: {item['A']}")
                if st.button(f"{labels['add_to_list']}", key=f"add_select_{item['Q']}"):
                    # Add to favorites functionality
                    st.success(f"Added '{item['Q']}' to your favorites!")

    # Display favorites
    if st.button(f"{labels['my_list']}"):
        st.write(f"### {labels['my_list']}:")
        # Dummy favorites list (this would ideally be persistent with state or database)
        favorites = []  # Add logic to store favorites
        if not favorites:
            st.write(labels["no_favorites"])

        for item in favorites:
            st.write(f"- **{item['Q']}**: {item['A']}")
            if st.button(f"{labels['remove_from_list']}", key=f"remove_{item['Q']}"):
                # Logic for removing from favorites
                st.success(f"Removed '{item['Q']}' from your favorites!")

if __name__ == "__main__":
    main()
