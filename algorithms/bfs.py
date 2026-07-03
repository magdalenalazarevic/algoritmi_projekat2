"""
BFS obilazak grafa pracenja po nivoima konekcija (zadatak 8).
"""

from collections import deque


def bfs_connections_by_level(graph, start_user_id, max_level):
    """
    Vraca dict {level: [user_id, ...]} za korisnike dostizne iz start_user_id.

    Nivo 1 su korisnici koje start_user_id direktno prati, nivo 2 su korisnici
    dostizni preko jednog posrednika, itd. Svaki korisnik se obradjuje najvise
    jednom, preko visited skupa.
    """
    if graph.get_user(start_user_id) is None or max_level <= 0:
        return {}

    levels = {}
    visited = {start_user_id}
    queue = deque([(start_user_id, 0)])

    while queue:
        current_id, current_level = queue.popleft()
        if current_level == max_level:
            continue

        next_level = current_level + 1
        for neighbor_id in graph.get_following(current_id):
            if neighbor_id in visited:
                continue
            visited.add(neighbor_id)
            levels.setdefault(next_level, []).append(neighbor_id)
            queue.append((neighbor_id, next_level))

    return levels
