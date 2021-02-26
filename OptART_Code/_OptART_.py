from __future__ import print_function
from __future__ import division 
import numpy as np
import math
import cv2
import video
from visual import *
from visual.controls import *
import itertools
from itertools import *
import time
import wx
from decimal import *

camIn = raw_input('Choose WebCam to be used(0 for the first one, 1 for the second one, so on...): ')

if not camIn.strip():
    camIn = 0

pxResEnt = raw_input('Objects Grid resolution(The lower the number the higher number of objects): ')

if not pxResEnt.strip():
    pxResEnt = 12

pxRes_in = int(pxResEnt)

sty = raw_input('Choose a style to start with from 1, 2, 3 or 4: ')
sty1 = [34, 88, 64, 31, 11, -2, 1, 10, 4, 0, 0, 100, 100, 0, 100, 34, 0, 1, 1, 1, 104, 97, 4, 69, 56, 261, 1, 97, 104, False, False, 49, 4]
sty2 = [92, 63, 0, 20, 14, -3, 0, -1, 119, 0, 0, 24, 40, 70, 81, 10, 40, 90, 50, 50, 56, 56, 1, 49, 35, 35, 8, 22, 22, True, False, 0, 15]
sty3 = [38, 63, 0, 57, 21, -3, 1, 4, -4, 0, 0, 96, 42, 30, 16, 40, 40, 344, 1, 1, 186, 179, 3, 192, 186, 186, 35, 1, 165, False, False, 95, 3]
sty4 = [97, 60, 99, 100, 10, -10, 0, 2, 12, 0, 0, 18, 52, 80, 16, 40, 40, 1, 1, 1, 247, 254, 0, 146, 146, 153, 15, 15, 15, True, True, 23, 3]
sty5 = [0, 18, 99, 39, 1, -2, 1, 1, 4, 0, 0, 100, 0, 0, 0, 100, 0, 1, 1, 1, 90, 97, 1, 104, 97, 104, 69, 64, 69, True, False, 23, 3]


#===== Opticalflow computing =====
pxRes = pxRes_in  # optical flow reselution
def mainOptData(img, flow, step=pxRes):
    global flowData 
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    ## this is what get the data
    for (x1, y1), (x2, y2) in lines:
        L = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
        flowData.append([x1,y1,x2,y2,L])
        del flowData[:-pointTot]
    return vis
flowData = []

#===== web Camera settings =====        
cam = video.create_capture(camIn)   #0 is the first cam 1 the second and so on 
ret, img = cam.read()
img = cv2.flip(img, 1)  #flip video
prevgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # used in optical flow
cam_h, cam_w, channels = img.shape
pointW = int(math.ceil((cam_w/pxRes)-0.5))    # to culculate number of points in   #*******only when it is above 0.5********
pointH = int(math.ceil((cam_h/pxRes)-0.5))    # to culculate number of points in Y
pointTot = pointW*pointH            # the total number of points 
print ("camera width",cam_w,"/","camera Hight",cam_h)
print ("X number of Objects",pointW,"/","Y number of Objects",pointH,"/","Total Objects",pointTot)
print ("=====================")
print ("Press ESC or Q to exit")
print ("=====================")

# ===== VPython GUI=====

# defining changes
s01cIN = int (sty1[0] if sty == "1" else sty2[0] if sty == "2" else sty3[0] if sty == "3" else sty4[0] if sty == "4" else sty5[0])
s02cIN = int (sty1[1] if sty == "1" else sty2[1] if sty == "2" else sty3[1] if sty == "3" else sty4[1] if sty == "4" else sty5[1])
s03cIN = int (sty1[2] if sty == "1" else sty2[2] if sty == "2" else sty3[2] if sty == "3" else sty4[2] if sty == "4" else sty5[2])
bgColor = (s01cIN/100,s02cIN/100,s03cIN/100)
def togglebgColor(evt): 
    global bgColor
    vR = s01c.GetValue()/100
    vG = s02c.GetValue()/100
    vB = s03c.GetValue()/100
    bgColor = (vR,vG,vB)
    return bgColor


