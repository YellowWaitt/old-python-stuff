# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.colorchooser import *
from random import choice


class MenuBarre (Frame):

    def __init__ (self, boss):
        Frame.__init__(self, bg ="white")
        self.boss = boss
        self.start = Button(self, text ="Démarrer", command=self.boss.demarrer,
                            relief =RAISED, bg ="white")
        self.start.pack(side =LEFT, padx =3)
        self.pause = Button(self, text ="Pause", command =self.boss.pause,
                            state =DISABLED, relief =RAISED, bg ="white")
        self.pause.pack(side =LEFT, padx =3)
        Button(self, text ="Reset", command =self.boss.reset, relief =RAISED,
               bg ="white").pack(side =LEFT, padx =3)
        Label(self, text ="Lambda : ", bg ="white").pack(side =LEFT, padx =3)
        Scale(self, orient ="horizontal", from_ =0, to =1, resolution =0.01,
              bg ="white", command =self.boss.panneau.set_coef,
              highlightthickness =0).pack(side =LEFT, padx =3)
        Label(self, text =" Inverser vecteur : ", bg ="white").pack(side =LEFT,
        padx =3)
        Checkbutton(self, bg ="white", command =self.boss.panneau.set_direc,
                    variable =self.boss.panneau.var).pack(side =LEFT, padx =3)
        Label(self, text ="Vitesse : ", bg ="white").pack(side =LEFT, padx =3)
        Scale(self, orient ="horizontal", from_ =0, to =10, resolution =1,
              bg ="white", command =self.boss.set_vitesse,
              highlightthickness =0).pack(side =LEFT, padx =3)
        self.mess_iter = Label(self, text ="Nombre d'itérations : 0",
                               bg ="white")
        self.mess_iter.pack(side =LEFT, padx =3)
        BoutonCouleur(self, text ="Couleur fond",
                      command =self.boss.panneau.set_bg
                      ).pack(side =LEFT, padx =3)
        BoutonCouleur(self, text ="Couleur sommets 1", couleur ="red",
                      command =self.boss.panneau.sommets[0].set_couleur
                      ).pack(side =LEFT, padx =3)
        BoutonCouleur(self, text ="Couleur sommets 2", couleur ="blue",
                      command =self.boss.panneau.sommets[1].set_couleur
                      ).pack(side =LEFT, padx =3)
        BoutonCouleur(self, text ="Couleur points", couleur ="white",
                      command =self.boss.panneau.set_couleur_point
                      ).pack(side =LEFT, padx =3)


class BoutonCouleur (Button):

    def __init__ (self, boss, text ="Couleur", couleur ="black",
                  command =None, **kwargs):
        Button.__init__(self, boss, bg =couleur, relief =RAISED, width =5,
                        highlightthickness =0, command =self.changer_couleur,
                        **kwargs)
        self.couleur = couleur
        self.text = text
        self.commande = command

    def changer_couleur (self):
        couleur = askcolor(self.couleur, title =self.text)[1]
        if couleur:
            self.couleur = couleur
            self.configure(bg =couleur)
            self.commande(couleur)


class Application (Tk):

    def __init__ (self):
        Tk.__init__(self)
        self.title(" Chaos")
        self.geometry("1000x600+10+10")
        self.anim_active = False
        self.vitesse = 1000
        self.nbr_iter = 0
        self.panneau = Panneau(self)
        self.menu = MenuBarre(self)
        self.menu.pack(expand =NO, fill =X, side =TOP)
        self.panneau.pack(expand =YES, fill =BOTH)

    def demarrer (self):
        self.anim_active = True
        self.menu.start.configure(state =DISABLED)
        self.menu.pause.configure(state =NORMAL)
        self.panneau.unbind("<Button-1>")
        self.panneau.unbind("<Button-3>")
        self.sommets = self.panneau.get_sommets()
        self.animation()

    def pause (self):
        self.anim_active = False
        self.menu.start.configure(state =NORMAL)
        self.menu.pause.configure(state =DISABLED)

    def reset (self):
        self.anim_active = False
        self.menu.start.configure(state =NORMAL)
        self.menu.pause.configure(state =DISABLED)
        self.panneau.reset()
        self.nbr_iter = 0
        self.menu.mess_iter.config(text="Nombre d'itération : %i"%self.nbr_iter)

    def set_vitesse (self, event):
        self.vitesse = [1000, 700, 500, 320, 160, 80, 40, 20, 10, 5, 1] \
        [int(float(event))]

    def animation (self):
        for ens_sommets in self.sommets:
            choix = ens_sommets.point_random()
            self.panneau.etape(choix)
            self.nbr_iter += 1
            self.menu.mess_iter.config(text="Nombre d'itération : %i"
                                       %self.nbr_iter)
        if self.anim_active:
            self.after(self.vitesse, self.animation)


