import cv2
import sys, getopt
import math
import numpy as np

def load_files(inputfile):
   print('Loading file...') 
   return cv2.imread(inputfile)

def parse_args(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print( 'test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print( 'test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   my_dict = {'inputfile': inputfile, 'outputfile' : outputfile}
   return my_dict

def find_and_order_contours(image):
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   gray = cv2.GaussianBlur(gray, (5, 5), 0)
   blur = cv2.GaussianBlur(gray,(1,1),1000)
   edged = cv2.Canny(gray, 75, 200)
   contours, hierarchy  = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   return sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

# currently going off largest area due to the fact that i am scanning one card at a time
def find_card_border(contours):
   for c in contours:
      # approximate the contour
      epsilon = (0.2 * cv2.arcLength(c,True))
      approx = cv2.approxPolyDP(c, 0.02 * epsilon, True)
      print(len(approx), cv2.contourArea(c))
      if len(approx) == 4:
         print(cv2.contourArea(c))
         return c

def calculate_rotation(original_image, border):
   rows,cols = original_image.shape[:2]
   [vx,vy,x,y] = cv2.fitLine(border, cv2.DIST_L2,0,0.01,0.01)

   lefty = int((-x*(vy/vx)) + y)
   righty = int(((cols-x)*(vy/vx))+y)
   # cv2.line(original_image,(cols-1,righty),(0,lefty),(0,255,0),2)
   myradians = math.atan2((cols-1), (righty-lefty))
   mydegrees = math.degrees(myradians)
   print(mydegrees)
   
   if mydegrees < 90:
      return - mydegrees
   else:
      return 180 - mydegrees

# ---- MAIN PROGRAM ----
paths = parse_args(sys.argv[1:])
original_image = load_files(paths['inputfile'])
contours = find_and_order_contours(original_image)
# border = find_card_border(contours)
border = contours[0]
rotation = calculate_rotation(original_image, border)

rows,cols = original_image.shape[:2]
M = cv2.getRotationMatrix2D((int(cols/2),int(rows/2)), rotation , 1.0)
original_image = cv2.warpAffine(original_image,M,(cols,rows)) 

# CROP
contours = find_and_order_contours(original_image)
c = contours[0]

rect = cv2.minAreaRect(c)
((x,y),(w,h),angle) = cv2.minAreaRect(c)

box = cv2.boxPoints(rect)

ext_left = tuple(c[c[:, :, 0].argmin()][0])
ext_right = tuple(c[c[:, :, 0].argmax()][0])
ext_top = tuple(c[c[:, :, 1].argmin()][0])
ext_bot = tuple(c[c[:, :, 1].argmax()][0])

original_image = original_image[ext_top[1] - 150:ext_bot[1]+150, ext_left[0] - 300:ext_right[0]+300]

cv2.imwrite(paths['outputfile'], original_image)


# https://stackoverflow.com/questions/51689127/python-opencv-perspective-correction-for-rectangle-with-rounded-corners
# https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/