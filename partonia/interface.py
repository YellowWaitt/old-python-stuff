# -*- coding: utf-8 -*-

from plateau import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

class MenuBarre (Frame):
    """Barre de menus deroulants"""

    def __init__ (self, boss =None):
        """Ajout de tout les menus"""
        Frame.__init__(self, bd =2, relief =GROOVE)
        # Menu fichier
        menu_fichier = Menubutton(self, text ='Fichier')
        menu_fichier.pack(side =LEFT, padx =5)
        me = Menu(menu_fichier)
        # Sous menu nouvelle partie
        new_g = Menu(me)
        for mode, label in enumerate(["Joueur vs Joueur",
                                      "Joueur vs IA",
                                      "IA vs IA"]):
            new_g.add_command(label =label, command = \
                              lambda x =mode +1: boss.app.nouvelle_partie(x))
        me.add_cascade(label ='Nouvelle partie', underline =0, menu =new_g)
        # Suite du menu fichier
        for label, command in [('Charger partie', boss.app.charger_partie),
                               ('Sauvegarder partie', boss.app.sauvegarder_partie),
                               ('Quitter partie', boss.app.quitter_partie)]:
            me.add_command(label =label, underline =0, command =command)
        menu_fichier.configure(menu =me)
        # Menu aide
        menu_aide = Menubutton(self, text ='Aide')
        menu_aide.pack(side =LEFT, padx =5)
        me = Menu(menu_aide)
        for label, command in [('Règles du jeu', boss.app.afficher_regle),
                               ('A propos ...', boss.app.a_propos)]:
            me.add_command(label =label, underline =0, command =command)
        menu_aide.configure(menu =me, state =DISABLED)

class Panneau (Frame):
    """Panneau permettant d'afficher des messages"""

    def __init__ (self, boss =None, **kwargs):
        Frame.__init__(self, **kwargs)
        self.bind('<Configure>', self.redim)
        self.label = Label(self, text ='Partonia')
        self.label.pack()

    def redim (self, event):
        """Gestionnaire de redimmensionnement"""
        largeur, hauteur = event.width, event.height
        cote = min(largeur /10, hauteur)
        self.label.configure(font =('President', -int(cote *0.8)))

class Interface (Frame):
    """Fenêtre principale de l'application"""

    def __init__ (self, app):
        self.app = app
        Frame.__init__(self)
        self.master.title(' Partonia')
        self.master.geometry('500x580')
        self.master.minsize(width =500, height =500)
        self.menu_barre = MenuBarre(self)
        self.menu_barre.pack(side =TOP, expand =NO, fill =X, padx =2, pady =2)
        self.panneau = Panneau(self)
        self.panneau.pack(expand =NO, fill =X, padx =3, pady =3)
        self.plateau = Grille(self, app)
        self.plateau.pack(expand =YES, fill =BOTH, padx =5, pady =5)
        self.pack()

class Grille (Plateau): # A revoir pour amélioré
    """Widget permettant d'afficher le plateau"""

    def __init__ (self, boss, app, **kwargs):
        self.boss = boss
        self.app = app
        Plateau.__init__(self, **kwargs)
        self.grille.bind('<Button-1>', self.clic)
        self.bind('<Configure>', self.dessin_pion, add ='+')
        self.pion_est_selectionne = False
        self.pion_choisi = ()

    def clic (self, event):
        """Gestionnaire du clic gauche de la souris"""
        # Si aucune partie n'est en cours on ne clic pas
        if self.app.partie_termine:
            return
        # On récupère les coordonnées de la case cliquée
        lig, col = int(event.y /self.cote), int(event.x /self.cote)
        # Déselection d'un pion
        if self.pion_est_selectionne and (lig, col) == self.pion_choisi:
            self.pion_est_selectionne = False
            self.dessin_pion()
        # Selection d'un pion
        elif self.app.jeu.grille[lig][col] == self.app.jeu.tour:
            self.pion_est_selectionne = True
            self.pion_choisi = (lig, col)
            self.dessin_pion()
        # S'il clique sur un pion ennemi on retire le focus du pion
        elif self.app.jeu.grille[lig][col] == self.app.jeu.adversaire:
            self.pion_est_selectionne = False
            self.dessin_pion()
        # Il ne reste plus qu'à choisir une case vide
        elif self.pion_est_selectionne:
            self.pion_est_selectionne = False
            # On effectue un tour de jeu une fois que c'est bon
            self.app.effectuer_tour_jeu(self.pion_choisi, (lig, col))
            self.app.attribuer_tour()

    def dessin_pion (self, event =None):
        """Ajoute les pions sur le plateau de jeu"""
        # Si aucune partie n'est en cours on ne dessine pas les pions
        if self.app.partie_termine:
            return
        self.grille.delete('pion')
        for ind_lig, ligne in enumerate(self.app.jeu.grille):
            for ind_col, pion in enumerate(ligne):
                if pion == 2:
                    continue
                self.ajout_pion(ind_lig, ind_col, ['yellow', 'black'][pion])
        if self.pion_est_selectionne:
            self.selection_pion()

    def selection_pion (self):
        """Met en évidence le pion sélectionné par le joueur"""
        self.ajout_pion(self.pion_choisi[0], self.pion_choisi[1],
                        ['yellow', 'black'][self.app.jeu.tour],
                        3, 'white')

    def ajout_pion (self, ind_lig, ind_col, coul, width =1, outline ='black'):
        """Dessine un pion sur la case ind_lig, ind_col de la couleur coul"""
        # Calcul des coordonnées correcte pour le dessin
        x1 = (ind_col +0.1) *self.cote
        x2 = (ind_col +0.9) *self.cote
        y1 = (ind_lig +0.1) *self.cote
        y2 = (ind_lig +0.9) *self.cote
        self.grille.create_oval(x1, y1, x2, y2, fill =coul, width =width,
                                outline =outline, tags ='pion')