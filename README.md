# ASP Projekat 2 - simulacija društvene mreže

Konzolna Python aplikacija koja učitava usmereni graf društvene mreže i omogućava rangiranje korisnika PageRank algoritmom, pretragu profila, dodavanje novih veza praćenja i pregled istorije interakcija.

Projekat koristi priložene skupove podataka iz specifikacije predmeta. Trenutno su u potpunosti implementirani zadaci 1-5, odnosno osnovni deo projekta.

## Zahtevi

- Python 3.10 ili noviji
- Nisu potrebne dodatne biblioteke

Koriste se isključivo moduli iz Python standardne biblioteke, kao što su `heapq`, `re` i `datetime`.

## Pokretanje

Program treba pokrenuti iz korenskog direktorijuma projekta:

```powershell
python main.py
```

Veličina skupa podataka bira se promenom konstante `DATASET_VELICINA` u fajlu `main.py`:

```python
DATASET_VELICINA = "small"  # "small", "medium" ili "full"
```

Za razvoj i brzo testiranje preporučuje se `small`, za demonstraciju `medium`, dok je `full` namenjen proveri performansi.

## Ulazni podaci

Za svaku veličinu skupa očekuju se sledeća tri fajla unutar direktorijuma `dataset/<velicina>/`.

### `users.txt`

Podaci o korisnicima u formatu:

```text
id|username|bio
```

- `id` - jedinstveni celobrojni identifikator korisnika
- `username` - korisničko ime
- `bio` - tekstualni opis profila

### `connections.txt`

Usmerene veze praćenja u formatu:

```text
from_id|to_id
```

Zapis znači da korisnik `from_id` prati korisnika `to_id`.

### `blocked.txt`

Podaci o blokiranju u formatu:

```text
blocker_id|blocked_id
```

Zapis znači da je korisnik `blocker_id` blokirao korisnika `blocked_id`. Podaci se trenutno učitavaju u graf; njihova primena pri preporukama i dodavanju veza pripada dodatnom delu projekta.

## Implementirane funkcionalnosti

### 1. Graf društvene mreže

- klase `User` i `SocialGraph`
- usmereni graf praćenja
- hash mape za pristup korisnicima po ID-u i korisničkom imenu
- odvojeno čuvanje ulaznih i izlaznih veza
- efikasan pristup ulaznom i izlaznom stepenu korisnika
- učitavanje blokada u oba smera radi kasnije efikasne provere

### 2. PageRank

- sopstvena iterativna implementacija PageRank algoritma
- damping faktor `0.85`
- zaustavljanje pri konvergenciji sa `epsilon = 1e-6`
- pravilna obrada korisnika bez izlaznih veza
- warm start pri ponovnom računanju nakon dodavanja veze
- izdvajanje najuticajnijih korisnika pomoću heap strukture

### 3. Pretraga korisnika

- case-insensitive pretraga po korisničkom imenu
- pretraga po rečima iz biografije
- normalizacija teksta i tokenizacija
- inverted index koji se formira jednom pri pokretanju
- rangiranje prema relevantnosti, a zatim prema PageRank vrednosti
- izdvajanje top rezultata pomoću heap strukture

Kod pretrage po korisničkom imenu tačno poklapanje ima najveću relevantnost, zatim prefiks, pa pojavljivanje upita unutar imena. Kod pretrage biografije relevantnost predstavlja broj različitih reči iz upita pronađenih u biografiji.

### 4. Istorija interakcija

- evidentiranje novih veza dodatih tokom rada programa
- pregled korisnika koje je zadati korisnik zapratio
- pregled korisnika koji su zapratili zadatog korisnika
- hronološki prikaz sa vremenom nastanka događaja

Početne veze iz skupa podataka predstavljaju početno stanje grafa i ne upisuju se u istoriju tekuće sesije.

### 5. Tekstualni meni

Meni omogućava:

1. pretragu po korisničkom imenu ili biografiji;
2. prikaz najuticajnijih korisnika;
3. dodavanje nove veze praćenja;
4. prikaz istorije interakcija;
5. izlazak iz programa.

Unosom `q` pri unosu celobrojnih parametara moguće je otkazati trenutnu operaciju.

## Primeri za demonstraciju

Pošto se korisnička imena i ID-jevi razlikuju između skupova, praktični primeri mogu se pronaći direktno u odgovarajućem fajlu `dataset/<velicina>/users.txt`.

Predloženi tok demonstracije:

1. pokrenuti program nad `medium` skupom;
2. prikazati deset najuticajnijih korisnika;
3. pretražiti često korišćenu reč poput `python`, `data`, `music` ili `research` u biografijama;
4. pretražiti celo korisničko ime i deo tog imena;
5. dodati novu vezu između dva postojeća korisnika koja već nije prisutna;
6. pokazati ponovno računanje PageRank-a i istoriju oba učesnika.

## Struktura projekta

```text
.
|-- algorithms/
|   |-- pagerank.py       # PageRank i izbor top korisnika
|   `-- search.py         # pretraga i inverted index
|-- data_io/
|   `-- loader.py         # učitavanje ulaznih fajlova
|-- dataset/
|   |-- small/
|   |-- medium/
|   `-- full/
|-- models/
|   |-- user.py
|   `-- social_graph.py
|-- text/
|   `-- text_processing.py
|-- history.py
|-- menu.py
`-- main.py
```

U projektu postoje i moduli namenjeni funkcionalnostima dodatnog dela. Funkcionalnost se u ovom dokumentu smatra implementiranom tek kada je povezana sa ostatkom aplikacije i dostupna kroz meni.

## Performanse

Kontrolno merenje nad priloženim `full` skupom dalo je sledeće rezultate:

| Operacija | Vreme |
|---|---:|
| Učitavanje 81.306 korisnika i 1.768.135 veza | oko 4,5 s |
| Početno računanje PageRank-a | oko 35,8 s |
| Formiranje inverted index-a | oko 2,4 s |

Vremena zavise od računara i Python okruženja. Strukture se formiraju jednom pri pokretanju i ne učitavaju se ponovo pri svakoj operaciji.

## Plan dodatnog dela

Za kompletiranje projekta do 25 poena potrebno je završiti i integrisati:

- Trie i autocomplete;
- hibridne preporuke pomoću Personalized PageRank-a i sličnosti biografija;
- BFS obilazak po nivoima konekcija;
- „Did you mean“ predloge;
- primenu blokada pri preporukama i dodavanju novih veza;
- završnu validaciju unosa, dokumentaciju i proveru performansi.

## Napomena o izmenama

Nove veze i ponovo izračunate PageRank vrednosti čuvaju se tokom trenutnog pokretanja programa. Upis izmena nazad u ulazne fajlove nije neophodan prema specifikaciji i trenutno nije implementiran.
