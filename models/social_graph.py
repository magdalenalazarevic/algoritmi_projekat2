class SocialGraph:
    """
    Usmereni graf drustvene mreze (zadatak 1).

    Struktura podataka:
        users           : dict  user_id -> User
                          (hash mapa za brz pristup korisniku po id-u)
        username_to_id  : dict  username.lower() -> user_id
                          (hash mapa za brzu case-insensitive pretragu po
                          korisnickom imenu, koristi se kasnije u zadatku 3 i 9)
        following       : dict  user_id -> set(user_id)
                          (IZLAZNE veze - koga dati korisnik prati)
        followers       : dict  user_id -> set(user_id)
                          (ULAZNE veze - ko prati datog korisnika)
        blocked_by_user : dict  blocker_id -> set(blocked_id)
                          (koga je dati korisnik blokirao)
        blocked_user_by : dict  blocked_id -> set(blocker_id)
                          (ko je blokirao datog korisnika - obrnuta mapa,
                          drzimo je radi brze provere u oba smera)

    Setovi su koriscени umesto lista za veze jer je potrebna brza provera
    "da li vec postoji veza / blokada" (O(1) prosecno), kao i izbegavanje
    duplikata.

    Logika koriscenja blocked_by_user/blocked_user_by (zabrana preporuke,
    zabrana dodavanja veze) implementira se u zadatku 10 - ovde se samo
    gradi struktura nad podacima iz blocked.txt.
    """

    def __init__(self):
        self.users = {}
        self.username_to_id = {}
        self.following = {}
        self.followers = {}
        self.blocked_by_user = {}
        self.blocked_user_by = {}

    # ---------- Dodavanje korisnika ----------

    def add_user(self, user):
        """
        Dodaje korisnika u graf. Odmah pravi prazne setove za njegove veze,
        da bi get_following/get_followers uvek vracali validan set umesto
        da baca KeyError za korisnika koji jos nema nijednu vezu.
        """
        self.users[user.user_id] = user
        self.username_to_id[user.username.lower()] = user.user_id
        self.following.setdefault(user.user_id, set())
        self.followers.setdefault(user.user_id, set())

    # ---------- Dodavanje veza praćenja ----------

    def add_connection(self, from_id, to_id):
        """
        Dodaje usmerenu vezu praćenja from_id -> to_id (from_id prati to_id).

        Vraca True ako je veza uspesno dodata, False ako vec postoji ili
        ako jedan od korisnika ne postoji u grafu.

        Napomena: ova metoda namerno NE proverava blokiranje niti
        rekalkulise PageRank - to je odgovornost viseg nivoa (menija /
        zadatka 10), jer se ova metoda koristi i za masovno ucitavanje
        connections.txt pri pokretanju programa, gde te provere nisu
        potrebne.
        """
        if from_id not in self.users or to_id not in self.users:
            return False
        if to_id in self.following[from_id]:
            return False  # veza vec postoji
        self.following[from_id].add(to_id)
        self.followers[to_id].add(from_id)
        return True

    # ---------- Dodavanje blokiranja ----------

    def add_blocked(self, blocker_id, blocked_id):
        """
        Belezi da je blocker_id blokirao blocked_id.
        Vraca True ako je uspesno dodato, False ako jedan od korisnika
        ne postoji u grafu.
        """
        if blocker_id not in self.users or blocked_id not in self.users:
            return False
        self.blocked_by_user.setdefault(blocker_id, set()).add(blocked_id)
        self.blocked_user_by.setdefault(blocked_id, set()).add(blocker_id)
        return True

    # ---------- Upiti nad grafom ----------

    def get_user(self, user_id):
        """Vraca User objekat za dati id, ili None ako korisnik ne postoji."""
        return self.users.get(user_id)

    def get_user_id_by_username(self, username):
        """Case-insensitive pronalazenje id-a korisnika po korisnickom imenu."""
        return self.username_to_id.get(username.lower())

    def get_following(self, user_id):
        """Vraca set id-jeva korisnika koje dati korisnik prati."""
        return self.following.get(user_id, set())

    def get_followers(self, user_id):
        """Vraca set id-jeva korisnika koji prate datog korisnika."""
        return self.followers.get(user_id, set())

    def out_degree(self, user_id):
        """Broj korisnika koje dati korisnik prati (izlazni stepen)."""
        return len(self.following.get(user_id, set()))

    def in_degree(self, user_id):
        """Broj korisnika koji prate datog korisnika (ulazni stepen)."""
        return len(self.followers.get(user_id, set()))

    def all_user_ids(self):
        """Vraca sve id-jeve korisnika u grafu (npr. za inicijalizaciju PageRank-a)."""
        return list(self.users.keys())

    def number_of_users(self):
        return len(self.users)

    def number_of_connections(self):
        return sum(len(s) for s in self.following.values())

    def __repr__(self):
        return (f"SocialGraph(users={self.number_of_users()}, "
                f"connections={self.number_of_connections()})")