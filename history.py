"""
Istorija interakcija (zadatak 4).

Evidentira dodavanje NOVIH veza pracenja - dakle dogadjaje koji se dese
TOKOM RADA programa (preko menija), a ne pocetno ucitavanje
connections.txt. Pocetno stanje grafa je samo polazna tacka, ne "dogadjaj"
koji treba evidentirati - ovo je u skladu sa formulacijom iz specifikacije
("evidentirati DODAVANJE NOVIH veza pracenja") i FAQ napomenom da se
izmene (poput nove veze) odrzavaju tokom jednog pokretanja programa.

Za zadatog korisnika omogucava prikaz:
    - koga je on zapratio (hronoloskim redom)
    - ko je njega zapratio (hronoloskim redom)
"""

from datetime import datetime


class InteractionHistory:
    """
    Cuva istoriju "follow" dogadjaja nastalih tokom jednog pokretanja
    programa.

    Struktura podataka:
        following_history : dict  user_id -> list(other_user_id, datetime)
                             (koga je user_id zapratio, hronoloskim redom)
        follower_history   : dict  user_id -> list(other_user_id, datetime)
                             (ko je zapratio user_id, hronoloskim redom)

    Liste su uvek hronoloske bez potrebe za naknadnim sortiranjem, jer se
    u njih iskljucivo dodaje (append) u trenutku kada se dogadjaj zaista
    desi - redosled dodavanja JESTE hronoloski redosled.
    """

    def __init__(self):
        self.following_history = {}
        self.follower_history = {}

    def record_follow(self, from_id, to_id):
        """
        Belezi da je from_id upravo zapratio to_id.

        Poziva se NAKON sto je veza vec uspesno dodata u SocialGraph
        (graph.add_connection) - ova klasa ne dodaje vezu u graf, samo
        pamti da se dogadjaj desio.
        """
        timestamp = datetime.now()
        self.following_history.setdefault(from_id, []).append((to_id, timestamp))
        self.follower_history.setdefault(to_id, []).append((from_id, timestamp))

    def get_following_history(self, user_id):
        """Hronoloska lista (other_user_id, datetime) - koga je korisnik zapratio."""
        return self.following_history.get(user_id, [])

    def get_followers_history(self, user_id):
        """Hronoloska lista (other_user_id, datetime) - ko je zapratio korisnika."""
        return self.follower_history.get(user_id, [])

    def print_history(self, user_id, graph):
        """
        Stampa citljiv pregled istorije interakcija za datog korisnika -
        koga je zapratio i ko je njega zapratio, hronoloskim redom.
        """
        user = graph.get_user(user_id)
        if user is None:
            print(f"Korisnik sa id={user_id} ne postoji.")
            return

        print(f"\nIstorija interakcija za korisnika '{user.username}' (id={user_id}):")

        following = self.get_following_history(user_id)
        print(f"\nKorisnici koje je '{user.username}' zapratio ({len(following)}):")
        if not following:
            print("  (nema novih veza dodatih tokom ove sesije)")
        else:
            for other_id, ts in following:
                other = graph.get_user(other_id)
                ime = other.username if other else f"id={other_id}"
                print(f"  {ts.strftime('%Y-%m-%d %H:%M:%S')}  ->  zapratio: {ime}")

        followers = self.get_followers_history(user_id)
        print(f"\nKorisnici koji su zapratili '{user.username}' ({len(followers)}):")
        if not followers:
            print("  (niko ga nije zapratio tokom ove sesije)")
        else:
            for other_id, ts in followers:
                other = graph.get_user(other_id)
                ime = other.username if other else f"id={other_id}"
                print(f"  {ts.strftime('%Y-%m-%d %H:%M:%S')}  ->  zapratio ga: {ime}")