s07cIN = int (sty1[3] if sty == "1" else sty2[3] if sty == "2" else sty3[3] if sty == "3" else sty4[3] if sty == "4" else sty5[3])
camZoom = s07cIN
def togglecamZoom(evt): 
    global camZoom
    camZoom = s07c.GetValue()
    return camZoom

s08cIN = int (sty1[4] if sty == "1" else sty2[4] if sty == "2" else sty3[4] if sty == "3" else sty4[4] if sty == "4" else sty5[4])
camFOV = s08cIN/10
def togglecamFOV(evt): 
    global camFOV
    camFOV = s08c.GetValue()/10
    return camFOV

sCP1IN = int (sty1[5] if sty == "1" else sty2[5] if sty == "2" else sty3[5] if sty == "3" else sty4[5] if sty == "4" else sty5[5])
sCP2IN = int (sty1[6] if sty == "1" else sty2[6] if sty == "2" else sty3[6] if sty == "3" else sty4[6] if sty == "4" else sty5[6])
sCP3IN = int (sty1[7] if sty == "1" else sty2[7] if sty == "2" else sty3[7] if sty == "3" else sty4[7] if sty == "4" else sty5[7])
camPan = (sCP1IN,sCP2IN,sCP3IN)
def togglecamPan(evt): 
    global camPan
    vx = sCP1.GetValue()
    vy = sCP2.GetValue()
    vz = sCP3.GetValue()
    camPan = (vx,vy,vz)
    return camPan

sCR1IN = int (sty1[8] if sty == "1" else sty2[8] if sty == "2" else sty3[8] if sty == "3" else sty4[8] if sty == "4" else sty5[8])
sCR2IN = int (sty1[9] if sty == "1" else sty2[9] if sty == "2" else sty3[9] if sty == "3" else sty4[9] if sty == "4" else sty5[9])
sCR3IN = int (sty1[10] if sty == "1" else sty2[10] if sty == "2" else sty3[10] if sty == "3" else sty4[10] if sty == "4" else sty5[10])
camRot = (sCR1IN/100,sCR2IN/100,sCR3IN/100)
def togglecamRot(evt): 
    global camRot
    vx = sCR1.GetValue()/100
    vy = sCR2.GetValue()/100
    vz = sCR3.GetValue()/100
    camRot = (vx,vy,vz)
    return camRot

s01aIN = int (sty1[11] if sty == "1" else sty2[11] if sty == "2" else sty3[11] if sty == "3" else sty4[11] if sty == "4" else sty5[11])
s02aIN = int (sty1[12] if sty == "1" else sty2[12] if sty == "2" else sty3[12] if sty == "3" else sty4[12] if sty == "4" else sty5[12])
s03aIN = int (sty1[13] if sty == "1" else sty2[13] if sty == "2" else sty3[13] if sty == "3" else sty4[13] if sty == "4" else sty5[13])
movColor = (s01aIN/100,s02aIN/100,s03aIN/100)
def togglemovColor(evt):        
    global movColor
    vR = s01a.GetValue()/100
    vG = s02a.GetValue()/100
    vB = s03a.GetValue()/100
    movColor = (vR,vG,vB)
    return movColor

s01bIN = int (sty1[14] if sty == "1" else sty2[14] if sty == "2" else sty3[14] if sty == "3" else sty4[14] if sty == "4" else sty5[14])
s02bIN = int (sty1[15] if sty == "1" else sty2[15] if sty == "2" else sty3[15] if sty == "3" else sty4[15] if sty == "4" else sty5[15])
s03bIN = int (sty1[16] if sty == "1" else sty2[16] if sty == "2" else sty3[16] if sty == "3" else sty4[16] if sty == "4" else sty5[16])
styColor = (s01bIN/100,s02bIN/100,s03bIN/100)
def togglestyColor(evt): 
    global styColor
    vR = s01b.GetValue()/100
    vG = s02b.GetValue()/100
    vB = s03b.GetValue()/100
    styColor = (vR,vG,vB)
    return styColor

