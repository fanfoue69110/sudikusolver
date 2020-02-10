# -*- coding: utf-8 -*-
"""
Programme de détermination d'une vitesse pour un nouvel enquêteur arrivant 
dans le réseau.

Algorithme : arbre de décision

Created on Tue Feb  4 13:13:20 2020

F. Lebrun - Février 2020

"""




#%%

#def selectcity(dep: str,com: str) -> (int,str):
#    with UseDatabase(database) as cursor:
#        _SQL = """
#        select pop , nomcom from population 
#        where (dep = '%s' and com = '%s')
#        """%(dep,com)
#        cursor.execute(_SQL)
#        content= cursor.fetchone()
#        return (content[0],content[1])


#%%
# Fonction de calcul de la vitesse Opale
def vitesseopale(pop: int , dist : float) -> str:
    """Fonction qui retourne la vitesse d'un enquêteur quand on lui communique :
        - la distance moyenne à la zone de collecte
        - la population moyenne des communes de la zone de collecte"""
    test1 = 61*(pop > 17000)
    test2 = 67*(pop > 4900)
    test3 = 71*(dist > 21)
    test4 = 73*(dist > 17)
    test5 = 79*(pop > 44500)
    test6 = 83*(dist > 16)
    test7 = 89*(dist > 6)
    test8 = 97*(pop > 82000)
    
    chemin1 = test1 + test2 + test3
    chemin2 = test1 + test2 + test3 + test4
    chemin3 = test1 + test2
    chemin4 = test1 + test5 + test6
    chemin5 = test1 + test5 + test7
    chemin6 = test1 + test5 + test7 + test8
    
    resultat = ""
    if chemin1 == 71:
        resultat = "50"
    if chemin2 == 0:
        resultat = resultat + "50"
    if chemin2 == 73:
        resultat = resultat + "30"
    if chemin3 == 67:
        resultat = resultat + "30"
    if chemin4 == 144:
        resultat = resultat + "30"
    if chemin4 == 61:
        resultat = resultat + "15"
    if chemin5 == 140:
        resultat = resultat + "15"
    if chemin6 == 229:
        resultat = resultat + "15"
    if chemin6 == 326:
        resultat = resultat + "10"
    
    return (resultat)

#%%
class ListeCommunes(dict):
    """Dictionnaires des communes pour lesquelles compter du temps"""
    def __init__(self):
        self.database='AppliVitesse.db'
        self.communes={}
        self.inc=1
        self.dep=""
        self.com=""
        self.dist=0.0

    def ajoute(self,dep, com, dist):
        
        """Ajout d'une commune dans le dictionnaire.
        Paramètres à fournir:
            1 - numéro de département (caractère)
            2 - numéro de commune (caractère)
            3 - distance du domicile à la commune (numérique . = sep décimal)
            
        Ajoute la population et le nom de la commune à l'entrée du dictionnaire
        """

        
        with UseDatabase(self.database) as cursor:
            _SQL = """
            select nomcom, pop from population 
            where (dep = '%s' and com = '%s')
            """%(dep,com)
            cursor.execute(_SQL)
            self.curs = cursor.fetchone()
            nomcom = self.curs[0]
            pop = self.curs[1]
        nomrow = "row_"+str(self.inc)
        self.communes[nomrow] = [dep, com, nomcom, int(pop) , float(dist)]
        self.inc += 1
    
    def supprcommune(self,key):
        """Supprime une commune identifiée par son numéro d'observation"""
        self.communes.pop(key)
    
    def moyennes(self):
        """Calcule les population et distances moyennes des communes présentes
        dans le dictionnaire"""
        table = pd.DataFrame.from_dict(self.communes, orient='index')
        self.popmoy = round(table[3].mean(),ndigits=1)
        self.distmoy = round(table[4].mean(),ndigits=1)
        return (self.popmoy,self.distmoy)
#%%

