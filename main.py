"""
Glavni ulaz u program - ucitava podatke, racuna pocetni PageRank, gradi
inverted index za pretragu po biografiji i pokrece tekstualni meni
(zadatak 5).
"""

from data_io.loader import load_dataset
from algorithms.pagerank import compute_pagerank
from algorithms.search import build_inverted_index
from algorithms.trie import build_username_trie
from history import InteractionHistory
from menu import run_menu

DATASET_VELICINA = "medium"  # "small", "medium" ili "full"

USERS_PATH = f"dataset/{DATASET_VELICINA}/users.txt"
CONNECTIONS_PATH = f"dataset/{DATASET_VELICINA}/connections.txt"
BLOCKED_PATH = f"dataset/{DATASET_VELICINA}/blocked.txt"


def main():
    graph = load_dataset(USERS_PATH, CONNECTIONS_PATH, BLOCKED_PATH)

    print("Racunam pocetni PageRank...")
    ranks = compute_pagerank(graph)

    print("Gradim inverted index za pretragu po biografiji...")
    inverted_index = build_inverted_index(graph)

    print("Gradim trie za autocomplete korisnickih imena...")
    username_trie = build_username_trie(graph)

    history = InteractionHistory()

    run_menu(graph, ranks, inverted_index, username_trie, history)


if __name__ == "__main__":
    main()
