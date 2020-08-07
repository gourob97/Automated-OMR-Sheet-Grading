# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 22:34:29 2020

@author: ASUS
"""

from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse as ap
import imutils as imtl
import cv2 as cv

ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

################################################
image=cv.imread('images/omr.png')
gray=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
blurred=cv.GaussianBlur(gray,(5,5),0)
edged=cv.Canny(blurred,75,200)
################################################




########################################################################################
cntr=cv.findContours(edged.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
cntr=imtl.grab_contours(cntr)
docCnt=None

if len(cntr) > 0:
    cntr = sorted(cntr, key=cv.contourArea, reverse=True)
    for c in cntr:
        peri=cv.arcLength(c,True)
        approx=cv.approxPolyDP(c,0.02*peri,True)
        if len(approx) == 4:
            docCnt = approx
            break
#cnt=cv.drawContours(image,[docCnt], 0, (0,255,0), 1)

paper = four_point_transform(image,docCnt.reshape(4,2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))
########################################################################################




########################################################################################
thresh = cv.threshold(warped, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
cnts = cv.findContours(thresh.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
cnts=imtl.grab_contours(cnts)
questionCnts = []
#cnt=cv.drawContours(paper,cnts, -1, (0,255,0), 1)
for c in cnts:
    (x , y , w , h) = cv.boundingRect(c)
    ar = w/float(h)
    if w>=20 and h>=20 and ar>=0.9 and ar<=1.1:
        questionCnts.append(c)
    
#print(len(questionCnts))    
########################################################################################




########################################################################################
questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]
print(len(questionCnts))
correct = 0
t=0
for (q,i) in enumerate(np.arange(0 , len(questionCnts), 5)):
    
    cnts = contours.sort_contours(questionCnts[i:i+5])[0]
    bubbled = None
    
    for (j , c) in enumerate(cnts):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv.drawContours(mask , [c] , -1, 255, -1)
        mask = cv.bitwise_and(thresh , thresh , mask= mask)
        total = cv.countNonZero(mask)
        if bubbled is None or total > bubbled[0]:
            bubbled = (total , j)
    print(bubbled)
    color = (0, 0, 255)
    k = ANSWER_KEY[q]        
    if(k==bubbled[1]):
        color = (0,240,0)
        correct += 1
    cv.drawContours(paper, [cnts[k]], -1, color, 2)    
######################################################################################## 



################################################
score = correct
print("[INFO] score: {:.2f}".format(score))
cv.putText(paper, "{:.2f}".format(score), (10, 30),
	cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0,0 ), 2)  
cv.imshow('gray image',paper)
cv.waitKey(0)
cv.destroyAllWindows()
################################################