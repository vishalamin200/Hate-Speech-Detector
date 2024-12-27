from flask import Flask, request, jsonify
import re
import string
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from googletrans import Translator
import nltk

app = Flask(__name__)

class HateController:

    stopword = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Custom contraction map
    CONTRACTIONS = {
        "don't": "do not",
        "can't": "cannot",
        "won't": "will not",
        "i'm": "i am",
        "you're": "you are",
        "they're": "they are",
        "we're": "we are",
        "it's": "it is",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "hasn't": "has not",
        "haven't": "have not",
        "hadn't": "had not",
        "doesn't": "does not",
        "didn't": "did not",
        "shouldn't": "should not",
        "wouldn't": "would not",
        "couldn't": "could not",
        "mightn't": "might not",
        "mustn't": "must not",
    }

    def __init__(self):
        # nltk.download('punkt')
        # nltk.download('stopwords')
        # nltk.download('wordnet')
        pass

    @staticmethod
    def hate_build():
        # Retrieve JSON data from the request
        json_data = request.get_json()
        print("route hit")

        # Extract initial_state and goal_state from JSON data
        initial_state = json_data.get("initial_state")
        language = json_data.get("lang")

        # Validate input data
        if initial_state is None:
            return jsonify({"error": "Initial audio/text not provided"}), 400
        if language is None:
            return jsonify({"error": "Language not provided"}), 400

        solution = ""
        converted_text = ""
        if language == "en-US":
            solution = HateController.check_speech(initial_state)
        else:
            print("Other than english")
            converted_text = HateController.translate_to_english(initial_state, language)
            solution = HateController.check_speech(converted_text)

        # Prepare the response

        response = {"vibe": solution, "converted_text": converted_text}

        # Return the response with status code 200 (OK)
        return jsonify(response), 200




    @staticmethod
    def clean(text):
        # Lowercase the text
        text = text.lower()
    
        # Expand contractions
        for contraction, full_form in HateController.CONTRACTIONS.items():
            text = re.sub(rf"\b{contraction}\b", full_form, text)
    
        # Remove URLs
        text = re.sub(r"https?://\S+|www\.\S+", "", text)
    
        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)
    
        # Remove emojis and non-ASCII characters
        text = re.sub(r"[^\x00-\x7f]", "", text)
    
        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))
    
        # Remove numbers
        text = re.sub(r"\b\d+\b", "", text)
    
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()
    
        # Tokenization
        words = word_tokenize(text)
    
        # Remove stopwords and apply lemmatization
        words = [HateController.lemmatizer.lemmatize(word) for word in words if word not in HateController.stopword]
    
        # Join words back into a single string
        text = " ".join(words)
    
        return text


    @staticmethod
    def check_speech(initial_state):
        try:
            # Load the CountVectorizer
            cv = joblib.load("models/Countvectorizer_model.pkl")  # Load CountVectorizer from file

            # Load the trained model
            model = joblib.load("models/Hate_model.pkl")  # Load your trained model from file  

        except (FileNotFoundError, joblib.JoblibError) as e:
            # Handle file not found or deserialization errors
            print("Error loading model:", e)
            return "Model loading error"

        # Clean the input text
        cleaned_text = HateController.clean(initial_state)

        # Transform the cleaned text using the loaded CountVectorizer
        input_data = cv.transform([cleaned_text])

        # Make predictions
        prediction = model.predict(input_data)[0]  # Predict whether the text is hate speech
        
        return prediction


    @staticmethod
    def translate_to_english(text, source_language):
        print(source_language, text)
        try:
            if text is None:
                raise ValueError("Input text is None")
            if source_language is None or len(source_language) < 2:
                raise ValueError("Invalid source language")

            print("Input text:", text)
            print("Source language:", source_language)

            translator = Translator()

            # Extract language code from source_language
            src_lang = source_language.split('-')[0]

            print("Source language code:", src_lang)

            # Translate the text to English
            translation = translator.translate(text, src=src_lang, dest='en')

            # Get the translated text
            translated_text = translation.text
            print("Translation:", translated_text)

            return translated_text

        except Exception as e:
            print("Error during translation:", e)
            return "Translation error"


@app.route('/hate', methods=['POST'])
def solve_hate():
    return HateController.hate_build()

if __name__ == '__main__':
    app.run(debug=True)
