# import nltk

# print("Downloading WordNet...")
# nltk.download('wordnet')
# print("Downloading Open Multilingual WordNet...")
# nltk.download('omw-1.4')
# print("Done! WordNet is ready to use.")


try:
    from nltk.corpus import wordnet
    print(" WordNet is installed!")
    print(wordnet.synsets('test'))
except LookupError:
    print(" WordNet is NOT installed")