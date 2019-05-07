# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:52:44 2018

@author: herve
"""
from morpionIA import*
from plateau import*
from robotNao import *
import random
import cv2
import copy

def jouerMorpion():
    board=plateau()
    Nao=robotNao("192.168.1.4", 9559)
    NaoIA=morpionIA(board)
    Nao.initRobot()

    Nao.captureBoard()

    flag=0
    invitAJouer=["C'est a vous de jouer", "C'est a vous", "Vous pouvez jouer", "Allez y"]   
    while board.finDePartie()[0]==False :
        board.MAJ(Nao.readBoard())
        #    print(board.etat())
        stateBoard=copy.deepcopy(board.etat())
        expectedBoard=copy.deepcopy(stateBoard)
        if board.tourDeJouer()=='O':
            flag=0
            Nao.ledsOn()
            #        time.sleep(random.randint(1,5))
            coup=NaoIA.jouer()
            
            Nao.jouer(coup,board.etat())
            expectedBoard=copy.deepcopy(stateBoard)
            expectedBoard[coup]='O'
            while board.etat()!=expectedBoard :
                board.MAJ(Nao.readBoard())
                #            print(board.etat())
                if board.etat()!=expectedBoard and board.etat()!=stateBoard:
                    print("Le pion est mal place, verifiez")
        elif board.tourDeJouer()=='X' and flag==0 : 
            flag=1
            numCoup=board.etat().count('X')
        
            Nao.dire(invitAJouer[numCoup])
                
    Nao.finDePartie(board.finDePartie()[1])
    NaoIA=None
    board=None
    Nao=None
    
jouerMorpion()
