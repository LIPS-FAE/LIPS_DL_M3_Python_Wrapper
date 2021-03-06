import cv2
import numpy as np
from openni import openni2
from openni import _openni2 as c_api
openni2.initialize("C:\Program Files\OpenNI2\Tools")	# can also accept the path of the OpenNI redistribution
dev = openni2.Device.open_any()
color_stream = dev.create_color_stream()
color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 640, resolutionY = 480, fps = 30))
color_stream.start()

while True:
	frame = color_stream.read_frame()
	frame_data = frame.get_buffer_as_uint8()
	img_bgr = np.frombuffer(frame_data, dtype=np.uint8)
	img_bgr.shape = (480, 640, 3)

	#Change OpenCV BGR to RGB and show color image from cv2
	img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
	cv2.namedWindow("image", cv2.WINDOW_NORMAL)
	cv2.imshow("image", img_rgb)
	cv2.waitKey(34)
	
	if (cv2.waitKey(1) == 27):
		break

openni2.unload()
cv2.destroyAllWindows()
