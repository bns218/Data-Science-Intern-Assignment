import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

#Open saved text file
with open('preprocess_text.txt','r') as file:
    text = file.read()

text_list = text.split("\n")

# Connection to chromadb database and load collections
persist = 'db'
client = chromadb.PersistentClient(path=persist)
collection = client.get_or_create_collection(name='corpus_collection')

#Embedding model load
model = SentenceTransformer('all-MiniLM-L6-v2')

# Collections add to vector database
collection.add(documents=[text],embeddings=[model.encode(text).tolist()],ids=[text])



print("Generating embeddings and storing in ChromaDB...")
for i, row in enumerate(text_list):
    text = row
    embedding = model.encode(text)
    collection.add(
        documents=[text],  # Original text
        metadatas=[{"id": 'wikipedia'}],  # Metadata for reference
        ids=[f"doc_{i}"],  # Unique ID for the document
        embeddings=[embedding.tolist()]  # Convert to list for compatibility
    )
print("ChromaDB collection created and populated successfully!")


print('Exmaple query results')
results = collection.query(
    query_texts=["what is nlp"],
    n_results=2)

print(results['documents'][0][0])
