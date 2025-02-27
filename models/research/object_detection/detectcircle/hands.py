import os
import numpy as np
from matplotlib import pyplot as plt 
import argparse
import math
from math import cos
from math import sin
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
import sys
import json
from PIL import Image
import os.path
import posixpath
ch_eleven = 0
ch_two = 0


def detect_line(roi,data):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200)
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 10  # minimum number of pixels making up a line
    max_line_gap = 10  # maximum gap in pixels between connectable line segments
    line_image = np.copy(roi) * 0  # creating a blank to draw lines on
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),min_line_length, max_line_gap)
    #print(lines)
    points = []
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),2)
    # for line in lines:
    #     for x1, y1, x2, y2 in line:
    #         #points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
    #         cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
    
    cv2.circle(line_image,(x1,y1),2,(249, 201, 251),10)   
    cv2.circle(line_image,(x2,y2),2,(249, 201, 251),10) 
    # show images
    Image.fromarray(line_image).show()
    return x1,y1,x2,y2

def checkcrash(data_num,x1,y1,x2,y2,typehand,h,k,r):
    list_crash = []
    list_status= []
    list_distance = []
    list_num = [] 
    global ch_eleven,ch_two
    newX1 = x1
    newY1 = y1
    newX2 = x2
    newY2 = y2
    distance = 0
    m = slope(x1,y1,x2,y2)
    i=1
    while(math.pow((newX1-h),2) + math.pow((newY1-k),2) <= math.pow((r),2)):
        newX1+=i         
        newY1 = y1-(m*(x1 - newX1))
        #cv2.line(rec,(x1,y1),(int(newX1),int(newY1)),(255,123,45),2)
        status,number=inArea((int(newX1),int(newY1)),data_num)
        distance = math.sqrt(((int(newX1)-x1)**2)+((int(newY1)-y1)**2) )
        if(status):
            crash = (x1,y1,int(newX1),int(newY1),typehand)
            break
    list_distance.append(distance)
    list_crash.append((x1,y1,int(newX1),int(newY1),typehand))
    list_num.append(number)
    list_status.append(status)
    #print(status,number)
    newX1 = x1
    newY1 = y1
    newX2 = x2
    newY2 = y2

    i=-1
    while(math.pow((newX1-h),2) + math.pow((newY1-k),2) <= math.pow((r),2)):
        newX1+=i         
        newY1 = y1-(m*(x1 - newX1))
        #cv2.line(rec,(x1,y1),(int(newX1),int(newY1)),(255,123,45),2)
        #print((int(newX),int(newY)))
        status,number=inArea((int(newX1),int(newY1)),data_num)
        distance = math.sqrt(((int(newX1)-x1)**2)+((int(newY1)-y1)**2) )
        if(status):
            crash = (x1,y1,int(newX1),int(newY1),typehand)
            break
    list_distance.append(distance)
    list_crash.append((x1,y1,int(newX1),int(newY1),typehand))
    list_num.append(number)
    list_status.append(status)
    newX1 = x1
    newY1 = y1
    newX2 = x2
    newY2 = y2

    i=1
    while(math.pow((newX2-h),2) + math.pow((newY2-k),2) <= math.pow((r),2)):
        newX2+=i         
        newY2 = y2-(m*(x2 - newX2))
        #cv2.line(rec,(x2,y2),(int(newX2),int(newY2)),(5, 107, 120),2)
        #print((int(newX),int(newY)))
        status,number=inArea((int(newX2),int(newY2)),data_num)
        distance = math.sqrt(((int(newX2)-x2)**2)+((int(newY2)-y2)**2) )
        if(status):
            crash = (x2,y2,int(newX2),int(newY2),typehand)
            break
    list_distance.append(distance)
    list_crash.append((x2,y2,int(newX2),int(newY2),typehand))
    list_num.append(number)
    list_status.append(status)
    newX1 = x1
    newY1 = y1
    newX2 = x2
    newY2 = y2
    
    i=-1
    while(math.pow((newX2-h),2) + math.pow((newY2-k),2) <= math.pow((r),2)):
        newX2+=i         
        newY2 = y2-(m*(x2 - newX2))
        status,number=inArea((int(newX2),int(newY2)),data_num)
        #cv2.line(rec,(x2,y2),(int(newX2),int(newY2)),(255,123,45),2)
        distance = math.sqrt(((int(newX2)-x2)**2)+((int(newY2)-y2)**2) )
        if(status):
            crash = (x2,y2,int(newX2),int(newY2),typehand)
            break
    list_distance.append(distance)
    list_crash.append((x2,y2,int(newX2),int(newY2),typehand))
    list_num.append(number)
    list_status.append(status)
    x=0
    y=0
    newX=0
    newY=0

    idx = list_distance.index(min(list_distance))
    x,y,newX,newY = list_crash[idx][0],list_crash[idx][1], list_crash[idx][2], list_crash[idx][3]
    print(list_status[idx],list_num[idx],list_crash[idx][4])
    cv2.line(rec,(x,y),(newX,newY),(255,123,45),3)  
    if(list_crash[idx][4]=="hour" and list_num[idx]==11):
        ch_eleven = 1
    if(list_crash[idx][4]=="minute" and list_num[idx]==2):
        ch_two = 1
    print("jam ",ch_eleven,ch_two)
    return ch_eleven,ch_two
    
