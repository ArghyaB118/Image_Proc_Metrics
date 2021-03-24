# pip install --upgrade pip
# pip install Pillow
# 0 = black = not segmented and 255 = white = segmented
from __future__ import division
from PIL import Image
import glob
import decimal
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure

image_list1 = []
image_list2 = []
filenames1 = glob.glob("GT/*.png")
filenames1.sort()
filenames2 = glob.glob("Output/*.png")
filenames2.sort()


GTnum = 0
for filename1 in filenames1: #assuming gif
    im1=Image.open(filename1)
    image_list1.append(im1)
    GTnum = GTnum + 1

SEGnum = 0
for filename2 in filenames2: #assuming gif
    im2=Image.open(filename2)
    image_list2.append(im2)
    SEGnum = SEGnum + 1

print GTnum, SEGnum

outputfile = "metrics.csv"

if (GTnum == SEGnum):
	with open(outputfile, 'w') as csvfile:
		for counter in range(0,GTnum):
			im1 = image_list1[counter]
			pixels1 = list(im1.getdata())
			width, height = im1.size
			pixels1 = [pixels1[i * width:(i + 1) * width] for i in xrange(height)]
			im2 = image_list2[counter]
			pixels2 = list(im2.getdata())
			width, height = im2.size
			pixels2 = [pixels2[i * width:(i + 1) * width] for i in xrange(height)]

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
			specificity = format(TN / (TN + FP), '.6f')
			#fmeasure = format((2 * precision * sensitivity / (precision + sensitivity)), '.6f')
			#print (TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)
			mcc = format((TP * TN - FP * FN) / math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)), '.6f')
			dice = format(2 * TP / (2 * TP + FP + FN), '.6f')
			jaccard = format(TP / (TP + FP + FN), '.6f')
			csvwriter = csv.writer(csvfile)
			row = [accuracy, precision, sensitivity, specificity, mcc, dice, jaccard] 
			csvwriter.writerow(row)

			new_img = Image.blend(im1, im2, 0.5)
			# Find contours at a constant value of 0.8
			contours = measure.find_contours(im1, 1)
			contours2 = measure.find_contours(im2, 1)

			# Display the image and plot all contours found
			fig, ax = plt.subplots()
			ax.imshow(new_img, cmap=plt.cm.gray)
			for contour in contours:
			    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
			for contour in contours2:
			    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

			#ax.axis('image')
			#ax.set_xticks([])
			#ax.set_yticks([])
			#plt.show()
			new_img_name = "Overlapped/" + str(counter) + "_overlapped.png"
			fig.savefig(new_img_name)
			plt.close()



