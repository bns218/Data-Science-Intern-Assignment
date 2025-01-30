from flask import Flask, request, jsonify
import chromadb
from sentence_transformers import SentenceTransformer
import mysql.connector
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
import os

app = Flask(__name__)

# Please enter your api key
api_key = input(str("Please use your google generative ai api key: "))
os.environ["GOOGLE_API_KEY"] = api_key

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Please enter your database password
password = input(str('Please use your Database password: ',))

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': password, 
    'database': 'chatbot_db' 
}


# Connection to chromadb database and load collections
persit = 'db'
client = chromadb.PersistentClient(path=persit)
collection = client.get_collection(name='corpus_collection')

#Load the sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')



# Connection to your database
def get_connection():
    return mysql.connector.connect(**db_config)

# Create a Database and Table
def set_up_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                     timestamp DATETIME NOT NULL,
                   role TEXT NOT NULL,
                content TEXT NOT NULL
                   )
                      ''')
    conn.commit()

set_up_db()


#Retrive relevant chunks from chroma database
def retrive_relevant_chunks(query):
    query_embedding = model.encode(query)
    response = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=2
        )
    return response['documents'][0][0]


# Generate response using google gemini ai 
def generate_response(query,retrive_chunks):
    message = [
        ('system','You are an AI assistant that provides precise and accurate responses.'),
        ('human',f'Context: {retrive_chunks}\n\nQuestion: {query}')
        ]
    result = llm.invoke(message)
    return result.content


# Save chat history to database
def save_to_history(role, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (timestamp, role, content) VALUES (%s, %s, %s)", 
                   (datetime.now(), role, content))
    conn.commit()

@app.route('/')
def home():
    return 'Welcome the RAG ChatBot'

@app.route('/chat',methods=['POST'])
def chat():
    # get the JSON data from the api request
    data = request.json
    query = data.get("query", None)

    # check if input is provided
    if not data:
        return jsonify({"error": "Input data not provided"}), 400
    
    relevant_chunks = retrive_relevant_chunks(query)
    ans_generate = generate_response(query,relevant_chunks)

    save_to_history('user', query)
    save_to_history('generate_answer', ans_generate)

    return jsonify({
        "query": query,
        "retrieved_chunks": relevant_chunks,
        "answer": ans_generate })

@app.route('/history',methods=['GET'])
def get_history():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp")
    history = cursor.fetchall()
    return jsonify(history)


if __name__ == "__main__":
    app.run(debug=True)








