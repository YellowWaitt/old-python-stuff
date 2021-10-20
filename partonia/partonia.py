# -*- coding: utf-8 -*-

class  Partonia ():
    """Classe en charge de définir toute les règles et mécanismes du jeu"""

    def __init__ (self):
        # La meilleure initialisation jamais vue
        pass

    def initialiser_partie (self):
        """Création de la grille de jeu avec les pions à leur position de
        départ"""
        # Le plateau est représenté sous forme de liste de liste
        self.grille = [[2]*10 for loop in range(10)] # 2 pour case vide
        self.grille[1] = [0] *10   # 0 pour les jaunes
        self.grille[6] = [0] *10
        self.grille[3] = [1] *10   # 1 pour les noirs
        self.grille[8] = [1] *10
        self.nombre_pion = [20, 20]
        self.tour = 0  # Le joueur jaune commence
        self.adversaire = 1 # Le joueur noir est l'opposant du joueur jaune
        self.pile_modif =[] # Pour mémoriser les coups joués et les annuler

    def tour_de_jeu (self, case_dep, case_arr):
        """Déroulement d'un tour de jeu"""
        self.deplacer_pion(case_dep, case_arr)
        self.capturer_pion(case_arr)
        self.changer_tour()

    def dejoue (self):
        """Annule le dernier coup joué"""
        # Rajout des pions supprimés
        nbr_capture = self.pile_modif.pop(-1)
        self.nombre_pion[self.tour] += nbr_capture
        for loop in range(nbr_capture):
            lig, col = self.pile_modif.pop(-1)
            self.grille[lig][col] = self.tour
        # Annulation du mouvement
        self.changer_tour()
        lig, col = self.pile_modif.pop(-1)
        self.grille[lig][col] = 2
        lig, col = self.pile_modif.pop(-1)
        self.grille[lig][col] = self.tour

    def deplacer_pion (self, case_dep, case_arr):
        """Déplace le pion en case_dep vers case_arr"""
        self.grille[case_dep[0]][case_dep[1]] = 2
        self.grille[case_arr[0]][case_arr[1]] = self.tour
        # Mémorisation du coup
        self.pile_modif.append(case_dep)
        self.pile_modif.append(case_arr)

    def capturer_pion (self, case):
        """Captures les éventuels pions qui peuvent l'être par le pion sur
        la case 'case'"""
        lig, col = case
        nbr_capture = 0
        for dl, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            if self.pion_est_capture(lig, col, dl, dc):
                # Supprime le pion
                self.grille[lig + dl][col + dc] = 2
                # Décremente le compteur de pion
                self.nombre_pion[self.adversaire] -= 1
                # Garde une trace des captures
                self.pile_modif.append([lig +dl, col +dc])
                nbr_capture += 1
        self.pile_modif.append(nbr_capture)

    def coup_legaux (self): # Pour l'IA
        """Renvoie la liste des coups legaux du joueur dont c'est le tour"""
        liste_coup = []
        for lig in range(10):
            for col in range(10):
                if self.grille[lig][col] == self.tour:
                    for dl, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                        if self.coup_est_valide((lig, col),
                                                (lig +dl, col +dc)):
                            liste_coup.append(Coup((lig, col),
                                              (lig +dl, col +dc),
                                              self.tour))
        return liste_coup

    def coup_quiescence (self): # Pour l'IA
        """Renvoie la liste des coups qui capture un pion"""
        liste_coup = self.coup_legaux()
        liste_coup_quiescence = []
        for coup in liste_coup:
            for dl, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                if self.pion_est_capture(coup.case_dep[0], coup.case_dep[1],
                                         dl, dc):
                    liste_coup_quiescence.append(coup)
        return liste_coup_quiescence

    def evaluation (self): # Pour l'IA
        """Donne une évaluation du plateau, attribue 4 points pour chacun de
        ses pions en vie et 2 points par pion adverse menacé, retranche
        l'équivalent de l'adversaire"""
        nbr_ami_menace = nbr_ennemi_menace = 0
        for lig in range(10):
            for col in range(10):
                if self.grille[lig][col] == self.tour:
                    nbr_ami_menace += self.pion_peut_etre_capture(lig, col)
                elif self.grille[lig][col] != 2:
                    nbr_ennemi_menace += self.pion_peut_etre_capture(lig, col)
        return (4 * (self.nombre_pion[self.tour] -
                    self.nombre_pion[self.adversaire]) +
                2 * (nbr_ennemi_menace -nbr_ami_menace))

    def pion_peut_etre_capture (self, lig, col): # Pour l'IA
        """Vérifie si le pion sur la case d'indice lig et d'indice col peut
        être capturé en un coup"""
        adversaire = (self.grille[lig][col] +1)%2
        # On commence par vérifier si le pion est aligné  avec une case vide et
        # d'un pion ennemi
        for dl, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            if self.case_dans_grille([lig +dl, col +dc]) and \
            self.grille[lig +dl][col +dc] == 2 and \
            (not self.case_dans_grille([lig -dl, col -dc])or \
            self.grille[lig -dl][col -dc] == adversaire):
                # On vérifie que la case vide et à côté d'un pion ennemi
                for dlt, dct in [(1,0), (-1,0), (0,1), (0,-1)]:
                    if self.case_dans_grille([lig +dl +dlt, col +dc +dct]) and\
                    self.grille[lig +dl +dlt][col +dc +dct] == adversaire:
                        return True
        return False

    def pion_est_capture (self, lig, col, dl, dc):
        """Vérifie si le pion sur la case de coordonnées lig +dl et col +dc a
        capturé un pion adverse"""
        # Si le pion en (lig +dl, col +dc) est de couleur opposé et qu'il
        # est entouré de deux pions ennemis ou contre un mur
        return self.case_dans_grille((lig +dl, col +dc)) and \
        self.grille[lig +dl][col +dc] == self.adversaire and (\
        not(self.case_dans_grille((lig + 2*dl, col + 2*dc))) or \
        self.grille[lig + 2*dl][col + 2*dc] == self.tour)

    def coup_est_valide (self, case_dep, case_arr):
        """Renvoie True si le pion sur la case case_dep peut se déplacer
        sur la case case_arr, renvoie False sinon"""
        return self.case_dans_grille(case_dep) and \
        self.case_dans_grille(case_arr) and \
        self.grille[case_dep[0]][case_dep[1]] == self.tour and \
        self.grille[case_arr[0]][case_arr[1]] == 2 and \
        self.case_adjacente(case_dep, case_arr)

