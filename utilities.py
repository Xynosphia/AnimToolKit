import os
import sys
import re

import maya.cmds as cmds
from collections import defaultdict
import math

# Directory containing utilities.py
script_root = os.path.dirname(os.path.abspath(__file__))

# UI file path
ui_file = os.path.join(script_root, 'ui', 'AnimToolKit.ui')


# dictionary

cam_dict = {'CAM_SHAPE': [],
            'SUBJECT': [],
            'SELECTED': [],
            }

# utility functions and other functions 

def get_scene_cam():
    # for choosing camera
    cameras = cmds.ls(type='camera')
    exclude = ["frontShape","perspShape","sideShape","topShape","bottomShape","leftShape","backShape"]
    user_cam = list(set(cameras) - set(exclude))
    return user_cam

def get_selected_cam():
    # selected cam
    return cmds.ls(selection=True, type='camera')

def get_scene_geo():
    # for choosing cubject
    geo = cmds.ls(geometry=True)
    return geo

def get_selected_geo():
    # for choosing selected subject
    selgeo = cmds.ls(selection=True)
    return selgeo

def get_memory():
    # for memory pressure bar at the bottom
    totalMemory = cmds.memory(physicalMemory=True, gigaByte=True)
    freeMemory = cmds.memory(freeMemory=True, gigaByte=True)
    usedMemory = totalMemory - freeMemory
    return usedMemory, totalMemory, freeMemory 
    #can i use it less frequently to reduce performance impact? maybe every 10 mins or when a button is pressed?


def get_distance_to_active_camera():
    # for getting subject
    subject = get_selected_geo 
   #  if not subject: 
        #INSERT SELECTED GEO FROM BUTTON
    
    # Subject world space position
    subj_pos = cmds.xform(subject, query=True, worldSpace=True, rotatePivot=True)

    # for getting active camera
    active_panel = cmds.getPanel(withFocus=True)
    if cmds.getPanel(typeOf=active_panel) == "modelpanel":
        active_cam = cmds.modelPanel(active_panel, query=True, camera=True)
    else:
        # FALLBACK
        active_cam = "perspShape"

    # Camera World space position
    cam_pos = cmds.xform(active_cam, query=True, worldSpace=True, rotatePivot=True) 

    distance = math.dist(cam_pos, subj_pos)
    return distance

def camera_focus():
    # Camera focal distance
    user_cam = get_selected_cam
    distance = get_distance_to_active_camera
    focus = cmds.camera(get_selected_cam, depthOfField=True, focusDistance=get_distance_to_active_camera)
    return focus

def create_locator():
    locator = cmds.spaceLocator(name='Locator', radius=1.0)
    return locator

def locator_to_subject():
    locator = create_locator
    subject = get_selected_geo
    # MATCH XFROM
    xform = cmds.matchTransform('locator','subject')
    return xform

def bake_sim():
    # LINK THE CAM
    bake = cmds.bakeSimulation()

def smart_bake():
    # LINK THE CAM
    bake = cmds.bakeSimulation(sr=True)













    












   




