"""
Slicnost tekstualnih biografija za hibridne preporuke (zadatak 7).
"""

from text.text_processing import normalize_text


def bio_word_set(user):
    return set(normalize_text(user.bio))


def jaccard_similarity(first_words, second_words):
    """
    Jaccard(A, B) = |A presek B| / |A unija B|.
    """
    if not first_words and not second_words:
        return 0.0
    union = first_words | second_words
    if not union:
        return 0.0
    return len(first_words & second_words) / len(union)
