## Repository Structure
```
/Data-Science-Intern-Assignments
│── Assignment1
│   ├── data_ingestion.py
│   ├── model_training.py
│   ├── app.py
│   ├── requirements.txt
│   ├── database_schema.sql
│   ├── README.md
│
│── Assignment2
│   ├── data_preprocessing.py
│   ├── embed_store.py
│   ├── rag_chatbot.py
│   ├── requirements.txt
│   ├── database_schema.sql
│   ├── README.md
│   ├── Dockerfile (Optional)
│
│── README.md

```

# Assignment 1: End-to-End Sentiment Analysis Pipeline

## Project Overview
This project involves building a machine learning model and deploying it using a Flask API. The repository includes scripts for data ingestion, model training, and serving predictions via an API.


## Setup Instructions
### 1. Clone the Repository
```bash
git clone <repository_url>
cd Assignment1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up the Database (if applicable)
- If using MySQL/PostgreSQL, create the necessary tables using this file ('data_setup.ipynb').

### 4. Run the Model Training Script
```bash
jupyter notebook train_model.ipynb
```
Ensure the trained model is saved as `model.pkl`.

### 5. Start the Flask API Server
```bash
python app.py
```
This will start the server at `http://127.0.0.1:5000/`.

### 6. Test the API
Use `test_api.ipynb` to test API endpoints 
or
use `curl`:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "Sample input text"}' http://127.0.0.1:5000/predict
```

## Model Information
- **Approach**: The model uses TF-IDF for text vectorization and a machine learning algorithm for classification.
- **Performance**: (Include accuracy or other evaluation metrics after training).

## Notes
- If using a database, ensure to document schema creation.

---
**Author:** Bhonagiri Nagasai


# Assignment 2: RAG (Retrieval-Augmented Generation) Chatbot

## Project Setup

### Install and Run Locally
```sh
git clone <repo_url>
cd <repo_directory>
pip install -r requirements.txt
```

### Set Up MySQL Database
1. Install MySQL and create a database:
```sh
python setup_db.py
```
2. Ensure the required tables are created in `chatbot_db`.

## Running Instructions

### Start the API Server
```sh
python rag_chatbot.py
```

### Test Endpoints
#### Test `/chat`
```sh
python test_api.ipynb
```

#### Test `/history`
```sh
python test_api.ipynp

