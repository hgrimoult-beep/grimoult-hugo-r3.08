"""TP3 - Partie B : gestionnaire de bibliothèque."""
from partie_a import Livre, Utilisateur


class Bibliotheque:
    """Regroupe les livres et les utilisateurs.
    Chaque méthode renvoie True si l'action a réussi, False sinon
    (avec un message), sans jamais planter."""

    def __init__(self):
        self.livres = {}         # titre -> Livre
        self.utilisateurs = {}   # nom -> Utilisateur

    def ajouter_livre(self, livre):
        """Ajoute un livre (le titre sert de clé, il doit être unique)."""
        if livre.titre in self.livres:
            print(f"Le livre « {livre.titre} » existe déjà.")
            return False
        self.livres[livre.titre] = livre
        return True

    def ajouter_utilisateur(self, utilisateur):
        """Ajoute un utilisateur (le nom sert de clé, il doit être unique)."""
        if utilisateur.nom in self.utilisateurs:
            print(f"L'utilisateur « {utilisateur.nom} » existe déjà.")
            return False
        self.utilisateurs[utilisateur.nom] = utilisateur
        return True

    def emprunter(self, nom, titre):
        """L'utilisateur 'nom' emprunte le livre 'titre'."""
        utilisateur = self.utilisateurs.get(nom)
        livre = self.livres.get(titre)

        # Cas d'échec : on explique pourquoi et on s'arrête
        if utilisateur is None:
            print(f"Utilisateur inconnu : {nom}")
            return False
        if livre is None:
            print(f"Livre inconnu : {titre}")
            return False
        if not livre.disponible:
            print(f"« {titre} » est déjà emprunté par {livre.emprunteur}.")
            return False

        utilisateur.emprunter_livre(livre)
        print(f"{nom} a emprunté « {titre} ».")
        return True

    def rendre(self, nom, titre):
        """L'utilisateur 'nom' rend le livre 'titre'."""
        utilisateur = self.utilisateurs.get(nom)
        livre = self.livres.get(titre)

        if utilisateur is None:
            print(f"Utilisateur inconnu : {nom}")
            return False
        if livre is None:
            print(f"Livre inconnu : {titre}")
            return False
        if livre.disponible:
            print(f"« {titre} » n'est pas emprunté.")
            return False
        # Seul l'emprunteur peut rendre le livre
        if livre.emprunteur != nom:
            print(f"« {titre} » est emprunté par {livre.emprunteur}, pas par {nom}.")
            return False

        utilisateur.rendre_livre(livre)
        print(f"{nom} a rendu « {titre} ».")
        return True

    def afficher_livres(self):
        """Affiche les livres en deux groupes : disponibles puis empruntés."""
        disponibles = [l for l in self.livres.values() if l.disponible]
        empruntes = [l for l in self.livres.values() if not l.disponible]

        print("--- Livres disponibles ---")
        for livre in disponibles:
            livre.afficher()
        if not disponibles:
            print("(aucun)")

        print("--- Livres empruntés ---")
        for livre in empruntes:
            livre.afficher()
        if not empruntes:
            print("(aucun)")


if __name__ == "__main__":
    bib = Bibliotheque()
    bib.ajouter_livre(Livre("1984", "Orwell", 1949))
    bib.ajouter_livre(Livre("Dune", "Herbert", 1965))
    bib.ajouter_utilisateur(Utilisateur("Ana"))
    bib.ajouter_utilisateur(Utilisateur("Léo"))

    bib.emprunter("Ana", "1984")       # réussi
    bib.emprunter("Léo", "1984")       # échec : déjà emprunté
    bib.emprunter("Zoé", "Dune")       # échec : utilisateur inconnu
    bib.emprunter("Ana", "Inconnu")    # échec : livre inconnu
    bib.rendre("Léo", "1984")          # échec : rendu par un autre
    bib.afficher_livres()
    bib.rendre("Ana", "1984")          # réussi
    bib.afficher_livres()
