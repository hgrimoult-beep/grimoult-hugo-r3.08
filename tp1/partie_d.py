"""TP1 - Partie D : jeu du Pendu (+ bonus ASCII art et mode 2 joueurs)."""
import unicodedata
from getpass import getpass

from partie_c import charger_mots, choisir_mot, masque

MAX_ERREURS = 7

# Bonus : ASCII art, un dessin par nombre d'erreurs (0 à 7)
PENDU = [
    "\n\n\n\n\n\n=========",
    "\n      |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n      |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
]


def sans_accent(texte):
    """'éléphant' -> 'ELEPHANT' (pour comparer sans tenir compte des accents/casse)."""
    decompose = unicodedata.normalize("NFD", texte)
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn").upper()


def jouer_pendu(mot):
    """Une partie. Renvoie True si le joueur gagne."""
    mot = mot.strip().upper()
    reference = [sans_accent(c) for c in mot]     # version sans accent, pour comparer
    cache = masque(mot)
    for i, c in enumerate(mot):                   # révèle d'emblée espaces, tirets...
        if not c.isalpha():
            cache[i] = c

    erreurs = 0
    proposees = []

    while "_" in cache and erreurs < MAX_ERREURS:
        print(PENDU[erreurs])
        print("Mot      :", " ".join(cache))
        print(f"Erreurs  : {erreurs}/{MAX_ERREURS}")
        print("Proposées:", " ".join(proposees) if proposees else "-")

        saisie = sans_accent(input("Une lettre : ").strip())
        if len(saisie) != 1 or not saisie.isalpha():
            print("Entrez UNE lettre.")
            continue
        if saisie in proposees:
            print("Lettre déjà proposée, pas d'erreur en plus.")
            continue

        proposees.append(saisie)
        if saisie in reference:
            for i, c in enumerate(reference):
                if c == saisie:
                    cache[i] = mot[i]             # on révèle la lettre d'origine (accentuée)
        else:
            erreurs += 1
            print("Absente !")

    if "_" not in cache:
        print("Mot      :", " ".join(cache))
        print("Gagné !")
        return True

    print(PENDU[MAX_ERREURS])
    print(f"Perdu, le mot était {mot}")
    return False


def mot_deux_joueurs():
    """Bonus : un joueur saisit le mot (masqué à l'écran) pour l'autre."""
    while True:
        mot = getpass("Mot secret (invisible) : ").strip()
        if mot and all(c.isalpha() or c in " -'" for c in mot):
            print("\n" * 40)  # on repousse l'écran au cas où la saisie serait visible
            return mot.upper()
        print("Mot invalide (lettres uniquement).")


if __name__ == "__main__":
    mode = input("1 ou 2 joueurs ? (1/2) : ").strip()
    mot = mot_deux_joueurs() if mode == "2" else choisir_mot(charger_mots())
    jouer_pendu(mot)
