"""
Did you mean predlozi za pogresno uneta korisnicka imena (zadatak 9).
"""

import heapq

from text.text_processing import normalize_word


def levenshtein_distance(first, second):
    """
    Racuna minimalan broj umetanja, brisanja i zamena karaktera potreban da se
    first pretvori u second.
    """
    first = normalize_word(first)
    second = normalize_word(second)

    if first == second:
        return 0
    if not first:
        return len(second)
    if not second:
        return len(first)

    previous = list(range(len(second) + 1))
    for i, first_char in enumerate(first, start=1):
        current = [i]
        for j, second_char in enumerate(second, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            replace_cost = previous[j - 1] + (first_char != second_char)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current

    return previous[-1]


def suggest_usernames(query, graph, ranks, k=5):
    """
    Vraca nekoliko najblizih postojecih username predloga.
    Sortiranje: manji Levenshtein distance, zatim veci PageRank.
    """
    query_norm = normalize_word(query)
    if not query_norm:
        return []

    candidates = []
    query_len = len(query_norm)
    for user_id, user in graph.users.items():
        username_norm = normalize_word(user.username)
        # Jednostavno skracenje posla za ocigledno predaleka imena.
        if abs(len(username_norm) - query_len) > max(3, query_len // 2):
            continue
        distance = levenshtein_distance(query_norm, username_norm)
        candidates.append((distance, -ranks.get(user_id, 0.0), user_id, user.username))

    best = heapq.nsmallest(k, candidates)
    return [
        (user_id, username, distance, -negative_rank)
        for distance, negative_rank, user_id, username in best
    ]
