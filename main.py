"""
Glavni ulaz u program. Za sada samo ucitava podatke i ispisuje osnovne
statistike grafa, da bismo proverili da li ucitavanje radi ispravno pre
nego sto se doda tekstualni meni (zadatak 5).
"""

from data_io.loader import load_dataset

DATASET_VELICINA = "small"  # "small", "medium" ili "full"

USERS_PATH = f"dataset/{DATASET_VELICINA}/users.txt"
CONNECTIONS_PATH = f"dataset/{DATASET_VELICINA}/connections.txt"
BLOCKED_PATH = f"dataset/{DATASET_VELICINA}/blocked.txt"


def main():
    graph = load_dataset(USERS_PATH, CONNECTIONS_PATH, BLOCKED_PATH)
    print(graph)

    # brza rucna provera - ispis prvog korisnika i njegovih veza
    prvi_id = graph.all_user_ids()[0]
    prvi_user = graph.get_user(prvi_id)
    print()
    print(f"Primer - korisnik: {prvi_user}")
    print(f"  prati: {graph.out_degree(prvi_id)} korisnika")
    print(f"  prati ga: {graph.in_degree(prvi_id)} korisnika")


if __name__ == "__main__":
    main()