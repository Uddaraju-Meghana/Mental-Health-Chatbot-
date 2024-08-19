import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
from flask import Flask, render_template, request

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents and responses from JSON file
intents = json.loads(open('data.json').read())

def clean_up_sentence(sentence):
    # Tokenize the sentence
    sentence_words = nltk.word_tokenize(sentence)
    # Lemmatize each word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    # Tokenize the sentence
    sentence_words = clean_up_sentence(sentence)
    # Create a bag of words array
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return bag

def predict_class(sentence, intents_json):
    # Get the list of words and classes
    words = set()
    for intent in intents_json['intents']:
        for pattern in intent['patterns']:
            words.update(clean_up_sentence(pattern))
    words = sorted(list(words))
    
    # Get the bag of words
    bow = bag_of_words(sentence, words)
    
    # Simple rule-based prediction
    for intent in intents_json['intents']:
        for pattern in intent['patterns']:
            if set(clean_up_sentence(sentence)).intersection(set(clean_up_sentence(pattern))):
                return {"intent": intent['tag'], "probability": "1.0"}
    return {"intent": "unknown", "probability": "0.0"}

def get_response(prediction, intents_json):
    tag = prediction['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "I didn't understand that."

def chatbot_response(msg):
    prediction = predict_class(msg, intents)
    response = get_response(prediction, intents)
    return response

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

if __name__ == "__main__":
    app.run()
