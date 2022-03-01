#!/usr/bin/env python
# coding: utf-8

""" L'algorithme du sac à dos où l'on parcourt un arbre des cas possibles en décidant
    de prendre ou non une action constituera la base de notre solution optimisée.
"""

# ### 1. Préparation des données
#


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
        elapsed = (time_end-time_start)/1000000000
        print(f"Total time running {function.__name__}: {str(elapsed)}s seconds")
        return result
    return function_timer


# strips a string from its weird caracters
def clean_char(texte: str) -> str:
    """ on ne conserve que les caractères lisibles
    les lettres, chiffres, ponctuations décimales et signes
    les valeurs negatives sont acceptées, du point de vue profit.
    """
    texte_propre = re.sub(r"[^a-zA-Z0-9\-\.\,\+]", "", texte.replace(',','.'))
    return texte_propre



# ### 2. Amélioration des données
#
#
# #### 2.1 Nettoyage technique.

#   lecture, nettoyage et chargement en dict.
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
                    if cout < 0 :
                        print(f" line {idx} had neg cost data; dropped.")
                        cout = 0
                        clean_data = False
                    if cout == 0 :
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
                    print('      ',idx,line)
                if clean_data:
                    action_dict[cle] = (cout, cout*gain_percent/STEP)
                    compteur_ligne += 1
                else:
                    print('      ',idx,line)
            print("nombre d'actions retenues: ", compteur_ligne)
    except FileNotFoundError:
        print(f" fichier non trouvé, Merci de vérifier son nom "
                    f"dans le répertoire data {file_name} : {FileNotFoundError}")
    except IOError:
        print(f" une erreur est survenue à l'écriture du fichier {file_name} : {IOError}")

# ### 2. Résolution en programmation dynamique
#

@fn_timer
def measure_optimise(budget, liste):
    """ measures run time."""
    return knap_sack_optimise(budget,liste)


def knap_sack_optimise(budget, actions):
    """ buils a solution based on previous best solution."""
    # initialize matrix of size budget x share number
    # columns are budget increasing value whereas every line is a share
    matrice = [[0 for x in range(0, budget + 1)] for x in range(len(actions) + 1)]
    # for every share in book ; +1 as the zero line
    for i in range(1, len(actions) + 1):
        # for every budget value up to max BUDGET
        for cout_courant in range(1, budget + 1):
            # if enough money to buy the current share
            if actions[i-1][1] <= cout_courant:
                # take the max btw
                # current share profit + the previous best solution for remaining cost
                # btw courrent_budget - share cost
                # the previous Max value of the same budget column
                matrice[i][cout_courant] = max(actions[i-1][2] +
                                            matrice[i-1][cout_courant-actions[i-1][1]],
                                                matrice[i-1][cout_courant])
            else:
            # if not enough money, keep the previous solution
                matrice[i][cout_courant] = matrice[i-1][cout_courant]

    # track back the selected shares
    budget_courant = budget
    action_courante = len(actions)
    actions_porte_feuille = []

    while budget_courant >= 0 and action_courante >= 0:
        action_data = actions[action_courante-1]
        if (matrice[action_courante][budget_courant] ==
            matrice[action_courante-1][budget_courant-action_data[1]] + action_data[2]):
            actions_porte_feuille.append(action_data)
            budget_courant -= action_data[1]

        action_courante -= 1

    return matrice[-1][-1], actions_porte_feuille
# This code also was inspired by Algomius





clean_data_set()

liste_actions = [(cle,val[0],val[1]) for cle,val in action_dict.items()]
valeur, action_pf = knap_sack_optimise(BUDGET,liste_actions)


print('At cost of ',round(sum([x[1] for x in action_pf])/STEP,2),
         ' ', [x[0] for x in action_pf], ' actions brought a profit of ',
                round(valeur/(STEP*STEP),2))

#liste_actions = [(cle,val[0],val[1]) for cle,val in action_dict.items()]
measure_optimise(BUDGET,liste_actions)
