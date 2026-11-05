"""TP3 - Partie D : programme principal (menu texte interactif)."""
import os

from partie_a import Livre, Utilisateur
from partie_b import Bibliotheque
from partie_c import charger, sauvegarder

# Les fichiers de sauvegarde sont placés à côté du programme,
# pour retrouver le même état quel que soit le dossier de lancement.
DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_LIVRES = os.path.join(DOSSIER, "livres.csv")
FICHIER_UTILISATEURS = os.path.join(DOSSIER, "utilisateurs.csv")


def afficher_menu():
    print("\n===== Bibliothèque =====")
    print("1. Ajouter un livre")
    print("2. Ajouter un utilisateur")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Afficher les livres")
    print("6. Quitter et sauvegarder")


def demander_texte(message):
    """Demande un texte et le renvoie sans espaces autour (peut être vide)."""
    return input(message).strip()


def ajouter_livre(bib):
    """Option 1 : saisie et ajout d'un livre."""
    titre = demander_texte("Titre : ")
    auteur = demander_texte("Auteur : ")
    annee_texte = demander_texte("Année : ")

    if not titre or not auteur:
        print("Le titre et l'auteur ne peuvent pas être vides.")
        return
    # L'année doit être un nombre entier
    try:
        annee = int(annee_texte)
    except ValueError:
        print("L'année doit être un nombre entier.")
        return

    if bib.ajouter_livre(Livre(titre, auteur, annee)):
        print(f"Livre « {titre} » ajouté.")


def ajouter_utilisateur(bib):
    """Option 2 : saisie et ajout d'un utilisateur."""
    nom = demander_texte("Nom : ")
    if not nom:
        print("Le nom ne peut pas être vide.")
        return
    if bib.ajouter_utilisateur(Utilisateur(nom)):
        print(f"Utilisateur « {nom} » ajouté.")


def emprunter(bib):
    """Option 3 : un utilisateur emprunte un livre."""
    nom = demander_texte("Nom de l'utilisateur : ")
    titre = demander_texte("Titre du livre : ")
    bib.emprunter(nom, titre)   # la méthode affiche elle-même le résultat


def rendre(bib):
    """Option 4 : un utilisateur rend un livre."""
    nom = demander_texte("Nom de l'utilisateur : ")
    titre = demander_texte("Titre du livre : ")
    bib.rendre(nom, titre)


def main():
    bib = Bibliotheque()

    # Au lancement : on recharge l'état précédent s'il existe
    if charger(bib, FICHIER_LIVRES, FICHIER_UTILISATEURS):
        print("Sauvegarde chargée.")
    else:
        print("Aucune sauvegarde trouvée : on démarre avec une bibliothèque vide.")

    while True:
        afficher_menu()
        choix = demander_texte("Votre choix : ")

        if choix == "1":
            ajouter_livre(bib)
        elif choix == "2":
            ajouter_utilisateur(bib)
        elif choix == "3":
            emprunter(bib)
        elif choix == "4":
            rendre(bib)
        elif choix == "5":
            bib.afficher_livres()
        elif choix == "6":
            if sauvegarder(bib, FICHIER_LIVRES, FICHIER_UTILISATEURS):
                print("Données sauvegardées. À bientôt !")
            break
        else:
            print("Choix invalide, entrez un nombre de 1 à 6.")


if __name__ == "__main__":
    main()
