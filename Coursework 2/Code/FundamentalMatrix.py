def findFundamental(Image1, Image2, ImageA, ImageB):

	#ImageA = img1.jpg
	#ImageB = img3.jpg
	#Set of points manually selected from images, should be replaced with our own
	#interest points
	# Image1 = 'img1.jpg'
	# Image2 = 'img3.jpg'
	img1 = cv2.imread('Photos/' + Image1)
	img2 = cv2.imread('Photos/' + Image2)
	img1 = np.asarray(img1)
	img2 = np.asarray(img2)
	ImageA = np.concantenate(ImageA, np.ones((len(ImageA,1))))
	ImageB = np.concantenate(ImageB, np.ones((len(ImageB,1))))

	# ImageA = np.array([[253, 183, 1], 
	#                   [306, 196, 1],
	#                   [397, 211, 1],
	#                   [389, 329, 1],
	#                   [473, 391, 1],
	#                   [481, 279, 1],
	#                   [99, 473, 1],
	#                   [287, 435, 1],
	#                   [510, 110, 1]])
	# ImageB = np.array([[287, 196, 1],
	#                   [314, 222, 1],
	#                   [359, 260, 1],
	#                   [331, 359, 1],
	#                   [362, 429, 1], 
	#                   [387,338, 1],
	#                   [129, 431, 1],
	#                   [253, 435, 1],
	#                   [433, 205, 1]])

	shape = img1.shape

	nbPoints = len(ImageA)
	chi = np.zeros((nbPoints, 9))

	#populate chi matrix
	for i in range(0,nbPoints):
		chi[i][:] = [ImageA[i,0]*ImageB[i,0], ImageA[i,0]*ImageB[i,1], ImageA[i,0], ImageA[i,1]*ImageB[i,0], ImageA[i,1]*ImageB[i,1], ImageA[i,1], ImageB[i,0], ImageB[i,1], 1]

	U, S, V = np.linalg.svd(chi)
	F = V.T[:,-1].reshape(3,3) / V[-1][-1]
	detF = np.linalg.det(F)

	FU, FD, FV = np.linalg.svd(F)
	FV = FV.T
	FD = np.diagflat(FD)
	FD[-1][-1] = 0
	F = np.dot(FU, np.dot(FD,FV.T))

	print(F)

	plt.figure()
	plt.subplot(2,1,1), plt.imshow(img1)
	plt.subplot(2,1,2), plt.imshow(img2)

	colour = ['yellow', 'red','gold', 'chartreuse', 'lightseagreen', 
			  'darkturquoise', 'navy', 'mediumpurple', 'darkorchid', 'white'
			  'magenta', 'black','coral', 'orange', 'ivory',
			  'salmon','silver','teal','orchid','plum']

	for i in range(0,nbPoints):

		# Finding epipolar line on image 1
		epipole1 = FV.T[:,-1]
		epipole1 = epipole1/epipole1[-1]
		epipole_x = np.arange(2*shape[0])
		epipole_y = ImageA[i,1] + (epipole_x - ImageA[i,0])*(epipole1[1]-ImageA[i,1])/(epipole1[0]-ImageA[i,0])

		# Finding epipolar line on image 2
		Epipolar = np.dot(F, ImageA[i,:].T)
		Epipolar_x = np.arange(2*shape[0])
		Epipolar_y = (-Epipolar[2] - Epipolar[0]*Epipolar_x)/Epipolar[1]

		# Plotting epipolar lines onto images
		plt.subplot(2,1,1), plt.plot(ImageA[i,0], ImageA[i,1], '+', color=colour[i])
		plt.plot(epipole_x, epipole_y, color=colour[i])
		plt.axis([0, shape[1], shape[0], 0])
		plt.subplot(2,1,2), plt.plot(ImageB[i,0], ImageB[i,1], '+', color=colour[i])
		plt.plot(Epipolar_x, Epipolar_y, color=colour[i])
		plt.axis([0, shape[1], shape[0], 0])

	plt.show()