# -*- coding: utf-8 -*-

from time import time

class IA ():
    """Implémentation d'un algorithme de recherche arborescente qui utilise
    les heuristiques associées, sont implementées ici :
        - les coupes alpha beta
        - la recherche quiescente
        - l'approfondissement iteratif
        - l'heuristique de l'historique

    J'ai repris et adapté les algorithmes du cour "Intelligence artificielle :
    Une approche ludique" de Tristan Cazenave, trouvé à la BU de Paul Sab"""

    def __init__ (self, partie, app, temp_max =10):
        self.partie = partie
        self.app = app
        self.temp_max = temp_max

    def alpha_beta (self, profondeur, alpha, beta, vp):
        """Algorithme classique de recherche min/max avec coupes alpha/beta"""
        # Arrêt des recherches une fois le temps limite atteint
        if time() - self.debut > self.temp_max:
            return -1000
        if not profondeur: # Recherche des quiescences à profondeur 0
            return self.quiescence(alpha, beta)
        liste_coup = self.partie.coup_legaux()
        if not liste_coup: # Si aucun coup n'est jouable arrêt des recherches
            return self.partie.evaluation()
        # La liste des coups est triée en fonction de leur note de coupe
        liste_coup.sort(key =lambda x: self.historique[x.nombre()],
                        reverse =True)
        for coup in liste_coup: # Recherche pour tout les coups possibles
            vptemp = [] # Liste temporaire des coups trouvés
            # On simule un tour
            self.partie.tour_de_jeu(coup.case_dep, coup.case_arr)
            # L'evaluation dépend des coups suivants
            evaluation = -self.alpha_beta(profondeur -1, -beta, -alpha, vptemp)
            # Si on trouve un coup meilleur on le mémorise
            if evaluation > alpha:
                alpha = evaluation
                vp.clear()
                vp.extend(vptemp)
                vp.insert(0, coup)
            # On annule le coup simulé
            self.partie.dejoue()
            # Si les coups n'apporte rien à l'évaluation on arrête de chercher
            if alpha >= beta:
                # Mise à jour dela note de coupe du coup
                self.historique[coup.nombre()] += 4 << (profondeur *2)
                return beta
        return alpha

    def quiescence (self, alpha, beta):
        """Complément de l'alpha beta qui a pour but de limiter l'effet
        d'horizon"""
        if time() - self.debut > self.temp_max:
            return -1000
        # On ne s'intéresse qu'au coup qui capture un pion
        liste_coup = self.partie.coup_quiescence()
        # Si aucune capture n'est possible on renvoie l'évaluation normale
        if not liste_coup:
            return self.partie.evaluation()
        # Le reste de la structure est la même que l'alpha beta
        for coup in liste_coup:
            self.partie.tour_de_jeu(coup.case_dep, coup.case_arr)
            evaluation = -self.quiescence(-beta, -alpha)
            self.partie.dejoue()
            if evaluation > alpha:
                alpha = evaluation
            if alpha >= beta:
                return beta
        return alpha

    def approfondissement_iteratif (self, vp):
        """Algorithme effectuant la recherche par niveau de profondeur de
        l'arbre en un temps limite"""
        vptemp = []
        alpha, beta = -1000, 1000
        self.historique = [0] *1024
        # Démarrage d'un chrono qui permet de contrôler le temps de recherche
        self.debut = time()
        # La recherche se fait de la profondeur 1 à maximum 3
        for profondeur in range(1, 4):
            eval_temp = self.alpha_beta2(profondeur, alpha, beta, vptemp)
#            if eval_temp <= alpha:
#                print("\t"*(3-profondeur)+"Fail alpha")
#                eval_temp = self.alpha_beta(profondeur, -1000, alpha, vptemp)
#            elif eval_temp >= beta:
#                print("\t"*(3-profondeur)+"Fail beta")
#                eval_temp = self.alpha_beta(profondeur, beta, 1000, vptemp)
            # On ne retient pas un résultat après la limite de temps
            if time() - self.debut < self.temp_max:
                # On retient le meilleur coup obtenu après chaque recherche
                evaluation = eval_temp
                vp.clear()
                vp.extend(vptemp)
#                alpha = evaluation - 4
#                beta = evaluation + 4
        return evaluation

    def jouer (self):
        """Lance la recherche d'un coup puis le joue"""
        vp = [] # Liste des coups prévus par l'IA
        evaluation = self.approfondissement_iteratif(vp)
        fin = time()
        print("\nRecherche faite en %f secondes"%(fin - self.debut))
        print(' / '.join([' -- > '.join(map(str,[coup.case_dep, coup.case_arr]))\
                                            for coup in vp]))
        print('Evaluation : %i'%evaluation)
        self.app.effectuer_tour_jeu(vp[0].case_dep, vp[0].case_arr)

    def alpha_beta2 (self, profondeur, alpha, beta, vp):
        """Variante avec variation principale"""
        if time() - self.debut > self.temp_max:
            return -1000
        if not profondeur: # Recherche des quiescences à profondeur 0
            return self.quiescence(alpha, beta)
        liste_coup = self.partie.coup_legaux()
        if not liste_coup: # Si aucun coup n'est jouable arrêt des recherches
            return self.partie.evaluation()
        # La liste des coups est triée en fonction de leur note de coupe
        liste_coup.sort(key =lambda x: self.historique[x.nombre()],
                        reverse =True)
        variationPrincipaleTrouve = False
        for coup in liste_coup: # Recherche pour tout les coups possibles
            vptemp = [] # Liste temporaire des coups trouvés
            # On simule un tour
            self.partie.tour_de_jeu(coup.case_dep, coup.case_arr)
            if variationPrincipaleTrouve:
#                print("\t"*(3-profondeur)+"vPT")
                evaluation = -self.alpha_beta2(profondeur -1, -alpha -2, -alpha,
                                               vptemp)
                if evaluation > alpha:
#                    print("\t"*(3-profondeur)+"fail")
                    evaluation = -self.alpha_beta2(profondeur -1, -beta, -alpha,
                                                  vptemp)
            else:
#                print("\t"*(3-profondeur)+"Pas trouvé")
                evaluation = -self.alpha_beta2(profondeur -1, -beta, -alpha,
                                              vptemp)
            # Si on trouve un coup meilleur on le mémorise
            if evaluation > alpha:
                alpha = evaluation
                variationPrincipaleTrouve = True
#                print("\t"*(3-profondeur)+"Trouvé")
                vp.clear()
                vp.extend(vptemp)
                vp.insert(0, coup)
            # On annule le coup simulé
            self.partie.dejoue()
            # Si les coups n'apporte rien à l'évaluation on arrête de chercher
            if alpha >= beta:
#                print("\t"*(3-profondeur)+"Coupe")
                # Mise à jour dela note de coupe du coup
                self.historique[coup.nombre()] += 4 << (profondeur *2)
                return beta
        return alpha