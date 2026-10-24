"""TP1 - Partie B : mini-jeu « Devine le nombre »."""
import random


def demander_entier(message):
    """Redemande tant que la saisie n'est pas un entier."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Merci d'entrer un nombre entier.")


def jouer(borne_min=1, borne_max=100, essais_max=10):
    """Une partie. Renvoie True si le joueur gagne."""
    secret = random.randint(borne_min, borne_max)
    print(f"J'ai choisi un nombre entre {borne_min} et {borne_max}. "
          f"Vous avez {essais_max} essais.")

    for essai in range(1, essais_max + 1):
        proposition = demander_entier(f"Essai {essai}/{essais_max} : ")
        if proposition < secret:
            print("Trop petit")
        elif proposition > secret:
            print("Trop grand")
        else:
            print(f"Gagné en {essai} essai(s) !")
            return True

    print(f"Perdu ! Le nombre était {secret}.")
    return False


def main():
    # Bonus : bornes personnalisables + rejouabilité
    while True:
        choix = input("Bornes personnalisées ? (o/n, défaut 1-100) : ").strip().lower()
        if choix == "o":
            bas = demander_entier("Borne min : ")
            haut = demander_entier("Borne max : ")
            if bas >= haut:
                print("La borne min doit être inférieure à la borne max.")
                continue
            jouer(bas, haut)
        else:
            jouer()
        if input("Rejouer ? (o/n) : ").strip().lower() != "o":
            break
    print("À bientôt !")


if __name__ == "__main__":
    main()