s04aIN = int (sty1[17] if sty == "1" else sty2[17] if sty == "2" else sty3[17] if sty == "3" else sty4[17] if sty == "4" else sty5[17])
s05aIN = int (sty1[18] if sty == "1" else sty2[18] if sty == "2" else sty3[18] if sty == "3" else sty4[18] if sty == "4" else sty5[18])
s06aIN = int (sty1[19] if sty == "1" else sty2[19] if sty == "2" else sty3[19] if sty == "3" else sty4[19] if sty == "4" else sty5[19])
movObj = (s04aIN/100,s05aIN/100,s06aIN/100)
def togglemovObj(evt): 
    global movObj
    vx = s04a.GetValue()/100
    vy = s05a.GetValue()/100
    vz = s06a.GetValue()/100
    movObj = (vx,vy,vz)
    return movObj

s04bIN = int (sty1[20] if sty == "1" else sty2[20] if sty == "2" else sty3[20] if sty == "3" else sty4[20] if sty == "4" else sty5[20])
s05bIN = int (sty1[21] if sty == "1" else sty2[21] if sty == "2" else sty3[21] if sty == "3" else sty4[21] if sty == "4" else sty5[21])
s06bIN = int (sty1[22] if sty == "1" else sty2[22] if sty == "2" else sty3[22] if sty == "3" else sty4[22] if sty == "4" else sty5[22])
movObjstill = (s04bIN/100,s05bIN/100,s06bIN)
def togglemovObjstill(evt): 
    global movObjstill
    vx = s04b.GetValue()/100
    vy = s05b.GetValue()/100
    vz = s06b.GetValue()
    movObjstill = (vx,vy,vz)
    return movObjstill

s07aIN = int (sty1[23] if sty == "1" else sty2[23] if sty == "2" else sty3[23] if sty == "3" else sty4[23] if sty == "4" else sty5[23])
s08aIN = int (sty1[24] if sty == "1" else sty2[24] if sty == "2" else sty3[24] if sty == "3" else sty4[24] if sty == "4" else sty5[24])
s09aIN = int (sty1[25] if sty == "1" else sty2[25] if sty == "2" else sty3[25] if sty == "3" else sty4[25] if sty == "4" else sty5[25])
scObjmov = (s07aIN/100,s08aIN/100,s09aIN/100)
def togglescObjmov(evt): 
    global scObjmov
    vx = s07a.GetValue()/100
    vy = s08a.GetValue()/100
    vz = s09a.GetValue()/100
    scObjmov = (vx,vy,vz)
    return scObjmov

s07bIN = int (sty1[26] if sty == "1" else sty2[26] if sty == "2" else sty3[26] if sty == "3" else sty4[26] if sty == "4" else sty5[26])
s08bIN = int (sty1[27] if sty == "1" else sty2[27] if sty == "2" else sty3[27] if sty == "3" else sty4[27] if sty == "4" else sty5[27])
s09bIN = int (sty1[28] if sty == "1" else sty2[28] if sty == "2" else sty3[28] if sty == "3" else sty4[28] if sty == "4" else sty5[28])
scObjstill = (s07bIN/100,s08bIN/100,s09bIN/100)
def togglescObjstill(evt): 
    global scObjstill
    vx = s07b.GetValue()/100
    vy = s08b.GetValue()/100
    vz = s09b.GetValue()/100
    scObjstill = (vx,vy,vz)
    return scObjstill           

RMOIN = (sty1[29] if sty == "1" else sty2[29] if sty == "2" else sty3[29] if sty == "3" else sty4[29] if sty == "4" else sty5[29])
rotObjmove = int( 0 if RMOIN == True else 1)
def togglerotObjmove(evt): 
    global rotObjmove
    bVal = RMO.GetValue()
    if bVal == True:
        rotObjmove = 0
    else:
        rotObjmove = 1
    return rotObjmove  

RSOIN = (sty1[30] if sty == "1" else sty2[30] if sty == "2" else sty3[30] if sty == "3" else sty4[30] if sty == "4" else sty5[30])
rotObjStill = int( 0 if RSOIN == True else 1)
def togglerotObjStill(evt): 
    global rotObjStill
    bVal = RSO.GetValue()
    if bVal == True:
        rotObjStill = 0
    else:
        rotObjStill = 1
    return rotObjStill 

