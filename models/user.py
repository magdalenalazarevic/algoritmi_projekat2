class User:
    """
    Predstavlja jednog korisnika drustvene mreze.

    Atributi:
        user_id (int): jedinstveni identifikator korisnika (id iz users.txt)
        username (str): korisnicko ime
        bio (str): tekstualni opis profila korisnika (sirov tekst, jos neobradjen -
                    obrada teksta (lowercase, tokenizacija) radi se kasnije u
                    modulu za pretragu, zadatak 3)
    """

    def __init__(self, user_id: int, username: str, bio: str):
        self.user_id = user_id
        self.username = username
        self.bio = bio

    def __repr__(self):
        return f"User(id={self.user_id}, username='{self.username}')"

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)