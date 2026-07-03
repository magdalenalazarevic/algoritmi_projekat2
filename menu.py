"""
Tekstualni meni (zadatak 5).

Nudi tacno opcije iz specifikacije: pretragu, prikaz najuticajnijih
korisnika, dodavanje nove veze pracenja, prikaz istorije interakcija i
izlazak iz programa.
"""

from algorithms.fuzzy_match import suggest_usernames
from algorithms.bfs import bfs_connections_by_level
from algorithms.pagerank import compute_pagerank, top_k_users
from algorithms.recommendations import recommend_users
from algorithms.search import search_by_bio, search_by_username
from algorithms.trie import autocomplete_usernames


def print_menu():
    print()
    print("==================== MENI ====================")
    print("1. Pretraga korisnika (po imenu / po biografiji)")
    print("2. Prikaz najuticajnijih korisnika (PageRank)")
    print("3. Dodavanje nove veze pracenja")
    print("4. Prikaz istorije interakcija korisnika")
    print("5. Autocomplete korisnickih imena")
    print("6. BFS obilazak mreze po nivoima")
    print("7. Did you mean predlozi za username")
    print("8. Hibridne preporuke korisnika")
    print("0. Izlazak")
    print("================================================")


def ask_int(prompt):
    """
    Trazi od korisnika ceo broj dok ga ispravno ne unese.
    Unos 'q' u bilo kom trenutku otkazuje trenutnu akciju.
    """
    while True:
        raw = input(prompt).strip()
        if raw.lower() == "q":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Neispravan unos - ocekivan je ceo broj. "
                  "Probaj ponovo (ili 'q' za otkazivanje).")


def ask_float(prompt):
    while True:
        raw = input(prompt).strip()
        if raw.lower() == "q":
            return None
        try:
            return float(raw)
        except ValueError:
            print("Neispravan unos - ocekivan je decimalni broj. "
                  "Probaj ponovo (ili 'q' za otkazivanje).")


def handle_search(graph, ranks, inverted_index):
    print()
    print("a) pretraga po korisnickom imenu")
    print("b) pretraga po recima iz biografije")
    izbor = input("Izaberi (a/b): ").strip().lower()

    if izbor not in ("a", "b"):
        print("Neispravan izbor.")
        return

    upit = input("Unesi upit za pretragu: ").strip()
    if not upit:
        print("Prazan upit.")
        return

    k = ask_int("Koliko rezultata da prikazem (npr. 5)? ")
    if k is None:
        return

    if izbor == "a":
        rezultati = search_by_username(upit, graph, ranks, k=k)
    else:
        rezultati = search_by_bio(upit, inverted_index, ranks, k=k)

    if not rezultati:
        print("Nema rezultata.")
        if izbor == "a":
            suggestions = suggest_usernames(upit, graph, ranks, k=5)
            if suggestions:
                print("Did you mean:")
                for _, username, distance, pagerank in suggestions:
                    print(f"  {username:20s}  distance={distance}  "
                          f"pagerank={pagerank:.6f}")
        return

    print(f"\nRezultati pretrage ({len(rezultati)}):")
    for user_id, relevance, pagerank in rezultati:
        user = graph.get_user(user_id)
        print(f"  {user.username:20s}  relevantnost={relevance}  "
              f"pagerank={pagerank:.6f}")


def handle_top_users(graph, ranks):
    k = ask_int("Koliko najuticajnijih korisnika da prikazem (npr. 10)? ")
    if k is None:
        return

    print(f"\nTop {k} najuticajnijih korisnika:")
    for user_id, score in top_k_users(ranks, k):
        user = graph.get_user(user_id)
        print(f"  {user.username:20s}  pagerank={score:.6f}  "
              f"pratilaca={graph.in_degree(user_id)}")


def handle_add_connection(graph, history):
    """
    Dodaje novu vezu pracenja i evidentira je u istoriji interakcija.

    Vraca True ako je veza uspesno dodata (sto znaci da PageRank treba
    ponovo izracunati), inace False.
    """
    from_id = ask_int("Unesi id korisnika koji prati (from_id): ")
    if from_id is None:
        return False
    to_id = ask_int("Unesi id korisnika kog prati (to_id): ")
    if to_id is None:
        return False

    if graph.get_user(from_id) is None or graph.get_user(to_id) is None:
        print("Jedan od ta dva korisnika ne postoji u grafu.")
        return False

    if from_id == to_id:
        print("Korisnik ne moze da prati samog sebe.")
        return False

    if graph.is_blocked_between(from_id, to_id):
        print("Veza ne moze da se doda jer izmedju korisnika postoji blokada.")
        return False

    dodato = graph.add_connection(from_id, to_id)
    if not dodato:
        print("Ova veza pracenja vec postoji.")
        return False

    history.record_follow(from_id, to_id)
    print(f"Korisnik '{graph.get_user(from_id).username}' sada prati "
          f"'{graph.get_user(to_id).username}'.")
    return True


def handle_history(graph, history):
    user_id = ask_int("Unesi id korisnika cija istorija te zanima: ")
    if user_id is None:
        return
    history.print_history(user_id, graph)