def checkNumberClass(text):
    if(text == "one"):
        return 1
    elif(text == "two"):
        return 2
    elif(text == "three"):
        return 3
    elif(text == "four"):
        return 4
    elif(text == "five"):
        return 5
    elif(text == "six"):
        return 6
    elif(text == "seven"):
        return 7
    elif(text == "eight"):
        return 8
    elif(text == "nine"):
        return 9
    elif(text == "ten"):
        return 10
    elif(text == "eleven"):
        return 11
    elif(text == "twelve"):
        return 12

 #  check line in number's area n=0 : arrownohead , n=1 : arrow
def inArea(p,data) : #,n,x1,y1,x2,y2
    status = False
    number = 0
    for i in data:
        top_left = (int(i[2]), int(i[0]))
        bottom_right = (int(i[3]), int(i[1]))
        cv2.rectangle(rec, top_left, bottom_right,(53, 77, 206 ), 2) 
        text = str(i[5][0]).split(':')
        check = checkInArea(top_left,bottom_right,p)
        if(check == True):
            status = True
            num_text = str(i[5][0]).split(':')
            #print("true",num_text[0])
            number = checkNumberClass(num_text[0])
    return status,number
    
def checkInArea(top_left,bottom_right,p):
    if (p[0] >= top_left[0] and p[0] <= bottom_right[0] and p[1] >= top_left[1] and p[1] <= bottom_right[1]) :
        return True
    else :
        return False   

def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m

def checkline(h,k,xhead,yhead,xtail,ytail,rec,data_num,r,typehand):
    global ch_eleven,ch_two
    newX = xhead
    newY = yhead
    print(xhead,yhead,xtail,ytail)
    i= -1
    if(xhead>xtail):
        i=1
    m = slope(xhead,yhead,xtail,ytail)
    while(math.pow((newX-h),2) + math.pow((newY-k),2) <= math.pow((r),2)):
        c = xhead-((m)*yhead)
        newX+=i         
        newY = ytail-(m*(xtail - newX))
        cv2.line(rec,(xtail,ytail),(int(newX),int(newY)),(17, 17, 127 ),2)
        #print((int(newX),int(newY)))
        status,number=inArea((int(newX),int(newY)),data_num)
        if(status):
            if(number==11 and typehand=="hour"):
                ch_eleven = 1
            if(number==2 and typehand=="minute"):
                ch_two = 1
            break
    # print(status,number,typehand)
    return ch_eleven,ch_two


def checkarrowinbox(h,k,xhead,yhead,xtail,ytail,rec,data_num,r,typehand):
    global ch_eleven,ch_two
    newX = xhead
    newY = yhead
    cv2.circle(rec,(xhead,yhead),2,234,5)
    cv2.circle(rec,(xtail,ytail),2,123,2)
    i= -1
    if(xhead<xtail):
        i=1
    m = slope(xhead,yhead,xtail,ytail)
    while(math.pow((newX-h),2) + math.pow((newY-k),2) <= math.pow((r),2)):
        #print(i)
        c = xhead-((m)*yhead)
        newX+=i         
        newY = ytail-(m*(xtail - newX))
        cv2.line(rec,(xtail,ytail),(int(newX),int(newY)),(223, 222, 39 ),2)
        status,number=inArea((int(newX),int(newY)),data_num)
        if(status):
            if(number==11 and typehand=="hour"):
                ch_eleven = 1
            if(number==2 and typehand=="minute"):
                ch_two = 1
            break
    print(status,number,typehand)
    return ch_eleven,ch_two


def get_values(iterables, key_to_find):
  return list(filter(lambda x:key_to_find in x, iterables)) 

