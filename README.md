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
      ` python glouton.py  `
      ` python bruteforce.py  `
      ` python optimized.py  `

Les scripts lisent les données de fichier texte au format csv dans le répertoire "data". Assurez-vous avoir les droits de créer le répertoire "data" et les fichiers ".csv".  