import cv2, numpy as np

# # # # # # The purpose of this script is to make it easy to determine what HSV values are
# appropriate in trying to locate markers in a MoCap video file. Can use images
# or video.

# be sure to change this to coincide with OS
vid = '/home/godfreap/Desktop/Scripts/LeftLower_Trimmed.mp4'
cap = cv2.VideoCapture(vid)
# uncomment following line to debug with webcam
# cap = cv2.VideoCapture(0)

cv2.namedWindow('HSVColorBars')
cv2.namedWindow('trackbars')

# single image debug
# img = '/home/godfreap/Desktop/Scripts/LeftLower_Cropped.png'

def emptyCallback():
	pass

# get video properties
totalFrames = cap.get(7)
fps = cap.get(5)

# set up sliders
hh = 'H-Hue'
hl = 'L-Hue'
sh = 'H-Sat'
sl = 'L-Sat'
vh = 'H-Val'
vl = 'L-Val'
wnd = 'HSVColorBars'
trk = 'trackbars'
cv2.createTrackbar(hl, trk, 0, 179, emptyCallback)
cv2.createTrackbar(hh, trk, 0, 179, emptyCallback)
cv2.createTrackbar(sl, trk, 0, 255, emptyCallback)
cv2.createTrackbar(sh, trk, 0, 255, emptyCallback)
cv2.createTrackbar(vl, trk, 0, 255, emptyCallback)
cv2.createTrackbar(vh, trk, 0, 255, emptyCallback)

# set trackbar defaults for 'high' to max so image doesn't start blacked out
cv2.setTrackbarPos(hh,trk, 179)
cv2.setTrackbarPos(sh, trk, 255)
cv2.setTrackbarPos(vh, trk, 255)

while(1):
	# read the video, reset if last frame
	curFrame = cap.get(1)
	if curFrame == totalFrames:
		cap.set(1, 0)
	ret, frame = cap.read()

	# test with an image first, see if htat works
	# frame = cv2.imread(img)

	frame = cv2.GaussianBlur(frame, (5, 5), 0)
	hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# get values from the trackbar
	hul = cv2.getTrackbarPos(hl, trk)
	huh = cv2.getTrackbarPos(hh, trk)
	sal = cv2.getTrackbarPos(sl, trk)
	sah = cv2.getTrackbarPos(sh, trk)
	val = cv2.getTrackbarPos(vl, trk)
	vah = cv2.getTrackbarPos(vh, trk)

	hsvlow = np.array([hul, sal, val])
	hsvhigh = np.array([huh, sah, vah])

	mask = cv2.inRange(hsvimg, hsvlow, hsvhigh)
	res = cv2.bitwise_and(hsvimg, hsvimg, mask = mask)

	cv2.imshow(wnd, res)
	k = cv2.waitKey(5) & 0xFF
	if k == ord('q'):
		break

cv2.destroyAllWindows()