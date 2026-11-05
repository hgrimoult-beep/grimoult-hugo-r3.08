"""TP3 - Partie A : classes de base (Livre et Utilisateur)."""


class Livre:
    """Un livre de la bibliothèque."""

    def __init__(self, titre, auteur, annee):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.disponible = True   # True tant que personne ne l'a emprunté
        self.emprunteur = None   # nom de l'emprunteur actuel (None si disponible)

    def afficher(self):
        """Affiche le livre sur une ligne, avec son état."""
        if self.disponible:
            etat = "disponible"
        else:
            etat = f"emprunté par {self.emprunteur}"
        print(f"{self.titre} - {self.auteur} ({self.annee}) [{etat}]")

    def emprunter(self, nom):
        """Marque le livre comme emprunté par 'nom'.
        Renvoie False si le livre est déjà emprunté."""
        if not self.disponible:
            return False
        self.disponible = False
        self.emprunteur = nom
        return True

    def rendre(self):
        """Remet le livre à disposition.
        Renvoie False si le livre n'était pas emprunté."""
        if self.disponible:
            return False
        self.disponible = True
        self.emprunteur = None
        return True


class Utilisateur:
    """Un utilisateur de la bibliothèque, avec la liste de ses emprunts."""

    def __init__(self, nom):
        self.nom = nom
        self.emprunts = []   # liste d'objets Livre

    def emprunter_livre(self, livre):
        """Emprunte un livre. Renvoie True si l'emprunt a réussi."""
        # Le livre lui-même vérifie s'il est libre
        if not livre.emprunter(self.nom):
            return False
        self.emprunts.append(livre)
        return True

    def rendre_livre(self, livre):
        """Rend un livre. Renvoie False si l'utilisateur ne l'a pas emprunté."""
        if livre not in self.emprunts:
            return False
        livre.rendre()
        self.emprunts.remove(livre)
        return True

    def afficher_emprunts(self):
        """Affiche les livres actuellement empruntés."""
        if not self.emprunts:
            print(f"{self.nom} n'a aucun emprunt.")
            return
        print(f"Emprunts de {self.nom} :")
        for livre in self.emprunts:
            print("  -", end=" ")
            livre.afficher()


if __name__ == "__main__":
    # Jeu d'essai de l'énoncé
    l = Livre("1984", "Orwell", 1949)
    print(l.emprunter("Ana"))   # True
    print(l.emprunter("Léo"))   # False (déjà emprunté)
    print(l.rendre())           # True
    print(l.rendre())           # False (n'était plus emprunté)

    ana = Utilisateur("Ana")
    print(ana.emprunter_livre(l))   # True
    ana.afficher_emprunts()
    print(ana.rendre_livre(l))      # True
    ana.afficher_emprunts()
