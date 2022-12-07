#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 13:51:33 2022

@author: laura
"""

import math

class Tracked:
    def __init__(self, centerx, centery, x,y,w,h,ident):
        self.x = x
        self.y = y
        self.center_x = centerx
        self.center_y = centery
        self.w = w
        self.h = h
        self.direc = -1 # 1 si puja, 0 si baixa
        self.id = ident
        self.counter_frames = 0
        self.life_frames = 1


class Tracker:
    def __init__(self, limit):
        self.center_points = {}
        self.id_count = 1
        self.limit = limit
        self.id_counted = []
        self.up = 0
        self.down = 0
        
    def update(self, objects_rect):
        objects_bbs_ids = []

        for rect in objects_rect:
            x, y, w, h = rect
            center_x = (x + x + w) // 2
            center_y = (y + y + h) // 2

            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(center_x - pt.center_x, center_y - pt.center_y)
                if dist < 25:

                    if(pt.center_y > center_y):
                        pt.direc = 1
                    else:
                        pt.direc = 0
                    
                    pt.life_frames += 1
                    pt.center_x = center_x
                    pt.center_y = center_y
                    pt.x = x
                    pt.y = y
                    
                    if(pt.center_y >= self.limit and id not in self.id_counted):
                        if(pt.direc == 1 and pt.life_frames > 15):
                            self.up += 1
                            self.id_counted.append(id)
                        elif(pt.direc == 0 and pt.life_frames > 75):
                            self.down += 1
                            self.id_counted.append(id)
                    
                    print(self.center_points)
                        
                    objects_bbs_ids.append([x, y, w, h, id])     
                    same_object_detected = True
                    break
           
            if same_object_detected is False:
               t = Tracked(center_x, center_y, x,y,w,h, self.id_count)  
               self.center_points[self.id_count] = t                  
               objects_bbs_ids.append([x, y, w, h, self.id_count])       
               self.id_count += 1

        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            var,var,var,var, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
            
        for id, pt in self.center_points.items():
            if id not in new_center_points and pt.counter_frames<50:
                new_center_points[id]=pt
                pt.counter_frames += 1
            elif id in new_center_points:
                pt.counter_frames = 0

        self.center_points = new_center_points.copy()
        return objects_bbs_ids
