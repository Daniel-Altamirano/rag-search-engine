import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords

def search_command(query: str, limit: int=DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    for movie in movies:
        query_tokens = tokenize_text(query)
        title_tokens = tokenize_text(movie["title"])
        if has_matching_token(query_tokens, title_tokens):
            results.append(movie)
            if len(results) >= limit:
                break
    return results


def has_matching_token(query_tokens: list[str], title_tokens: list[str]) -> bool:
    return any(query_token in title_token
               for query_token in query_tokens
               for title_token in title_tokens)


def preprocess_text(text: str) -> str:
    remove_punctuation = str.maketrans("", "", string.punctuation)
    text = text.translate(remove_punctuation).lower()
    return text


def tokenize_text(text: str) -> list[str]:
    text = preprocess_text(text)
    tokens = text.split()
    stopwords = load_stopwords()
    filtered_words = []
    for token in tokens:
        if token not in stopwords:
            filtered_words.append(token)
    return filtered_words
