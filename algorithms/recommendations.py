"""
Hibridne preporuke korisnika (zadatak 7).

Skor kombinuje Personalized PageRank iz perspektive zadatog korisnika i
slicnost biografija:

    alpha * PPR + (1 - alpha) * content_similarity
"""

import heapq

from algorithms.similarity import bio_word_set, jaccard_similarity


def compute_personalized_pagerank(graph, start_user_id, damping=0.85,
                                  epsilon=1e-6, max_iterations=50):
    """
    Personalized PageRank: teleportacija se vraca na start_user_id, pa korisnici
    blizi i vazniji iz njegove perspektive dobijaju veci skor.
    """
    user_ids = graph.all_user_ids()
    n = len(user_ids)
    if n == 0 or start_user_id not in graph.users:
        return {}

    index_of = {uid: i for i, uid in enumerate(user_ids)}
    start_index = index_of[start_user_id]
    outgoing = [
        [index_of[to_id] for to_id in graph.get_following(uid)]
        for uid in user_ids
    ]

    ranks = [0.0] * n
    ranks[start_index] = 1.0

    for _ in range(max_iterations):
        new_ranks = [0.0] * n
        new_ranks[start_index] = 1.0 - damping
        dangling_sum = 0.0

        for i, neighbors in enumerate(outgoing):
            if not neighbors:
                dangling_sum += ranks[i]
                continue
            share = damping * ranks[i] / len(neighbors)
            for neighbor_index in neighbors:
                new_ranks[neighbor_index] += share

        new_ranks[start_index] += damping * dangling_sum

        diff = sum(abs(new_ranks[i] - ranks[i]) for i in range(n))
        ranks = new_ranks
        if diff < epsilon:
            break

    return {uid: ranks[index_of[uid]] for uid in user_ids}


def recommend_users(graph, start_user_id, alpha=0.5, k=10):
    """
    Vraca top-k preporuka kao:
    (user_id, combined_score, ppr_score, content_similarity).
    """
    start_user = graph.get_user(start_user_id)
    if start_user is None:
        return []

    alpha = max(0.0, min(1.0, alpha))
    ppr = compute_personalized_pagerank(graph, start_user_id)
    already_following = graph.get_following(start_user_id)
    start_words = bio_word_set(start_user)

    candidates = []
    for user_id, user in graph.users.items():
        if user_id == start_user_id:
            continue
        if user_id in already_following:
            continue
        if graph.is_blocked_between(start_user_id, user_id):
            continue

        content_score = jaccard_similarity(start_words, bio_word_set(user))
        ppr_score = ppr.get(user_id, 0.0)
        combined = alpha * ppr_score + (1.0 - alpha) * content_score
        if combined <= 0:
            continue
        candidates.append((user_id, combined, ppr_score, content_score))

    return heapq.nlargest(k, candidates, key=lambda item: item[1])
