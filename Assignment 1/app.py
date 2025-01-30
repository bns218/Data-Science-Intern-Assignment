from flask import Flask, request, jsonify
import pickle
import re
import nltk
from nltk.corpus import stopwords 
import pandas as pd


app = Flask(__name__)


with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('tfid.pkl', 'rb') as file:
    tfidf = pickle.load(file)



def remove_stopwords(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.split()
    text = [word for word in text if word not in stopwords.words('english')]
    text = ' '.join(text)
    return text

@app.route("/")
def home():
    return "Predicting Sentiment of a Moive Review"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # get the JSON data from the api request
        data = request.get_json()

        input_data = pd.DataFrame([data])

        # check if input is provided
        if not data:
            return jsonify({"error": "Input data not provided"}), 400

        # validate input columns
        required_columns = ['review_text']
        if not all(col in input_data.columns for col in required_columns):
            return jsonify({"error": f"Required columns missing. Required columns: {required_columns}"}), 400

        # remove stopwords
        input_data['review_text'] = input_data['review_text'].apply(remove_stopwords)

        # TF-IDF
        tfidf_data = tfidf.transform(input_data['review_text'])

        # make prediction
        Prediction = model.predict(tfidf_data)

        # response
        response = {
            "Prediction": "Postive " if Prediction[0] == 1 else "Negative"
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__=="__main__":
    app.run(debug=True)
