"""Dewarp a given image."""

# -*- coding: utf-8 -*-
# -----------------------------------------
# author      : Cinmoy Das
# mail        : cinmoy98@gmail.com
# date        : 13.01.2020
# -----------------------------------------

import cv2 as cv
import imutils as imtl
import numpy as np
from imutils.perspective import four_point_transform


def dewarp_book(image):
    """Fix and image warp (dewarp an image).

    Parameters
    ----------
    image : numpy ndarray
        The input image.

    Returns
    -------
    numpy ndarray
        The dewarped image.

    """
    # get input image ration to keep best output resolution quality
    ratio = image.shape[0] / 500.0
    # copy source image for filter operations
    orig = image.copy()
    # resize the input image
    image = imtl.resize(image, height=500)

    
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    '''cv.namedWindow('gray image', cv.WINDOW_NORMAL) 
    cv.resizeWindow('gray image', 1080, 720) 
    cv.imshow("gray image", gray )
    #cv.imshow("warped image", boximg[0] )
    cv.waitKey(0)
    cv.destroyAllWindows()
    '''
    sigma = 0.33

    
    v = np.median(image)

   
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv.Canny(image, lower, upper)
    '''cv.namedWindow('edged image', cv.WINDOW_NORMAL) 
    cv.resizeWindow('edged image', 1080, 720) 
    cv.imshow("edged image", edged )
    #cv.imshow("warped image", boximg[0] )
    cv.waitKey(0)
    cv.destroyAllWindows()'''

   
    '''kernel = np.ones((5,5),np.uint8)
    edged = cv2.dilate(edged,kernel,iterations = 1)'''

   
    cnts = cv.findContours(edged.copy(), cv.RETR_LIST,
                            cv.CHAIN_APPROX_SIMPLE)
    cnts = imtl.grab_contours(cnts)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:5]    
    for c in cnts:
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break    
    ###########################################################################
    '''cnt=cv.drawContours(image,[screenCnt], 0 , (0,255,0), 2)
    cv.namedWindow('approx image', cv.WINDOW_NORMAL) 
    cv.resizeWindow('approx image', 1080, 720) 
    cv.imshow("approx image", cnt )
    #cv.imshow("warped image", boximg[0] )
    cv.waitKey(0)
    cv.destroyAllWindows()'''
    ###########################################################################
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    '''cv.namedWindow('warped image', cv.WINDOW_NORMAL) 
    cv.resizeWindow('warped image', 1080, 720) 
    cv.imshow("warped image", warped )
    #cv.imshow("warped image", boximg[0] )
    cv.waitKey(0)
    cv.destroyAllWindows()'''
    ###########################################################################
    return warped