def detect_arrow(img):
    #Image.fromarray(img).show()
    k = 1
    list_center = []
    list_dist = []
    list_namemean = []
    # convert image to gray scale image 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # detect corners with the goodFeaturesToTrack function. 
    corners = cv2.goodFeaturesToTrack(gray, 8, 0.005,10) 
    corners = np.int0(corners) 
    # making a circle at each point that we think is a corner. 
    for i in corners: 
        x, y = i.ravel() 
        center = x,y
        list_center.append(center)
        cv2.circle(img, (x, y), 3, 255, 2)
        #cv2.putText(img,str(k),(x, y), font, 0.1, (0,122,22), 1, cv2.LINE_AA)
        #k = k + 1
    list_diff = []    
    max_corr = []
    # cv2.rectangle(img, (x, y), (x+20, y+20), (255,0,0), 10)
    xmean, ymean = (np.mean(corners, axis = 0)).ravel()
    center = (int(xmean),int(ymean))
    #cv2.circle(img,center,1,(72, 45, 238),6)
    #Image.fromarray(img).show()
    for i in list_center:
        x,y = i
        distance = math.sqrt(((xmean-x)**2)+((ymean-y)**2) )
        dist = int(distance)
        max_corr.append((x,y))
        list_dist.append(dist)
    idx = list_dist.index(max(list_dist))
    #print(max(list_dist))
    distance = max(list_dist)
    (p1,p2) = max_corr[idx]
    #print(max_corr[idx])
    # cv2.circle(img,(max_corr[idx]),2,(11, 170, 53),10)
    # cv2.circle(img,center,2,(221, 238, 45),5)
    # Image.fromarray(img).show()

        # maxval=0
        # for i in range(0, len(list_dist)):
        #     #print(list_dist[i][2])
        #     if (list_dist[i][2]>=maxval):
        #         maxval = list_dist[i][2]
        #         print(maxval)
        #         p1,p2 = list_dist[i][0],list_dist[i][1]
    # namemean = img,center,p1,p2
    # list_namemean.append(namemean)
    # print(p1,p2)
    # cv2.circle(img,(p1,p2),2,(11, 170, 53),10)
    # cv2.circle(img,center,2,(11, 170, 53),5)
    # cv2.imshow('p1p2',img)
    # cv2.waitKey(0)
    # return img,center,p1,p2
    return distance,(p1,p2),center

def check_boxarrow(rec,box_hand,data_num,h,k,r):
    print(box_hand) #[('hour', (370, 198, 395, 169, 'arrow')), ('miniute', (305, 192, 329, 227, 'arrow'))]
    for i in range(0,len(box_hand)):
        #print(box_hand[i][1][4])
        if(box_hand[i][1][4]=="arrow"):
            checkcrash(data_num,box_hand[i][1][0],box_hand[i][1][1],box_hand[i][1][2],box_hand[i][1][3],box_hand[i][0],h,k,r)
        if(box_hand[i][1][4]=="arrownohead"):
            checkcrash(data_num,box_hand[i][1][0],box_hand[i][1][1],box_hand[i][1][2],box_hand[i][1][3],box_hand[i][0],h,k,r)

def arrownohead(xmin,ymin,lenx,leny,data_corr,rec):
    roi = output[ymin:ymin+leny,xmin:xmin+lenx]
    Image.fromarray(roi).show()
    x1,y1,x2,y2 = detect_line(roi,data_corr)
    distance = math.sqrt( ((x1-x2)**2)+((y1-y2)**2))
    # cv2.circle(rec,(x1+xmin,y1+ymin),1,(72, 45, 238),5)
    # cv2.circle(rec,(x2+xmin,y2+ymin),1,(72, 45, 238),5)
    #Image.fromarray(rec).show()
    print(distance,x1,y1,x2,y2)
    return distance,x1,y1,x2,y2

def arrow(xmin,ymin,lenx,leny,data_corr,rec):
    roi = output[ymin:ymin+leny,xmin:xmin+lenx]
    distance,(p1,p2),center = detect_arrow(roi) #p1,p2 : tail
    x,y = center
    #cv2.circle(rec,(x+xmin,y+ymin),1,(72, 45, 238),5)
    #Image.fromarray(rec).show()
    return distance,(p1,p2),center

