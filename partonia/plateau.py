from tkinter import *

class Plateau (Frame):
    """Plateau de jeu personnalisable"""

    def __init__ (self, boss =None, nbrLigne =10, nbrColone = 10,
                  bgBordure ='#582900', bordureActive =True, indiceHaut ='let',
                  indiceCote ='nbr', coulIndice ='white', police ='Helvetica',
                  bgPlateau ='dark green', coulLigne ='black', **kwargs):
        # Frame principale
        self.boss = boss
        Frame.__init__(self, **kwargs)
        self.nbrLigne = nbrLigne
        self.nbrColone = nbrColone
        self.bordureActive = bordureActive
        # Mémorisation des options esthetiques
        self.options = {'bgBordure': bgBordure,
                        'indiceHaut': indiceHaut,
                        'indiceCote': indiceCote,
                        'coulIndice': coulIndice,
                        'police': police,
                        'bgPlateau': bgPlateau,
                        'coulLigne': coulLigne}
        # Les dimensions dependront de la Frame pincipale
        self.bind('<Configure>', self.redim)
        # Utilisation de Canvas pour la bordure et la grille
        self.bordure = Canvas(self, bg =bgBordure, bd =0,
                             highlightthickness =0)
        self.grille = Canvas(self, bg =bgPlateau, bd =0,
                             highlightthickness =0)
        self.bordure.pack()

    def redim (self, event):
        """Gestionnaire de redimmensionnement"""
        largeur, hauteur = event.width, event.height
        # Calcul des nouvelles dimensions
        self.cote = min(largeur/(self.nbrColone +self.bordureActive),
                        hauteur/(self.nbrLigne +self.bordureActive))
        self.largeur = self.cote*self.nbrColone
        self.hauteur = self.cote*self.nbrLigne
        # Application des nouvelles dimensions
        self.bordure.configure(width =self.cote *(self.nbrColone +
                                                  self.bordureActive),
                               height =self.cote *(self.nbrLigne +
                                                   self.bordureActive))
        self.grille.configure(width =self.largeur +1,
                              height =self.hauteur +1)
        # On redessine le plateau avec labonne taille
        self.dessin_plateau()

    def dessin_plateau (self):
        """Dessine le plateau"""
        self.bordure.delete(ALL)
        self.dessin_grille()
        # Rajout de la grille dans le plateau
        self.bordure.create_window((self.nbrColone +self.bordureActive)*
                                   self.cote/2,
                                   (self.nbrLigne +self.bordureActive)*
                                   self.cote/2,
                                   window =self.grille)
        # Dessin de la bordure uniquement si elle est active
        if self.bordureActive:
            font = (self.options['police'], -int(self.cote/4))
            # Ajout des marqueurs superieurs
            if self.options['indiceHaut'] == 'let':
                fonc = lambda n: chr(n +65)
            else:
                fonc = lambda n: str(n +1)
            for col in range(self.nbrColone): # Indices horinzontaux
                self.bordure.create_text((col +1) *self.cote, self.cote /4,
                                         text = fonc(col),
                                         fill = self.options['coulIndice'],
                                         font = font)
            # Ajout des marqueurs lateraux
            if self.options['indiceCote'] == 'let':
                fonc = lambda n: chr(n +65)
            else:
                fonc = lambda n: str(n +1)
            for lig in range(self.nbrLigne): # Indices verticaux
                self.bordure.create_text(self.cote /4, (lig +1) *self.cote,
                                         text = fonc(lig),
                                         fill = self.options['coulIndice'],
                                         font = font)

    def dessin_grille (self):
        """Dessine uniquement la grille"""
        self.grille.delete(ALL)
        # Trace des lignes de la grille
        rang = 0
        for lig in range(self.nbrLigne +1): # Horizontale
            self.grille.create_line(0, rang, self.largeur, rang,
                                    fill =self.options['coulLigne'])
            rang += self.cote
        rang = 0
        for col in range(self.nbrColone +1): # Verticale
            self.grille.create_line(rang, 0, rang, self.hauteur,
                                    fill =self.options['coulLigne'])
            rang += self.cote

    def set_apparence (self, **kwargs):
        """Modifie l'apparence du plateau en fonction des arguments de kwargss"""
        key_valide = self.options.keys()
        key_invalide = [key for key in kwargss if key not in key_valide()]
        arg_invalide = [1 for arg in kwargss.values() if not(isinstance(arg, str))]
        if not key_invalide:
            if not arg_invalide:
                self.options.update(kwargs)
                self.dessin_plateau()
            else:
                raise ValueError('Les arguments doivent être de type str')
        else:
            raise KeyError('%s ne sont pas des cle valides'
                           %','.join(key_invalide))

    def set_nbr_colone (self, nbrColone):
        """Modifie le nombre de colone actuel par 'nbrColone'"""
        if isinstance(nbrColone, int) and nbrColone > 0:
            self.nbrColone = nbrColone
            self.redim()
        else:
            raise ValueError('Le nombre de colone doit être positif')

    def set_nbr_ligne (self, nbrLigne):
        """Modifie le nombre de ligne actuel par 'nbrLigne'"""
        if isinstance(nbrLigne, int) and nbrLigne > 0:
            self.nbrLigne = nbrLigne
            self.redim()
        else:
            raise ValueError('Le nombre de ligne doit être positif')

    def set_bordure (self, etat):
        """Active ou désactive la bordure"""
        if isinstance(etat, bool):
            self.bordureActive = etat
            self.redim()
        else:
            raise TypeError("'etat' doit être un bool")

if __name__ == '__main__':
    fen = Tk()
    fen.geometry('500x500')
    grille = Plateau(fen)
    grille.pack(expand =YES, fill =BOTH)
    fen.mainloop()