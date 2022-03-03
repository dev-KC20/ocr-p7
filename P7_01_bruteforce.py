#!/usr/bin/env python
# coding: utf-8
""" L'algorithme Force brute:
Le nombre de combinaison est la somme du nombre de combinaisons de k pris parmi n,  k allant de 1 à n.
C'est n fois le nombre de combinaisons.
 $$
 n \\times {n \\choose k}= n \\times {\\frac {n!}{k!(n-k)!}}
 $$
"""
# ### 1. Préparation des données

# modules importés
# lecture de fichiers csv et dict colonnes
import csv
# nettoyage des caractères via expression regex
import re
# mesure du temps passé -> time spend over complexity
import time
# mesure de l'occupation mémoire space complexity
from sys import argv


# constants
FILE = "data/p7-20-shares.csv"
FIELDNAMES = ['name', 'cost', 'profit']
STEP = 100
BUDGET = 500 * STEP


# check if file name was passed as parm to the script
if __name__ == '__main__':
    if len(argv) == 2:
        FILE = argv[1]


def fn_timer(function):
    """ starts before & stops after the run of the function, a time counter"""

    def function_timer(*args, **kwargs):
        time_start = time.perf_counter_ns()
        result = function(*args, **kwargs)
        time_end = time.perf_counter_ns()
        elapsed = (time_end-time_start)
        print(f"Total time running {function.__name__}: {str(elapsed)}s nanoseconds")
        # elapsed = (time_end-time_start)/1000000000
        # print(f"Total time running {function.__name__}: {str(elapsed)}s seconds")
        return result
    return function_timer


# strips a string from its weird caracters
def clean_char(texte: str) -> str:
    """ on ne conserve que les caractères lisibles
    les lettres, chiffres, ponctuations décimales et signes
    les valeurs negatives sont acceptées, du point de vue profit.
    """
    texte_propre = re.sub(r"[^a-zA-Z0-9\-\.\,\+]", "", texte.replace(',', '.'))
    return texte_propre


# ### 2. Amélioration des données

# #### 2.1 Nettoyage technique.
# On observe les données reçues pour s'assurer de leur qualité.
# Cas particuliers traités:
# Cout nul ; il pourrait s'agir d'action gratuite mais nous avons décidé de les supprimer du jeu d'essai.
# Cout negatif ; supprimé.
# profit négatif ; conservé car une perte est possible.
#
# On aurait pu diminuer encore plus le nombre d'action en suppromant les actions dont le profit =0.
#
# #### 2.2 Nettoyage métier.
# On vérifie que le profit est possiblement un pourcentage du cout et non une valeur.
# La bourse rapporte 8% en moyenne par an sur les 30 dernières années.
#
# Entre 1988 et 2018 (chiffres arrêtés au 18 mai), les actions avec dividendes ont rapporté 1.352%,
# l’immobilier à Paris 402%, l’assurance vie en euros370%, les Sicav monétaires 209%, l’or 179%,
# le Livret A 135%. À titre d’information, l’inflation sur la période a été de 67%.
# Hors dividendes, la performance tombe à 461%, ce qui reste très honorable.
# -> Prenons un ratio de 15%/an.
#
# Si plus de 50% des actions ont un ratio profit/cout >> 1,30 alors on estime que le profit est estimé en valeur.
#
# Après estimation via Excel, 691 actions au profit < 1,30 et donc 266 > 1.30.
# On estime que le profit est exprimé en % age du coût.


#  lecture, nettoyage et chargement en dict.
#     les non valeurs NaN sont rejetées.


action_dict = {}
file_name = FILE