s10aIN = int (sty1[31] if sty == "1" else sty2[31] if sty == "2" else sty3[31] if sty == "3" else sty4[31] if sty == "4" else sty5[31])
rotAnglmove = s10aIN/100
def togglerotAnglmove(evt): 
    global rotAnglmove
    rotAnglmove = s10a.GetValue()/100
    return rotAnglmove

s10bIN = int (sty1[32] if sty == "1" else sty2[32] if sty == "2" else sty3[32] if sty == "3" else sty4[32] if sty == "4" else sty5[32])
rotAnglStill = s10bIN/100
def togglerotAnglStill(evt): 
    global rotAnglStill
    rotAnglStill = s10b.GetValue()/100
    return rotAnglStill

OFthsh = 1
def toggleOFthsh(evt): 
    global OFthsh
    OFthsh = OFthshSLID.GetValue()/10
    return OFthsh


key = ()
def keyInput():
    global key
    key = scene.kb.getkey()
    return key


def printVal(evt):
    print ([s01c.GetValue(),s02c.GetValue(),s03c.GetValue(),s07c.GetValue(),s08c.GetValue()
            ,sCP1.GetValue(),sCP2.GetValue(),sCP3.GetValue(),sCR1.GetValue(),sCR2.GetValue(),sCR3.GetValue(),s01a.GetValue()
            ,s02a.GetValue(),s03a.GetValue(),s01b.GetValue(),s02b.GetValue(),s03b.GetValue(),s04a.GetValue(),s05a.GetValue()
            ,s06a.GetValue(),s04b.GetValue(),s05b.GetValue(),s06b.GetValue(),s07a.GetValue(),s08a.GetValue(),s09a.GetValue()
            ,s07b.GetValue(),s08b.GetValue(),s09b.GetValue(),RMO.GetValue(),RSO.GetValue(),s10a.GetValue(),s10b.GetValue()])

#WxPython UI
guiWd = 280
guiHi = 870
w = window(width=guiWd, height=guiHi,menus=False, title='OptART Controller',x=0, y=0,style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
w.fullscreen = False 
p = w.panel

x1c = 10
y1c1 = 30
y1cA = 30
x2c = 25
x3c = 150


wx.StaticText(p, pos=(x2c+10,y1c1), label='Background Color')
s01c = wx.Slider(p, pos=(x2c,y1c1+(y1cA*1)), size=(100,25), minValue=0, maxValue=100)
s01c.Bind(wx.EVT_SCROLL, togglebgColor)
s02c = wx.Slider(p, pos=(x2c,y1c1+(y1cA*2)), size=(100,25), minValue=0, maxValue=100)
s02c.Bind(wx.EVT_SCROLL, togglebgColor)
s03c = wx.Slider(p, pos=(x2c,y1c1+(y1cA*3)), size=(100,25), minValue=0, maxValue=100)
s03c.Bind(wx.EVT_SCROLL, togglebgColor)

wx.StaticText(p, pos=(x3c+20,y1c1), label='Camera Zoom')
s07c = wx.Slider(p, pos=(x3c,y1c1+(y1cA*1)), size=(100,25), minValue=1, maxValue=100)
s07c.Bind(wx.EVT_SCROLL, togglecamZoom)

wx.StaticText(p, pos=(x3c+20,y1c1+(y1cA*2)), label='Camera FOV')
s08c = wx.Slider(p, pos=(x3c,y1c1+(y1cA*3)), size=(100,25), minValue=1, maxValue=30)
s08c.Bind(wx.EVT_SCROLL, togglecamFOV)


wx.StaticText(p, pos=(x2c+30,y1c1+(y1cA*4)), label='Camera Pan')
sCP1 = wx.Slider(p, pos=(x2c,y1c1+(y1cA*5)), size=(100,25), minValue=-10, maxValue=10)
sCP1.Bind(wx.EVT_SCROLL, togglecamPan)
sCP2 = wx.Slider(p, pos=(x2c,y1c1+(y1cA*6)), size=(100,25), minValue=-10, maxValue=10)
sCP2.Bind(wx.EVT_SCROLL, togglecamPan)
sCP3 = wx.Slider(p, pos=(x2c,y1c1+(y1cA*7)), size=(100,25), minValue=-10, maxValue=10)
sCP3.Bind(wx.EVT_SCROLL, togglecamPan)

wx.StaticText(p, pos=(x3c+20,y1c1+(y1cA*4)), label='Camera Rotate')
sCR1 = wx.Slider(p, pos=(x3c,y1c1+(y1cA*5)), size=(100,25), minValue=-300, maxValue=300)
sCR1.Bind(wx.EVT_SCROLL, togglecamRot)
sCR2 = wx.Slider(p, pos=(x3c,y1c1+(y1cA*6)), size=(100,25), minValue=-300, maxValue=300)
sCR2.Bind(wx.EVT_SCROLL, togglecamRot)
sCR3 = wx.Slider(p, pos=(x3c,y1c1+(y1cA*7)), size=(100,25), minValue=-300, maxValue=300)
sCR3.Bind(wx.EVT_SCROLL, togglecamRot)

wx.StaticText(p, pos=(x2c+10,y1c1+(y1cA*8)+15), label='Moving Objects')
wx.StaticText(p, pos=(x3c+25,y1c1+(y1cA*8)+15), label='Still Objects')

wx.StaticText(p, pos=(x2c+95,y1c1+(y1cA*9)+5), label='Color')

s01a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*10)), size=(100,25), minValue=0, maxValue=100)
s01a.Bind(wx.EVT_SCROLL, togglemovColor)
s02a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*11)), size=(100,25), minValue=0, maxValue=100)
s02a.Bind(wx.EVT_SCROLL, togglemovColor)
s03a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*12)), size=(100,25), minValue=0, maxValue=100)
s03a.Bind(wx.EVT_SCROLL, togglemovColor)

