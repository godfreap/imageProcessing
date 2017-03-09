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
cv2.createTrackbar(hl, wnd, 0, 179, emptyCallback)
cv2.createTrackbar(hh, wnd, 0, 179, emptyCallback)
cv2.createTrackbar(sl, wnd, 0, 255, emptyCallback)
cv2.createTrackbar(sh, wnd, 0, 255, emptyCallback)
cv2.createTrackbar(vl, wnd, 0, 255, emptyCallback)
cv2.createTrackbar(vh, wnd, 0, 255, emptyCallback)

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
	hul = cv2.getTrackbarPos(hl, wnd)
	huh = cv2.getTrackbarPos(hh, wnd)
	sal = cv2.getTrackbarPos(sl, wnd)
	sah = cv2.getTrackbarPos(sh, wnd)
	val = cv2.getTrackbarPos(vl, wnd)
	vah = cv2.getTrackbarPos(vh, wnd)

	hsvlow = np.array([hul, sal, val])
	hsvhigh = np.array([huh, sah, vah])

	mask = cv2.inRange(hsvimg, hsvlow, hsvhigh)
	res = cv2.bitwise_and(hsvimg, hsvimg, mask = mask)

	cv2.imshow(wnd, res)
	k = cv2.waitKey(5) & 0xFF
	if k == ord('q'):
		break

cv2.destroyAllWindows()