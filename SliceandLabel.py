import cv2
import os
import math
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def alphabet2letter(iterator):

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
    if itr < 26:
        return alphabet[iterator]
    elif itr >= 26:
        return alphabet[math.floor(itr/26)-1] + alphabet[iterator % 26]


pic_path = '/Users/dgomez/Desktop/pics'
font_path = '/Users/dgomez/Desktop/font/cmunrm.ttf'

os.chdir(pic_path)

picture_list = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]

if '.DS_Store' in picture_list:
    picture_list.remove('.DS_Store')

picture_list = sorted(picture_list, key=lambda x: float(x.split('t')[1]))
border = [0, 1, 0, 0]
y = 136
h = 140
x = 0
w = 512
ROI = [x, x+w, y, y+h]
WHITE = [255, 255, 255]
count = 0
xspace = 5
yspace = 1
pix = (xspace, yspace)
color = (255, 255, 255)
itr = 0
run = '3'
letter = alphabet2letter(itr)

font = ImageFont.truetype(font_path, 16)

FinalImagePath = '/Users/dgomez/Desktop/Final.tiff'
stackedImageOG = cv2.imread(picture_list[0])
croppedImageOG = stackedImageOG[y:y+h, x:x+w]
borderImageOG = cv2.copyMakeBorder(croppedImageOG, border[0], border[1], border[2], border[3], cv2.BORDER_CONSTANT,
                                   value=WHITE)
cv2.imwrite(FinalImagePath, borderImageOG)
writeImageOG = Image.open(FinalImagePath)
drawImageOG = ImageDraw.Draw(writeImageOG)

drawImageOG.text(pix, run+letter, color, font=font)
writeImageOG.save(FinalImagePath)
itr += 1
letter = alphabet2letter(itr)
pix = (pix[0], pix[1]+h+border[1])

for i in range(len(picture_list)-1):
    stackedImage = cv2.imread(picture_list[i+1])
    croppedImage = stackedImage[y:y+h, x:x+w]
    borderImage = cv2.copyMakeBorder(croppedImage, border[0], border[1], border[2], border[3], cv2.BORDER_CONSTANT,
                                     value=WHITE)
    intImage = cv2.imread(FinalImagePath)
    intImage = np.concatenate((intImage, borderImage), axis=0)
    cv2.imwrite(FinalImagePath, intImage)
    writeImage = Image.open(FinalImagePath)
    draw = ImageDraw.Draw(writeImage)
    draw.text(pix, run+letter, color, font=font)
    itr += 1
    pix = (pix[0], pix[1]+h+border[1])
    letter = alphabet2letter(itr)
    writeImage.save(FinalImagePath)
