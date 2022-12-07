#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 12:57:02 2022

@author: laura
"""
import cv2
import numpy as np


from tracker import Tracker
tracker = Tracker(860)
  

vidcap = cv2.VideoCapture('divi33.mp4')
fgbg = cv2.createBackgroundSubtractorKNN()
success,image = vidcap.read()

frame_width = int(vidcap.get(3))
frame_height = int(vidcap.get(4))
   
size = (frame_width, frame_height)
   

result = cv2.VideoWriter('exemple.mp4', 
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         30, size)


frames = []
while success:

    area = np.array([(163, 511), (397, 506), (443, 947), (45, 952)])
    imAux = np.zeros(shape=(image.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area], -1, (255), -1)
    image_area = cv2.bitwise_and(image, image, mask=imAux)

    
    fgmask = fgbg.apply(image_area)
    otsu_threshold, image_result = cv2.threshold(fgmask, 150, 255, cv2.THRESH_BINARY)

    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(image_result, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    
    kernel2 = np.ones((5,2), np.uint8)
    img_dilatada = cv2.dilate(closing,kernel2,iterations=3)
    

    
    contorns,_ = cv2.findContours(img_dilatada.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    img_cnts = cv2.drawContours(img_dilatada.copy(),[area],-1,(255,0,255),2)
    
    img_cnts2 = cv2.drawContours(image.copy(),contorns,-1,(255,0,255),2)

    
    ll_contorns = []
    for cont in contorns:
        area_cont = cv2.contourArea(cont)
        print(area_cont)
        if(area_cont>5000 and area_cont<40000):
            x, y, w, h = cv2.boundingRect(cont)
            ll_contorns.append((x,y,w,h))
    
    boxes = tracker.update(ll_contorns)
    
    for box in boxes:
        xb,yb,wb,hb,iden = box
        punt1 = xb,yb
        punt2 = xb+wb, yb+hb
        cv2.rectangle(image, punt1, punt2, (255, 0, 0), 2)
        cv2.putText(image,str(iden), (xb, yb - 10),
        		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    
    cv2.line(image, (50, 860), (435, 860), (123, 81, 243), 3)
    
    res = "Cotxes que entren: "+str(tracker.down)
    res2 = "Cotxes que surten: "+str(tracker.up)
    
    text_size, _ = cv2.getTextSize(res, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    text_w, text_h = text_size
    
    cv2.rectangle(image, (10,10), (55+text_w,70+text_h), (0, 0, 0), -1)
    
    cv2.putText(image,res, (0 + 20, 0 + 40),
    		cv2.FONT_HERSHEY_SIMPLEX, 1, (124, 225, 122), 2)
    
    cv2.putText(image,res2, (0 + 20, 0 + 80),
    		cv2.FONT_HERSHEY_SIMPLEX, 1, (77, 77, 236), 2)

        
    
    result.write(image)
    

    success,image = vidcap.read()
    
    


print("guardant..")
vidcap.release()
result.release()