def check_data(data,img):
    list_distance = [] 
    list_hands = []
    box_arrow = []
    box_hand = []
    if(len(data)==2):
        for i in range(0, len(data)):
            #print(len(data))
            ymin  = data[i][0]
            ymax = data[i][1]
            xmin = data[i][2]
            xmax = data[i][3]
            #cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(212, 238, 127),2)
            name = data[i][5][0].split(":")
            lenx = xmax-xmin
            leny = ymax-ymin
            area = lenx * leny
            #print(area)
            start_point = (data[i][2],data[i][0])
            end_point = (data[i][3],data[i][1])
            #print(name[0])
            if(name[0]=="arrownohead"):
                distance,x1,y1,x2,y2 = arrownohead(xmin,ymin,lenx,leny,data_corr,rec)
                list_distance.append(distance)
                box_arrow.append((x1+xmin,y1+ymin,x2+xmin,y2+ymin,name[0]))
            if(name[0]=="arrow"):     
                distance,(p1,p2),center = arrow(xmin,ymin,lenx,leny,data_corr,rec)
                x,y = center
                list_distance.append(distance)
                box_arrow.append((x+xmin,y+ymin,p1+xmin,p2+ymin,name[0]))

        if(list_distance[0]!=list_distance[1]):
            minute = max(list_distance)
            hour = min(list_distance)
            idx_minute_hand = list_distance.index(minute)
            idx_hour_hand = list_distance.index(hour)
            minute_hand = ("minute",box_arrow[idx_minute_hand]) 
            hour_hand = ("hour",box_arrow[idx_hour_hand]) 
            #check_boxarrow(box_arrow)
            box_hand.append(hour_hand)
            box_hand.append(minute_hand)
            score_4 = 2
        else: 
            score_4 = 1
        # print(second_hand,box_arrow[idx_second_hand])
        # print(hour_hand,box_arrow[idx_hour_hand])
    else:
        score_4 = 0
    return box_hand,list_hands,score_4
# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'
IMAGE_NAME = 'hand2'
FILE = '.jpg'
IMAGE_FOLDER = 'image_test'

# Grab path to current working directory
CWD_PATH = os.getcwd()
PREVIOS_PATH = os.path.abspath(CWD_PATH+ "/../")
# Path to image
PATH_TO_IMAGE = os.path.join(PREVIOS_PATH,IMAGE_FOLDER,IMAGE_NAME+FILE)
#Read image 
image = cv2.imread(PATH_TO_IMAGE)

#read hand
with open("json/script"+IMAGE_NAME+".json") as f:
  data = json.load(f)
  
data_corr = []
data_circle = []
# read num from json
with open("json/scriptnew_num.json") as f:
  data2 = json.load(f)
  for p in data2['coordinate']:
	  data_corr.append(p)
  for p in data2['circle']:
	  data_circle.append(p)

#load coordinates from json file
name=[]
list_point=[] #list of coordinate no head [(x1,y2),(x2,y2)]
list_centroid =[]
list_crashnum = []
hour_hand = 0
minute_hand = 0
output = image.copy()
rec = image.copy()
font=cv2.FONT_ITALIC
#data[0][0] = ymin , data[0][1]=ymax, data[0][2]=xmin, data[0][3]=xmax
h,k,r = data_circle
#score
score_4 = 0
score_5 = 0

box_hand,list_hands,score_4 = check_data(data,rec)
check_boxarrow(rec,box_hand,data_corr,h,k,r)
#rule4    

#rule5
if(ch_eleven==1):
    score_5 = score_5 + 1
if(ch_two==1):
    score_5 = score_5 + 1

