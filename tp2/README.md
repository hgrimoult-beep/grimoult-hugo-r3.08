# 🎮 TP2 — Morpion en POO (R3.08)

> Un Morpion en Python, cinq fichiers, zéro dépendance externe.
> Chaque partie de l'énoncé a son fichier, commenté et lançable tout seul.

## ⚡ Démarrage express

Depuis la racine du monorepo :

```bash
python3 tp2/partie_a.py      # la grille et son jeu d'essai
python3 tp2/partie_c.py      # une partie contre l'IA
python3 tp2/essais.py        # tout vérifier (8/8)
```

C'est tout. Le reste, c'est du bonus.

## 🗂️ Le dossier

| Fichier | Ce qu'on y trouve | Démo |
| --- | --- | --- |
| `partie_a.py` | La classe `Grille` | `python3 tp2/partie_a.py` |
| `partie_b.py` | Les joueurs (`Humain`, `IA`) | `python3 tp2/partie_b.py` |
| `partie_c.py` | Le jeu complet et les scores | `python3 tp2/partie_c.py` |
| `partie_bonus.py` | L'IA qui bloque + le championnat | `python3 tp2/partie_bonus.py` |
| `essais.py` | Les jeux d'essai de l'énoncé | `python3 tp2/essais.py` |

B pioche dans A, C dans A + B, le bonus dans tout le monde : on lit dans
l'ordre **A → B → C → bonus**, et chaque fichier se termine par une petite
démo.

## 🕹️ Jouer

```bash
python3 tp2/partie_c.py                 # vous (X) contre l'IA (O)
python3 tp2/partie_c.py --mode hh       # deux humains
python3 tp2/partie_bonus.py --jouer     # vous contre l'IA maligne
```

Les coordonnées, c'est `x` = ligne et `y` = colonne, avec `(0, 0)` en haut à
gauche :

```text
(0,0)  (0,1)  (0,2)
(1,0)  (1,1)  (1,2)
(2,0)  (2,1)  (2,2)
```

On tape par exemple `1 1` pour jouer au centre. `--help` liste les options
(`--parties`, `--graine`, `--muet`).

## 🤖 L'IA maligne, en trois idées

1. Si un coup la fait gagner, elle le joue.
2. Sinon, elle occupe la case qui ferait gagner l'adversaire.
3. Sinon, elle joue au hasard.

Résultat d'un petit championnat maison sur 200 parties : **155 victoires**,
34 nuls, 11 défaites. Pas mal pour trois règles.

## ✅ Et si je casse tout ?

- Coup sur une case occupée, `x = 3`, `x = -1`, saisie farfelue : message,
  on redemande, **aucun plantage**.
- 20 parties IA contre IA : toujours une victoire ou un nul.
- `python3 tp2/essais.py` vérifie les 8 jeux d'essai de l'énoncé.

```text
8/8 essais réussis.
```

## 🧠 Les petits plus du code

- La grille est une liste **par ligne** : le piège `[[VIDE] * 3] * 3` est évité.
- La victoire est testée **avant** la grille pleine : le dernier coup qui
  aligne trois symboles est bien une victoire.
- L'IA simule ses coups sur une **copie** de la grille, jamais sur la vraie.
- Le tout tourne avec Python 3.10+ et la bibliothèque standard uniquement.

## 📦 Rendu

Un commit par partie (`TP2 partie A`, `TP2 partie B`, `TP2 partie C`,
`TP2 bonus`), et le dossier `tp2/` à côté de `tp1/` et `tp3/` dans le
monorepo.