#    def coup_possible (self, case_dep, case_arr):
#        """Si case_dep contient un pion du joueur dont c'est le tour et
#        case_arr est vide renvoie True, renvoie False sinon"""
#        return self.grille[case_dep[0]][case_dep[1]] == self.tour and \
#        self.grille[case_arr[0]][case_arr[1]] == 2

    def case_adjacente (self, case_dep, case_arr):
        """Vérifie que case_dep et case_arr sont adjacentes"""
        lig_dep, col_dep = case_dep
        lig_arr, col_arr = case_arr
        for dl, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            if lig_dep + dl == lig_arr and col_dep + dc == col_arr:
                return True
        return False

    def case_dans_grille (self, case):
        """Si les coordonnées de case sont dans la grille renvoie True,
        renvoie False sinon"""
        return 0 <= case[0] <= 9 and 0 <= case[1] <= 9

    def changer_tour (self):
        """Passe au tour du joueur suivant"""
        self.tour, self.adversaire = self.adversaire, self.tour


class Coup ():
    """Classe utilisée uniquement par l'IA"""

    def __init__ (self, case_dep, case_arr, couleur):
        self.case_dep = case_dep
        self.case_arr = case_arr
        self.couleur = couleur

    def nombre (self):
        """Fonction renvoyant un numéro unique à chacun des coups possibles.
        On utilise 1 bit pour la couleur du pion, 2 bits pour la direction du
        déplacement et 7 bits pour la case de départ"""
        direc = (self.case_arr[0] -self.case_dep[0],
                 self.case_arr[1] -self.case_dep[1])
        return ((((self.couleur << 2 ) +
                 [(1,0), (-1,0), (0,1), (0,-1)].index(direc)) << 7) +
                 self.case_dep[0] *10 + self.case_dep[1])