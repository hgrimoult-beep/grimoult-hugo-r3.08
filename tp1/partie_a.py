print("Jeu d'essai") #Le nom du jeu


def ajouter_etudiant(d, nom, note): 
    d[nom] = float(note)                    #On définit la fonction etudiant

etudiants = {}
ajouter_etudiant(etudiants, "Alice", 12)
ajouter_etudiant(etudiants, "Bob", 15)
ajouter_etudiant(etudiants, "Claire", 9.5)
print(etudiants)                            #On ajoute les étudiants et on affiche leurs noms

def moyenne_classe(d):      #Définition de la fonction pour la moyenne
    if not d:
        return 0            #Si le dictionnaire est vide, retourne rien
    total = sum(d.values()) #On additionne les valeurs de d
    return total / len(d)   #Il retourne l'addition précédente divisé par le nombre d'étudiant

def meilleur_etudiant(d):   #Définition de la fonction pour le meilleur étudiant
    if not d:
        return None         #Si le dictionnaire est vide, il ne retourne rien
    meilleur = max(d, key=d.get)    #Dans meilleur, il choisi le max dans un dictionnaire en regardant la value de chaque utilisateur
    return meilleur, d[meilleur]    #Il retourne le nom et avec d.get, il retourne aussi la note

print("La moyenne de la classe est :", moyenne_classe(etudiants)) #affiche la moyenne
print("Le meilleur étudiant est :", meilleur_etudiant(etudiants)) #affiche le meilleur etudiant