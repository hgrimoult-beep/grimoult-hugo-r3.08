"""TP2 — R3.08 — Partie C : le jeu complet.

Objectif de l'énoncé
--------------------
Faire s'affronter deux joueurs dans une boucle :
    - chacun joue à son tour ;
    - un coup invalide affiche un message et le MÊME joueur rejoue ;
    - on s'arrête à la victoire d'un joueur ou quand la grille est pleine (nul).

Bonus demandés dans cette partie :
    - score sur plusieurs parties ;
    - mode « 2 humains ».

Dépend des parties A (Grille) et B (joueurs).
Lancement :  python3 tp2/partie_c.py             (humain contre IA)
             python3 tp2/partie_c.py --mode hh   (deux humains)
"""

from __future__ import annotations

import argparse

from partie_a import SYMBOLES, Grille
from partie_b import Coup, Joueur, JoueurHumain, JoueurIA


class Jeu:
    """Orchestre une ou plusieurs parties entre deux joueurs.

    Exemple d'utilisation :
        jeu = Jeu(JoueurHumain("Vous", "X"), JoueurIA("IA", "O", graine=42))
        jeu.jouer()      # une partie
        jeu.jouer(10)    # dix parties, avec un bilan
    """

    def __init__(
        self,
        joueur_x: Joueur,
        joueur_o: Joueur,
        *,
        affichage: bool = True,
    ) -> None:
        # Le jeu associe un joueur à chaque symbole. On impose « X » puis
        # « O » pour que le reste du code n'ait jamais à se poser la question.
        if joueur_x.symbole != "X" or joueur_o.symbole != "O":
            raise ValueError(
                "le premier joueur doit avoir le symbole 'X' "
                "et le second le symbole 'O'"
            )

        self.joueurs: dict[str, Joueur] = {"X": joueur_x, "O": joueur_o}
        self.affichage = affichage
        self.scores: dict[str, int] = {"X": 0, "O": 0, "nuls": 0}

    # ------------------------------------------------------------------
    # Une partie
    # ------------------------------------------------------------------
    def jouer_une_partie(self, premier: str = "X") -> str | None:
        """Joue UNE partie et renvoie « X », « O », ou None en cas de nul."""
        if premier not in SYMBOLES:
            raise ValueError(f"symbole de départ invalide : {premier!r}")

        grille = Grille()
        symbole = premier

        # La boucle principale : un tour = un coup joué.
        while True:
            joueur = self.joueurs[symbole]

            # 1) Montrer la situation au joueur (sauf en mode silencieux).
            if self.affichage:
                print()
                grille.afficher()
                print(f"Au tour de {joueur.nom} ({symbole}).")

            # 2) Demander un coup valide. _demander_coup ne rend la main que
            #    lorsque le coup est jouable : un coup refusé fait rejouer.
            x, y = self._demander_coup(grille, joueur, symbole)
            grille.jouer(x, y, symbole)  # le coup est déjà validé

            # 3) Victoire ? On teste AVANT la grille pleine : si le dernier
            #    coup libre réalise un alignement, c'est une victoire et non
            #    un match nul.
            if grille.est_gagnant(symbole):
                if self.affichage:
                    print()
                    grille.afficher()
                    print(f"*** {joueur.nom} ({symbole}) gagne ! ***")
                return symbole

            # 4) Plus aucune case libre et personne n'a gagné : match nul.
            if grille.est_plein():
                if self.affichage:
                    print()
                    grille.afficher()
                    print("Match nul : la grille est pleine.")
                return None

            # 5) Au tour de l'autre joueur.
            symbole = "O" if symbole == "X" else "X"

    def _demander_coup(
        self, grille: Grille, joueur: Joueur, symbole: str
    ) -> Coup:
        """Demande un coup jusqu'à en obtenir un valide.

        Un coup refusé (case occupée, hors grille...) affiche un message et
        c'est LE MÊME joueur qui rejoue, conformément à l'énoncé.
        """
        essais = 0

        while True:
            coup = joueur.prochain_coup(grille, symbole)

            # On vérifie d'abord la forme du coup : une IA défectueuse
            # pourrait renvoyer autre chose qu'un couple (x, y).
            try:
                x, y = coup
            except (TypeError, ValueError):
                erreur = f"coup illisible : {coup!r}"
            else:
                erreur = grille.verifier(x, y)

            # Coup valide : on peut le renvoyer à jouer_une_partie().
            if erreur is None:
                return (x, y)

            # Coup refusé : on explique pourquoi et on redemande au même joueur.
            essais += 1
            if self.affichage:
                print(f"  [!] Coup refusé : {erreur}. {joueur.nom} rejoue.")

            # Sécurité anti-boucle infinie : une IA qui ne produirait que des
            # coups invalides finit par déclencher une erreur explicite.
            # Un humain, lui, n'est pas limité (ESSAIS_ILLIMITES = True).
            if not joueur.ESSAIS_ILLIMITES and essais >= joueur.MAX_ESSAIS:
                raise RuntimeError(
                    f"{joueur.nom} n'a proposé aucun coup valide en "
                    f"{essais} essais (dernier coup : {coup!r})."
                )

    # ------------------------------------------------------------------
    # Série de parties (bonus « score multi-parties »)
    # ------------------------------------------------------------------
    def jouer(self, nb_parties: int = 1) -> dict[str, int]:
        """Enchaîne `nb_parties` parties et renvoie les scores.

        Le joueur « X » commence les parties impaires, « O » les parties
        paires : le score reste équitable sur une longue série.
        """
        if nb_parties < 1:
            raise ValueError("il faut jouer au moins une partie")

        # On repart de zéro à chaque appel : les scores ne s'accumulent pas
        # d'une série de parties à l'autre.
        self.scores = {"X": 0, "O": 0, "nuls": 0}

        for i in range(nb_parties):
            if nb_parties > 1 and self.affichage:
                print(f"\n=== Partie {i + 1}/{nb_parties} ===")

            # Alterne qui commence : X aux parties 1, 3, 5..., O aux autres.
            premier = "X" if i % 2 == 0 else "O"
            vainqueur = self.jouer_une_partie(premier)

            # On range le résultat dans la bonne case du dictionnaire.
            cle = "nuls" if vainqueur is None else vainqueur
            self.scores[cle] += 1

        if self.affichage:
            self.afficher_bilan()
        return dict(self.scores)

    def afficher_bilan(self) -> None:
        """Affiche le score cumulé de la série."""
        joueur_x = self.joueurs["X"]
        joueur_o = self.joueurs["O"]
        print(
            f"\nBilan : {joueur_x.nom} (X) {self.scores['X']} — "
            f"{joueur_o.nom} (O) {self.scores['O']} — "
            f"nuls {self.scores['nuls']}"
        )


