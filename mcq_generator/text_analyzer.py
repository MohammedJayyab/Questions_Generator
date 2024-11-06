from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def extract_key_phrases(subtopic_text):
    try:
        sentences = sent_tokenize(subtopic_text)
        stop_words = set(stopwords.words("english"))
        key_phrases = []

        for sentence in sentences:
            words = word_tokenize(sentence)
            filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]
            if filtered_words:
                key_phrases.append(filtered_words[0])
        return key_phrases
    except Exception as e:
        print(f"Error extracting key phrases: {e}")
        return []
