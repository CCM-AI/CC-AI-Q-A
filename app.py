def main():
    language_dict = translate_language_options()
    target_language = st.selectbox(
        "What does this mean in your own language?",
        list(language_dict.keys()), 
        format_func=lambda x: language_dict[x]
    )

    translate = target_language != 'en'
    strings = get_translated_strings(target_language)

    st.write(strings['welcome'])
    option = st.radio(strings['choose_option'], [strings['search_by_keywords'], strings['select_from_list'], strings['my_list']])

    if option == strings['search_by_keywords']:
        query = st.text_input(strings['search_by_keywords'])
        if query:
            results = search_qa(query, target_language)
            if results:
                st.write(f"{strings['found']} {len(results)} {strings['matching_question']}:")
                display_qa_for_selection(results, translate, target_language, strings)
            else:
                st.warning(strings['no_results_found'])
    
    elif option == strings['select_from_list']:
        st.write(strings['select_from_list'])
        display_qa_for_selection(qa_data, translate, target_language, strings)
    
    elif option == strings['my_list']:
        if st.session_state.favorites:
            st.write(f"### {strings['my_list']}:")
            display_qa_for_selection(st.session_state.favorites, translate, target_language, strings)
        else:
            st.write(strings['no_favorites'])

if __name__ == "__main__":
    main()