# ---------------------------------------------------------------------------
# Ligne de commande
# ---------------------------------------------------------------------------
MODES: dict[str, str] = {
    "hh": "deux humains",
    "hia": "humain (X) contre IA (O)",
    "iah": "IA (X) contre humain (O)",
    "iaia": "IA (X) contre IA (O)",
}


def construire_joueurs(mode: str, graine: int | None) -> tuple[Joueur, Joueur]:
    """Construit le couple (joueur X, joueur O) correspondant au mode."""
    if mode == "hh":
        return JoueurHumain("Joueur 1", "X"), JoueurHumain("Joueur 2", "O")

    if mode == "hia":
        return JoueurHumain("Vous", "X"), JoueurIA("IA", "O", graine)

    if mode == "iah":
        return JoueurIA("IA", "X", graine), JoueurHumain("Vous", "O")

    if mode == "iaia":
        # Deux graines différentes : sinon les deux IA joueraient « pareil ».
        seconde_graine = None if graine is None else graine + 1
        return JoueurIA("IA 1", "X", graine), JoueurIA("IA 2", "O", seconde_graine)

    raise ValueError(f"mode inconnu : {mode!r}")


def lire_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    """Analyse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        prog="partie_c.py",
        description="Morpion — TP2 R3.08 (partie C).",
        epilog=(
            "Pour jouer contre l'IA qui bloque : python3 tp2/partie_bonus.py --jouer"
        ),
    )
    parser.add_argument(
        "--mode",
        choices=sorted(MODES),
        default="hia",
        help="qui s'affronte (défaut : hia)",
    )
    parser.add_argument(
        "--parties",
        type=int,
        default=1,
        help="nombre de parties enchaînées (défaut : 1)",
    )
    parser.add_argument(
        "--graine",
        type=int,
        default=None,
        help="graine du hasard, pour des parties reproductibles",
    )
    parser.add_argument(
        "--muet",
        action="store_true",
        help="ne pas afficher les grilles (utile pour les longues séries)",
    )
    args = parser.parse_args(argv)
    if args.parties < 1:
        parser.error("--parties doit valoir au moins 1")
    return args


def main(argv: list[str] | None = None) -> int:
    """Lance le jeu et renvoie un code de sortie."""
    args = lire_arguments(argv)
    joueur_x, joueur_o = construire_joueurs(args.mode, args.graine)
    jeu = Jeu(joueur_x, joueur_o, affichage=not args.muet)

    if not args.muet:
        print("=== TP2 — Morpion (partie C) ===")
        print(f"Mode : {MODES[args.mode]}")
        print("Coordonnées : x = ligne, y = colonne (0 à 2).")
        print("Exemple : « 0 2 » joue en haut à droite.")
        if isinstance(joueur_x, JoueurHumain) or isinstance(joueur_o, JoueurHumain):
            print("Ctrl-D pour quitter.")
        print()

    jeu.jouer(args.parties)

    # En mode silencieux, on garde au moins le score final.
    if args.muet:
        jeu.afficher_bilan()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
