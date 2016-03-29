import sys
import numpy as np
from operator import itemgetter, attrgetter
import Image
from math import *
import math

# Prend en argument un fichier .data
# Outputs the NN algorithm image from the .data file


try:
    sys.argv[1]
except NameError:
    startingpoint = 'Missing an arg'
else:
    startingpoint = sys.argv[1]

Tableau = []
BaseData = []
DECIMATION = 1 	# Should we do a basic summation on the pixels, hence reducing the noice and the size of the picture?

Tableau = []
k=0
with open(startingpoint, 'r') as echOpenLog:
	for line in echOpenLog:
	    line = line.split('\t')
	    del line[-1]		
	    Tableau.append(line)


SortedTable = Tableau
PointsPerLine = len(SortedTable[0])
NbOfLines = len(SortedTable)

# Debugging the image creation
print PointsPerLine 	# length of processed data
print NbOfLines 	# length of processed data


SortedTable = np.array(SortedTable).astype(int)
SortedTable = SortedTable[np.argsort(SortedTable[:,0])]
print SortedTable

# Refaire l'image
Depth = PointsPerLine
size = (NbOfLines,(int)(Depth/((DECIMATION)))) # aller jusqu'au bocal
ImagePoints=np.zeros(shape=(NbOfLines,Depth/DECIMATION))
ImagePoints = np.array(ImagePoints).astype(int)
#Prepare the png image
im = Image.new('RGB',size)
pix = im.load()


	
# Creation d'une image non scan-converted
for i in range(size[0]): # les lignes
    for j in range(size[1]):
	value = 0
	for k in range(DECIMATION):
		value = value + SortedTable[i][j*DECIMATION+k]*(1.9*(j*DECIMATION+k)**(0.6)/(Depth**(0.6)))
	value = int(value/DECIMATION)
	ImagePoints[i][j] = (int)(value/64)
        pix[i,j] = (ImagePoints[i][j],ImagePoints[i][j],ImagePoints[i][j]) 


outfile = startingpoint +"-DEC"+str(DECIMATION)+".png"
im.save(outfile)


# Doing a basic ScanConversion, on 120 lines images
if True: #comment
	X=np.zeros(shape=(size[0],size[1]))
	Y=np.zeros(shape=(size[0],size[1]))
	for i in range(size[0]):
	    for j in range(size[1]):
		X[i][j] = j*math.cos(math.radians(0.5*i-30)) #0.5 factor because 120*0.5 = 60 max in an out
		Y[i][j] = (size[1]+1)/2.0+j*math.sin(math.radians(0.5*(i)-30)) # same

	MaxDepth = int(size[1]*math.cos(math.radians(30)))

	sizeSC = (size[1],size[1])
	ScanConverted=np.zeros(shape=(size[1],size[1]))
	ScanConverted = ScanConverted + 40
	im = Image.new('RGB',(size[1],size[1]))
	pix = im.load()
	print sizeSC

	for i in range(MaxDepth):
	    if (i>=0 & i<(size[1])):
		    for j in range((size[1]/2-i/2),(size[1]/2+i/2)):
			D = (X-i)**2 + (Y-j)**2
			resul = np.unravel_index(D.argmin(), D.shape)
			# here is a basic NN, not even a 2-tap
			ScanConverted[i][j] = ImagePoints[resul[0]][resul[1]]

			value = int(ScanConverted[i][j])
			pix[j,i] = (value,value,value)
	    print i 
	outfile = startingpoint +"-DEC"+str(DECIMATION)+"-SC.png"
	im.save(outfile)

