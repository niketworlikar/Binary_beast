
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
from PIL import Image

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

#im1 = Image.open("r6.jpg")
#new_img=im1.resize(500,500)
image = cv2.imread('r7.png',0)
image2 = cv2.imread('r7.png',1)

#im.save("new_img.jpg")
gray = cv2.GaussianBlur(image, (7, 7), 0)


edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

for c in cnts:
	if cv2.contourArea(c) < 25000:
		continue

	#image2 = image.copy()
	box = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")

	
	box = perspective.order_points(box)
	cv2.drawContours(image2, [box.astype("int")], -1, (0, 255, 0), 2)

	for (x, y) in box:
		cv2.circle(image2, (int(x), int(y)), 5, (0, 0, 255), -1)

	
	(tl, tr, br, bl) = box
	(tltrX, tltrY) = midpoint(tl, tr)
	(blbrX, blbrY) = midpoint(bl, br)

	
	(tlblX, tlblY) = midpoint(tl, bl)
	(trbrX, trbrY) = midpoint(tr, br)

	cv2.circle(image2, (int(tltrX), int(tltrY)), 5, (0, 255, 0), -1)
	cv2.circle(image2, (int(blbrX), int(blbrY)), 5,(0, 255, 0), -1)
	cv2.circle(image2, (int(tlblX), int(tlblY)), 5, (0, 255, 0), -1)
	cv2.circle(image2, (int(trbrX), int(trbrY)), 5, (0, 255, 0), -1)

	cv2.line(image2, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
		(0, 255, 0), 2)
	cv2.line(image2, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
		(0, 255, 0), 2)

	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

	
	if pixelsPerMetric is None:
		pixelsPerMetric = dB / 200

	"""dimA = dA / pixelsPerMetric
	dimB = dB / pixelsPerMetric

	draw the object sizes on the image
	cv2.putText(image2, "{:.1f}in".format(dimA),
		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 0), 2)
	cv2.putText(image2, "{:.1f}in".format(dimB),
		(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 0), 2)"""

	cv2.imshow("Image", image2)
	cv2.imwrite('pics/output.jpg', image2)
	cv2.waitKey(0)