s01b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*10)), size=(100,25), minValue=0, maxValue=100)
s01b.Bind(wx.EVT_SCROLL, togglestyColor)
s02b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*11)), size=(100,25), minValue=0, maxValue=100)
s02b.Bind(wx.EVT_SCROLL, togglestyColor)
s03b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*12)), size=(100,25), minValue=0, maxValue=100)
s03b.Bind(wx.EVT_SCROLL, togglestyColor)

wx.StaticText(p, pos=(x2c+85,y1c1+(y1cA*13)), label='Translation')

s04a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*14)), size=(100,25), minValue=1, maxValue=500)
s04a.Bind(wx.EVT_SCROLL, togglemovObj)
s05a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*15)), size=(100,25), minValue=1, maxValue=500)
s05a.Bind(wx.EVT_SCROLL, togglemovObj)
s06a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*16)), size=(100,25), minValue=1, maxValue=500)
s06a.Bind(wx.EVT_SCROLL, togglemovObj)

s04b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*14)), size=(100,25), minValue=1, maxValue=500)
s04b.Bind(wx.EVT_SCROLL, togglemovObjstill)
s05b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*15)), size=(100,25), minValue=1, maxValue=500)
s05b.Bind(wx.EVT_SCROLL, togglemovObjstill)
s06b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*16)), size=(100,25), minValue=0, maxValue=10)
s06b.Bind(wx.EVT_SCROLL, togglemovObjstill)

wx.StaticText(p, pos=(x2c+95,y1c1+(y1cA*17)), label='Scale')

s07a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*18)), size=(100,25), minValue=1, maxValue=500)
s07a.Bind(wx.EVT_SCROLL, togglescObjmov)
s08a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*19)), size=(100,25), minValue=1, maxValue=500)
s08a.Bind(wx.EVT_SCROLL, togglescObjmov)
s09a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*20)), size=(100,25), minValue=1, maxValue=500)
s09a.Bind(wx.EVT_SCROLL, togglescObjmov)

s07b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*18)), size=(100,25), minValue=1, maxValue=500)
s07b.Bind(wx.EVT_SCROLL, togglescObjstill)
s08b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*19)), size=(100,25), minValue=1, maxValue=500)
s08b.Bind(wx.EVT_SCROLL, togglescObjstill)
s09b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*20)), size=(100,25), minValue=1, maxValue=500)
s09b.Bind(wx.EVT_SCROLL, togglescObjstill)

