import numpy as np
import cv2
import sys, getopt
import math

def load_files(inputfile):
   print('Loading file...') 
   return cv2.imread(inputfile)

def parse_args():
   inputfile = ''
   outputfile = ''
   scale = '1.2'
   debug = False
   text = ''
   try:
      opts, args = getopt.getopt(sys.argv[1:],'dhi:o:s:t:',['ifile=','ofile=', 'scale=', 'debug', 'text='])
   except getopt.GetoptError:
      print( 'test.py -i <inputfile> -o <outputfile> -s <scale ammount>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print( 'test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ('-i', '--ifile'):
         inputfile = arg
      elif opt in ('-o', '--ofile'):
         outputfile = arg
      elif opt in ('-s', '--scale'):
         scale = arg
      elif opt in ('-d', '--debug'):
         debug = True
      elif opt in ('-t', '--text'):
         text = arg 
   return {'inputfile': inputfile, 'outputfile' : outputfile, 'scale': scale, 'debug': debug, 'text': text}
    
def find_and_order_contours(image):
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   gray = cv2.GaussianBlur(gray, (5, 5), 0)
   blur = cv2.GaussianBlur(gray,(1,1),1000)
   edged = cv2.Canny(gray, 75, 200)
   contours, hierarchy  = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   return sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

def bounding_debug(image, border):
   cv2.drawContours(image,[border] , -1, (255, 255, 0), 5)
   M = cv2.moments(border)
   cX = int(M['m10'] / M['m00'])
   cY = int(M['m01'] / M['m00'])
   cv2.drawContours(image, [border], -1, (0, 255, 0), 2)
   cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
   cv2.putText(image, 'center', (cX - 20, cY - 20),
      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# ---- MAIN PROGRAM ----
config = parse_args()

original_image = load_files(config['inputfile'])
border = find_and_order_contours(original_image)[0]

if config['debug']:
   bounding_debug(original_image,border)

rect = cv2.minAreaRect(border)
box = cv2.boxPoints(rect)
box = np.int0(box)

scale = float(config['scale'])
W = rect[1][0]
H = rect[1][1]

Xs = [i[0] for i in box]
Ys = [i[1] for i in box]
x1 = min(Xs)
x2 = max(Xs)
y1 = min(Ys)
y2 = max(Ys)

angle = rect[2]
rotated = False
if angle < -45:
    angle += 90
    rotated = True

center = (int((x1+x2)/2), int((y1+y2)/2))
size = (int(scale*(x2-x1)), int(scale*(y2-y1)))

M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)

cropped = cv2.getRectSubPix(original_image, size, center)
cropped = cv2.warpAffine(cropped, M, size)

croppedW = W if not rotated else H
croppedH = H if not rotated else W

original_image = cv2.getRectSubPix(
    cropped, (int(croppedW*scale), int(croppedH*scale)), (size[0]/2, size[1]/2))

rows,cols = original_image.shape[:2]

if config['text']:
   cv2.putText(original_image, config['text'], (10, int(croppedH*scale) - 10),
      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)


print('saving...')
if config['outputfile']:
   cv2.imwrite(config['outputfile'], original_image)
else:
   op = config['inputfile'].rsplit( ".", 1 )
   op = op[0] + '-op.' + op[1]
   cv2.imwrite(op, original_image)

