import ssl
import nltk

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download NLTK data with retries
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('punkt', raise_on_error=True)
        nltk.download('averaged_perceptron_tagger', raise_on_error=True)

# Call this at startup
download_nltk_data()