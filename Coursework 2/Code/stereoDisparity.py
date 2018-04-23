# ------------------------- Packages --------------------------------
import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
from scipy import signal
import time
import random
import tkinter as tk
from PIL import ImageTk, Image
import os
from math import atan2
from itertools import groupby

def dispMap(Image1, Image2, windowSize):
	# Load images in grayscale
	img1 = cv2.imread('Photos/' + Image1,0)
	img1 = np.asarray(img1)
	img2 = cv2.imread('Photos/' + Image2,0)
	img2 = np.asarray(img2)

	# Initialisation
	halfWS = int((windowSize-1)/2)
	disparityMap = np.zeros(img1.shape)
	height, width = img1.shape
	disparityRange = int(min(width, height)/10)

	# Looping
	for i in range(width):
		minW = max(0, i-halfWS)
		maxW = min(width, i+halfWS)
		for j in range(height):
			minH = max(0, j-halfWS)
			maxH = min(height, j+halfWS)
			minD = max(-disparityRange, -minW);
			maxD = min(disparityRange, width - maxW);
			# Select the reference block from img1
			template = img1[minH:maxH, minW:maxW]
			# Get the number of blocks in this search.
			numBlocks = maxD - minD
			# Create a vector to hold the block differences.
			blockDiffs = np.zeros((numBlocks, 1));
			for k in range(minD,maxD):
				block = img2[minH:maxH, minW+k:maxW+k]		
				blockIndex = k - minD
				blockDiffs[blockIndex] = np.sum(abs(template - block))
			bestMatchDisp = np.amin(blockDiffs)
			bestMatchIdx = np.where(blockDiffs == bestMatchDisp)
			bestMatchIdx = bestMatchIdx[0][0]

			if bestMatchIdx == 0 or bestMatchIdx == numBlocks - 1:
				disparityMap[j,i] = bestMatchIdx + minD
			else:
				C1 = blockDiffs[bestMatchIdx-1]
				C2 = bestMatchDisp
				C3 = blockDiffs[bestMatchIdx+1]
				disparityMap[j,i] = bestMatchIdx + minD - 0.5*(C3-C1)/(C1-2*C2+C3)

	return disparityMap

resultat = dispMap('right.png','left.png', 11)
print(resultat)
plt.figure()
plt.imshow(resultat, interpolation='nearest')
plt.show()