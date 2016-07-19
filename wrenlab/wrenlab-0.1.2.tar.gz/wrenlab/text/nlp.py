import os
import os.path

import nltk
import nltk.data

NLTK_DATA_DOWNLOADED = False

def ensure_nltk_data():
    global NLTK_DATA_DOWNLOADED
    if NLTK_DATA_DOWNLOADED is True:
        return

    path = os.path.expanduser("~/.local/share/nltk/data")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        nltk.download("all", download_dir=path)

    nltk.data.path.append(path)
    NLTK_DATA_DOWNLOADED = True

def punkt_sentence_tokenizer():
    ensure_nltk_data()
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    return tokenizer.tokenize
