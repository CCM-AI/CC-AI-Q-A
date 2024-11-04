import streamlit as st
import json
from fuzzywuzzy import process

# Load responses from JSON file
with open('responses.json') as f:
    responses = json.load(f)

# Streamlit app layout
st.title("Personal Assistant")
st.write("Ask me about health conditions and treatments.")

# User input
user_input = st.text_input("What would you like to know?").lower()

# Check for response
if user_input:
    question_list = [item["Q"].lower() for item in responses]
    response = process.extractOne(user_input, question_list)
    if response[1] > 80:  # Confidence threshold
        answer = next(item for item in responses if item["Q"].lower() == response[0])
        st.write(answer["A"])
    else:
        st.write("I'm sorry, I don't have information on that topic.")
