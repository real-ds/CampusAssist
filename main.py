import spacy
import csv
import difflib



# Load the English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# Mount Google Drive
drive.mount('/content/drive')

def tokenize_string(string):
    # Tokenize the string by splitting on spaces and removing punctuation
    return [token.strip(".,?!") for token in string.lower().split()]

def extract_nouns_from_question(question):
    # Process the question using spaCy
    doc = nlp(question)

    # Extract tokens that are nouns
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']

    return nouns

def search_record_in_csv(name, csv_file_path):
    # Open the CSV file and search for the exact match
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if name.lower() == row['Name'].lower():
                return row
    return None

# Function to print CSV content
def print_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

# Main function
def main():
    csv_file_path = '/content/drive/MyDrive/facdata - Sheet1.csv'  # Update with your CSV file path
    print_csv(csv_file_path)

    while True:
        question = input("Enter your query (type 'quit', 'thank you', or 'thanks' to end): ").strip()

        if question.lower() in ['quit', 'thank you', 'thanks']:
            print("Program ended.")
            break

        # Extract nouns from the question
        nouns = extract_nouns_from_question(question)

        if nouns:
            # Search for records in CSV based on extracted nouns
            for noun in nouns:
                found_record = search_record_in_csv(noun, csv_file_path)
                if found_record:
                    print("Match found for:", noun)
                    print("ID:", found_record['Id'])
                    print("Name:", found_record['Name'])
                    print("School:", found_record['School'])
                    print("Cabin Location:", found_record['Cabin Location'])
                    print("Email ID:", found_record['Email ID'])
                    break  # Stop searching if a match is found
            else:
                print("No match found for:", ", ".join(nouns))
        else:
            print("No relevant nouns found in the query.")

if __name__ == "__main__":
    main()
