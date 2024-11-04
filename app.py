import json

# Sample Q&A data with tags
qa_data = [
    {"tags": ["asthma"], "Q": "What is asthma?", "A": "Asthma is a chronic inflammatory disease of the airways that causes difficulty in breathing."},
    {"tags": ["blood pressure", "hypertension"], "Q": "What is considered high blood pressure?", "A": "High blood pressure (hypertension) is generally defined as a reading of 130/80 mm Hg or higher."},
    {"tags": ["diabetes"], "Q": "What is diabetes?", "A": "Diabetes is a chronic condition characterized by high blood sugar levels."},
    # Add more Q&A pairs as needed...
]

favorites = []

def display_qa(qa_list):
    if not qa_list:
        print("No results found.")
        return
    for i, item in enumerate(qa_list, start=1):
        print(f"{i}. Q: {item['Q']}\n   A: {item['A']}\n")

def search_qa(query):
    results = [item for item in qa_data if query.lower() in item['Q'].lower()]
    return results

def filter_by_tag(tag):
    results = [item for item in qa_data if tag.lower() in (t.lower() for t in item['tags'])]
    return results

def add_to_favorites(question):
    favorites.append(question)
    print("Added to favorites!")

def view_favorites():
    if not favorites:
        print("No favorite questions saved.")
        return
    display_qa(favorites)

def main():
    while True:
        print("Welcome to the Q&A Tool!")
        print("1. View all questions")
        print("2. Search for a question")
        print("3. Filter by tag")
        print("4. View favorite questions")
        print("5. Add a question to favorites")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            display_qa(qa_data)
        elif choice == '2':
            query = input("Enter a search term: ")
            results = search_qa(query)
            display_qa(results)
        elif choice == '3':
            tag = input("Enter a tag (e.g., asthma, diabetes): ")
            results = filter_by_tag(tag)
            display_qa(results)
        elif choice == '4':
            view_favorites()
        elif choice == '5':
            question_number = int(input("Enter the question number you want to add to favorites: ")) - 1
            if 0 <= question_number < len(qa_data):
                add_to_favorites(qa_data[question_number])
            else:
                print("Invalid question number.")
        elif choice == '6':
            print("Exiting the Q&A Tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
