"""
PageRank algoritam (zadatak 2) - racuna uticaj svakog korisnika u grafu
pracenja.

Damping factor (d) = verovatnoca da "slucajni setac" nastavi da prati
linkove (podrazumevano 0.85). Sa verovatnocom (1-d) "setac" se nasumicno
teleportuje na bilo kog korisnika u mrezi.

Napomena o implementaciji:
    Iako bi se algoritam mogao napisati direktno nad dict/set strukturama
    iz SocialGraph-a (sto je jednostavnije za citanje), to je sporo na
    full skupu podataka (~81000 korisnika, ~1.7 miliona veza) jer se u
    svakoj iteraciji ponavljaju hiljade poziva metoda i dict pretraga.
    Zato se na pocetku funkcije graf jednom "spljosti" u obicne Python
    liste indeksirane celim brojevima 0..n-1 (out_degree_arr, followers_arr),
    a sama iterativna petlja radi samo nad tim listama. Ovo je svedeno
    testiranjem sa ~81s na ~14s za full skup, uz identicne rezultate.
"""

import heapq


def compute_pagerank(graph, damping=0.85, epsilon=1e-6, max_iterations=100,
                      initial_ranks=None):
    """
    Racuna PageRank vrednost za svakog korisnika u grafu.

    Parametri:
        graph          : SocialGraph
        damping        : damping factor (podrazumevano 0.85)
        epsilon        : prag konvergencije - algoritam staje kada je
                         L1 razlika (suma apsolutnih razlika) izmedju dve
                         uzastopne iteracije manja od epsilon
        max_iterations : sigurnosna granica broja iteracija, da algoritam
                         ne bi rotirao u beskonacnost ako iz nekog razloga
                         ne konvergira
        initial_ranks  : opciono - dict {user_id: rank} sa prethodno
                         izracunatim vrednostima, koristi se kao polazna
                         tacka (warm start) umesto uniformne raspodele.
                         Koristi se kada se PageRank ponovo racuna nakon
                         dodavanja novog korisnika ili nove veze - tada je
                         potrebno znatno manje iteracija do konvergencije.

    Vraca:
        dict {user_id: pagerank_vrednost}, gde je suma svih vrednosti ~1.0

    Napomena o "dangling" cvorovima:
        Korisnik koji ne prati nikoga (out_degree = 0) bi inace "izgubio"
        svoj rank, jer nema kome da ga prosledi. Standardno resenje je da
        se taj rank ravnomerno rasporedi na SVE korisnike u mrezi - to
        racuna promenljiva `dangling_sum` u svakoj iteraciji.
    """
    user_ids = graph.all_user_ids()
    n = len(user_ids)
    if n == 0:
        return {}

    # --- "spljostimo" graf u liste indeksirane sa 0..n-1, radi brzine ---
    index_of = {uid: i for i, uid in enumerate(user_ids)}
    out_degree_arr = [graph.out_degree(uid) for uid in user_ids]
    followers_arr = [
        [index_of[follower_id] for follower_id in graph.get_followers(uid)]
        for uid in user_ids
    ]
    dangling_indices = [i for i in range(n) if out_degree_arr[i] == 0]

    if initial_ranks is not None:
        ranks = [initial_ranks.get(uid, 1.0 / n) for uid in user_ids]
    else:
        ranks = [1.0 / n] * n

    diff = float("inf")

    for iteration in range(1, max_iterations + 1):
        dangling_sum = sum(ranks[i] for i in dangling_indices) #rank korisnika koji nikoga ne prati se ravnomerno rasporedi svima
        base = (1 - damping) / n + damping * dangling_sum / n

        new_ranks = [0.0] * n
        for i in range(n):
            incoming = 0.0
            for follower_index in followers_arr[i]:
                incoming += ranks[follower_index] / out_degree_arr[follower_index]
            new_ranks[i] = base + damping * incoming

        diff = sum(abs(new_ranks[i] - ranks[i]) for i in range(n)) #kolika je promena u odnosu na prethodnu interaciju
        ranks = new_ranks

        if diff < epsilon: #promena jako mala stajemo
            print(f"PageRank konvergirao posle {iteration} iteracija "
                  f"(razlika={diff:.2e})")
            break
    else:
        print(f"PageRank dostigao max_iterations={max_iterations} bez pune "
              f"konvergencije (poslednja razlika={diff:.2e})")

    # vracamo nazad u oblik {user_id: rank} kako bi ostatak programa mogao
    # da radi sa stvarnim id-jevima korisnika, ne sa internim indeksima
    return {uid: ranks[index_of[uid]] for uid in user_ids}


def top_k_users(ranks, k=10):
    """
    Vraca k korisnika sa najvecim PageRank vrednostima, koriscenjem heap-a
    (heapq.nlargest interno koristi heap, sto je trazeno specifikacijom).

    Vraca listu (user_id, rank) torki, sortiranu opadajuce po rank-u.
    """
    return heapq.nlargest(k, ranks.items(), key=lambda pair: pair[1])
