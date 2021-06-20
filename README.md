# Unbeatable Rock Paper Scissors

## Auteur

- [Alexandre Jeunot-Caire](https://github.com/jeunotca)

## Visuel

<img src="./img/demo.gif" alt="Rendu de l'algorithme" style="margin: auto;"/>

## Description

Programme <b>personnel</b> développé en `Python` afin de découvrir la bibliothèque [Mediapipe](https://github.com/google/mediapipe).

L'idée est de créer un joueur "imbattable" au célèvre jeu "Pierre, Feuille, Ciseaux !". Le projet est initialement parti d'une petite plaisanterie, où j'ai fait croire à la création d'une intelligence artificielle très évoluée qui serait imbattable. Le programme cherche en réalité à identifier la forme de la main le plus vite possible pour trouver le coup battant celui du joueur. La rapidité du programme et de la bibliothèque Mediapipe permettent en effet de traiter en temps réel le mouvement des mains.

### Informations supplémentaires

La plupart des joueurs ayant tendance à former un poing derrière leur tête et à ne le déployer qu'au cours du mouvement, le programme utilise une `file` (deque) afin de comparer 3 mouvements. Lorsque les trois mouvements sont identiques, le programme décide en fonction de la position des doigts le mouvement effectué par l'utilisateur, puis trouve une parade. Il attendra toutefois d'en avoir 5 identiques avant de terminer le round, permettant d'éviter des erreurs en sa faveur. Ainsi, il est possible de gagner contre l'ordinateur dans de rares situations !

Lorsqu'un round est terminé, vous pouvez appuer sur la barre d'espace pour en commencer un nouveau.

Il est possible que l'ordinateur soit "bloqué" et joue sans montrer votre mouvement. Cela signifie qu'il n'est pas sûr de ce que vous avez fait. Par précaution et pour ne pas donner de points immérité, le round sera considéré comme nul et vous pourrez relancer un round avec `ESPACE`.

### Position des doigts

Le moment le plus important est celui-ci :

```python
            fingers_open = [res[4][1] < res[3][1], #true if thumb is open
                            res[8][2] < res[6][2], #true if index is open
                            res[12][2] < res[10][2], #true if middle finger is open
                            res[16][2] < res[14][2], #true if ring finger is open
                            res[20][2] < res[18][2] #true if little finger is open
                            ]
```

Ce code réside sur le schéma suivant :

<img src="./img/hand_landmarks.png" alt="Description d'une main" style="magin: auto;"/>

Analysons-le ensemble :
- tout d'abord, le pouce est un cas particulier, qui se ferme horizontalement. C'est la raison pour laquelle on cherche à comparer la composante horizontale du bout du pouce par rapport au milieu du doigt.
- Pour les autres doigts, on cherche à vérifier que le milieu du doigt est au-dessus de son extrémité.

### Déterminer le signe

Pour déterminer le signe, je procède de la sorte :
- Par défaut, on suppose que la `pierre` va être jouée
- Si l'annulaire ou l'auriculaire sont levés, le joueur a fait `feuille`
- S'ils sont fermés et que l'index et le majeur sont ouverts, le joueur a fait `ciseaux`

## Comment jouer ?

### Récupération des sources

* Depuis l'invité de commandes (HTTP):
```bash
$ git clone https://github.com/jeunotca/unbeatable-rock-paper-scissors.git
$ cd unbeatable-rock-paper-scissors
```

### Dépendances

Ce programme a été réalisé à l'aide de :
- [Mediapipe](https://github.com/google/mediapipe)

Vous pouvez installer les dépendances avec :
```bash
pip install -r requirements.txt
```

### Exécution

```bash
python main.py
```

Au cours du jeu, appuyez sur `ESPACE` pour lancer le round suivant. Appuyez sur `R` pour réinitialiser le score, et sur `Esc` pour quitter.