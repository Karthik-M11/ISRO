
# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import cv2


def led_finder(image):
    
    # dimension = image.shape    

    # convert it to grayscale, and blur it
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.blur(gray_image, (11,11))

    # threshold the image to reveal light regions in the blurred image
    threshold_image = cv2.threshold(blur_image, 90, 255, cv2.THRESH_BINARY)[1]

    # perform a series of erosions and dilations to remove any small blobs of noise from the thresholded image
    threshold_image = cv2.erode(threshold_image, None, iterations=2)
    threshold_image = cv2.dilate(threshold_image, None, iterations=3)

    # Using Hough circles transform to identify the circles in the given image
    circles = cv2.HoughCircles(threshold_image, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=100, param2=50,
                               minRadius=50, maxRadius=100)
    
    # Executed if no circles are identified in the given image
    if circles is None:
        return [], [], threshold_image
    # Executed if circles are identified in the given image
    else:
        center_list = []
        rad_list = []
        # To draw the circle outline
        for i in circles[0, :]:
            center = (int(i[0]), int(i[1]))
            radius = int(i[2]) - 2
            cv2.circle(image, center, radius, (0, 0, 255), 3)
            
            center_list.append(center)
            rad_list.append(radius)

        # cv2.imshow(f"{image_name}_result", image)    
        # cv2.imwrite(f"{image_name}_result.png", image)
        # cv2.waitKey(0)     
                       
        return center_list, rad_list, threshold_image
    

IP = r"http://192.168.104.197:8080/video"
# video = cv2.VideoCapture(IP)

# while video.isOpened():
#     _, frame = video.read()
#     center, radius, thresh = led_finder(frame)
#     for i in range(len(center)):
#         area = 3.14 * radius[i]**2
#         # cv2.putText(img=frame, text=f"Area:{area}", org=center[i], fontFace=10, fontScale=1, color=(255, 0, 0))
#     # print(type(thresh))
#     cv2.imshow('Title', frame)
#     if cv2.waitKey(1) == ord('q'): break

img = cv2.imread('moon.jpg', 1)
center, rad, thresh = led_finder(img)
cv2.imshow('title', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows




# image_png = args.image # Obtains the image file name from the argument parser
# image = cv2.imread(image_png, 1) # Reads the image
# image_name = image_png.split('.')[0]
# type_list, cen_list = led_finder(image, image_name)

# # Code to create file image_name.txt corresponding to the image_name.png file.
# with open(f"{image_name}.txt", "w") as file:
#         for i in range(len(type_list)):
#             file.write(f"Organism Type: {type_list[i]}\n")
#             file.write(f"Centroid: {cen_list[i]}\n\n")
# file.close()