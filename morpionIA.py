# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 21:49:10 2018

@author: herve
"""

#from drawGraph import*

class morpionIA() :
    __nom=None
    __joueur=None
    __board=None    
    
    def __init__(self,plateau):
        self.__nom='Nao'
        self.__joueur='O'
        self.__board=plateau
#        self.__graph=drawGraph()
        print("Joueur", self.__nom, "cree avec jetons", self.__joueur)
    
    def id(self):
        return self.__nom
        
        
    def adversaire(self,joueur):
        #Indiquer le joueur adverse du joueur qui joue
        if joueur=='X':
            return 'O'
        else :
            return'X'

    def evaluationStatique(self):
        #Evalue la situation du plateau (+10,-10,0)
        gagne,qui=self.__board.analyserPlateau()    
        
        if qui==self.__joueur and gagne==True :
            score=10
        elif qui==self.adversaire(self.__joueur) and gagne==True :
            score=-10
        elif self.__board.plateauComplet()==True:
            score=0
        else : score=None
        return score
    
    def evaluerCoup(self,joueur,positionCoup):
        #Evaluer un nouveau coup
        self.__board.jouer(positionCoup,joueur)    
        score=self.evaluationStatique()
        return score

                 
    def minmax(self,joueur,level):
    #Identifier le meilleur coup (algo Min_Max)
        
        if joueur ==self.__joueur :
            meilleurScore=-20
        else : meilleurScore =20
        coupPrecedent=list(self.__board.etat())    
        for i in self.__board.coupsRestants():
            score=self.evaluerCoup(joueur,i)

            if score==None:
                nextLevel=level+1
                score,_=self.minmax(self.adversaire(joueur),nextLevel)

            if joueur==self.__joueur and score>meilleurScore:
                meilleurScore=score
                position=i
        
            if joueur==self.adversaire(self.__joueur) and score<meilleurScore:
                meilleurScore=score
                position=i


            self.__board.jouer(i,'.')
        return meilleurScore,position
    
    def jouer(self):
        
        return self.minmax(self.__joueur,1)[1]