def handle_autocomplete(graph, ranks, username_trie):
    prefix = input("Unesi prefiks korisnickog imena (npr. mar ili mar*): ").strip()
    if not prefix:
        print("Prazan prefiks.")
        return

    k = ask_int("Koliko predloga da prikazem (npr. 5)? ")
    if k is None:
        return

    suggestions = autocomplete_usernames(prefix, username_trie, graph, ranks, k)
    if not suggestions:
        print("Nema autocomplete predloga za dati prefiks.")
        return

    print(f"\nAutocomplete predlozi ({len(suggestions)}):")
    for user_id, username, pagerank in suggestions:
        print(f"  {username:20s}  id={user_id}  pagerank={pagerank:.6f}")


def handle_bfs(graph):
    user_id = ask_int("Unesi id pocetnog korisnika: ")
    if user_id is None:
        return
    if graph.get_user(user_id) is None:
        print("Korisnik ne postoji.")
        return

    max_level = ask_int("Do kog nivoa da radim BFS (npr. 3)? ")
    if max_level is None:
        return
    if max_level <= 0:
        print("Nivo mora biti pozitivan broj.")
        return

    levels = bfs_connections_by_level(graph, user_id, max_level)
    user = graph.get_user(user_id)
    print(f"\nBFS konekcije za '{user.username}' do nivoa {max_level}:")
    if not levels:
        print("  Nema dostiznih konekcija za zadati nivo.")
        return

    for level in range(1, max_level + 1):
        user_ids = levels.get(level, [])
        print(f"\nNivo {level} ({len(user_ids)} korisnika):")
        if not user_ids:
            print("  (nema korisnika)")
            continue
        for other_id in user_ids[:20]:
            other = graph.get_user(other_id)
            print(f"  {other.username:20s}  id={other_id}")
        if len(user_ids) > 20:
            print(f"  ... prikazano 20 od {len(user_ids)} korisnika")


def handle_did_you_mean(graph, ranks):
    query = input("Unesi korisnicko ime za proveru: ").strip()
    if not query:
        print("Prazan unos.")
        return

    exact_id = graph.get_user_id_by_username(query)
    if exact_id is not None:
        user = graph.get_user(exact_id)
        print(f"Korisnik postoji: {user.username} (id={exact_id})")
        return

    suggestions = suggest_usernames(query, graph, ranks, k=5)
    if not suggestions:
        print("Nema dovoljno slicnih korisnickih imena.")
        return

    print("\nDid you mean:")
    for user_id, username, distance, pagerank in suggestions:
        print(f"  {username:20s}  id={user_id}  distance={distance}  "
              f"pagerank={pagerank:.6f}")


def handle_recommendations(graph):
    user_id = ask_int("Unesi id korisnika za preporuke: ")
    if user_id is None:
        return
    if graph.get_user(user_id) is None:
        print("Korisnik ne postoji.")
        return

    alpha = ask_float("Unesi alpha izmedju 0 i 1 (npr. 0.5): ")
    if alpha is None:
        return
    if not 0 <= alpha <= 1:
        print("Alpha mora biti u opsegu [0, 1].")
        return

    k = ask_int("Koliko preporuka da prikazem (npr. 10)? ")
    if k is None:
        return

    print("Racunam hibridne preporuke...")
    recommendations = recommend_users(graph, user_id, alpha, k)
    if not recommendations:
        print("Nema preporuka za zadatog korisnika.")
        return

    print(f"\nTop {len(recommendations)} preporuka:")
    for rec_id, score, ppr_score, content_score in recommendations:
        user = graph.get_user(rec_id)
        print(f"  {user.username:20s}  id={rec_id}  skor={score:.6f}  "
              f"ppr={ppr_score:.6f}  bio={content_score:.6f}")


def run_menu(graph, ranks, inverted_index, username_trie, history):
    """
    Glavna petlja menija.

    `ranks` je lokalna promenljiva koja se po potrebi azurira (warm start)
    nakon sto se uspesno doda nova veza, posto se PageRank tada mora
    ponovo izracunati (zahtev iz specifikacije/FAQ).
    """
    print("Dobrodosli u simulaciju drustvene mreze!")
    print(f"Ucitano korisnika: {graph.number_of_users()}, "
          f"veza pracenja: {graph.number_of_connections()}")

    while True:
        print_menu()
        izbor = input("Izaberi opciju: ").strip()

        if izbor == "1":
            handle_search(graph, ranks, inverted_index)
        elif izbor == "2":
            handle_top_users(graph, ranks)
        elif izbor == "3":
            promenjeno = handle_add_connection(graph, history)
            if promenjeno:
                print("Ponovo racunam PageRank (warm start)...")
                ranks = compute_pagerank(graph, initial_ranks=ranks)
        elif izbor == "4":
            handle_history(graph, history)
        elif izbor == "5":
            handle_autocomplete(graph, ranks, username_trie)
        elif izbor == "6":
            handle_bfs(graph)
        elif izbor == "7":
            handle_did_you_mean(graph, ranks)
        elif izbor == "8":
            handle_recommendations(graph)
        elif izbor == "0":
            print("Hvala na koriscenju programa. Dovidjenja!")
            break
        else:
            print("Nepoznata opcija, pokusaj ponovo.")

    return ranks
