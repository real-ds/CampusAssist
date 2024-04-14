from flask import Flask, render_template, request, jsonify
import csv
import difflib
import spacy

# Load the English language model for spaCy
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# Load CSV data
csv_file_path = 'facdata - Sheet1 (1).csv'  # Update with your CSV file path
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    csv_data = list(reader)

def extract_nouns_from_question(question):
    # Define a set of question words and the verb "is"
    question_words = {"where", "what", "how", "when", "who", "does", "is"}

    # Process the question using spaCy
    doc = nlp(question)

    # Extract tokens that are not question words or "is"
    nouns = [token.text for token in doc if token.text.lower() not in question_words and token.text.lower() != "is"]

    # Remove possessive marker "'s" from the remaining tokens
    nouns = [token[:-2] if token.endswith("'s") else token for token in nouns]

    return nouns

def search_record_in_csv(name, info_type):
    matches = []
    for row in csv_data:
        # Tokenize the name from the CSV file
        csv_name_tokens = row['Name'].lower().split()
        name_tokens = name.lower().split()
        # Compute similarity using difflib's SequenceMatcher
        similarity = difflib.SequenceMatcher(None, name_tokens, csv_name_tokens).ratio()
        if similarity > 0.6:  # Adjust the threshold as needed
            matches.append((row, similarity))

    if matches:
        # Sort matches by similarity and return the closest match
        matches.sort(key=lambda x: x[1], reverse=True)
        found_record = matches[0][0]
        if info_type.lower() == 'cabin':
            return found_record['Cabin Location']
        elif info_type.lower() == 'email':
            return found_record['Email ID']
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/collegemap')
def index1():
    return render_template('collegemap.html')

@app.route('/facultydetails')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    question = data['question']
    nouns = extract_nouns_from_question(question)
    if nouns:
        info_type = 'cabin'  # Default to cabin location
        if 'contact' in question.lower() or 'email' in question.lower():
            info_type = 'email'

        # Search for records in CSV based on extracted nouns
        for noun in nouns:
            found_info = search_record_in_csv(noun, info_type)
            if found_info: 
                response = f"{info_type.capitalize()} found: {found_info}"
                return jsonify({'response': response})
        else:
            response = f"No {info_type} found for any entered Query in the question."
            return jsonify({'response': response})
    else:
        response = "No relevant Faculty Data found in the question You Mentioned."
        return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
