# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:54:32 2018

@author: herve
"""


import numpy as np
import cv2 
from keras.models import load_model
from keras.preprocessing.image import img_to_array


class BoardAnalyse() :

    def __init__(self) :
        self.__im=0
        self.__imWraped=0
        self.__matrice=0
        self.__modelX = load_model('croix.mdl')
        self.__modelO = load_model('rond.mdl')
        self.__numMove=0
        self.__boardState=['.','.','.','.','.','.','.','.','.']
        self.__boardStateTemp=['.','.','.','.','.','.','.','.','.']
        self.__repetition=0

    def imRead(self,image) :
        self.__im=image

    def readBoard(self,image):
        self.imRead(image)
        self.adjustImage()
#        self.display("image traitee", 1)
        return self.__imWraped
#        print ('Press any key to validate stettings')
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
    
    def display(self,title,mode) :
        if mode==0 : img=self.__im
        elif mode==1 :  img=self.__imWraped  
        cv2.imshow(title,img)
        
        
    def calibrateCam(self,image):
        self.imRead(image)
        self.displayCorners()
        self.getMatrice()
        print ('Press any key to continue')
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.adjustImage()
        self.display("Plateau redresse",1)



#        cv2.destroyAllWindows()
    
    
    def displayCorners(self):
        corners=self.cornersDetection()
        self.__im[corners>0.1*corners.max()]=255 #Corners markers
        self.display('Corners',0)
    
    def cornersDetection(self):
        gray=cv2.GaussianBlur(self.__im, (3, 3), 0)
        ret,thresh=cv2.threshold(gray,85,255,cv2.THRESH_BINARY)
        corners=cv2.cornerHarris(thresh,4,3,0.05) #Corners detection
        corners[corners<0.1*corners.max()]=0.0                
        return corners
        
    
    def fourCornersDetection(self):
        corners=self.cornersDetection()
        rect=np.zeros((4,2),dtype="float32")
        mask=np.zeros(corners.shape)
        mask[corners>0]=1.0
        pos=np.argwhere(mask)
        rect[0]=pos[np.argmin(pos.sum(axis=1))]
        rect[2]=pos[np.argmax(pos.sum(axis=1))]
        rect[1]=pos[np.argmin(np.diff(pos,axis=1))]
        rect[3]=pos[np.argmax(np.diff(pos,axis=1))]
        for i in range(4):
            rect[i][0],rect[i][1]=rect[i][1],rect[i][0]
        return rect

    def adjustImage(self):
        img = cv2.warpPerspective(self.__im, self.__matrice, (72,72))
        image=cv2.GaussianBlur(img, (3, 3), 0)
        _,image=cv2.threshold(img,110,255,cv2.THRESH_BINARY)
        image = cv2.resize(image, (72, 72))
#        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self.__imWraped=image
    
    def getMatrice(self):
        size=np.float32([[0,0],[0,72],[72,72],[72,0]])
        rect=self.fourCornersDetection()
        self.__matrice = cv2.getPerspectiveTransform(rect,size)
        
    def extractCells(self,image):
        self.readBoard(image)
        result=self.__imWraped
        screen=[result[:24,:24],result[:24,24:48],result[:24,48:72],result[24:48,:24],result[24:48,24:48],result[24:48,48:72],result[48:72,:24],result[48:72,24:48],result[48:72,48:72]]
        return screen
        
    def getCellsValues(self,image):
        result=[]
        cells=self.extractCells(image)
        for i in range(9):
            image = cells[i]
            image=cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

            image=cv2.resize(image, (24, 24))
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            (notCross, Cross) = self.__modelX.predict(image)[0]
            (notCircle,Circle) = self.__modelO.predict(image)[0]
            if Cross> 0.7 :
                result.append("X")
            elif Circle>0.7 :
                result.append("O")
            else :
                result.append(".")
        print("plateau lu :",result)
        return result


                
                



