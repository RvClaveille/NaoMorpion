# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:51:47 2018

@author: herve
"""
import os
import time
class plateau :

    __plateau=9*[]
#Variables static de la fonction MAJ
    __check=0
    __time=0
    
  
    
    def __init__(self):
        self.nouveauPlateau()
        self.__time=time.time()+2
        self.__check=0
        
    def tourDeJouer(self):
        #Indiquer le joueur qui doit jouer
        if (self.__plateau.count('X')==self.__plateau.count('O'))  :
            return('O')
        else:
            return('X')
    
    def jouer(self,positionCoup,joueur):
#Joouer le coup du joueur sur le plateau
        self.__plateau[positionCoup]=joueur

    def afficherGrille(self):
        #Affiche l'etat du plateau sur la console
        os.system("clear") 
        print(self.__plateau[0],"|",self.__plateau[1],"|",self.__plateau[2],"|")
        print("-----------")
        print(self.__plateau[3],"|",self.__plateau[4],"|",self.__plateau[5],"|")
        print("-----------")
        print(self.__plateau[6],"|",self.__plateau[7],"|",self.__plateau[8],"|")
    
    def MAJ(self,board):
        #Mettre a jour le plateau en verifiant 10 fois a qla qualite de lecture
        nbDifferences=0
        rythm=[1, 0.5, 0.5, 0.2, 0.2, 0.2 ]
        #Jouer le coup du joueur sur le plateau
        currentTime=time.time()
        if currentTime>self.__time:
            self.__time=time.time()+rythm[self.__check]
            for i in range(9):
                if self.__plateau[i]!=board[i] : nbDifferences+=1
            if nbDifferences==1: self.__check+=1
            else : self.__check=0
        if self.__check==6:
            self.__check=0
            self.__plateau=board
            print(self.__plateau)

    
    def etat(self):
        return self.__plateau
     
    def nouveauPlateau(self):
        self.__plateau=9*['.']
        
        
    def plateauComplet(self):
        #Identifier la situation plateau plein

        if "." in self.__plateau :
            return(False)
        else :
            return(True)

    def coupsRestants(self):
        #Lister les coups possible
        j=0
        indexes=[]
        for i in self.__plateau:
            if i=='.':
                indexes.append(j)
            j+=1
        return(indexes)

    def analyserPlateau(self):
        table=self.__plateau
        #Identifier le vainqueur de la partie
        coupsGagnants=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for i in coupsGagnants:
            if (table[i[0]]=='O' or table[i[0]]=='X') and table[i[0]]==table[i[1]] and table[i[0]]==table[i[2]]:
                return (True,table[i[0]])
            
        return(False,None)
    
    def finDePartie(self):
        if self.plateauComplet()==True : return (True,'0')
        elif self.analyserPlateau()[0]==True : return self.analyserPlateau()
        else : return (False,None)