print("4.have 2 hands: ",score_4)
print("5.hands on correct digit:",score_5)
Image.fromarray(rec).show()
cv2.imwrite(os.path.join(PREVIOS_PATH,IMAGE_FOLDER,IMAGE_NAME+'frame.jpg'),rec)

        # roi = output[ymin:ymin+leny,xmin:xmin+lenx]
        # x1,y1,x2,y2 = detect_line(,data_corr)
        # distance = math.sqrt( ((x1-x2)**2)+((y1-y2)**2))

    # if(name[0]=="arrownohead"):
    #     roi = output[ymin:ymin+leny,xmin:xmin+lenx]
    #     #Image.fromarray(roi).show()
    #     x1,y1,x2,y2 = detect_line(roi,data_corr)
    #     distance = math.sqrt( ((x1-x2)**2)+((y1-y2)**2))
    #     #print(distance)
    #     if (distance<curr_dist):
    #         arrow = "hourhand"
    #         curr_dist = distance
    #         # status,number=inArea((x1,y1),data_corr)
    #         ch_eleven,ch_two=checkcrash(data_corr,x1+xmin,y1+ymin,x2+xmin,y2+ymin,"hourhand")
    #         #cv2.circle(rec, (x1+xmin,y1+ymin), 3, 255, 2)
    #         #cv2.circle(rec, (x2+xmin,y2+ymin), 3, 255, 2)

    #         # status,number=inArea((x2,y2),data_corr)
    #     if(distance>curr_dist):
    #          arrow = "minutehand"
    #          ch_eleven,ch_two=checkcrash(data_corr,x1+xmin,y1+ymin,x2+xmin,y2+ymin,"hourhand")
    #          #cv2.circle(rec, (x1+xmin,y1+ymin), 3, 255, 2)
    #          #cv2.circle(rec, (x2+xmin,y2+ymin), 3, 255, 2)
    #     cv2.putText(rec,str(arrow),(x1+xmin,y1+ymin), font, 0.7, (200,12,0), 1, cv2.LINE_AA)
    #     list.append(str(arrow))
    #     # ch_eleven,ch_two = checkarrowinbox(h,k,x1,y1,x2,y2,rec,data_corr,r,arrow)
    #     # cv2.circle(rec,(x1+xmin,y1+ymin), 3,200,10)
    #     # cv2.circle(rec,(x2+xmin,y2+ymin), 3,200,2)

    # #find hour and minute hand #ROI = image[y1:y2, x1:x2] (xmin:ymin , xmax:ymax)
    # else:
    #     print(curr_area)
    #     if(area < curr_area):
    #         print(area,"hourhand")
    #         arrow = "hourhand"
    #         curr_area = area
    #         roi_hour = output[ymin:ymin+leny,xmin:xmin+lenx]
    #         img,head,p1,p2,name = detect_arrow(roi_hour,arrow)
    #         x,y = head
    #         #cv2.circle(rec,(x+xmin,y+ymin), 3,100,10)
    #         xhead = x+xmin
    #         yhead = y+ymin
    #         xtail = p1+xmin
    #         ytail = p2+ymin 
    #         cv2.circle(rec,(xtail,ytail),1,(17, 17, 127),2)
    #         #cv2.circle(rec,(xhead,yhead), 3,500,10)
    #         ch_eleven,ch_two = checkarrowinbox(h,k,xhead,yhead,xtail,ytail,rec,data_corr,r,"hourhand")
    #         #x+min,y+ymin = จุดเริ่มตรงกลาง , p1+xmin,p2+ymin = จุดไกลพุ่งไปเลข
    #         cv2.line(rec,(xtail,ytail),(xhead,yhead),(17, 17, 127),2)
    #         cv2.putText(rec,str(arrow),(xmin-60,ymax+20), font, 0.7, (17, 17, 127), 1, cv2.LINE_AA)
    #         list.append(str(arrow))
    #     if(area > curr_area):
    #         print(curr_area,"in minu")
    #         print(area,"minutes")
    #         arrow = "minutehand"
            
    #         roi_minute = output[ymin:ymin+leny,xmin:xmin+lenx]
    #         img,head,p1,p2,name = detect_arrow(roi_minute,arrow)
    #         x,y = head
    #         #cv2.circle(rec,(x+xmin,y+ymin), 3,100,10)
    #         xhead = x+xmin
    #         yhead = y+ymin
    #         xtail = p1+xmin
    #         ytail = p2+ymin 
    #         cv2.circle(rec,(xtail,ytail),1,(224, 155, 8),2)
    #         #cv2.circle(rec,(xhead,yhead), 3,500,10)
    #         ch_eleven,ch_two = checkarrowinbox(h,k,xhead,yhead,xtail,ytail,rec,data_corr,r,"minutehand")
    #     # list_crashnum.append([status,number,typehand])
    #         cv2.line(rec,(xtail,ytail),(xhead,yhead),(224, 155, 8),2)
    #         cv2.putText(rec,str(arrow),(start_point), font, 0.7, (224, 155, 8), 1, cv2.LINE_AA)
            
        
    #         list.append(str(arrow))

# ch_min = 0
# ch_hr = 0
# if 'minutehand' in list_hands :
#     ch_min = 1
#     score_4 = score_4 + ch_min
# if 'hourhand' in list_hands :
#     ch_hr = 1
#     score_4 = score_4 + ch_hr
# else:
#     ch_hr = 0
#     ch_min= 0




# result = Image.fromarray((rec * 255).astype(np.uint8))
# result.save(IMAGE_NAME+'.jpg')
# #Image.fromarray(output).show()
