# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 20:16:16 2020

@author: ASUS
"""
import cv2 as cv
import dewapper

import generate_answer

source_image = cv.imread("images/pic30.jpg")
warped = dewapper.dewarp_book(source_image)
answer=generate_answer.get_answer(warped)


cv.namedWindow('warped image', cv.WINDOW_NORMAL) 
cv.resizeWindow('warped image', 1080, 720) 
cv.imshow("warped image", warped )
cv.waitKey(0)
cv.destroyAllWindows()
