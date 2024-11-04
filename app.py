import streamlit as st
import json
from googletrans import Translator

# Load the responses from the JSON file
with open('responses.json', 'r', encoding='utf-8') as f:
    responses = json.load(f)

# Initialize the translator
translator = Translator()

# Streamlit app layout
st.title("Multilingual Assistant")
user_input = st.text_input("Ask your question:")

if user_input:
    # Translate the user input to English
    translated_input = translator.translate(user_input, dest='en').text
    
    # Check for response
    response_found = False
    for entry in responses:
        if entry["Q"].lower() == translated_input.lower():
            st.write(entry["A"])
            response_found = True
            break
    
    if not response_found:
        st.write("I'm sorry, I don't have information on that topic.")
