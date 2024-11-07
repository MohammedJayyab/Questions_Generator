import os
import nltk

# Define the NLTK data directory within your virtual environment
nltk_data_path = os.path.join(os.path.dirname(__file__), "..", "venv", "nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)
os.environ["NLTK_DATA"] = nltk_data_path

# Download necessary resources to the specified directory
def download_nltk_resources():
    resources = ['punkt', 'stopwords' ]
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            print(f"Downloading NLTK resource: {resource}")
            nltk.download(resource, download_dir=nltk_data_path)

if __name__ == "__main__":
    download_nltk_resources()
