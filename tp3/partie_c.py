"""TP3 - Partie C : persistance des données en CSV."""
import csv

from partie_a import Livre, Utilisateur
from partie_b import Bibliotheque

FICHIER_LIVRES = "livres.csv"
FICHIER_UTILISATEURS = "utilisateurs.csv"


def sauvegarder(bib, chemin_livres=FICHIER_LIVRES,
                chemin_utilisateurs=FICHIER_UTILISATEURS):
    """Écrit les livres (titre, auteur, année, disponible, emprunteur)
    et les utilisateurs dans deux fichiers CSV.
    Renvoie True si tout s'est bien passé."""
    try:
        with open(chemin_livres, "w", newline="", encoding="utf-8") as f:
            ecrivain = csv.writer(f)
            ecrivain.writerow(["titre", "auteur", "annee", "disponible", "emprunteur"])
            for livre in bib.livres.values():
                # emprunteur vaut None si le livre est disponible : on écrit ""
                ecrivain.writerow([livre.titre, livre.auteur, livre.annee,
                                   livre.disponible, livre.emprunteur or ""])

        # Les utilisateurs sont sauvegardés à part, pour garder aussi
        # ceux qui n'ont aucun emprunt
        with open(chemin_utilisateurs, "w", newline="", encoding="utf-8") as f:
            ecrivain = csv.writer(f)
            ecrivain.writerow(["nom"])
            for nom in bib.utilisateurs:
                ecrivain.writerow([nom])
        return True
    except OSError as erreur:
        print(f"Erreur pendant la sauvegarde : {erreur}")
        return False


def charger(bib, chemin_livres=FICHIER_LIVRES,
            chemin_utilisateurs=FICHIER_UTILISATEURS):
    """Remplit la bibliothèque 'bib' à partir des fichiers CSV.
    Renvoie False si le fichier des livres est absent (pas de plantage)."""
    # 1) Les utilisateurs (fichier facultatif)
    try:
        with open(chemin_utilisateurs, newline="", encoding="utf-8") as f:
            for ligne in csv.DictReader(f):
                nom = (ligne.get("nom") or "").strip()
                if nom:
                    bib.ajouter_utilisateur(Utilisateur(nom))
    except FileNotFoundError:
        pass   # pas de fichier : les utilisateurs seront déduits des emprunteurs
    except OSError as erreur:
        print(f"Erreur de lecture de {chemin_utilisateurs} : {erreur}")

    # 2) Les livres
    try:
        with open(chemin_livres, newline="", encoding="utf-8") as f:
            for ligne in csv.DictReader(f):
                _charger_ligne_livre(bib, ligne)
    except FileNotFoundError:
        return False
    except OSError as erreur:
        print(f"Erreur de lecture de {chemin_livres} : {erreur}")
        return False
    return True


def _charger_ligne_livre(bib, ligne):
    """Transforme une ligne du CSV en Livre et l'ajoute à la bibliothèque."""
    titre = (ligne.get("titre") or "").strip()
    auteur = (ligne.get("auteur") or "").strip()
    try:
        annee = int(ligne.get("annee") or "")
    except ValueError:
        print(f"Ligne ignorée (année invalide) : {dict(ligne)}")
        return
    if not titre:
        print(f"Ligne ignorée (titre vide) : {dict(ligne)}")
        return

    livre = Livre(titre, auteur, annee)
    if not bib.ajouter_livre(livre):
        return   # doublon : déjà signalé par ajouter_livre

    # On se fie à la colonne 'emprunteur' (la colonne 'disponible'
    # est redondante) : s'il y a un nom, le livre est emprunté.
    emprunteur = (ligne.get("emprunteur") or "").strip()
    if emprunteur:
        if emprunteur not in bib.utilisateurs:
            bib.ajouter_utilisateur(Utilisateur(emprunteur))
        livre.disponible = False
        livre.emprunteur = emprunteur
        bib.utilisateurs[emprunteur].emprunts.append(livre)


if __name__ == "__main__":
    # Jeu d'essai de l'énoncé : Ana emprunte « 1984 », sauvegarde, rechargement
    bib = Bibliotheque()
    bib.ajouter_livre(Livre("1984", "Orwell", 1949))
    bib.ajouter_utilisateur(Utilisateur("Ana"))
    bib.emprunter("Ana", "1984")
    sauvegarder(bib, "test_livres.csv", "test_utilisateurs.csv")

    nouvelle = Bibliotheque()
    charger(nouvelle, "test_livres.csv", "test_utilisateurs.csv")
    nouvelle.afficher_livres()          # « 1984 » emprunté par Ana
    nouvelle.rendre("Ana", "1984")      # Ana peut le rendre
    print("Fichier absent :", charger(Bibliotheque(), "absent.csv", "absent2.csv"))
