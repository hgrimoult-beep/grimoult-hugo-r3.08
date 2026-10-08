print("Jeu d'essai")


def ajouter_etudiant(d, nom, note):
    d[nom] = float(note)

etudiants = {}
ajouter_etudiant(etudiants, "Alice", 12)
ajouter_etudiant(etudiants, "Bob", 15)
ajouter_etudiant(etudiants, "Claire", 9.5)
print(etudiants)

def moyenne_classe(d):
    if not d:
        return 0
    total = sum(d.values())
    return total / len(d)

def meilleur_etudiant(d):
    if not d:
        return None
    meilleur = max(d, key=d.get)
    return meilleur, d[meilleur]

print("La moyenne de la classe est :", moyenne_classe(etudiants))
print("Le meilleur étudiant est :", meilleur_etudiant(etudiants))