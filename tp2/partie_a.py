"""TP2 — R3.08 — Partie A : la classe Grille.

Objectif de l'énoncé
--------------------
Représenter une grille de Morpion 3×3 par une liste de listes, avec :

    - afficher()           : un rendu lisible dans le terminal ;
    - jouer(x, y, joueur)  : place « X » ou « O » si la case est libre ;
    - est_gagnant(joueur)  : détecte un alignement de 3 symboles ;
    - est_plein()          : True quand plus aucune case n'est libre.

Convention de coordonnées (celle du jeu d'essai du sujet)
---------------------------------------------------------
x est l'indice de LIGNE, y l'indice de COLONNE, tous deux dans 0..2.
Ainsi (0, 0) est en haut à gauche et (2, 2) en bas à droite :

    jouer(0, 0, "X")  ->  X en haut à gauche
    jouer(0, 1, "O")  ->  O au milieu de la première ligne
    jouer(1, 1, "X")  ->  X au centre

Ce fichier est autonome : il ne dépend d'aucune autre partie du TP.
Lancement :  python3 tp2/partie_a.py
"""

from __future__ import annotations  # annotations "en texte" : pas de souci d'ordre

# ---------------------------------------------------------------------------
# Constantes du jeu
# ---------------------------------------------------------------------------
TAILLE = 3            # grille 3 × 3
VIDE = " "            # contenu d'une case libre
SYMBOLES = ("X", "O")  # les deux seuls symboles autorisés

# Les 8 alignements gagnants, écrits une fois pour toutes sous forme de
# coordonnées (x, y) : 3 lignes, 3 colonnes et 2 diagonales.
# Les écrire ici évite de répéter huit tests dans est_gagnant() et rend la
# méthode beaucoup plus lisible.
COMBINAISONS_GAGNANTES = (
    # --- les 3 lignes ---
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    # --- les 3 colonnes ---
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    # --- les 2 diagonales ---
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
)


