# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 22:34:35 2020

@author: ASUS
"""

from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
from numpy import array
import argparse as ap
import imutils as imtl
import cv2 as cv
import dewapper
import generate_answer
import generate_roll
##############################################################################
img = cv.imread('images/pic36.jpg')
warpe = dewapper.dewarp_book(img)

roll=generate_roll.get_roll(warpe)
print(roll)
#answer=generate_answer.get_answer(warpe)
answer=[1, 2, 1, 2, 0, 1, 2, 1, 1, 3, 2, 2, 0, 1, 1, 1, 3, 0, 0, 1, 2, 1, 2, 3, 3, 1, 0, 2, 1, 3, 0, 3, 0, 2, 1]
#answer = array(answer)
print(answer)

img = cv.imread('images/pic36.jpg')
warped = dewapper.dewarp_book(img)

gray=cv.cvtColor(warped,cv.COLOR_BGR2GRAY)
blurred=cv.GaussianBlur(gray,(5,5),0)
edged=cv.Canny(blurred,75,200)
# Declaring the array of answers // index = question number //  Value = answer number ( 0=A , 1=B , 2=C , 3=D ) 


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

cnt=cv.drawContours(warped, boxcnts, -1, (0,255,0), 20)
cv.namedWindow('bubble outer box image', cv.WINDOW_NORMAL) 
cv.resizeWindow('bubble outer box image', 1080, 720) 
cv.imshow("bubble outer box image", cnt )
#cv.imshow("warped image", boximg[0] )
cv.waitKey(0)
cv.destroyAllWindows()

boxcnts = contours.sort_contours(boxcnts)[0]
##############################################################################



##############################################################################
# for storing the box images from contours
boximg=[]

for c in boxcnts:
    (x , y , w , h) = cv.boundingRect(c)
    boxcnt=warped[y:y+h,x:x+w]
    boximg.append(boxcnt)
correct=0
coun=0
for d in range(len(boximg)):
    #print(d)
    gray=cv.cvtColor(boximg[d],cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    cnts,hierarchy = cv.findContours(thresh.copy(),cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    
    #cnt=cv.drawContours(warped, boxcnts, -1, (0,255,0), 2)
    cv.namedWindow('bubble outer box thresh', cv.WINDOW_NORMAL) 
    cv.resizeWindow('bubble outer box thresh', 1080, 720) 
    cv.imshow("bubble outer box thresh", thresh )
    #cv.imshow("warped image", boximg[0] )
    cv.waitKey(0)
    cv.destroyAllWindows()

    bubbles=[]
    for c in cnts:
        (x , y , w , h) = cv.boundingRect(c)
        ar = w/float(h)
        if w>=105 and w<=130 and h>=105 and h<=130 and ar>=0.9 and ar<=1.2:
            bubbles.append(c)
        cnt=cv.drawContours(boximg[d],bubbles, -1, (0,255,0), 3)
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
            '''cv.namedWindow('mask of each bubble', cv.WINDOW_NORMAL) 
            cv.resizeWindow('mask of each bubble', 1080, 720) 
            #cv.imshow("warped image", warped )
            cv.imshow("mask of each bubble",mask)
            cv.waitKey(0)
            cv.destroyAllWindows()'''
            total = cv.countNonZero(mask)
            #print(total)
            if bubbled is None or total > bubbled[0]:
                bubbled = (total , j)
        color = (0, 0, 255)
        #ansq = coun+q
        #print(q)
        if(q>34):
            break
        k = answer[q]
        if(k==bubbled[1]):
            color = (0,240,0)
            correct += 1
        cv.drawContours(boximg[d], [cnts[k]], -1, color, 20)
    coun=25

print(correct)

score = correct
print("[INFO] score: {:.2f}".format(score))
cv.putText(warped, "{:.2f}".format(score), (2887, 3826),
	cv.FONT_HERSHEY_SIMPLEX, 5, (255, 0,0 ), 20)
cv.putText(warped, "{:.0f}".format(int(roll)), (2898, 1005),
	cv.FONT_HERSHEY_SIMPLEX, 5, (255, 0,0 ), 20)

roll=1604092
correct = 25
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="omr"
)
mycursor = mydb.cursor()

sql = "INSERT INTO Marks (roll, mark) VALUES (%s,%s)"
val=(int(roll),int(correct))

mycursor.execute(sql,val)

mydb.commit()

cv.namedWindow('warped image', cv.WINDOW_NORMAL) 
cv.resizeWindow('warped image', 1080, 720) 
cv.imshow("warped image", warped )
#cv.imshow("warped image", boximg[0] )
cv.waitKey(0)
cv.destroyAllWindows()