RMO = wx.ToggleButton(p, label="Stop Rotation", pos=(x2c,y1c1+(y1cA*21)), size=(90,25))
RMO.Bind(wx.EVT_TOGGLEBUTTON,togglerotObjmove)
RSO = wx.ToggleButton(p, label="Stop Rotation", pos=(x3c,y1c1+(y1cA*21)), size=(90,25))
RSO.Bind(wx.EVT_TOGGLEBUTTON,togglerotObjStill)

wx.StaticText(p, pos=(x2c+70,y1c1+(y1cA*22)), label='Rotation Speed')

s10a = wx.Slider(p, pos=(x2c,y1c1+(y1cA*23)), size=(100,25), minValue=0, maxValue=100)
s10a.Bind(wx.EVT_SCROLL, togglerotAnglmove)
s10b = wx.Slider(p, pos=(x3c,y1c1+(y1cA*23)), size=(100,25), minValue=0, maxValue=100)
s10b.Bind(wx.EVT_SCROLL, togglerotAnglStill)


SOO = wx.Button(p, label="print Val", pos=(x2c-15,y1c1+(y1cA*26)), size=(100,25))
SOO.Bind(wx.EVT_BUTTON,printVal)


wx.StaticText(p, pos=(x2c+50,y1c1+(y1cA*24)), label='Optical Flow Threshold')

OFthshSLID = wx.Slider(p, pos=(x2c+60,y1c1+(y1cA*25)), size=(100,25), minValue=0, maxValue=100)
OFthshSLID.Bind(wx.EVT_SCROLL, toggleOFthsh)


wx.StaticText(p, pos=(x1c,y1c1+(y1cA*1)), label='R')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*2)), label='G')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*3)), label='B')

wx.StaticText(p, pos=(x1c,y1c1+(y1cA*5)), label='X')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*6)), label='Y')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*7)), label='Z')

wx.StaticText(p, pos=(x1c,y1c1+(y1cA*10)), label='R')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*11)), label='G')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*12)), label='B')

wx.StaticText(p, pos=(x1c,y1c1+(y1cA*14)), label='X')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*15)), label='Y')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*16)), label='Z')

wx.StaticText(p, pos=(x1c,y1c1+(y1cA*18)), label='X')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*19)), label='Y')
wx.StaticText(p, pos=(x1c,y1c1+(y1cA*20)), label='Z')


#======== VPython intial settings ========
scene.title = "OptART"
scene.width  = cam_w 
scene.height = cam_h 
scene.range = camZoom                    # 3d camera zoom out/in
scene.autocenter = False  
scene.background = bgColor
#scene.up = (1,0,0)
scene.bind('keydown', keyInput)
scene.fullscreen = True