class Grille:
    """Une grille de Morpion 3×3.

    La grille est stockée dans `self.cases` : une liste de 3 listes de 3
    chaînes. Chaque case vaut soit VIDE (" "), soit "X", soit "O".

    Exemple d'utilisation :
        >>> g = Grille()
        >>> g.jouer(1, 1, "X")
        True
        >>> g.est_plein()
        False
    """

    def __init__(self) -> None:
        # Piège classique : [[VIDE] * 3] * 3 créerait UNE seule liste réutilisée
        # trois fois. En modifiant une case, on modifierait la même case dans
        # les trois lignes ! La double compréhension ci-dessous crée bien trois
        # listes indépendantes (une par ligne).
        self.cases: list[list[str]] = [
            [VIDE for _ in range(TAILLE)] for _ in range(TAILLE)
        ]

    # ------------------------------------------------------------------
    # Affichage
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        """Renvoie la grille sous forme de texte (utilisé par afficher())."""
        # 4 * 3 - 3 = 9 tirets, comme dans l'exemple de l'énoncé.
        separateur = "-" * (4 * TAILLE - 3)

        # Chaque ligne ressemble à " X | O |   " : join() intercale " | "
        # entre les trois cases, et on ajoute un espace de chaque côté.
        lignes = (" " + " | ".join(ligne) + " " for ligne in self.cases)

        # On relie les trois lignes par le trait horizontal.
        return ("\n" + separateur + "\n").join(lignes)

    def afficher(self) -> None:
        """Affiche la grille de façon lisible dans le terminal."""
        # print(self) appelle automatiquement __str__ : le rendu est défini
        # à un seul endroit.
        print(self)

    # ------------------------------------------------------------------
    # Lecture de la grille
    # ------------------------------------------------------------------
    def est_libre(self, x: int, y: int) -> bool:
        """Renvoie True si la case (x, y) existe et n'est pas occupée."""
        # On vérifie d'abord le type : sans cela, comparer "a" à un entier
        # déclencherait une TypeError. Une case hors grille n'est pas libre.
        return (
            isinstance(x, int)
            and isinstance(y, int)
            and 0 <= x < TAILLE
            and 0 <= y < TAILLE
            and self.cases[x][y] == VIDE
        )

    def cases_libres(self) -> list[tuple[int, int]]:
        """Renvoie la liste des cases encore vides, dans l'ordre de lecture."""
        # Double boucle : on parcourt les lignes (x), puis les colonnes (y).
        return [
            (x, y)
            for x in range(TAILLE)
            for y in range(TAILLE)
            if self.cases[x][y] == VIDE
        ]

    def est_plein(self) -> bool:
        """Renvoie True si aucune case n'est libre."""
        # all(...) : il faut que TOUTES les cases soient différentes de VIDE.
        # Le double for parcourt les 3 lignes puis les 3 cases de chaque ligne.
        return all(case != VIDE for ligne in self.cases for case in ligne)

    def est_gagnant(self, joueur: str) -> bool:
        """Renvoie True si `joueur` aligne trois symboles.

        Vérifie les 3 lignes, les 3 colonnes et les 2 diagonales.
        """
        # Un symbole qui n'est ni "X" ni "O" ne peut pas gagner. Ce garde-fou
        # évite aussi que la case VIDE soit prise pour un alignement (sinon
        # une grille vide serait déclarée gagnante !).
        if joueur not in SYMBOLES:
            return False

        # any(...) : True dès qu'UN alignement est complet.
        # all(...) : il faut que les TROIS cases de cet alignement soient
        # occupées par ce joueur.
        return any(
            all(self.cases[x][y] == joueur for x, y in alignement)
            for alignement in COMBINAISONS_GAGNANTES
        )

    # ------------------------------------------------------------------
    # Écriture de la grille
    # ------------------------------------------------------------------
    def verifier(self, x: int, y: int) -> str | None:
        """Vérifie qu'un coup est possible, SANS le jouer.

        Renvoie None si le coup est valide, sinon une chaîne expliquant le
        refus. Cette séparation « vérifier / jouer » permet au jeu d'afficher
        un message précis (« case occupée », « hors grille »...) tout en
        gardant jouer() simple et sans exception.
        """
        # Cas 1 : ce ne sont pas des entiers (ex. "a", 3.5...).
        if not isinstance(x, int) or not isinstance(y, int):
            return "les coordonnées doivent être deux entiers"

        # Cas 2 : entiers, mais en dehors de la grille (ex. 3 ou -1).
        if not (0 <= x < TAILLE and 0 <= y < TAILLE):
            return (
                f"({x}, {y}) est hors grille : "
                f"x et y doivent être dans 0..{TAILLE - 1}"
            )

        # Cas 3 : la case est déjà prise par un des deux joueurs.
        if self.cases[x][y] != VIDE:
            return f"la case ({x}, {y}) est déjà occupée par {self.cases[x][y]}"

        # Aucun problème : le coup est jouable.
        return None

    def jouer(self, x: int, y: int, joueur: str) -> bool:
        """Place « X » ou « O » en (x, y) si la case est libre.

        Renvoie True si le coup a été joué, False s'il est refusé. Aucune
        exception n'est levée : c'est le défi « pas de plantage » de l'énoncé
        (case occupée, x = 3, x = -1, saisie non entière...).
        """
        # 1) Le symbole doit être l'un des deux symboles du jeu.
        if joueur not in SYMBOLES:
            return False

        # 2) Les coordonnées doivent désigner une case libre de la grille.
        if self.verifier(x, y) is not None:
            return False

        # 3) Tout est bon : on écrit le symbole dans la case.
        self.cases[x][y] = joueur
        return True

    def copie(self) -> "Grille":
        """Renvoie une copie indépendante de la grille.

        Utile à l'IA « qui bloque » : elle peut essayer un coup sur la copie
        sans abîmer la vraie grille de la partie.
        """
        nouvelle = Grille()
        # ligne[:] crée une nouvelle liste pour chaque ligne : les deux
        # grilles ne partagent aucune case.
        nouvelle.cases = [ligne[:] for ligne in self.cases]
        return nouvelle


# ---------------------------------------------------------------------------
# Jeu d'essai de l'énoncé (exécuté seulement si on lance ce fichier)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Partie A — jeu d'essai de l'énoncé ===")

    g = Grille()
    g.jouer(0, 0, "X")
    g.jouer(0, 1, "O")
    g.jouer(1, 1, "X")

    print("Grille après trois coups :")
    g.afficher()

    # Case occupée : le coup doit être refusé (False), sans plantage.
    print("jouer(0, 0, 'O')  ->", g.jouer(0, 0, "O"))
    # Coordonnées hors grille : refusées aussi.
    print("jouer(3, 0, 'O')  ->", g.jouer(3, 0, "O"))
    print("jouer(-1, 0, 'O') ->", g.jouer(-1, 0, "O"))

    # Avant le 4e coup, personne n'a trois symboles alignés.
    print("est_gagnant('X') avant (2, 2) :", g.est_gagnant("X"))

    # X complète la diagonale (0,0) - (1,1) - (2,2) : il gagne.
    g.jouer(2, 2, "X")
    print("est_gagnant('X') après (2, 2) :", g.est_gagnant("X"))

    # Petites vérifications automatiques, en plus des affichages.
    assert not g.est_gagnant("O")
    assert g.est_gagnant("X")
    assert not g.est_plein()
    print("\nPartie A : tous les essais passent.")
