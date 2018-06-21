# Author: Diego Gomez   dgomez1@tulane.edu
# Date: June 19th, 2018
# Write Time: ~ 2.5hrs (not including commenting)
# Purpose: To take 512x512 images, crop and merge them on top of one another.

# Lines 21 -> 27 are where we load the python modules for this script. Each one of these is needed but
# the order does not.
#
# Line 21 is where we import module cv2. This stands for computer vision library version 2 http://opencv.org.
# This module will be used in the opening, modifying and writing of the images used.
#
# Line 22 -> 23 is where we import rename and listdir (list directory) from the os module. os module is used for
# interacting with the terminal through python itself. We will use these to navigate through directories in this script
#
# Line 24 is where we import numpy using the namespace np. Numpy will be used to add the pixels together to create the
# final image
#
# Lines 25 -> 27 is where we import PIL. This stands for python imaging library
# https://pillow.readthedocs.io/en/3.0.x/index.html. This module will be used for writing the text on the final image.

import cv2
from os import rename, listdir
import os
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

os.chdir("/Users/dgomez/Desktop/pics")  # Changing the working directory to where the picture files are stored.
badprefex = "40x_ipor2_x_run021 (very nice black background first pictures)"  # The removal of most of the junk that's
# at the beginning of the file names
fnames = listdir('.')  # All fnames (file names) are listed here by telling python to list directory all the content
# that contains a . this is probably poor schema because it relies on the user to only have files that are image type
# and directories that do not have a period but since I did this pretty fast I'll go with it.

for fname in fnames:  # Here we start to iterate through each fname (file) in fnames (all files)
    if fname.startswith(badprefex):  # If the file name starts with the badprefex then ->
        rename(fname, fname.replace(badprefex, "", 1))  # rename fname by replacing the bad prefix with nothing and do
        # it one time. This is the python way of removing the bad prefix.

picture_list = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]  # Here I am creating a picture
# list by going through everything that's listed in the directory that I'm in and if it is a file then add it
# to picture list. picture list would now look something like this:
# print(picture_list) -> ['.DS_Store', 't0111.tif', 't0112.tif',
# 't0113.tif', 't0114.tif', 't0115.tif', 't0116.tif', 't0117.tif', 't0118.tif', 't0119.tif']

if '.DS_Store' in picture_list:  # We don't care about the .DS_Store file which contains the custom attributes
    # of this folder like icon size, placement or background so if it is in the list it gets removed.
    picture_list.remove('.DS_Store')

# Here is where we define the dimensions for where we want to take our slices of this picture. The Region of Interest
# (ROI) will begin at 160 pixels (counted from the top) and span another 80 pixels towards the bottom and the
# entire width of the picture that is 512 pixels. These lines are "hard coded" right now and if this were to be a more
# robust program it would probably make more sense to access the image size.

y = 136
h = 140
x = 0
w = 512
count = 0  # Initialization of the count variable that we will use to name the cropped images.

for picture in picture_list:  # For each picture in my list of pictures
    img = cv2.imread(picture)  # Create a dummy variable call img (image) and use the function from the cv2 module
    # imread (image read) to read in the pictures within the list of pictures
    crop_img = img[y:y+h, x:x+w]  # My cropped image will be the read in img from the line above and spanned by my ROI
    cv2.imwrite("/Users/dgomez/Desktop/pics/cropped/cropped%d.tiff" % count, crop_img)  # Then write this cropped image
    # to a new directory located here
    count += 1  # Each time you go through the loop the count adds one to itself

os.chdir("/Users/dgomez/Desktop/pics/cropped")  # Now change directory to where the cropped images are
cropped_list = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]  # Create a list of all the cropped
# images. It will look something like this:
# print(cropped_list) ->  ['cropped0.tiff', 'cropped1.tiff', 'cropped2.tiff',
# 'cropped3.tiff', 'cropped4.tiff', 'cropped5.tiff', 'cropped6.tiff', 'cropped7.tiff', 'cropped8.tiff']

if '.DS_Store' in cropped_list:  # Again if .DS_Store file is in the list remove it
    cropped_list.remove('.DS_Store')

# Here we define the border length as one pixel
border = 1

# Create the intImage (intermediate Image) which will be the image that will "appended" to the bottom by the
# subsequent images by reading the first cropped image in the list
intImage = cv2.imread(cropped_list[0])
intImage = cv2.copyMakeBorder(intImage, 0, border, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])  # Add the border
# to the image with 0 border at the top, border of length border on the bottom and 0 border on the left and right.
# The border will be constant and the color of it in [r, g, b] is [255, 255, 255] which is white.

for i in range(len(cropped_list)-1):  # Iterate through all pictures in the cropped list
    image = cv2.imread(cropped_list[i+1])  # Start at the second picture
    image = cv2.copyMakeBorder(image, 0, border, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])  # Create a border
    # the same  as the line above
    intImage = np.concatenate((intImage, image), axis=0)  # Add the new image the the previous image. This line
    # stacks the images on one another vertically by setting axis = 0. We use np.concatenate because python saves these
    # images as arrays. Within each array is the information for each pixel, it's location (denoted by its position in
    # the array) and its color. To create a larger image you can just add these arrays to each other.

finalImage = intImage  # Bogus line setting finalImage to the stacked image

cv2.imwrite('/Users/dgomez/Desktop/FINALIMAGE.tiff', finalImage)  # Write the final Image to the desktop

run = '3'  # This is the number prefix that will show up on the image

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']  # This is the alphabet that we'll be iterating
# through to display which picture we're looking at

xspace = 5  # Setting the distance from the left side that the
yspace = 1  # This is what the spacing from the "border" is
pix = (xspace, yspace)  # The pixel location in the photo where the text will go
color = (255, 255, 255)  # This corresponds to the color white in RGB
itr = 0  # Variable that is iterating through the alphabet. Since we want to start at A we initialize the variable to
# Start at 0

img = Image.open('/Users/dgomez/Desktop/FINALIMAGE.tiff')  # Here we open the stacked image and save it to img
draw = ImageDraw.Draw(img)  # We open that image for drawing and call it draw
font = ImageFont.truetype('/Users/dgomez/Desktop/font/cmunrm.ttf', 16)  # Here we set the font type from a downloaded
# font file https://www.fontsquirrel.com/fonts/computer-modern and is the standard font for LaTex

for j in range(len(cropped_list)):  # I want to draw on every slice on the stacked photo which is the length of the
    # cropped list
    draw.text(pix, run+alphabet[itr], color, font=font)  # Draw on the "draw" photo using
    # text at the pixel location, write the run number and the corresponding letter for each photo, the color we want
    # the text to be and that the font equals the font we defined in line 117
    itr += 1  # Add one to the iterator so the next text contains the next letter
    pix = (pix[0], pix[1]+h+border)  # Change the pixel location. X is constant and will always be where xspace is
    # and y will change by the height of the sliced photos plus the border size.

img.save('/Users/dgomez/Desktop/TextImage.tiff')  # Viola we have finished our photo and we now save it to the desktop

# NOTES:
# This program works but is super inefficient. If you showed this to a serious python developer they might have a heart
# attack. The 3rd for loop (115 -> 122) should probably be incorporated into the 2nd (84 -> 91) but because this was
# done with haste and the number of photos that we're processing is relatively small it's not a big deal. This code
# also only works for 512x512 pixel images. Future versions should include adding the 3rd loop into the 2nd, removal
# of line 98, lines 56 -> 59 should not be "hard coded" and should access photo dimensions, image opening is all over
# the place and file names should be treated with more care and general robustness should be added throughout.