class Application(object):
    def __init__(self):
        """Constructeur de la fenêtre principale"""
        self.root = Tk()
        self.root.title('Attribuer une vitesse à un nouvel enquêteur')
        Label(self.root, text='Application d\'aide au choix de la vitesse pour un nouvel enquêteur', fg='red').grid(row = 1 , column = 1, columnspan=2,padx=3,pady=3)

        # Initialise la liste des communes
        self.listecommunes=ListeCommunes()

        # zone de saisie des données d'une nouvelle commune boutons
#        self.saisiecommune()
        self.afficheliste()
        bou3 = Button(self.root, text='Exécuter', command=self.resultat).grid(row = 13 ,column = 1,padx=3,pady=3)
        bou2 = Button(self.root, text='Quitter', command=self.root.destroy).grid(row = 13 ,column = 2,padx=3,pady=3)
        self.saisiecommune()
        self.root.mainloop()
        
    def afficheliste(self):
        Label(self.root, text = """Liste des communes servant à l'estimation de la vitesse : """).grid(row = 9 , columnspan=2 , pady = 5 ,padx = 10)
        self.txt = Text(self.root , width = 50 , height =10 , bg = 'ivory')
        self.txt.insert(INSERT, repr(self.listecommunes.communes))
        self.txt.grid(row = 10 , columnspan = 3 , pady = 3)
        
        
    def saisiecommune(self):
        Label(self.root , text = """Pour ajouter une commune de collecte, 
              veuillez remplir les champs suivants : """).grid(row = 3 ,column = 1, columnspan = 2 , pady = 10)

        # Entrée des valeurs pour une nouvelle commune
        
        Label(self.root , text = 'Numero de département : ').grid(row = 4 ,column = 1,sticky = E)
        Label(self.root , text = 'Numero de commune : ').grid(row = 5 ,column = 1,sticky = E)
        Label(self.root , text = 'Distance Domicile - comm (en km) : ').grid(row = 6 ,column = 1,sticky = E)

        self.entree1 = Entry(self.root)
        self.entree1.grid(row = 4 ,column = 2,padx=10)
        self.entree2 = Entry(self.root)
        self.entree2.grid(row = 5 ,column = 2,padx=10)
        self.entree3 = Entry(self.root)
        self.entree3.grid(row = 6 ,column = 2,padx=10)

        bou1 = Button(self.root, text='Ajouter une commune', command=  self.recuperevaleurs).grid(row = 7 ,column = 1,padx=3,pady=3)
        bou4 = Button(self.root, text='Retirer une commune', command=  self.supprimecom).grid(row = 7 ,column = 2,padx=3,pady=3)
        
    def supprimecom(self):

        try:
            key = [a for a  in self.listecommunes.communes.keys()].pop()
            self.listecommunes.supprcommune(str(key))
        except:
            self.txt.insert(INSERT,"Il n'y a aucune commune à enlever!")
        else:
            self.afficheliste()
        
    def recuperevaleurs(self):
        self.dep = self.entree1.get()
        self.com = self.entree2.get()
        self.dist = self.entree3.get()
        self.listecommunes.ajoute(self.dep,self.com,self.dist)
        self.afficheliste()

    def resultat(self):
        self.label = Text(self.root , width = 50 , height =6 , bg = 'ivory')
        try:
            self.listecommunes.moyennes()
        except:
            texte = "Il faut rentrer les données d'au moins une commune pour avoir un résultat."
        else:
            distmoy = self.listecommunes.distmoy
            popmoy = self.listecommunes.popmoy
            vitesse = vitesseopale(popmoy , distmoy)
            
            
            texte = """Valeurs moyennes calculées :
Population moyenne communale : {popmoy} hab.
Distance moyenne entre le domicile et les communes de collecte : {distmoy} kms.

La vitesse de l'enquêteur estimée : {vitesse} km/h.""".format(distmoy=distmoy,popmoy=popmoy,vitesse = vitesse)
        self.label.insert(INSERT, texte)
        self.label.grid(row = 11 , pady=3 , columnspan = 3)

if __name__=="__main__":
    from tkinter import *
    import os
    import pandas as pd 
    # Nécessaire de mettre le répertoire courant comme répertoire de travail pour permettre l'importation de DBcm.py
    #os.chdir('./')
    from DBcm import UseDatabase
    
    
    appli = Application()
    









   
    

    
      
