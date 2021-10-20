# -*- coding: utf-8 -*-

from partonia import *
from interface import *
from IA import *
from re import search, sub
from os import listdir, getcwd

class Application ():
    """Classe principale qui fait le lien entre l'utilisateur et le jeu"""

    def __init__ (self):
        self.application_active = True
        # L'applicatopn s'éxecute dans la console par défaut
        self.mode_graphique_active = False
        # Aucune partie n'est en cours au départ
        self.partie_termine = True
        self.jeu = Partonia()
        self.IA = IA(self.jeu, self)
        # Ensemble des fonctions du menu principal
        self.dic_menu_princ = {'1': self.nouvelle_partie,
                               '2': self.charger_partie,
#                               '3': self.afficher_regle,
#                               '4': self.afficher_aide,
                               '5': self.mode_graphique,
#                               '6': self.a_propos,
                               '7': self.quitter_application}
        # Ensemble des fonctions executable en cours de partie
        self.dic_fonc_partie = {'quitter': self.quitter_partie,
#                                'aide': self.afficher_aide,
#                                'regle': self.afficher_regle,
                                'undo': self.jeu.dejoue,
                                'sauver': self.sauvegarder_partie,
                                'fenetre': self.mode_graphique,
                                'afficher': self.afficher_grille,
                                'eval': lambda x=0:print(self.jeu.evaluation())}
        # Panneau d'acceuil sympa
        print('\n'+'#'*28+'\n#'+' '*26+'#\n#'+' '*9+'PARTONIA'+' '*9+'#\n#'+
              ' '*26+'#\n'+'#'*28+'\n')
        self.menu_principal()

    def menu_principal (self):
        """Définition du menu principal de l'application"""
        while self.application_active:
            print('\n\n=====  Menu principal  =====')
            # Menu avec les différents choix
            print("""\n1. Nouvelle partie
                  \r2. Charger une partie
                  \r3. Règles du jeu
                  \r4. Aide
                  \r5. Activer le mode graphique
                  \r6. A propos
                  \r7. Quitter""")
            entre = input('\nFaite votre choix : ')
            if entre.isnumeric():
                if entre in self.dic_menu_princ:
                    self.dic_menu_princ[entre]()
                else:
                    print("%s n'est pas une action définie"%entre)
            else:
                print('Pour faire votre choix entrez un des numéros affichés')

    def mode_graphique (self):
        """Permet de basculer du mode console au mode graphique"""
        self.mode_graphique_active = True
        self.interface = Interface(self)
        self.interface.mainloop()
        # Une fois la fenêtre  fermée on désactive le mode graphique
        self.mode_graphique_active = False

    def effectuer_tour_jeu (self, case_depart, case_arrive):
        """Effectue un tour de jeu avec les cases données en paramètres"""
        if self.jeu.coup_est_valide(case_depart, case_arrive):
            # Effectue un tour de jeu
            self.jeu.tour_de_jeu(case_depart, case_arrive)
            # Si le joueur n'a plus de pions c'est fini
            if not self.jeu.nombre_pion[self.jeu.tour]:
                self.fin_de_partie()
            else:
                self.afficher_grille()
        elif not self.mode_graphique_active: # Message d'erreur console
            print('Coup non valide')

    def fin_de_partie (self):
        """Gestion de la fin de partie"""
        # On reviens sur le tour du gagnant pour afficher les messages
        self.jeu.changer_tour()
        if self.mode_graphique_active:
            self.afficher_grille()
            self.interface.panneau.label.configure(
            text ='Victoire du joueur %i'%(self.jeu.tour +1),
            fg =['yellow', 'black'][self.jeu.tour])
            self.partie_termine = True
        else:
            self.partie_termine = True
            self.afficher_grille()
            input('\nAppuyez sur Entrer')

    def attribuer_tour (self):
        """Gestion des changements de tours entre joueurs et IA"""
        fin = False
        while not fin:
            if self.mode_graphique_active: # Mise à jour forcée de l'affichage
                self.interface.update()
            # Tour de jeu de l'IA
            if (self.mode_jeu >= 2 and self.jeu.tour == 1 or \
                self.mode_jeu == 3 and self.jeu.tour == 0):
                self.IA.jouer()
            # Tour du joueur
            elif not self.mode_graphique_active:
                self.saisie_clavier()
            # Si la partie est terminée ou le mode graphique activé on sort
            if self.partie_termine or (self.mode_graphique_active and \
                                       self.mode_jeu != 3):
                fin = True

    def saisie_clavier (self):
        """Au cours d'une partie, récupère les entrées claviers de
        l'utilisateur et éxecute les actions qui y sont associées"""
        entre_valide = False
        while not entre_valide:
            # On récupère une entrée clavier
            entre = input('Entrez un coup (A1 A2) : ').lower()
            if entre:
                entre = entre.split()
            else:
                print('Veuillez saisir quelque chose')
                continue
            # Si c'est une fonction définie on l'éxecute
            if entre[0] in self.dic_fonc_partie:
                entre_valide = True
                self.dic_fonc_partie[entre[0]]()
            # Si c'est une case on joue un tour avec
            elif self.est_un_coup(entre):
                entre_valide = True
                # On transforme l'entée en coordonnées de deux cases
                case_depart = (int(entre[0][1:]) -1, ord(entre[0][0]) -97)
                case_arrive = (int(entre[1][1:]) -1, ord(entre[1][0]) -97)
                self.effectuer_tour_jeu(case_depart, case_arrive)
            else:
                print("'%s' ne correspond pas à un coup" %' '.join(entre))

    def est_un_coup (self, entre):
        """Vérifie que entre correspond bien à un coup"""
        # ^([a-z][0-9]{1,2})$ = une lettre suivie d'un ou deux nombres
        return len(entre) == 2 and search('^([a-z][0-9]{1,2})$', entre[0]) and\
        search('^([a-z][0-9]{1,2})$', entre[1])

    def afficher_grille (self):
        """Affiche la grille"""
        # Si le mode graphique est actif on utilise la fonction de l'interface
        if self.mode_graphique_active:
            # Message du panneau
            self.interface.panneau.label.configure(
            text ='Au tour du joueur %i' %(self.jeu.tour +1),
            fg =['yellow', 'black'][self.jeu.tour])
            self.interface.plateau.dessin_pion()
            return
        # Indique le tour du joueur ou le gagnant
        if not self.partie_termine:
            print('\n' + ' ' *15 + 'Au tour du joueur %s\n'
                  %['O', 'X'][self.jeu.tour])
        else:
            print('\n' + ' ' *14 + 'Le joueur %s a gagné !\n'
                  %['O', 'X'][self.jeu.tour])
        # La grille est dotée de l'indice des cases sur les côtés
        print(' '*6 +'A   B   C   D   E   F   G   H   I   J')
        for ind, ligne in enumerate(self.jeu.grille):
            ligne_affiche = ' | '.join([['O', 'X', ' '][pion] for pion in ligne])
            print(' ' *4 + '-' *41) # Ligne de séparation
            print(' %2i | %s |' %(ind +1, ligne_affiche))
        print(' ' *4 + '-' *41)

    def nouvelle_partie (self, mode =None):
        """Permet de régler les paramètres d'une nouvelle partie"""
        # L'interface possède son propre menu de sélection
        if not self.mode_graphique_active:
            choix_fait = False
            while not choix_fait:
                print("\n=====  Nouvelle partie  =====")
                print("\nChoississez votre mode de jeu :")
                print("""\n1. Joueur vs Joueur
                \r2. Joueur vs IA
                \r3. IA vs IA
                \r4. Retour""")
                entre = input("\nFaites votre choix : ")
                if entre.isnumeric():
                    entre = int(entre)
                    if entre in range(1, 5):
                        self.mode_jeu = entre
                        choix_fait = True
                    else:
                        print("%i n'est pas disponible" %entre)
                else:
                    print("Faite votre choix en tapant un des numéros affichés")
            if self.mode_jeu == 4:
                return
        if mode: # Si la partie  est lancée depuis l'interface
            self.mode_jeu = mode
        # Initialisation et lancement de la partie
        self.partie_termine = False
        self.jeu.initialiser_partie()
        self.afficher_grille()
        if self.mode_graphique_active:
            self.interface.panneau.label.configure(
            text ='Au tour du joueur 1', fg ='yellow')
        self.attribuer_tour()

    def charger_partie (self):
        """Permet de continuer une partie sauvegardée"""
        # Emplacement du dossier de sauvegarde
        dossier_defaut = getcwd() + '\sauvegarde'
        if self.mode_graphique_active:
            file_name = askopenfilename(initialdir =dossier_defaut,
                                        filetypes=[('Texte', '.txt')])
        else:
            print('\n=====  Charger partie  =====')
            # Les noms des sauvegardes sont affichées sans extensions
            liste_fichier = [sub('([.][a-z]+)$', '', nom)\
                             for nom in listdir(dossier_defaut)]
            if not liste_fichier:
                print("Il n'y a aucune sauvegarde disponible")
                return
            print('\nListe des sauvegardes :\n%s' %'\n'.join(liste_fichier))
            print('\nEntrez le nom de la partie que vous\nsouhaitez charger ou\
 rien pour annuler :')
            file_name = input()
            if not file_name:
                print('Chargement annulé')
            elif file_name not in liste_fichier:
                print('%s ne correspond à aucune sauvegarde' %file_name)
                return
            else:
                file_name = dossier_defaut + '/' + file_name + '.txt'
        # Si l'opération a été annulée on ne charge pas
        if file_name:
            with open(file_name, 'r') as file:
                save = file.readline().split('\\')
            # On intercepte les éventuelles erreurs de chargement
            try:
                self.jeu.grille = [[[0, 1, 2][int(pion)] for pion in ligne]\
                                   for ligne in save[0].split('/')]
                self.jeu.tour = int(save[1])
                self.jeu.adversaire = (self.jeu.tour +1) %2
                self.jeu.nombre_pion = list(map(int, save[2].split('/')))
                self.mode_jeu = int(save[3])
            except:
                print('Erreur lors du chargement du fichier')
                return
            # Si tout c'est bien passé on lance la partie
            self.partie_termine = False
            self.afficher_grille()
            # Les anciens coups ne sont pas conservés avec la sauvegarde
            self.jeu.pile_modif = []
            if self.mode_graphique_active:
                self.interface.panneau.label.configure(
                text ='Au tour du joueur 1', fg ='yellow')
            self.attribuer_tour()

    def sauvegarder_partie (self):
        """Permet de sauvegardée une partie"""
        # Emplacement du dossier de sauvegarde
        dossier_defaut = getcwd() + '\sauvegarde'
        if self.mode_graphique_active:
            file_name = asksaveasfilename(initialdir =dossier_defaut,
                                          filetypes=[('Texte', '.txt')])
        else:
            print('\nEntrez un nom à la sauvegarde\nou rien pour annuler :')
            file_name = input()
            if not file_name:
                print('Sauvegarde annulée')
            else:
                file_name = dossier_defaut + '/' + file_name
        # Si l'opération a été annulée on ne sauvegarde pas
        if file_name:
            with open(file_name + '.txt', 'w') as file:
                # On conserve la grille, le tour de jeu, les nombres de pions
                # et le mode de jeu
                grille = '/'.join([''.join(map(str, ligne)) \
                                   for ligne in self.jeu.grille])
                nbr_pion = '/'.join(map(str, self.jeu.nombre_pion))
                file.write('\\'.join([grille, str(self.jeu.tour), nbr_pion,
                                      str(self.mode_jeu)]))
            if not self.mode_graphique_active:
                print('Sauvegarde réussie')

    def quitter_partie (self):
        """Permet de quitter la partie en cours"""
        self.partie_termine = True
        if self.mode_graphique_active:
            self.interface.plateau.grille.delete('pion')
            self.interface.panneau.label.configure(
            text ='Partonia', fg ='black')

    def afficher_aide (self):
        """Affiche l'aide"""
        pass

    def afficher_regle (self):
        """Affiche les règles du jeu"""
        pass

    def a_propos (self):
        """Quelques informations supplémentaires"""
        pass

    def quitter_application (self):
        """Met fin à l'éxecution de l'aplication"""
        self.application_active = False
        print('\nA bientôt ;)\n')

if __name__ == '__main__':
    Application()