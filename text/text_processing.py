"""
Osnovna obrada teksta nad biografijama korisnika (deo zadatka 3).
Koristi se i za inverted index i za pretragu, kako bi se tekst obradjivao
na isti nacin na oba mesta.
"""

import re

# \w u Python regex-u (nad str objektima) po default-u hvata unicode slova,
# cifre i donju crtu - ovo je bitno jer biografije u datasetu sadrze i
# cirilicu, akcentovanu latinicu i poneki drugi alfabet, ne samo engleska
# slova. Crtice, zapete i tacke se NE smatraju delom reci, vec razdvajacima.
_WORD_PATTERN = re.compile(r"\w+", re.UNICODE)


def normalize_text(text):
    """
    Normalizuje tekst (npr. biografiju ili upit za pretragu):
      - prebacuje sve u mala slova (pretraga mora biti case-insensitive)
      - izdvaja reci - nizove slovno-brojnih karaktera i donje crte

    Vraca listu reci (tokena), npr.:
        normalize_text("Machine learning researcher, Python developer.")
        -> ['machine', 'learning', 'researcher', 'python', 'developer']
    """
    if not text:
        return []
    return _WORD_PATTERN.findall(text.lower())


def normalize_word(word):
    """Normalizuje jednu rec/upit (mala slova, bez viska razmaka)."""
    return word.lower().strip()