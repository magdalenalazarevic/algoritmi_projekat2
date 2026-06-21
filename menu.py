"""
Tekstualni meni (zadatak 5).

Nudi tacno opcije iz specifikacije: pretragu, prikaz najuticajnijih
korisnika, dodavanje nove veze pracenja, prikaz istorije interakcija i
izlazak iz programa.
"""

from algorithms.pagerank import compute_pagerank, top_k_users
from algorithms.search import search_by_bio, search_by_username


def print_menu():
    print()
    print("==================== MENI ====================")
    print("1. Pretraga korisnika (po imenu / po biografiji)")
    print("2. Prikaz najuticajnijih korisnika (PageRank)")
    print("3. Dodavanje nove veze pracenja")
    print("4. Prikaz istorije interakcija korisnika")
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


def run_menu(graph, ranks, inverted_index, history):
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
        elif izbor == "0":
            print("Hvala na koriscenju programa. Dovidjenja!")
            break
        else:
            print("Nepoznata opcija, pokusaj ponovo.")

    return ranks