# -*- coding: utf-8 -*-

from tkinter import *


class Othello(Frame):
    """Fenêtre principale du programme"""

    def __init__(self):
        Frame.__init__(self)
        self.master.geometry('500x500')
        self.master.title('Othello')
        self.jeu = Plateau(self)
        self.jeu.pack(expand =YES, fill =BOTH)
        self.pack()

    def restart(self):
        """Fonction démarrant une nouvelle partie"""
        self.jeu.initJeu()
        self.jeu.dessinGrille()

    def undo(self):
        """Fonction permettant d'annuler le dernier coup joué"""
        if self.jeu.etat != self.jeu.coupPrec:
            for l in range(8):
                for c in range(8):
                    self.jeu.etat[l][c] = self.jeu.coupPrec[l][c]
            self.jeu.tourSuivant()
            self.jeu.dessinGrille()


class Plateau(Frame):
    """Classe définissant le plateau de jeu"""

    def __init__(self, boss =None):
        """Instanciation des principaux widgets"""
        self.boss = boss
        # Frame principale duquel dépendra les dimensions de la grille
        Frame.__init__(self)
        self.bind('<Configure>', self.redim)
        # Création d'un canvas qui contiendra la grille et le panneau
        self.can = Canvas(self, bg ='#582900', bd =0)
        # Création du canvas où sera dessiné la grille
        self.grille = Canvas(self.can, bg ='dark green', bd =0,
                             highlightthickness =0)
        # Les clics de souris ne seront détecté que sur la grille
        self.grille.bind('<Button-1>', self.clic)
        # Création du canvas qui contiendra le panneau
        self.pan = Canvas(self.can, bg ='dark green', bd =0,
                             highlightthickness =0)
        # Frame qui contiendra un bouton et deux labels
        self.fra = Frame(self.pan, bg='dark green')
        # Bouton undo / restart
        self.bou = Button(self.fra, width=8, bd=4, bg='#EFD809',
                          relief =GROOVE, activebackground ='#FFF036')
        self.bou.grid(row =0, column =1)
        # Variables utilisées pour compter les pions
        self.nbrB = IntVar()
        self.nbrN = IntVar()
        # Labels qui afficheront les scores
        self.lab =[0]*2
        for i in range(2):
            self.lab[i] = Label(self.fra, bg ='dark green', width =3,
                                fg =['white', 'black'][i],
                                textvariable =[self.nbrB, self.nbrN][i])
            self.lab[i].grid(row =0, column =2*i, sticky =[W, E][i])
        self.can.pack()
        self.initJeu()

    def initJeu(self):
        """Initialisation des paramètres d'une nouvelle partie"""
        # Création d'une liste de liste qui mémorisera l'état du jeu
        self.etat = []
        # Et d'une autre qui retiendra le dernier coup joué
        self.coupPrec =[]
        for i in range(8):
            self.etat.append([None]*8)
            self.coupPrec.append([None]*8)
        # Placement des 4 premiers pions
        self.etat[3][3] = self.etat[4][4] = self.tour = 0
        self.coupPrec[3][3] = self.coupPrec[4][4] = 0
        self.etat[3][4] = self.etat[4][3] = 1
        self.coupPrec[3][4] = self.coupPrec[4][3] = 1
        self.nbrB.set(2)
        self.nbrN.set(2)
        # Recherche des premiers coups possibles
        self.coupAutorise()
        # Configuration du bouton
        self.bou.configure(text ='Undo', command =self.boss.undo)

    def dessinPlateau(self):
        """Dessine entièrement le plateau de jeu"""
        # On efface tout
        self.can.delete(ALL)
        # On crée une fenêtre dans laquelle on place la grille
        self.dessinGrille()
        self.can.create_window(self.width/2, self.width/2, window =self.grille)
        # On crée une seconde fenêtre avec le panneau d'affichage
        self.dessinPanneau()
        self.can.create_window(self.width/2, self.cote *9.25, window =self.pan)
        # Rajout des lettres et numéros sur la bordure
        for n, let in enumerate("ABCDEFGH"):
            self.can.create_text((n +1) *self.cote, self.cote/4, text =let,
                                 fill ='white',
                                 font =('Helvetica', -int(self.cote/4)))
            self.can.create_text(self.cote/4, (n +1) *self.cote, text =n+1,
                                 fill ='white',
                                 font =('Helvetica', -int(self.cote/4)))

    def dessinGrille(self):
        """Dessine la grille avec ses pions"""
        # On efface l'ancienne grille
        self.grille.delete(ALL)
        # Tracé des lignes de la grille
        s = 0
        for n in range(9):
            self.grille.create_line(0, s, self.width, s)
            self.grille.create_line(s, 0, s, self.width)
            s += self.cote
        # Ajout des pions
        for l in range(8):
            for c in range(8):
                if self.etat[l][c] is None:
                    continue
                self.dessinPion(l, c, 0.1, ['white','black'][self.etat[l][c]],
                                self.grille)
        # On ajoute les marqueurs de coup autorisé
        self.dessinMarque()

    def dessinPanneau(self):
        # On efface l'ancien panneau
        self.pan.delete(ALL)
        # Reconfiguration de la taille de la frame
        for n in range(3):
            self.fra.columnconfigure(n, minsize =self.cote *2)
        for n in range(2):
            # Tracé de la bordure
            self.pan.create_line(0, n *self.cote, self.width, n*self.cote)
            self.pan.create_line(n *8*self.cote, 0, n *8*self.cote, self.cote)
            # Ajout des deux pions
            self.dessinPion(0, 7 *n, 0.15, ['white','black'][n], self.pan)
            # Ajustement de la taille du texte des labels
            self.lab[n].configure(font =('Helvetica', -int(self.cote /2)))
        # Ajustement de la taille du bouton
        self.bou.configure(font =('Helvetica', -int(self.cote /3)))
        # Rajout de la frame avec leslabels et le bouton
        self.pan.create_window(self.cote *4 +0.5, self.cote /2,
                               window =self.fra)

    def dessinPion(self, lig, col, marge, coul, can):
        """Dessine un pion sur la ligne 'lig' et la colone 'col' de la couleur
        'coul', marge détermine l'espace avec la bordure de la case"""
        # Calcul des coordonnées correspondantes
        x1 = (col +marge) *self.cote
        x2 = (col +1 -marge) *self.cote
        y1 = (lig +marge) *self.cote
        y2 = (lig +1 -marge) *self.cote
        # Ajout du pion
        can.create_oval(x1, y1, x2, y2, fill =coul, width =0)

    def dessinMarque(self):
        """Ajout de marqueurs sur les cases où les coups sont possibles"""
        for (l, c) in self.coup.keys():
            self.dessinPion(l, c, 0.45, 'red', self.grille)

    def redim(self, event):
        """Redéfinition de la taille des widgets"""
        # On récupère les nouvelles dimensions
        larg, haut = event.width, event.height
        # Calcul de la longueur d'une case
        self.cote = min(larg /9, haut /10)
        # Redimensionnement des widgets
        self.width, self.height = self.cote *9, self.cote *10
        self.can.configure(width =self.width, height =self.height)
        self.grille.configure(width =self.cote *8 +1, height =self.cote *8 +1)
        self.pan.configure(width =self.cote *8 +1, height =self.cote +1)
        # On redessine le plateau
        self.dessinPlateau()

    def clic(self, event):
        """Gestionnaire du clic gauche de la souris"""
        # On récupère les coordonnées de la case où le clic a eu lieu
        lig, col = int(event.y/self.cote), int(event.x/self.cote)
        # Si l'on clic sur une case où aucun coup est autorisé on ne fait rien
        if (lig, col) not in self.coup.keys():
            return
        # Mémorisation de l'ancienne grille
        for l in range(8):
            for c in range(8):
                self.coupPrec[l][c] = self.etat[l][c]
        # Sinon on modifie les pions qui doivent l'être
        for coup in self.coup[(lig, col)]:
            for (l, c) in coup:
                self.etat[l][c] = self.tour
        # On passe au tour suivant et redessine la grille
        self.tourSuivant()
        self.dessinGrille()

    def coupAutorise(self): # Essayer de mieux écrice cette partie
        """Fonction recherchant les coups autorisés"""
        # On crée un dictionnaire dans lequel on enregistre les cases où le
        # joueur peut jouer ainsi que la liste des pions impacté par le coup
        self.coup = {}
        # Parcours de la grille en cherchant les pions du joueur
        for n1 in range(64):
            lig, col = divmod(n1, 8)
            # S'il n'est pas de la même couleur on continue de chercher
            if self.etat[lig][col] != self.tour:
                continue
            # On cherche dans les 8 directions un coup possible
            for n2 in range(9):
                dx, dy = divmod(n2, 3)
                dx -= 1; dy -= 1
                # Liste des pions impacté par l'éventuel coup
                pions =[]
                for n in range (1, 8):
                    ligT = lig +n *dy
                    colT = col +n *dx
                    # Si l'on sort de la grille le coup est invalide
                    if ligT not in range(8) or colT not in range(8):
                        break
                    # Si le pion est de la  couleur opposée on l'ajoute
                    if self.etat[ligT][colT] == [1, 0][self.tour]:
                        pions.append((ligT, colT))
                        continue
                    # Si la case est vide et que l'on modifie des pions
                    # le coup est valide
                    if self.etat[ligT][colT] is None and pions:
                        pions.append((ligT, colT))
                        if (ligT, colT) not in self.coup.keys():
                            self.coup[(ligT, colT)] = [pions]
                        else:
                            self.coup[(ligT, colT)].append(pions)
                    # Si la case est vide ou de la même couleur on arrête
                    break

    def tourSuivant(self):
        """Passe la main au joueur suivant ou termine la partie"""
        # On compte de manière non intelligente les pions de chaque couleur
        b = n = 0
        for l in self.etat:
            for c in l:
                if c is None: continue
                if c:
                    n += 1
                else:
                    b += 1
        self.nbrB.set(b)
        self.nbrN.set(n)
        for n in range(2):
            # On passe au tour du joueur suivant
            self.tour = not self.tour
            # On recherche ses coups autorisés
            self.coupAutorise()
            # S'il en a on peut passer à son tour
            if self.coup:
                break
        else:
        # Si les tours des deux joueurs sont passés la partie est terminée
            print('Fin de la partie')
            self.bou.configure(text ='Restart', command =self.boss.restart)



if __name__ == '__main__':
   Othello().mainloop()