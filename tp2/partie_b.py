"""TP2 — R3.08 — Partie B : les joueurs.

Objectif de l'énoncé
--------------------
Deux façons de jouer, derrière la MÊME méthode :

    prochain_coup(tab, symbole) -> (x, y)

    - JoueurHumain : lit les coordonnées au clavier ;
    - JoueurIA     : choisit une case libre au hasard.

Un joueur ne modifie jamais la grille : il propose seulement un coup. C'est la
partie C (classe Jeu) qui vérifie le coup et le joue réellement.

Dépend de la partie A (classe Grille).
Lancement :  python3 tp2/partie_b.py
"""

from __future__ import annotations

import random
from abc import ABC, abstractmethod

from partie_a import SYMBOLES, Grille

# Un coup est un couple d'entiers : (x, y).
Coup = tuple[int, int]

# Sentinelle renvoyée quand aucun coup n'est possible (grille pleine).
# Cela évite de renvoyer None, qui provoquerait une erreur au moment de
# déballer le couple (x, y).
COUP_IMPOSSIBLE: Coup = (-1, -1)


class Joueur(ABC):
    """Classe mère (abstraite) de tous les joueurs.

    Elle impose un « contrat » : toute classe fille doit savoir répondre à
    prochain_coup(). On ne peut pas créer un Joueur directement, seulement
    un JoueurHumain ou un JoueurIA.
    """

    # Sécurité utilisée par la classe Jeu : au bout de 100 coups invalides,
    # une IA considérée comme défaillante provoque une erreur claire plutôt
    # qu'une boucle infinie. Un humain, lui, a le droit de se tromper sans
    # limite (voir ESSAIS_ILLIMITES ci-dessous).
    MAX_ESSAIS = 100
    ESSAIS_ILLIMITES = False

    def __init__(self, nom: str, symbole: str) -> None:
        # On vérifie le symbole dès la construction : un joueur ne peut être
        # que « X » ou « O ». Mieux vaut une erreur claire ici que plus tard.
        if symbole not in SYMBOLES:
            raise ValueError(
                f"symbole invalide : {symbole!r} "
                f"(attendu : {' ou '.join(SYMBOLES)})"
            )
        self.nom = nom
        self.symbole = symbole

    @abstractmethod
    def prochain_coup(self, tab: Grille, symbole: str | None = None) -> Coup:
        """Renvoie les coordonnées (x, y) du coup choisi.

        tab     : la grille courante (objet Grille) ;
        symbole : le symbole avec lequel on doit jouer. Il est optionnel :
                  par défaut, le joueur utilise le sien. Cela permet de
                  réutiliser un même objet joueur pour les deux camps.
        """

    def __str__(self) -> str:
        """Affichage lisible d'un joueur, pratique pour les messages."""
        return f"{self.nom} ({self.symbole})"


class JoueurHumain(Joueur):
    """Joueur qui saisit ses coordonnées au clavier."""

    # Un humain peut se tromper autant de fois qu'il veut : la boucle de
    # saisie ne s'arrête jamais toute seule (sauf Ctrl-D).
    ESSAIS_ILLIMITES = True

    def prochain_coup(self, tab: Grille, symbole: str | None = None) -> Coup:
        """Demande les coordonnées au clavier jusqu'à obtenir deux entiers.

        La validité du coup (case libre, coordonnées dans la grille) est
        vérifiée par la classe Jeu : ici, on se contente de lire correctement
        deux entiers. Si le coup est refusé, Jeu rappellera cette méthode.
        """
        symbole = symbole or self.symbole

        # On boucle jusqu'à obtenir une saisie correcte : deux entiers.
        while True:
            try:
                saisie = input(f"{self.nom} ({symbole}) — votre coup « x y » : ")
            except EOFError:
                # Ctrl-D (fin de l'entrée standard) : on quitte proprement,
                # sans afficher de traceback Python.
                print("\nPartie interrompue.")
                raise SystemExit(0) from None

            # On tolère « 1 2 », « 1,2 » et les espaces en trop :
            # la virgule est remplacée par un espace, puis split() découpe.
            morceaux = saisie.replace(",", " ").split()

            # Il faut exactement deux morceaux, tous les deux entiers.
            if len(morceaux) == 2:
                try:
                    return int(morceaux[0]), int(morceaux[1])
                except ValueError:
                    pass  # ce n'était pas des entiers : on redemande

            # Message d'aide, puis la boucle repose la question.
            print(
                "  [!] Saisie invalide : entrez deux entiers séparés par un "
                "espace, par exemple « 1 2 »."
            )


class JoueurIA(Joueur):
    """IA naïve : joue une case libre au hasard."""

    def __init__(
        self,
        nom: str = "IA",
        symbole: str = "O",
        graine: int | None = None,
    ) -> None:
        super().__init__(nom, symbole)

        # random.Random(graine) crée un générateur PRIVÉ. Avec la même graine,
        # on rejoue exactement les mêmes parties (très pratique pour tester),
        # sans perturber le hasard global du reste du programme.
        self._hasard = random.Random(graine)

    def choisir(self, libres: list[Coup]) -> Coup:
        """Choisit un coup parmi `libres`, ou la sentinelle si c'est vide."""
        # choice() lève une erreur sur une liste vide : on traite donc ce cas
        # à part, en renvoyant COUP_IMPOSSIBLE.
        if not libres:
            return COUP_IMPOSSIBLE
        return self._hasard.choice(libres)

    def prochain_coup(self, tab: Grille, symbole: str | None = None) -> Coup:
        # L'IA n'a besoin que de la liste des cases libres : elle en tire une
        # au hasard. Elle ne regarde même pas qui est en train de gagner.
        return self.choisir(tab.cases_libres())


# ---------------------------------------------------------------------------
# Démonstration (exécutée seulement si on lance ce fichier)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Partie B — les joueurs ===")

    # --- 1) L'IA au hasard -------------------------------------------
    grille = Grille()
    ia = JoueurIA("IA", "O", graine=1)
    print("Trois coups proposés par l'IA au hasard :")
    for _ in range(3):
        coup = ia.prochain_coup(grille, "O")
        print("  ", coup)
        # On place le symbole pour que l'IA propose à chaque fois une autre
        # case libre (sinon elle pourrait retomber sur la même case).
        x, y = coup
        grille.cases[x][y] = "O"

    # --- 2) Le joueur humain -----------------------------------------
    print("\nÀ vous : entrez deux entiers (x y), par exemple « 1 1 ».")
    humain = JoueurHumain("Vous", "X")
    coup = humain.prochain_coup(Grille(), "X")
    print("Coup saisi :", coup)

    print("\nPartie B : démonstration terminée.")
