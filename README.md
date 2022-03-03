# ocr-p7 Résolvez des problèmes en utilisant des algorithmes en Python

Disclaimer

---

This code is part of the openclassrooms learning adventure split in 13 business alike projects.  
  
  
This one is to code a chess management app following the rules of Swiss tournament.  
Some materials or links may have rights to be granted by https://openclassrooms.com. 
The additionnal code follows "CC BY-SA ".
  
** Not to be used for production **  


---
## Objet.  

"...
 Nous avons besoin que vous conceviez un algorithme qui maximisera le profit réalisé par nos clients après deux ans d'investissement. Votre algorithme doit suggérer une liste des actions les plus rentables que nous devrions acheter pour maximiser le profit d'un client au bout de deux ans.

Nous avons les contraintes suivantes :
* Chaque action ne peut être achetée qu'une seule fois.
* Nous ne pouvons pas acheter une fraction d'action.
* Nous pouvons dépenser au maximum 500 euros par client.

..."



## Installation.

Pour utiliser les scripts,   
il est conseillé sous le prompt bash python (ici cmd Anaconda3 sous Windows 10):  

1. de cloner l'ensemble du répertoire github dans un répertoire local dédié.  
        ``` git clone https://github.com/dev-KC20/ocr-p7.git   ```

2. se déplacer dans le sous répertoire de travail ocr-p4v2  
        ` cd ocr-p7   `

3. de créer un environnement virtuel python, env  
        ` python -m venv env  `

4. d'activer un environnement virtuel python, env  
        ` env\scripts\activate.bat  `

5. d'installer les paquets requis pour mémoire,   
        ` pip install -r requirements.txt  `

6. créer un répertoire data sous le répertoire courant ocr-p7, sous windows  
       ` mkdir data   `

7. d'executer le script  
      ` python P7-00-greedy.py  data/votre_fichier_data.csv `
      ` python P7-01-bruteforce.py  data/votre_fichier_data.csv`
      ` python P7-02-optimized.py  data/votre_fichier_data.csv`

Les scripts lisent les données de fichier texte au format csv dans le répertoire "data". Assurez-vous avoir les droits de créer le répertoire "data" et les fichiers ".csv".  


## En synthèse cas d'utilisation, limites et contraintes

L’algorithme de force brute est le plus précis car il évalue toutes les possibilités pertinentes mais ne peut être utilisé que sur de petit ensemble de données (de l’ordre des dizaines) pour des raisons de longs temps de traitement.

L’algorithme Glouton apporte une solution mais celle-ci ne sera pas optimale car locale et donc parfois peu précise. Le volume de donnée n’est pas une contrainte.

L’algorithme optimisé (programmation dynamique) est précis, plus rapide que celui de force brute. Le temps de traitement et l’espace mémoire utilisés dépendent du jeu de donnée et de la taille de la contrainte. (de l’ordre de moins du million pour n x budget). Le problème doit pouvoir s’exprimer en fonction de sous-problème.