# position creation for objects
sclFact = 0.5
iX = [(x - pointW // 2) * sclFact for x in range(pointW)]
iY = [(x - pointH // 2) * sclFact for x in range(pointH)]
iYr = iY[::-1]
iXr = iX[::-1]
ixyz = list(itertools.product(iXr,iYr,[-0.0]))          #[(0,0,0),...]
XYn =[(x,y) for x in iYr for y in iXr ]                 # [(0,0)]
Xs = [x[0]for x in XYn]                                 # X value all
Ys = [x[1]for x in XYn]                                 # Y value all
zr = np.random.uniform(low=-1*movObjstill[2], high=0, size=(pointTot,))
ixyzz = zip (Xs,Ys,zr)


# creating grid of objects
for element in ixyzz:
        cube = box(pos = element,
               size=( 0.5, 0.5, 0.5 ),)
cube.rotate( angle=0.000, axis=(0,1,0) )


# Initializations
#togglebgColor
s01c.SetValue(s01cIN)
s02c.SetValue(s02cIN)
s03c.SetValue(s03cIN)

#togglecamZoom
s07c.SetValue(s07cIN)

#togglecamFOV
s08c.SetValue (s08cIN)

#togglecamPan
sCP1.SetValue(sCP1IN)
sCP2.SetValue(sCP2IN)
sCP3.SetValue(sCP3IN)

#togglecamRot
sCR1.SetValue(sCR1IN)
sCR2.SetValue(sCR2IN)
sCR3.SetValue(sCR3IN)


#togglemovColor
s01a.SetValue(s01aIN)
s02a.SetValue(s02aIN)
s03a.SetValue(s03aIN)

#togglestyColor
s01b.SetValue(s01bIN)
s02b.SetValue(s02bIN)
s03b.SetValue(s03bIN)

#togglemovObj
s04a.SetValue(s04aIN)
s05a.SetValue(s05aIN)
s06a.SetValue(s06aIN)

#togglemovObjstill
s04b.SetValue(s04bIN)
s05b.SetValue(s05bIN)
s06b.SetValue(s06bIN)

#togglescObjmov
s07a.SetValue(s07aIN)
s08a.SetValue(s08aIN)
s09a.SetValue(s09aIN)

#togglescObjstill
s07b.SetValue(s07bIN)
s08b.SetValue(s08bIN)
s09b.SetValue(s09bIN)

#togglerotObjmove(evt): 
RMO.SetValue(RMOIN)

#togglerotObjStill
RSO.SetValue(RSOIN)

#togglerotAnglmove
s10a.SetValue(s10aIN)

#togglerotAnglStill
s10b.SetValue(s10bIN)

OFthshSLID.SetValue(10)


# ====== opticalflow Data getting loop + VPython anim =====

while True:
    scene.fov = camFOV
    scene.background = bgColor
    scene.range = camZoom
    scene.center = camPan
    scene.forward = (camRot[0],camRot[1],-1)
    scene.up = (1,camRot[2],0)
    scene.userspin = False
    scene.autoscale = False
    scene.userzoom = False
    
    iXdd = [(x - pointW // 2) * movObjstill[0] for x in range(pointW)]
    iYdd = [(x - pointH // 2) * movObjstill[1] for x in range(pointH)]
    iYrdd = iYdd[::-1]
    iXrdd = iXdd[::-1]
    ixyzdd = list(itertools.product(iXrdd,iYrdd,[-0.0]))          #[(0,0,0),...]
    XYndd =[(x,y) for x in iYrdd for y in iXrdd ]                 # [(0,0)]
    Xsdd = [x[0]for x in XYndd]                                 # X value all
    Ysdd = [x[1]for x in XYndd]                                 # Y value all
    zrm = [i*movObjstill[2] for i in zr]
    
    ret, img = cam.read()
    img = cv2.flip(img, 1)  #flip video
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    prevgray = gray
    
    finalImg = mainOptData(gray,flow)
    bgrimg = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    #cv2.imshow('flow', finalImg)
    
    # these are list [...] of data each
    #X1 = [item[0] for item in flowData]  
    #Y1 = [item[1] for item in flowData]
    #X2 = [item[2] for item in flowData]
    #Y2 = [item[3] for item in flowData]
    L = [item[4]/3 for item in flowData]
    G = OFthsh
    Ls = [ x if x > G else 0 for x in L]                    #Threshold
    LzR = [(bx if ax==0 else ax) for ax, bx in zip(Ls, zrm)]

    # to create x y + z position from optical flow 
    NXYZ = [i for i in izip(Xsdd,Ysdd,LzR)]                      # [(0,0,0)] newValues

    i = -1
    r = 500
    for obj in scene.objects:
        if isinstance(obj, box):
            obj.pos = NXYZ [i]
            i += 1
            if obj.pos[2] > 0:
                opSmal = obj.pos[2] / 3
                colMal = [x*opSmal for x in movColor]
                obj.color = colMal
                obj.up = (0,1,0)
                obj.rotate( angle=(rotAnglmove*rotObjmove), axis=(0,1,0) )
                obj.pos = (obj.pos[0]+movObj[0],obj.pos[1]+movObj[1],opSmal+movObj[2])
                obj.size = scObjmov #(obj.pos[2],obj.pos[2],obj.pos[2])   #if the scale 0 the dissapear and will not come back
            else:
                obj.color =  styColor
                obj.up = (1,1,1)
                obj.rotate( angle=(rotAnglStill*rotObjStill), axis=(0,1,0) )
                obj.size = scObjstill  # (1,1,1)

    
    # this part is unneccery but if I do not keep it it do not work
    rate(r)
    cube.rotate( angle=0.000, axis=(0,1,0) )

    # this stop close all windows
    if ( (key == 'esc') or (key == 'q') ) :
        print( "Bye!" )
        break

cam.release()
cv2.destroyAllWindows()
exit()
