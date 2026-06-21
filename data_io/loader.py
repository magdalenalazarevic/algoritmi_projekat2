"""
Ucitavanje podataka iz fajlova users.txt, connections.txt i blocked.txt
i punjenje SocialGraph strukture.

Format fajlova (videti specifikaciju projekta i FAQ):
    users.txt:        id|username|bio
    connections.txt:  from_id|to_id    (from_id prati to_id)
    blocked.txt:      blocker_id|blocked_id

Fajlovi imaju CRLF zavrsetke linija, ali Python u text modu ('r') to
automatski svodi na '\\n', pa o tome ne mora posebno da se vodi racuna.
"""

from models.user import User
from models.social_graph import SocialGraph


def load_users(graph, path):
    """
    Cita users.txt i dodaje sve korisnike u graf.

    Bio polje moze sadrzati zareze i tacke (npr. "Researcher sharing notes
    about science, education, and digital culture."), zato se linija deli
    na NAJVISE 3 dela (maxsplit=2) - tako i ako bi bio sadrzao karakter '|'
    (sto se u datasetu ne desava, ali je sigurnije ne pretpostavljati to),
    ostatak linije i dalje ide ispravno u bio.

    Linije koje su prazne ili neispravno formatirane se preskacu uz
    upozorenje, da ucitavanje ne bi puklo zbog poneke neispravne linije.
    """
    with open(path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split("|", maxsplit=2)
            if len(parts) != 3:
                print(f"[upozorenje] users.txt linija {line_number}: "
                      f"neispravan format, preskačem -> {line}")
                continue

            raw_id, username, bio = parts
            try:
                user_id = int(raw_id)
            except ValueError:
                print(f"[upozorenje] users.txt linija {line_number}: "
                      f"id nije broj, preskačem -> {line}")
                continue

            graph.add_user(User(user_id, username, bio))


def load_connections(graph, path):
    """
    Cita connections.txt i dodaje sve usmerene veze praćenja u graf.
    Vraca broj uspesno dodatih veza.
    """
    added = 0
    with open(path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split("|")
            if len(parts) != 2:
                print(f"[upozorenje] connections.txt linija {line_number}: "
                      f"neispravan format, preskačem -> {line}")
                continue

            try:
                from_id, to_id = int(parts[0]), int(parts[1])
            except ValueError:
                print(f"[upozorenje] connections.txt linija {line_number}: "
                      f"id nije broj, preskačem -> {line}")
                continue

            if graph.add_connection(from_id, to_id):
                added += 1
    return added


def load_blocked(graph, path):
    """
    Cita blocked.txt i belezi sve blokade u graf.
    Vraca broj uspesno dodatih blokada.
    """
    added = 0
    with open(path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split("|")
            if len(parts) != 2:
                print(f"[upozorenje] blocked.txt linija {line_number}: "
                      f"neispravan format, preskačem -> {line}")
                continue

            try:
                blocker_id, blocked_id = int(parts[0]), int(parts[1])
            except ValueError:
                print(f"[upozorenje] blocked.txt linija {line_number}: "
                      f"id nije broj, preskačem -> {line}")
                continue

            if graph.add_blocked(blocker_id, blocked_id):
                added += 1
    return added


def load_dataset(users_path, connections_path, blocked_path):
    """
    Glavna funkcija ucitavanja - cita sva tri fajla i vraca popunjen
    SocialGraph. Ovo je funkcija koju main.py poziva pri pokretanju
    programa.
    """
    graph = SocialGraph()

    load_users(graph, users_path)
    connections_added = load_connections(graph, connections_path)
    blocked_added = load_blocked(graph, blocked_path)

    print(f"Ucitano korisnika: {graph.number_of_users()}")
    print(f"Ucitano veza praćenja: {connections_added}")
    print(f"Ucitano blokada: {blocked_added}")

    return graph