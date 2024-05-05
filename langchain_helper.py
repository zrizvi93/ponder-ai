import os 
import pickle
from langchain_core.document_loaders import BaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

from download_helper import get_book


def load_or_parse_data():
    raw_file = "./data/don_quixote.txt"
    pickle_file = "./data/don_quixote.pkl"

    if os.path.exists(pickle_file):
        print("I found a pickle file!")
        with open(pickle_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        if not os.path.exists(raw_file):
            print("I did not find a text file!")
            get_book()

        print("I found a pickle file!")
        loader = TextLoader(raw_file)
        docs = loader.load()
        # Split
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        parsed_data = text_splitter.split_documents(docs)

        # Serialize the document splits to a pickle file
        with open(pickle_file, 'wb') as f:
            pickle.dump(parsed_data, f)

    return parsed_data


class CustomDocumentLoader(BaseLoader):
    def __init__(self, file_path, book_title, author):
        self.file_path = file_path
        self.book_title = book_title
        self.author = author

    def load_documents(self):
        documents = []
        chapter_number = 0
        line_number = 0
        chapter_text = []
        recording = False  # To start recording after the table of contents

        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                line_number += 1

                # Detect the start of the first chapter or subsequent chapters
                if "CHAPTER" in line:
                    if chapter_text:  # Save the previous chapter if any
                        document = {
                            "text": "\n".join(chapter_text),
                            "metadata": {
                                "chapter_number": chapter_number,
                                "book_title": self.book_title,
                                "author": self.author
                            }
                        }
                        documents.append(document)
                        chapter_text = []  # Reset for the next chapter
                    chapter_number += 1
                    recording = True  # Start recording chapter text

                if recording:
                    chapter_text.append(line)

        # Append the last chapter if there's any remaining text
        if chapter_text:
            document = {
                "text": "\n".join(chapter_text),
                "metadata": {
                    "chapter_number": chapter_number,
                    "book_title": self.book_title,
                    "author": self.author
                }
            }
            documents.append(document)

        return documents


