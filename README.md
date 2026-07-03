# ASP Projekat 2 - simulacija drustvene mreze

Konzolna Python aplikacija koja ucitava usmereni graf drustvene mreze i
omogucava PageRank rangiranje, pretragu profila, autocomplete, dodavanje veza,
istoriju interakcija, BFS obilazak, did-you-mean predloge i hibridne preporuke.

## Pokretanje

Program se pokrece iz korenskog direktorijuma projekta:

```powershell
python main.py
```

Podrazumevano je ukljucen `full` skup podataka:

```python
DATASET_VELICINA = "full"
```

Vrednost se u `main.py` moze promeniti na `"small"` ili `"medium"` za brze
testiranje.

## Ulazni fajlovi

Za svaki skup podataka postoje:

- `users.txt` u formatu `id|username|bio`
- `connections.txt` u formatu `from_id|to_id`
- `blocked.txt` u formatu `blocker_id|blocked_id`

Fajlovi se nalaze u `dataset/small`, `dataset/medium` i `dataset/full`.

## Implementirane funkcionalnosti

1. Graf drustvene mreze
   - klase `User` i `SocialGraph`
   - hash mape za korisnike po ID-u i username-u
   - izlazne veze `following`
   - ulazne veze `followers`
   - blokade u oba smera

2. PageRank
   - iterativni PageRank algoritam
   - damping factor `0.85`
   - epsilon `1e-6`
   - obrada dangling cvorova
   - warm start nakon dodavanja nove veze
   - top-k korisnici preko `heapq.nlargest`

3. Pretraga
   - username pretraga, case-insensitive
   - bio pretraga preko inverted index-a
   - normalizacija teksta i tokenizacija
   - rangiranje po relevantnosti, zatim po PageRank-u

4. Istorija interakcija
   - pamti nove follow veze dodate tokom rada programa
   - prikazuje koga je korisnik zapratio
   - prikazuje ko je zapratio korisnika
   - prikaz je hronoloski

5. Tekstualni meni
   - pretraga
   - najuticajniji korisnici
   - dodavanje veze
   - istorija
   - autocomplete
   - BFS
   - did-you-mean
   - preporuke

6. Trie i autocomplete
   - sopstvena trie struktura za username prefikse
   - unos moze biti `mar` ili `mar*`
   - rezultati se sortiraju po PageRank-u

7. Hibridne preporuke
   - Personalized PageRank iz perspektive zadatog korisnika
   - Jaccard slicnost biografija
   - skor: `alpha * PPR + (1 - alpha) * content_similarity`
   - filtrira samog korisnika, vec pracene korisnike i blokade u oba smera

8. BFS obilazak
   - prikazuje konekcije po nivoima
   - korisnik bira maksimalni nivo
   - svaki korisnik se obradjuje najvise jednom

9. Did you mean
   - Levenshtein distance za slicna korisnicka imena
   - case-insensitive
   - kod izjednacenja prednost ima veci PageRank

10. Blokirani korisnici
   - `blocked.txt` se ucitava
   - dodavanje veze se zabranjuje ako blokada postoji u bilo kom smeru
   - preporuke ne prikazuju blokirane korisnike u oba smera

## Primeri za rucno testiranje

Za brze testiranje preporucuje se privremeno staviti:

```python
DATASET_VELICINA = "small"
```

Primeri:

- PageRank top korisnici: opcija `2`, zatim `3`
- Username pretraga: opcija `1`, zatim `a`, upit `gui`, broj `5`
- Bio pretraga: opcija `1`, zatim `b`, upit `researcher science`, broj `5`
- Dodavanje veze: opcija `3`, zatim `1`, `2`
- Istorija: opcija `4`, zatim `1` ili `2`
- Autocomplete: opcija `5`, upit `gui`, broj `5`
- BFS: opcija `6`, korisnik `1`, nivo `2`
- Did you mean: opcija `7`, upit `guimanj`
- Preporuke: opcija `8`, korisnik `1`, alpha `0.5`, broj `5`

## Performanse

Kontrolna merenja na ovom racunaru:

| Skup | Ucitavanje | PageRank | Inverted index |
|---|---:|---:|---:|
| medium | oko 0.5 s | oko 1.8 s | oko 0.2 s |
| full | oko 4.2 s | oko 36 s | oko 1.7 s |

Na `full` skupu hibridne preporuke za jednog korisnika traju oko 32 s, jer
racunaju Personalized PageRank i prolaze kroz kandidate za slicnost biografija.

## Napomena

Izmene nastale tokom jednog pokretanja programa cuvaju se u memoriji. Upis novih
veza i istorije nazad u ulazne fajlove nije neophodan prema FAQ-u i nije
implementiran.
