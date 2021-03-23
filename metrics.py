# pip install --upgrade pip
# pip install Pillow
# 0 = black = not segmented and 255 = white = segmented
from __future__ import division
from PIL import Image
import glob
import decimal
import csv

image_list1 = []
image_list2 = []
filenames1 = glob.glob("GT/*.png")
filenames1.sort()
filenames2 = glob.glob("Output/*.png")
filenames2.sort()


i = 0
for filename1 in filenames1: #assuming gif
    im1=Image.open(filename1)
    image_list1.append(im1)
    i = i + 1

j = 0
for filename2 in filenames2: #assuming gif
    im2=Image.open(filename2)
    image_list2.append(im2)
    j = j + 1

print i , j

outputfile = "metrics.csv"

if (i == j):
	with open(outputfile, 'w') as csvfile:
		for counter in range(0,i):
			im1 = image_list1[counter]
			pixels1 = list(im1.getdata())
			width, height = im1.size
			pixels1 = [pixels1[i * width:(i + 1) * width] for i in xrange(height)]
			im2 = image_list2[counter]
			pixels2 = list(im2.getdata())
			width, height = im2.size
			pixels2 = [pixels2[i * width:(i + 1) * width] for i in xrange(height)]

			counter2 = 0
			TP = FP = FN = TN = 0
			for k in range(0, width):
				for m in range(0, height):
					#print pixels1[k][m], pixels2[k][m]
					if (pixels1[k][m] == 0 and pixels2[k][m] == 0):
						TN = TN + 1
					elif (pixels1[k][m] != 0 and pixels2[k][m] != 0):
						TP = TP + 1
					elif (pixels1[k][m] != 0 and pixels2[k][m] == 0):
						FN = FN + 1
					elif (pixels1[k][m] == 0 and pixels2[k][m] != 0):
						FP = FP + 1
			accuracy = format((TP + TN) * 100 / width / height, '.6f')
			precision = format(TP / (TP + FP), '.6f')
			sensitivity = format(TP / (TP + FN), '.6f')
			csvwriter = csv.writer(csvfile)
			row = [accuracy, precision, sensitivity] 
			csvwriter.writerow(row)



