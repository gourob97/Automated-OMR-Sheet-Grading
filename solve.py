# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:34:11 2020

@author: ASUS
"""
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
import generate_answer


##############################################################################
img = cv.imread('images/pic30.jpg')
warped = dewapper.dewarp_book(img)

gray=cv.cvtColor(warped,cv.COLOR_BGR2GRAY)
blurred=cv.GaussianBlur(gray,(5,5),0)
edged=cv.Canny(blurred,75,200)
answer=generate_answer.get_answer(warped)
##############################################################################



##############################################################################
ret, thresh = cv.threshold(gray, 127, 255, 0)
cntr, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#cnt=cv.drawContours(warped, cntr, -1, (0,255,0), 2)
boxcnts = []
for c in cntr:
    (x , y , w , h) = cv.boundingRect(c)
    ar = w/float(h)
    if w>=800 and h>=3500 and ar>=0.20 and ar<=0.30:
        boxcnts.append(c)
    #print(len(boxcnts))
    #cnt=cv.drawContours(warped, boxcnts, -1, (0,255,0), 2)
boxcnts = contours.sort_contours(boxcnts)[0]

boximg=[]
    
for c in boxcnts:
    (x , y , w , h) = cv.boundingRect(c)
    boxcnt=warped[y:y+h,x:x+w]
    boximg.append(boxcnt)
coun=0

gray=cv.cvtColor(boximg[0],cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
cnts,hierarchy = cv.findContours(thresh.copy(),cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)

bubbles=[]
for c in cnts:
    (x , y , w , h) = cv.boundingRect(c)
    ar = w/float(h)
    if w>=105 and w<=130 and h>=105 and h<=130 and ar>=0.9 and ar<=1.2:
        bubbles.append(c)
    cnt=cv.drawContours(boximg[0],bubbles, -1, (0,255,0), 3)
print(len(bubbles))
#qncn=len(bubbles)/4

correct=0
bubbles = contours.sort_contours(bubbles,method="top-to-bottom")[0]
for (q,i) in enumerate(np.arange(0 , len(bubbles), 4)):
    cnts = contours.sort_contours(bubbles[i:i+4])[0]
    bubbled = None
    for (j , c) in enumerate(cnts):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv.drawContours(mask , [c] , -1, 255, -1)
        mask = cv.bitwise_and(thresh , thresh , mask= mask)
        '''cv.namedWindow('warped image', cv.WINDOW_NORMAL) 
        cv.resizeWindow('warped image', 1080, 720) 
        cv.imshow("warped image",mask)
        cv.waitKey(0)
        cv.destroyAllWindows()
        '''
        total = cv.countNonZero(mask)
        #print(total)
        if bubbled is None or total > bubbled[0]:
            bubbled = (total , j)
    color = (0, 0, 255)
    k = answer[q]
    #print(k)
    #print(bubbled[1])        
    if(k==bubbled[1]):
        color = (0,240,0)
        correct += 1
    cv.drawContours(boximg[0], [cnts[k]], -1, color, 10)
print(correct)

score = correct
print("[INFO] score: {:.2f}".format(score))
cv.putText(warped, "{:.2f}".format(score), (2850, 3520),
	cv.FONT_HERSHEY_SIMPLEX, 5, (255, 0,0 ), 20)

cv.namedWindow('warped image', cv.WINDOW_NORMAL) 
cv.resizeWindow('warped image', 1080, 720) 
cv.imshow("warped image",warped)
cv.waitKey(0)
cv.destroyAllWindows()