def clean_data_set():

    """ retrieve and clean the data."""
    try:
        with open(file_name, "r", newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, fieldnames=FIELDNAMES,
                                        delimiter=',', doublequote=False)
            # skip the header
            next(csv_reader)
            compteur_ligne = 0
            for idx, line in enumerate(csv_reader):
                clean_data = True
                if line[FIELDNAMES[0]] != "":
                    cle = clean_char(line[FIELDNAMES[0]])
                else:
                    print(f" line {idx} had missing share name; dropped.")
                    clean_data = False
                if line[FIELDNAMES[1]] != "":
                    cout = int(STEP * float(clean_char(line[FIELDNAMES[1]])))
                    if cout < 0:
                        print(f" line {idx} had neg cost data; dropped.")
                        cout = 0
                        clean_data = False
                    if cout == 0:
                        print(f" line {idx} had null cost data ;"
                              f"could have been a gift but management decision: dropped.")
                        cout = 0
                        clean_data = False
                else:
                    print(f" line {idx} had missing cost data; dropped.")
                    clean_data = False
                if line[FIELDNAMES[2]] != "":
                    gain_percent = int(STEP * float(clean_char(line[FIELDNAMES[2]])))
                else:
                    print(f" line {idx} had missing profit percentage; dropped.")
                    clean_data = False
                if gain_percent <= 0:
                    print(f"** line {idx} had negative profit percentage ; "
                          f"accepted but pls check. **")
                    print('      ', idx, line)
                if clean_data:
                    action_dict[cle] = (cout, cout*gain_percent/STEP)
                    compteur_ligne += 1
                else:
                    print('      ', idx, line)
            print("nombre d'actions retenues: ", compteur_ligne)
    except FileNotFoundError:
        print(f" fichier non trouvé, Merci de vérifier son nom "
              f"dans le répertoire data {file_name} : {FileNotFoundError}")
    except IOError:
        print(f" une erreur est survenue à l'écriture du fichier {file_name} : {IOError}")


# ### 3. Résolution en force brute récurrente (pour mémoire):
# si on considère l'ensemble des 'actions' du porte-feuille potentiel, il existe de multiples combinaisons d''action'.
# Parmi toutes les combinaisons dont le cout est inférieur au budget d'investissement, l'une d'entre elles
# est optimale car elle fournit le plus grand profit.
#
#
# Maintenant quand on prend une 'action' au hasard,
# soit on selectionne cette 'action' comme partie de la solution
# soit on ne la selectionne pas.
#
# Quand on selectionne une 'action', il faut exprimer la valeur et le cout du porte-feuille en fonction
# de sa valeur avant sélection (pour introduire de la récurrence avec n fonction de n-1).
# valeur(pf(i)) = valeur(pf(i-1)) + valeur(action(i))
# cout(pf(i)) = cout(pf(i-1)) + cout(action(i))
# ou avec un cout exprimé en budget restant:
# budget_restant(pf(i)) = budget_restant(pf(i-1)) - cout(action(i))
#
# Quand on ne selectionne pas une action, la valeur et le poids du porte-feuille sont inchangés.
#
# Cas d'arrêt de la fonction récurrente : si tout le budget est épuisé ou si toutes les actions ont été considérées.
#
# Formalisons un peu mieux:


# recursively check all combinations
# compte_combinaison = 0
def knap_sack_brute(budget, actions, actions_porte_feuille=None):
    # global compte_combinaison
    # tant qu'il reste des actions non traitées
    if actions:
        # compte_combinaison +=1
        # si l'action n'était pas retenue
        profit_sans, liste_sans = knap_sack_brute(budget, actions[1:], actions_porte_feuille)
        # 1ère action du porte-feuille
        val = actions[0]
        cout = val[1]
        # si son cout est inférieur au budget
        if cout <= budget:
            # action prise, budget diminuée de son cout, et sous ensemble
            #   d'action restante et selection de l'action courante
            profit_avec, liste_avec = knap_sack_brute(budget - cout, actions[1:], actions_porte_feuille + [val])
            # Choix de l'optimum :
            if profit_sans < profit_avec:
                return profit_avec, liste_avec

        return profit_sans, liste_sans
    else:
        return sum([i[2] for i in actions_porte_feuille]), actions_porte_feuille
# This code was inspired by Algomius


@fn_timer
def measure_brute(budget, liste):
    return knap_sack_brute(budget, liste, [])

# Main section


clean_data_set()
liste_actions = [(cle, val[0], val[1]) for cle, val in action_dict.items()]
valeur, action_pf = knap_sack_brute(BUDGET, liste_actions, [])

# print('nombre de combinaison explorée', compte_combinaison)

print('At cost of ', round(sum([x[1] for x in action_pf])/STEP, 2), ' ', [x[0] for x in action_pf],
      ' actions brought a profit of ', round(valeur/(STEP*STEP), 2))

# mesasure CPU time
liste_actions = [(cle, val[0], val[1]) for cle, val in action_dict.items()]
measure_brute(BUDGET, liste_actions)
