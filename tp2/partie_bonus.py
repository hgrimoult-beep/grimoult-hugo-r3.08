"""TP2 — R3.08 — Bonus : l'IA qui bloque, et le championnat.

Jeu 1 de l'énoncé — l'IA qui bloque
-----------------------------------
JoueurIAMalin applique, dans cet ordre :
    1. si un coup la fait gagner, elle le joue ;
    2. sinon, si un coup fait gagner l'adversaire, elle l'occupe (blocage) ;
    3. sinon, elle joue au hasard.

Jeu 2 — le championnat
----------------------
L'énoncé propose d'affronter l'IA d'un voisin en salle. Ici, on automatise le
principe : l'IA au hasard contre l'IA maligne sur N parties, avec un score.

Dépend des parties A, B et C.
Lancement :  python3 tp2/partie_bonus.py            (scénarios + championnat)
             python3 tp2/partie_bonus.py --jouer    (vous contre l'IA maligne)
"""

from __future__ import annotations

import argparse

from partie_a import VIDE, Grille
from partie_b import COUP_IMPOSSIBLE, Coup, JoueurHumain, JoueurIA
from partie_c import Jeu


class JoueurIAMalin(JoueurIA):
    """IA un peu plus futée : elle gagne, sinon elle bloque, sinon au hasard.

    Elle hérite de JoueurIA pour réutiliser le générateur aléatoire (et la
    méthode choisir()), mais elle remplace prochain_coup().
    """

    def prochain_coup(self, tab: Grille, symbole: str | None = None) -> Coup:
        symbole = symbole or self.symbole
        adversaire = "O" if symbole == "X" else "X"

        libres = tab.cases_libres()
        if not libres:
            return COUP_IMPOSSIBLE

        # On cherche d'abord un coup gagnant pour soi (candidat = symbole),
        # puis, si on n'en trouve pas, un coup gagnant pour l'adversaire
        # (candidat = adversaire) : occuper cette case le bloque.
        for candidat in (symbole, adversaire):
            coup = self._coup_gagnant(tab, libres, candidat)
            if coup is not None:
                return coup

        # Aucun enjeu immédiat : on joue au hasard.
        return self.choisir(libres)

    @staticmethod
    def _coup_gagnant(tab: Grille, libres: list[Coup], symbole: str) -> Coup | None:
        """Renvoie la première case libre qui offrirait un alignement à `symbole`.

        On travaille sur une COPIE de la grille : les essais ne modifient
        jamais la vraie grille de la partie.
        """
        simulation = tab.copie()

        for x, y in libres:
            # On essaie le symbole sur la copie...
            simulation.cases[x][y] = symbole
            if simulation.est_gagnant(symbole):
                return (x, y)
            # ... puis on annule l'essai avant de passer à la case suivante.
            simulation.cases[x][y] = VIDE

        return None  # aucun coup ne fait gagner ce symbole


# ---------------------------------------------------------------------------
# Vérification des deux positions du « jeu d'essai » du bonus
# ---------------------------------------------------------------------------
def verifier_scenarios() -> None:
    """Rejoue les deux positions imposées par l'énoncé et vérifie le résultat."""
    ia = JoueurIAMalin("IA maligne", "O", graine=0)

    # --- Scénario 1 : il faut bloquer --------------------------------
    # X X _
    # _ O _
    # _ _ _
    grille = Grille()
    grille.jouer(0, 0, "X")
    grille.jouer(0, 1, "X")
    grille.jouer(1, 1, "O")

    coup = ia.prochain_coup(grille, "O")
    print("Scénario 1 (X X _ / _ O _ / _ _ _) : O joue", coup, "-> bloque")
    assert coup == (0, 2)

    # --- Scénario 2 : il faut gagner (prioritaire sur le blocage) ----
    # O O _
    # X X _
    # _ _ _
    grille = Grille()
    grille.jouer(0, 0, "O")
    grille.jouer(0, 1, "O")
    grille.jouer(1, 0, "X")
    grille.jouer(1, 1, "X")

    coup = ia.prochain_coup(grille, "O")
    print("Scénario 2 (O O _ / X X _ / _ _ _) : O joue", coup, "-> gagne")
    assert coup == (0, 2)


# ---------------------------------------------------------------------------
# Championnat automatique
# ---------------------------------------------------------------------------
def championnat(nb_parties: int, graine: int | None) -> None:
    """Fait s'affronter l'IA au hasard (X) et l'IA maligne (O)."""
    # Deux graines différentes pour que les deux IA ne jouent pas « pareil ».
    seconde_graine = None if graine is None else graine + 1

    jeu = Jeu(
        JoueurIA("IA au hasard", "X", graine),
        JoueurIAMalin("IA maligne", "O", seconde_graine),
        affichage=False,  # pas de grille : on veut juste le score final
    )

    print(f"\nChampionnat automatique : {nb_parties} parties...")
    jeu.jouer(nb_parties)
    # affichage=False masque les grilles, mais on veut quand même le score.
    jeu.afficher_bilan()


def main() -> int:
    """Point d'entrée du bonus."""
    parser = argparse.ArgumentParser(
        description="TP2 — bonus : IA qui bloque et championnat."
    )
    parser.add_argument(
        "--jouer",
        action="store_true",
        help="jouer vous-même contre l'IA maligne",
    )
    parser.add_argument(
        "--parties",
        type=int,
        default=200,
        help="nombre de parties du championnat automatique (défaut : 200)",
    )
    parser.add_argument(
        "--graine",
        type=int,
        default=None,
        help="graine du hasard, pour des parties reproductibles",
    )
    args = parser.parse_args()

    if args.parties < 1:
        parser.error("--parties doit valoir au moins 1")

    # Les deux positions de l'énoncé sont toujours vérifiées : c'est le
    # « jeu d'essai » du bonus.
    print("=== Bonus — jeu d'essai de l'IA qui bloque ===")
    verifier_scenarios()

    if args.jouer:
        # Mode interactif : vous êtes X, l'IA maligne est O.
        print("\n=== Vous (X) contre l'IA maligne (O) ===")
        jeu = Jeu(
            JoueurHumain("Vous", "X"),
            JoueurIAMalin("IA maligne", "O", args.graine),
        )
        jeu.jouer(1)
    else:
        # Mode automatique : le « championnat » demandé par l'énoncé.
        championnat(args.parties, args.graine)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
