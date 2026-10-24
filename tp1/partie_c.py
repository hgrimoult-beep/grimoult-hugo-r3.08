"""TP1 - Partie C : manipulation des mots."""
import random

MOTS_PAR_DEFAUT = ["python", "ordinateur", "reseau", "serveur", "pendu",
                   "algorithme", "variable", "fonction", "éléphant"]


def charger_mots(chemin="mots.txt"):
    """Charge un mot par ligne ; repli sur la liste par défaut si le fichier est absent/vide."""
    try:
        with open(chemin, encoding="utf-8") as f:
            mots = [ligne.strip() for ligne in f if ligne.strip()]
        return mots or list(MOTS_PAR_DEFAUT)
    except OSError:
        return list(MOTS_PAR_DEFAUT)


def choisir_mot(liste):
    """Renvoie un mot aléatoire en MAJUSCULES."""
    return random.choice(liste).strip().upper()


def masque(mot):
    """Liste de '_' de même longueur que le mot."""
    return ["_"] * len(mot)


if __name__ == "__main__":
    print(masque("PYTHON"))  # ['_', '_', '_', '_', '_', '_']
    print(choisir_mot(charger_mots()))
