# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 22:34:35 2020

@author: ASUS
"""

from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse as ap
import imutils as imtl
import cv2 as cv
import dewapper


def get_answer(warped):
    ##############################################################################
    #img = cv.imread('images/pic30.jpg')
    #warped = dewapper.dewarp_book(img)
    
    gray=cv.cvtColor(warped,cv.COLOR_BGR2GRAY)
    blurred=cv.GaussianBlur(gray,(5,5),0)
    edged=cv.Canny(blurred,75,200)
    # Declaring the array of answers // index = question number //  Value = answer number ( 0=A , 1=B , 2=C , 3=D ) 
    answer=[]
    #
    # Total question number
    bblcnt=35
    #
    # For checking the total processed answer.
    bblchkcnt=0
    #
    ##############################################################################
    
    
    
    ##############################################################################
    ret, thresh = cv.threshold(gray, 127, 255, 0)
    cntr, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cnt=cv.drawContours(warped, cntr, -1, (0,255,0), 2)
    
    #The outer box of the qustions//Pretended to be 2 box in the OMR sheet
    boxcnts = []
    #
    for c in cntr:
        (x , y , w , h) = cv.boundingRect(c)
        ar = w/float(h)
        if w>=800 and h>=3500 and ar>=0.20 and ar<=0.30:
            boxcnts.append(c)
    #print(len(boxcnts))
    #cnt=cv.drawContours(warped, boxcnts, -1, (0,255,0), 2)
    boxcnts = contours.sort_contours(boxcnts)[0]
    ##############################################################################
    
    
    
    ##############################################################################
    # for storing the box images from contours
    boximg=[]
    
    for c in boxcnts:
        (x , y , w , h) = cv.boundingRect(c)
        boxcnt=warped[y:y+h,x:x+w]
        boximg.append(boxcnt)
    coun=0
    for d in range(len(boximg)):
        #print(d)
        gray=cv.cvtColor(boximg[d],cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        cnts,hierarchy = cv.findContours(thresh.copy(),cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    
        bubbles=[]
        for c in cnts:
            (x , y , w , h) = cv.boundingRect(c)
            ar = w/float(h)
            if w>=105 and w<=130 and h>=105 and h<=130 and ar>=0.9 and ar<=1.2:
                bubbles.append(c)
            #cnt=cv.drawContours(boximg[d],bubbles, -1, (0,255,0), 3)
        #print(len(bubbles))
            #qncn=len(bubbles)/4
    
    
        bubbles = contours.sort_contours(bubbles,method="top-to-bottom")[0]
        for (q,i) in enumerate(np.arange(0 , len(bubbles), 4),coun):
            cnts = contours.sort_contours(bubbles[i:i+4])[0]
            bubbled = None
            for (j , c) in enumerate(cnts):
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv.drawContours(mask , [c] , -1, 255, -1)
                mask = cv.bitwise_and(thresh , thresh , mask= mask) 
            
                total = cv.countNonZero(mask)
                #print(total)
                if bubbled is None or total > bubbled[0]:
                    coun=coun+1
                    bubbled = (total , j)
                    answer.insert(q,j)
        coun=25
    
    finalanswer=[]
    for i in range(bblcnt):
        finalanswer.insert(i,answer[i])
    return finalanswer