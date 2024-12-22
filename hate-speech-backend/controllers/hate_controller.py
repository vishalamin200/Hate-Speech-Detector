from flask import Flask, request, jsonify
import re
import string
import joblib
# import nltk
from googletrans import Translator

app = Flask(__name__)

class HateController:
    # stopword = set(nltk.corpus.stopwords.words('english'))  # Define stopwords set

    def __init__(self):
        # nltk.download('stopwords')  # Download NLTK stopwords
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

    # @staticmethod
    # def clean(text):
    #     text = str(text).lower()
    #     text = re.sub('\[.*?\]', '', text)
    #     text = re.sub('https?://\S+|www\.\S+', '', text)
    #     text = re.sub('<.*?>+', '', text)
    #     text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    #     text = re.sub('\n', '', text)
    #     text = re.sub('\w*\d\w*', '', text)
    #     text = [word for word in text.split(' ') if word not in HateController.stopword]
    #     text = " ".join(text)
    #     return text


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

        # Preprocess the input
        # input_string = HateController.clean(initial_state)

        print(initial_state)

        # Transform the input using the loaded CountVectorizer
        input_data = cv.transform([initial_state])

        # Make predictions
        prediction = model.predict(input_data)[0] #here lies error
        
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
