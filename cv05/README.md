Cvičenie 5
==========

**Riešenie odovzdávajte podľa
[pokynov na konci tohoto zadania](#technické-detaily-riešenia)
do utorka 5.4. 23:59:59.**

Súbory potrebné pre toto cvičenie si môžete stiahnuť ako jeden zip
[`cv05.zip`](https://github.com/FMFI-UK-1-AIN-412/lpi/archive/cv05.zip).

toCnf (3b)
----------

Do tried na reprezentáciu formúl z cvičenia 3 doimplementujte metódu `toCnf()`,
ktorá vráti ekvisplniteľnú (alebo ekvivalentnú) formulu v konjunktívnej
normálnej forme (viď [Reprezentácia CNF](#reprezentácia-cnf)).

Na prednáške bolo spomenutých niekoľko rôznych prístupov s rôznymi
vlastnosťami. Pri našej reprezentácii formúl je asi najjednoduchší (na
naprogramovanie :) spôsob taký, že každej z našich predchádzajúcich tried
implementujeme virtuálnu metódu `toCnf`, ktorá daný typ formuly preloží do CNF tak, že
rekurzívne zavolá `toCnf` na svoje podformuly a potom ich CNF nejak spojí / upraví.

Premenná jednoducho vráti (zoznam obsahujúci) jednu klauzu, v ktorej je jeden
(nenegovaný) `Literal` so správnym menom.

Konjunkcia zavolá `toCnf` na jednotlivé konjunkty, dostane niekoľko CNF (zoznamov
kláuz) a vyrobí z nich jednu tak, že jednoducho dá dokopy všetky klauzy do
jedného zoznamu.

Disjunkcia už je zložitejšia, pretože čiastočné CNF pre jednotlivé disjunkty
musíme medzi sebou „roznásobiť“, pričom roznásobujeme ľubovoľne veľa
disjunktov, ktoré môžu obsahovať ľubovoľne veľa kláuz.

V prípade negácie sa tiež dostaneme k podobnému problému (oplatí sa
optimalizovať / špeciálne ošetriť prípad, keď je negovaná iba premenná).

Implikácia (a podobne aj ekvivalencia) sa najjednoduchšie implementuje tak, že
z nej spravíme disjunkciu a zavoláme `toCnf` na nej :) (pri takýchto operáciách si
ale treba dať pozor na „zacyklenie“).

Príklad pre disjunkciu:
```python
class Disjunction(Formula):
    def doProduct(self, cnfs, level, rClause, rCnf):
        if level < len(cnfs):
            for clause in cnfs[level]:
                extRClause = copy.deepcopy(rClause)
                extRClause.extend(copy.deepcopy(clause))
                self.doProduct(cnfs, level+1, extRClause, rCnf)
        else:
            rCnf.append(rClause)

    def toCnf(self):
        # prevedieme vsetky podformuly do CNF
        cnfs = []
        for sf in self.subf():
            cnfs.append(sf.toCnf())

        # roznasobime ich, pricom vzniknute klauzy
        # ukladame do c
        c = []
        self.doProduct(cnfs, 0, [], c)
        return c
```

## Reprezentácia CNF

Triedy, ktoré sme vyrobili v [cvičení 3](../cv03/), nie sú z viacerých dôvodov
veľmi vhodné na reprezentáciu formúl v CNF:
- kedykoľvek by sme očakávali formulu v CNF tvare,  museli by sme vždy
  kontrolovať, či naozaj má správny tvar;
- je trošku neefektívna ( `Negation(Variable("x"))`) a ťažkopádnejšia
  na použite (musíme zisťovať akého typu je podformula v `Disjunction` atď.);
- chceme pridať niekoľko metód, ktoré majú zmysel len pre CNF formulu.

Najpriamočiarejší spôsob, ako sa týmto problémom vyhnúť, je reprezentovať CNF
formulu jednoducho ako pole (pythonovský zoznam, list) kláuz, pričom každá klauza je pole
literálov. Literál by mohol byť reprezentovaný ako dvojica: meno
a boolovský flag hovoriaci, či je negovaný.
Operácie s takto reprezentovanými CNF formulami by ale potom nemohli byť
implementované ako ich metódy.

Obidve výhody dosiahneme tak,
že vytvoríme triedy `Cnf` a `Clause`, ktoré oddedíme od poľa (`list`-u)
a pridáme im navyše potrebné metódy.
Na reprezentáciu literálov vytvoríme triedu `Literal`.
Ďalšou výhodou takéhoto prístupu je aj to, že vieme písať kód,
ktorý sa oveľa ľahšie číta:
namiesto hromady hranatých zátvoriek vidíme, či vytvárame klauzu
alebo celú CNF formulu.

V súbore [`cnf.py`](cnf.py) nájdete hotové definície tried `Literal`,
`Clause` a `Cnf`, ktoré máte použiť na reprezentáciu literálov, kláuz a CNF
formúl. Vaše metódy `toCnf` teda majú vždy vracať inštanciu triedy `Cnf`.

V tom istom súbore nájdete aj ďalšiu pomocnú triedu `VariableMap`,
ktorá ale nie je dôležitá pre riešenie tohto cvičenia
(môžete sa však inšpirovať jej použitím v programe `prover.py`).

## prover.py

V súbore [`prover.py`](prover.py) je ukážka veľmi jednoduchej funkcie, ktorá
všetky naše doteraz implementované triedy používa, aby pomocou SAT solvera
dokazovala, či nejaká formula vyplýva z nejakej teórie (množiny formúl).
Samozrejme fungovať bude korektne, až keď korektne naimplementujete `toCnf`.

## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv05` v adresári `cv05`.  Odovzdávajte
(modifikujte) súbor `formula.py`. Program [`toCnfTest.py`](toCnfTest.py) musí
korektne zbehnúť s vašou knižnicou.

Súbor `formula.py` obsahuje vzorové riešenie predchádzajúceho cvičenia
`cv03`. Vašou úlohou je doimplementovať metódu `toCnf` pre každú triedu
odvodenú od `Formula`.

Odovzdávanie riešení v iných jazykoch konzultujte s cvičiacimi.

## Bonus

Uvedená „jednoduchá“ metóda je veľmi neefektívna vzhľadom na veľkosť /
komplikovanosť výsledných formúl. Napríklad pre niektoré formuly
stupňa menšieho ako 10 vyrobíme CNF obsahujúce desaťtisíce až
stotisíce výskytov literálov.

Ak implementujete nejakú efektívnejšiu (vzhľadom na veľkosť výslednej
formuly, ale pozor aj na čas behu) metódu na konverziu do CNF, uveďte
to v pull requeste s krátkym popisom vášho algoritmu (odkaz na nejaký
internetový zdroj je OK, implementácia ale musí byť vaša vlastná)
a môžete získať **až 4 bonusové body**.
