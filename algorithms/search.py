"""
Pretraga korisnika po korisnickom imenu i po recima iz biografije
(zadatak 3).

Rangiranje rezultata (kako specifikacija trazi): prvo po relevantnosti
upita, a u slucaju iste relevantnosti po PageRank vrednosti korisnika.
Za izdvajanje top-k rezultata koristi se heap (heapq.nlargest).
"""

import heapq

from text.text_processing import normalize_text, normalize_word


def build_inverted_index(graph):
    """
    Gradi inverted index za pretragu po biografijama: rec -> set(user_id)
    cija biografija sadrzi tu rec.

    Index se gradi JEDNOM, pri pokretanju programa (poziva se iz main.py
    posle ucitavanja grafa), a ne iznova prilikom svake pretrage - to je
    zahtev za efikasan rad nad vecim skupovima podataka (zadatak 12).
    """
    index = {}
    for user_id, user in graph.users.items():
        # set() da ista rec iz iste biografije ne bi vise puta "glasala"
        # za relevantnost kad korisnik kasnije trazi tu rec
        words = set(normalize_text(user.bio))
        for word in words:
            index.setdefault(word, set()).add(user_id)
    return index


def search_by_bio(query, inverted_index, ranks, k=10):
    """
    Pretraga korisnika po recima iz biografije.

    Upit moze sadrzati vise reci odvojenih razmakom - korisnik ulazi u
    rezultate ako njegova biografija sadrzi BAR JEDNU od trazenih reci.
    Relevantnost = broj RAZLICITIH reci iz upita koje se poklapaju sa
    biografijom (sto vise reci iz upita pronadjeno, to relevantnije).

    Rezultati se rangiraju prvo po relevantnosti, a kod izjednacenja po
    PageRank vrednosti korisnika.

    Vraca listu (user_id, relevance, pagerank) torki, najvise k komada.
    """
    query_words = set(normalize_text(query))
    if not query_words:
        return []

    matches = {}  # user_id -> broj poklopljenih reci iz upita
    for word in query_words:
        for user_id in inverted_index.get(word, ()):
            matches[user_id] = matches.get(user_id, 0) + 1

    candidates = [
        (user_id, relevance, ranks.get(user_id, 0.0))
        for user_id, relevance in matches.items()
    ]

    return heapq.nlargest(k, candidates, key=lambda item: (item[1], item[2]))


def search_by_username(query, graph, ranks, k=10):
    """
    Pretraga korisnika po (delu) korisnickog imena, case-insensitive.

    Relevantnost se racuna u 3 nivoa, da bi tacniji pogoci bili rangirani
    iznad priblicnih:
        3 - korisnicko ime se TACNO poklapa sa upitom
        2 - korisnicko ime POCINJE upitom (prefiks)
        1 - upit se javlja BILO GDE unutar korisnickog imena (sadrzi)

    Kod jednake relevantnosti, prednost ima korisnik sa vecom PageRank
    vrednoscu.

    Vraca listu (user_id, relevance, pagerank) torki, najvise k komada.

    Napomena: ovo je jednostavna (linearna) pretraga po svim korisnicima.
    Za brzu pretragu SAMO po prefiksu (autocomplete) postoji efikasnija
    trie struktura u zadatku 6 - ova funkcija je opstija jer pronalazi
    poklapanja bilo gde u imenu, ne samo na pocetku.
    """
    query_norm = normalize_word(query)
    if not query_norm:
        return []

    candidates = []
    for user_id, user in graph.users.items():
        username_lower = user.username.lower()

        if username_lower == query_norm:
            relevance = 3
        elif username_lower.startswith(query_norm):
            relevance = 2
        elif query_norm in username_lower:
            relevance = 1
        else:
            continue

        candidates.append((user_id, relevance, ranks.get(user_id, 0.0)))

    return heapq.nlargest(k, candidates, key=lambda item: (item[1], item[2]))