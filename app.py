import streamlit as st
import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the Q&A data from JSON
def load_qa_data():
    with open('responses.json', 'r') as f:
        qa_data = json.load(f)
    return qa_data

# Load initial Q&A data
qa_data = load_qa_data()
favorites = []

# Function to search questions by keyword
def search_qa(query):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

# Display the questions and answers as a mind map
def display_mind_map(qa_list):
    G = nx.Graph()  # Create an empty graph
    for item in qa_list:
        # Add a node for the question
        G.add_node(item['Q'])
        
        # Add an edge from the question to the answer
        G.add_edge(item['Q'], item['A'])
    
    # Draw the mind map
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # Positioning of nodes
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold")
    plt.title("Mind Map of Q&A", fontsize=16)
    st.pyplot(plt)

# Display questions for the user to select from
def display_qa_for_selection(qa_list):
    if not qa_list:
        st.write("No results found.")
        return

    # List the questions with buttons for selection
    for item in qa_list:
        if st.button(f"**{item['Q']}**"):
            # Display the answer
            st.write(f"**Answer**: {item['A']}")
            
            # Add to favorites button
            if st.button(f"Add '{item['Q']}' to Favorites"):
                favorites.append(item)
                st.success(f"Added '{item['Q']}' to your favorites!")

# Main Streamlit app
def main():
    st.title("Health Q&A Tool")
    st.write("Welcome! You can either search for questions or select from a list.")

    # Option to choose between search or selection
    option = st.radio("Choose how you want to explore:", ["Search by Keywords", "Select from a List"])

    if option == "Search by Keywords":
        query = st.text_input("Enter a keyword to search for questions:")
        
        if query:
            results = search_qa(query)
            
            if results:
                st.write(f"Found {len(results)} matching question(s):")
                display_qa_for_selection(results)
            else:
                st.warning("No questions found matching your search. Please try a different keyword.")

    elif option == "Select from a List":
        # Directly display all questions without categories
        st.write("Here are all the available questions:")
        display_qa_for_selection(qa_data)

    # Display the user's favorites
    if favorites:
        st.write("### Your Favorite Questions:")
        for item in favorites:
            st.write(f"- **{item['Q']}**")

    # If no favorites, guide the user to add one
    if not favorites:
        st.write("You haven't added any questions to your favorites yet. Try selecting or searching one.")

    # Optionally, show a mind map if there are questions displayed
    if query:
        display_mind_map(results)

if __name__ == "__main__":
    main()
