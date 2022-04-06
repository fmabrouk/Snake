from fltk import *
from time import sleep
from random import randint
#Pour compiler  python3 snake.py

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases
FRAMERATE = 17  # variable globale framerate
NB_OBSTACLES = 13  # variable globale nombre d'obstacles
obstacles_mode = False  # désactivée par defaut
fast_mode = False  # désactivée par defaut


def case_vers_pixel(case):
    """ Fonction recevevant les coordonnées d'une case du plateau sous
    la forme d'un couple d'entiers (ligne, colonne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):
    """ Fonction recevant une liste de couples d'entiers correspondant
    aux coordonnées des pommes et les affiches
    :param pommes: liste de couples
    """
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen')


def affiche_serpent(serpent):
    """ Fonction recevant une liste de couples d'entiers correspondant
    aux coordonnées du corps du serpent et les affiches
    :param serpent: liste de couples
    """
    for body in range(len(serpent)):
        x, y = case_vers_pixel(serpent[body])
        cercle(x, y, taille_case/2 + 1,
               couleur='darkgreen', remplissage='green')


def change_direction(direction, touche):
    """ Fonction recevant un couple d'entier correspondant à la
    à la direction actuelle du serpent et une chaine de caractères
    correspondant à la touche permettant une nouvelle direction
    :param direction: couple d'entiers
    :param touche: str
    :return value: couple d'entiers
    >>> change_direction((0, 1), 'Up')
    (0, 1)
    >>> change_direction((1, 0), 'Down')
    (0, -1)
    """
    if touche == 'Up' and direction != (0, 1):
        # flèche haut pressée
        return (0, -1)
    elif touche == 'Down' and direction != (0, -1):
        # flèche bas pressée
        return (0, 1)
    elif touche == 'Left' and direction != (1, 0):
        # flèche gauche pressée
        return (-1, 0)
    elif touche == 'Right' and direction != (-1, 0):
        # flèche droite pressée
        return (1, 0)
    else:
        # pas de changement !
        return direction


def deplacement_serpent(serpent, direction):
    """ Fonction recevant une liste de couples d'entiers correspondant
    aux coordonnées du serpent et la direction du serpent associée
    Cette fonction gere le deplacement du serpent en fonction des
    differentes situations dans le jeu
    :param serpent: liste de couples d'entiers
    :param direction: couple d'entiers
    :return value: bool
    """
    (hX, hY) = serpent[-1]  # tête du serpent
    X = hX + direction[0]  # var de la tête prochaine case (abscisse)
    Y = hY + direction[1]  # var de la tête prochaine case (ordonnée)
    if hX == -1 or hX == 40 or hY == -1 or hY == 30:  # Tete hors du terrain
        return False
    elif (X, Y) in pommes:  # Mange une pomme
        pommes.remove((X, Y))
    elif (X, Y) in serpent and len(serpent) != 1:  # Tete dans le corps
        return False
    elif len(serpent) == (taille_case * largeur_plateau +
                          taille_case * hauteur_plateau) - len(obstacles):
        efface_tout()
        texte(300, 200, "You win ! GG", couleur="darkblue", ancrage="center")
        attend_ev()
        # Longueur du serpent maximale atteinte, message de félicitation et fin
        return False
    elif (X, Y) in obstacles:
        return False
    else:
        serpent.pop(0)  # on retire la queue
    serpent.append((X, Y))  # on recrée la tête a chaque fois
    return True


def creer_pomme():
    """ Fonction qui crée les pommes du jeu, les pommes n'apparaissent
    que sur des cases inocuppées
    """
    while True:
        case_pomme = (randint(0, 39), randint(0, 29))
        if case_pomme not in serpent and case_pomme not in pommes and \
           case_pomme not in obstacles:
            pommes.append(case_pomme)
            break


def creer_obstacles():
    """ Fonction qui crée des obstacles, les obstacles sont crées dès
    le début du jeu, si la tête du serpent rentre dans une des cases
    de obstacles, le jeu s'arrête. Le nombre d'obstacles est géré
    par la variable globale NB_OBSTACLES
    """
    nb = 0
    while nb < NB_OBSTACLES:  # NB_OBSTACLES est une var globale
        obstacle = (randint(0, 39), randint(0, 29))
        if obstacle not in serpent and obstacle not in obstacles:
            obstacles.append(obstacle)
        nb += 1


def affiche_obstacles(obstacles):
    """ Fonction recevant une liste de couples d'entiers correspondant
    aux coordonnées des obstacles et les affiches
    :param pommes: liste de couples d'entiers
    """
    for obstacle in obstacles:
        x, y = case_vers_pixel(obstacle)
        cercle(x, y, taille_case/2,
               couleur='black', remplissage='chartreuse2')


def display_welcome():
    """ Fonction d'affichage avant le demarrage du jeu. Elle permet
    de laisser un temps de préparation pour le joueur
    """
    texte(235, 150, "Press", couleur="goldenrod")
    texte(250, 180, "Any", couleur="goldenrod")
    texte(250, 210, "Key", couleur="goldenrod")
    attend_ev()


# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    framerate = FRAMERATE   # taux de rafraîchissement du jeu en images/s
    direction = (0, 0)  # direction initiale du serpent
    pommes = []  # liste des coordonnées des cases contenant des pommes
    serpent = [(0, 0)]  # liste des coordonnées de cases adjacentes décrivant le serpent
    obstacles = []  # liste des coordonnées des cases contenant des obstacles
    cree_fenetre(taille_case * largeur_plateau,
                 taille_case * hauteur_plateau)
    compteur = 0  # majoration du framerate dans le fast_mode
    temps = 0  # var temps pour le fast_mode (framerate augmente avec le temps)
    freq_pomme = 0  # var de creation des pommes

    # menu
    while True:
        while True:
            rectangle(200, 85, 400, 155, remplissage="lime green")
            rectangle(200, 255, 400, 325, remplissage="light slate blue")
            texte(265, 100, "Play")
            texte(255, 270, "Modes")
            (a, b) = attend_clic_gauche()
            # on passe au jeu directement
            if a >= 200 and a <= 400 and b >= 85 and b <= 155:
                efface_tout()
                break
            elif a >= 200 and a <= 400 and b >= 255 and b <= 325:
                efface_tout()
            # configuration des modes
                while True:
                    if obstacles_mode is True:
                        rectangle(150, 40, 450, 110,
                                  remplissage="green", tag="a")
                        # mode activé == rectangle colorié
                    else:
                        rectangle(150, 40, 450, 110)
                        efface("a")
                    if fast_mode is True:
                        rectangle(150, 190, 450, 260,
                                  remplissage="green", tag="b")
                        # mode activé == rectangle colorié
                    else:
                        rectangle(150, 190, 450, 260)
                        efface("b")
                    rectangle(150, 340, 450, 410,
                              remplissage="light slate blue")
                    texte(190, 55, "obstacles mode")
                    texte(230, 205, "fast mode")
                    texte(205, 355, "back to menu")
                    (c, d) = attend_clic_gauche()
                    if c >= 200 and c <= 400 and d >= 40 and d <= 110:
                        obstacles_mode = not obstacles_mode
                        # bascule
                    if c >= 200 and c <= 400 and d >= 190 and d <= 260:
                        fast_mode = not fast_mode
                        # bascule
                    if c >= 200 and c <= 400 and d >= 340 and d <= 410:
                        efface_tout()
                        break
    # fin menu

        # debut du jeu, boule principale
        display_welcome()
        if obstacles_mode is True:
            creer_obstacles()
        jouer = True
        while jouer:
            if fast_mode is True:
                if compteur <= 35 and temps == 20:
                    framerate += .5
                    compteur += 1
                    temps = 0
            efface_tout()

            # affichage des objets
            if obstacles_mode is True:
                affiche_obstacles(obstacles)
            texte(570, 30, "Score : " + str(len(serpent)-1), ancrage="ne",
                  taille=15, couleur="deep sky blue")
            affiche_pommes(pommes)
            affiche_serpent(serpent)
            mise_a_jour()

            # gestion des événements
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                jouer = False
            elif ty == 'Touche':
                direction = change_direction(direction, touche(ev))
            if deplacement_serpent(serpent, direction) is False:
                jouer = False
            if freq_pomme == 15:
                creer_pomme()
                freq_pomme = 0
            freq_pomme += 1
            temps += .5

            # attente avant rafraîchissement
            sleep(1/framerate)

            # le joueur perd
            if jouer is False:

                # menu game over
                efface_tout()
                texte(300, 140, "Your score : " + str(len(serpent)-1),
                      ancrage="center", couleur="lime green")
                rectangle(50, 270, 250, 330, remplissage="SeaGreen2")
                rectangle(350, 270, 550, 330, remplissage="SeaGreen2")
                rectangle(200, 350, 400, 410, remplissage="sienna1")
                texte(78, 280, "new game", couleur="dodger blue")
                texte(410, 280, "menu", couleur="dodger blue")
                texte(270, 360, "quit", couleur="red2")
                (a, b) = attend_clic_gauche()
                while True:

                    # recommence une partie
                    if a >= 50 and a <= 250 and b >= 270 and b <= 330:
                        jouer = True
                        efface_tout()
                        framerate = FRAMERATE
                        obstacles = []
                        direction = (0, 0)
                        pommes = []
                        serpent = [(0, 0)]
                        freq_pomme = 0
                        display_welcome()
                        temps = 0
                        compteur = 0
                        if obstacles_mode is True:
                            creer_obstacles()
                        break

                    # retour vers le menu
                    elif a >= 350 and a <= 550 and b >= 270 and b <= 330:
                        framerate = FRAMERATE
                        direction = (0, 0)
                        pommes = []
                        serpent = [(0, 0)]
                        freq_pomme = 0
                        obstacles = []
                        efface_tout()
                        temps = 0
                        compteur = 0
                        break

                    # fermeture du jeu
                    elif a >= 200 and a <= 400 and b >= 350 and b <= 410:
                        exit()
                    else:
                        (a, b) = attend_clic_gauche()
