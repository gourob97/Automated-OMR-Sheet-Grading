# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 16:31:39 2020

@author: Cinmoy Das Shubra

"""
# -----------------------------------------
# author      : Cinmoy Das
# mail        : cinmoy98@gmail.com
# date        : 13.01.2020
# -----------------------------------------


from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse as ap
import imutils as imtl
import cv2 as cv
import dewapper

##############################################################################
def get_roll(warped):    
    #img = cv.imread('images/pic36.jpg')
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
        if w>=800 and h>=1400 and ar>=0.58 and ar<=0.68:
            boxcnts.append(c)
    #print(len(boxcnts))
    '''cnt=cv.drawContours(warped, boxcnts, -1, (0,255,0), 40)
    cv.namedWindow('outer roll box contour', cv.WINDOW_NORMAL) 
    cv.resizeWindow('outer roll box contour', 1080, 720) 
    #cv.imshow("warped image", warped )
    cv.imshow("outer roll box contour", cnt )
    cv.waitKey(0)'''
    cv.destroyAllWindows()
    
    #boxcnts = contours.sort_contours(boxcnts)[0]
    ##############################################################################
    
    
    
    ##############################################################################
    # for storing the box images from contours
    boximg=[]
    
    for c in boxcnts:
        (x , y , w , h) = cv.boundingRect(c)
        boxcnt=warped[y:y+h,x:x+w]
        boximg.append(boxcnt)
        ##########################################################################
        '''cv.namedWindow('outer roll box image', cv.WINDOW_NORMAL) 
        cv.resizeWindow('outer roll box image', 1080, 720) 
        #cv.imshow("warped image", warped )
        cv.imshow("outer roll box image", boximg[0] )
        cv.waitKey(0)
        cv.destroyAllWindows() '''   
        ##########################################################################
    gray=cv.cvtColor(boximg[0],cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    ##########################################################################
    '''cv.namedWindow('threshed roll box image', cv.WINDOW_NORMAL) 
    cv.resizeWindow('threshed roll box image', 1080, 720) 
    #cv.imshow("warped image", warped )
    cv.imshow("threshed roll box image",thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()    '''
    ##########################################################################
    cnts,hierarchy = cv.findContours(thresh.copy(),cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    cnt=cv.drawContours(boximg[0],cnts, -1, (0,255,0), 2)
    
    ##########################################################################
    '''cv.namedWindow('threshed roll box image', cv.WINDOW_NORMAL) 
    cv.resizeWindow('threshed roll box image', 1080, 720) 
    #cv.imshow("warped image", warped )
    cv.imshow("threshed roll box image",cnt)
    cv.waitKey(0)
    cv.destroyAllWindows()  '''  
    ##########################################################################
    
    bubbles=[]
    for c in cnts:
        (x , y , w , h) = cv.boundingRect(c)
        ar = w/float(h)
        if w>=100 and w<=130 and h>=100 and h<=130 and ar>=0.9 and ar<=1.2:
            bubbles.append(c)
        #cnt=cv.drawContours(boximg[0],bubbles, -1, (0,255,0), 10)
    #print(len(bubbles))
        #qncn=len(bubbles)/4
    
    
    bubbles = contours.sort_contours(bubbles,method="left-to-right")[0]
    for (q,i) in enumerate(np.arange(0 , len(bubbles), 10)):
        cnts = contours.sort_contours(bubbles[i:i+10],method = "top-to-bottom")[0]
        bubbled = None
        for (j , c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv.drawContours(mask , [c] , -1, 255, -1)
            mask = cv.bitwise_and(thresh , thresh , mask= mask)
            ##########################################################################
            '''cv.namedWindow('mask of each bubble', cv.WINDOW_NORMAL) 
            cv.resizeWindow('mask of each bubble', 1080, 720) 
            #cv.imshow("warped image", warped )
            cv.imshow("mask of each bubble",mask)
            cv.waitKey(0)
            cv.destroyAllWindows() '''   
            ##########################################################################
            
            total = cv.countNonZero(mask)
            #print(total)
            if bubbled is None or total > bubbled[0]:
                #coun=coun+1
                bubbled = (total , j)
                answer.insert(q,j)
    answer = answer[0:6]
    roll = ''.join(map(str, answer))
    return roll
'''
finalanswer=[]
for i in range(bblcnt):
    finalanswer.insert(i,answer[i])
return finalanswer

cv.namedWindow('warped image', cv.WINDOW_NORMAL) 
cv.resizeWindow('warped image', 1080, 720) 
#cv.imshow("warped image", warped )
cv.imshow("warped image", boximg[0] )
cv.waitKey(0)
cv.destroyAllWindows()'''
