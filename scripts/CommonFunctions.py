import cv2 as cv
from ProgramSettings import *
import numpy as np
from ColourCodes import  *

"""
**********************************************************************
	Regions of Interest
	-isolateROI(src,key:str) -> returns new MAT containgng ROI
	-drawROI(src,key, displayName) - > draws a single ROI directly onto src
	-drawROIs(src,displayNames) -> draws all rois directly onto src
**********************************************************************
"""
def convertROIValuesToPxls(src,key, displayName=False):
	global global_Settings
	
	if key in global_Settings["Camera_ROI_List"]:
		pos1 = ( global_Settings["Camera_ROI_List"][key][0].copy())
		pos2 = ( global_Settings["Camera_ROI_List"][key][1].copy())
		Color = global_Settings["Camera_ROI_List"][key][2]
		if(displayName == True):
			DrawText(src,key,[pos1[0],pos2[1]-2],textColour=Color)
		pos2 = ConvertPerCentToPxl(src,pos2)
		pos1 = ConvertPerCentToPxl(src,pos1)
		
		return pos1,pos2,Color
	
	return None,None,None
#returns bool,Mat
#src is a cv::Mat
#ROI is the key from the "Camera_ROI_List" dictionary
def isolateROI(src,key):
	global global_Settings

	if key in global_Settings["Camera_ROI_List"]:
		pos1,pos2,_ = convertROIValuesToPxls(src,key,False)
		#src[y1:y2, x1:x2]; dict values are [x1,y1],[x2,y2]
		roi = src[pos1[1]:pos2[1], pos1[0]:pos2[0]]
		
		return True,roi

	return False, roi

#merge a ROI back into it's source image
def mergeROI(src,key,roi):
	pos1,pos2,_ = convertROIValuesToPxls(src,key,False)
	if pos1 is not None:
		src[pos1[1]:pos2[1], pos1[0]:pos2[0]] = roi
	return

#draws a ROI selected from the global dictionary
def drawROI(src,key,displayName = True):
	pos1,pos2,Color = convertROIValuesToPxls(src,key,displayName)
	cv.rectangle(src, pos1, pos2,  ColourCodes['black'], thickness=4)
	cv.rectangle(src, pos1, pos2,  ColourCodes[Color], thickness=2)
	return

#draws every ROI from the global dictionary
def drawROIs(src,displayNames=True):
	global global_Settings, ColourCodes
	for key in global_Settings["Camera_ROI_List"]:
		drawROI(src,key,displayNames)
	return
"""
**********************************************************************
	string manipulations
**********************************************************************
"""
#find a substring between substr1 and substr2
def isolateSubstring(string, substr1,substr2):
    p1 = string.find(substr1) + len(substr1)
    p2 = string.find(substr2,p1)
    Name = string[p1:p2]
    return Name
"""
**********************************************************************
	converts between wdith/height percentages and pixels values
**********************************************************************
"""
#convert coordinates from percentages to pixles
def ConvertPerCentToPxl(src,org:list):
	pxls_y = src.shape[0]/100    #number of cols
	pxls_x = src.shape[1]/100    #number of rows
	org[0] *= pxls_x
	org[1] *= pxls_y
	org = (int(org[0]),int(org[1]))
	return org
"""
**********************************************************************
	add text to src
**********************************************************************
"""
#draws white text over a black background
def DrawText(src,Text,Org,scaleFactor=1.0,textColour='white'):
	fontscale = scaleFactor * (src.shape[0]/720)
	thickness = int(2* src.shape[0]/720)
	Org=ConvertPerCentToPxl(src,Org)
	cv.putText(src, text=Text,org=Org, fontFace=cv.FONT_HERSHEY_SIMPLEX,fontScale=fontscale, color=ColourCodes['black'], thickness=thickness*2,lineType=cv.LINE_AA)
	cv.putText(src, text=Text,org=Org, fontFace=cv.FONT_HERSHEY_SIMPLEX,fontScale=fontscale, color=ColourCodes[textColour], thickness=thickness,lineType=cv.LINE_AA)
