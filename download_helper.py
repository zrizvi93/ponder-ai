import os
import requests

def get_book():
    download_file = "./data/don_quixote.txt"
    # URL of the book
    url = 'https://www.gutenberg.org/cache/epub/996/pg996.txt'
    if not os.path.exists(download_file):
        # Send a GET request
        response = requests.get(url)

        # Save the text content to a file
        with open('./data/don_quixote.txt', 'w', encoding='utf-8') as file:
            file.write(response.text)
    return 
