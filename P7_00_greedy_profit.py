#!/usr/bin/env python
# coding: utf-8
""" L'algorithme glouton où l'on tri une liste dont on consomme les éléments
    les uns après les autres jusqu'à la limite du budget.
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
STEP = 1
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


# ## 2. Résolution avec un algorithme Glouton


@fn_timer
def algo_glouton(dictio: dict[str, tuple], budget: int) -> (int, list):
    """ Tri par densité de profit càd que les actions au meilleur rapport profit/cout
        sont les premières dans l'ordre
    """
    action_trie = dict(sorted(dictio.items(), key=lambda x: x[1][1], reverse=True))
    budget_left = budget
    action_selected: list[str] = []
    for cle, valeur in action_trie.items():
        if budget_left - valeur[0] > 0:
            action_selected.append(cle)
            budget_left -= valeur[0]
    return (budget_left, action_selected)


clean_data_set()

reste_budget, action_pf = algo_glouton(action_dict, BUDGET)
print('At cost of ', (BUDGET-reste_budget)/STEP, ' ', action_pf, ' actions brought a profit of ',
      round(sum(list(map(lambda x: action_dict[x][1], action_pf)))/(STEP*STEP), 2))