class Panneau (Canvas):

    def __init__ (self, boss):
        Canvas.__init__(self, bg ="black")
        self.boss = boss
#        self.largeur = boss.winfo_reqwidth()
#        self.hauteur = boss.winfo_reqheight()
        self.bind("<Button-1>", self.clic)
        self.bind("<Button-2>", self.changer_sommets_actif)
        self.bind("<Button-3>", self.ajout_point_depart)
#        self.bind("<Configure>", self.redim)
        self.sommets = [EnsembleSommets(couleur ="red"),
                        EnsembleSommets(couleur ="blue")]
        self.sommets_actif = 0
        self.taille_point = 1
        self.couleur_point = "white"
        self.coef = 0
        self.direc = 1
        self.var = IntVar()

#    def redim (self, event):
#        largeur, hauteur = event.width, event.height
#        ecart_largeur = largeur / self.largeur
#        ecart_hauteur = hauteur / self.hauteur
#        for sommet in self.sommets.values():
#            new_x = sommet.x * ecart_largeur
#            new_y = sommet.y * ecart_hauteur
#            sommet.set_coords(new_x, new_y)
#            self.coords(sommet,
#                        new_x - self.taille_sommet,
#                        new_y - self.taille_sommet,
#                        new_x + self.taille_sommet,
#                        new_y + self.taille_sommet)
#        self.largeur = largeur
#        self.hauteur = hauteur

    def clic (self, event):
        x, y = event.x, event.y
        objets = self.find_enclosed(x -10, y -10, x +10, y +10)
        if objets:
            for objet in objets:
                tags = self.gettags(objet)
                if "sommet" in tags:
                    ens_sommets = self.sommets[int(tags[1])]
                    ens_sommets.retrait_sommet(objet)
                    self.delete(objet)
        else:
            ens_sommets = self.sommets[self.sommets_actif]
            num = self.dessin_point(x, y, ens_sommets.taille_sommet,
                                    ens_sommets.couleur,
                                    ("sommet", self.sommets_actif))
            ens_sommets.ajout_sommet(x, y, num)

    def set_coef (self, event):
        self.coef = float(event)

    def set_direc (self):
        self.direc = [1, -1][self.var.get()]

    def ajout_point_depart (self, event):
        x, y = event.x, event.y
        self.last_point = Point(x, y)
        self.dessin_point(x, y, self.taille_point, self.couleur_point)

    def changer_sommets_actif (self, event):
        self.sommets_actif = [1, 0][self.sommets_actif]

    def get_sommets (self):
        return [ens_sommets for ens_sommets in self.sommets \
                if ens_sommets.non_vide()]

    def etape (self, sommet):
        mil_x = self.direc *(self.last_point.x -sommet.x) *self.coef +sommet.x
        mil_y = self.direc *(self.last_point.y -sommet.y) *self.coef +sommet.y
        self.last_point = Point(mil_x, mil_y)
        self.dessin_point(mil_x, mil_y, self.taille_point, self.couleur_point)

    def reset (self):
        self.delete(ALL)
        for ens_sommets in self.sommets:
            ens_sommets.reset()
        self.bind("<Button-1>", self.clic)
        self.bind("<Button-3>", self.ajout_point_depart)

    def dessin_point (self, x, y, taille, coul, tags = ()):
        return self.create_oval(x - taille, y - taille, x + taille, y + taille,
                                fill = coul, outline = coul, tags = tags)

    def set_bg (self, couleur):
        self.configure(bg =couleur)

    def set_couleur_point (self, couleur):
        self.couleur_point = couleur


class EnsembleSommets ():

    def __init__ (self, couleur ="white", taille =3):
        self.sommets = {}
        self.couleur = couleur
        self.taille_sommet = taille

    def ajout_sommet (self, x, y, nom):
        self.sommets[nom] = Point(x, y)

    def retrait_sommet (self, point):
        self.sommets.pop(point)

    def reset (self):
        self.sommets.clear()

    def get_sommets (self):
        return list(self.sommets.keys())

    def set_couleur (self, couleur):
        self.couleur = couleur
    
    def point_random (self):
        return self.sommets[choice(self.get_sommets())]
    
    def non_vide (self):
        return self.sommets != {}

class Point ():

    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def __str__ (self):
        return "(%f, %f)" %(self.x, self.y)

    def set_coords (self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    Application().mainloop()