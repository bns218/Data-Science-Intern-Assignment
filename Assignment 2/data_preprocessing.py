import re
import requests
from bs4 import BeautifulSoup

#Replace your url
url = 'https://en.wikipedia.org/wiki/Natural_language_processing'


# Function to scrape text from a Wikipedia page
def web_scrape():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = [p.get_text() for p in soup.find_all('p')]
    return text


corpus = web_scrape()


# Call the function and store the corpus
len(corpus)
def preprocess_text(text):
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    # Normalize case
    text = text.lower()
    # Remove special characters 
    text = re.sub(r'[^\w\s]', '', text)
    return text



def chunker(text, size = 200):
    return (text[i:size+i] for i in range(0, len(text), size))



chunks = []
for chunk in corpus:
    clean_text = preprocess_text(chunk)
    chunks.append(chunker(clean_text))   


chunks_list = []
for chunk in chunks:
    for text in chunk:
        chunks_list.append(text)

chunks_list
len(chunks_list)
with open('preprocess_text.txt','w', ) as file:
    for doc in chunks_list:
        file.write(doc + '\n ')
    
print('Save preprocesses text file')