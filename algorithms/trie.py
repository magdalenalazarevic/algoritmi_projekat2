"""
Trie struktura za autocomplete korisnickih imena (zadatak 6).

Trie cuva karakter po karakter normalizovanog korisnickog imena. Na kraju
svakog imena pamti user_id, a prefix pretraga prvo nadje cvor za prefiks,
pa obilaskom podstabla skuplja sve korisnike cija imena pocinju tim prefiksom.
"""

import heapq

from text.text_processing import normalize_word


class TrieNode:
    def __init__(self):
        self.children = {}
        self.user_ids = []


class UsernameTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, username, user_id):
        node = self.root
        for char in normalize_word(username):
            node = node.children.setdefault(char, TrieNode())
        node.user_ids.append(user_id)

    def find_prefix_node(self, prefix):
        node = self.root
        for char in normalize_word(prefix):
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def collect_user_ids(self, node):
        result = []
        stack = [node]
        while stack:
            current = stack.pop()
            result.extend(current.user_ids)
            stack.extend(current.children.values())
        return result

    def search_prefix(self, prefix):
        node = self.find_prefix_node(prefix)
        if node is None:
            return []
        return self.collect_user_ids(node)


def build_username_trie(graph):
    trie = UsernameTrie()
    for user_id, user in graph.users.items():
        trie.insert(user.username, user_id)
    return trie


def autocomplete_usernames(prefix, trie, graph, ranks, k=10):
    """
    Vraca top-k korisnika ciji username pocinje zadatim prefiksom.
    Rezultati se rangiraju po PageRank vrednosti, kao sto trazi specifikacija.
    """
    prefix = normalize_word(prefix).rstrip("*")
    if not prefix:
        return []

    user_ids = trie.search_prefix(prefix)
    candidates = [
        (user_id, graph.get_user(user_id).username, ranks.get(user_id, 0.0))
        for user_id in user_ids
    ]
    return heapq.nlargest(k, candidates, key=lambda item: item[2])
