# Author: Manato Ogawa
# Email: maogawa@wisc.edu
# Sources:
#   -https://www.geeksforgeeks.org/find-and-draw-contours-using-opencv-python/ (helped with findContours method)
#   -https://redketchup.io/color-picker (helped identifying the RGB values of the cones)
#   -https://www.projectpro.io/recipes/detect-specific-colors-from-image-opencv (helped with the inRange method)

# Import statements
import cv2
import numpy as np

# path to original red.png image and load into code and resize
original_image = cv2.imread('C:/Users/manat/WISC_autonomous/red.png')
original_image = cv2.resize(original_image, (600, 900))

# setting the color boundaries that I want the inRange function to detect later
lower_red = np.array([0, 0, 180], dtype = "uint8")
upper_red= np.array([80, 80, 230], dtype = "uint8")

# the inRange function allows for me to filter out unneccessary colors like black
# or green and only focus on important colors like the colors of the cones
mask = cv2.inRange(original_image, lower_red, upper_red)

# this creates the image that only shows the pixels of the filtered colors in the image
# shows cone shaped orange images and couple of patches that have similar colors to the
# cones with the background being pitch black
detected_output = cv2.bitwise_and(original_image, original_image, mask = mask)

# saving the newly created image in order to run methods to the new image
cv2.imwrite('C:/Users/manat/WISC_autonomous/detected_output.png', detected_output)

# loading new image that I previously created into code
image = cv2.imread('C:/Users/manat/WISC_autonomous/detected_output.png')

# applies a gray scale to the image which allows me to use the findContours method in the future
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

# I applied blur to minimize the noise of unwanted pixels like the patches that were shown
# so the findContours method can properly outline the cones and only the cones
blurred = cv2.GaussianBlur(gray, (5, 5), 0)


# the Canny method finds edges in the image which helps the findContours method to properly outline
# the cones
edged = cv2.Canny(blurred, 30, 200) 

# shows image with white outline of the cones
#cv2.imshow('Contours', edged) 
  
# the findContours method finds contours or outline of an object in a given image. in this case
# the Canny method helped in finding the edges of the cones which helps the findContours method to
# easily identify the cone shaped objects and draw a proper outline around each of the cones
contours, hierarchy = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

# draw all contours 
# -1 signifies drawing all contours 
cv2.drawContours(image, contours, -1, (255, 255, 255), 3) 

# list which will contain all of the coordinates of the contours
contour_points = []

# list of unique contour clusters and will later be filled with the midpoint
# of all of the contours of a specific cone to find the center
contour_cluster = []

# adds all of the coordinates to the contour_points list
for contour in contours:
    for point in contour:
        x, y = point[0]
        x = x.item()
        y = y.item()
        contour_points.append([x,y])
    
# represent the x and y of a cluster which will be updated after a new cluster
# is detected in a future loop
check_x = contour_points[0][0]
check_y = contour_points[0][1]

# identifies the height and width of the image from the cv2.imshow method
width = image.shape[1]
height = image.shape[0]

# sum of each of the x and y coordinates which allows me to find the midpoint
# of all of the contour points to find the coordinate of the center of the cone
mid_x_sum = 0
mid_y_sum = 0

# amount of contour points which will be used to divide with the sum to find
# the midpoint of the cone
mid_x_entry = 0
mid_y_entry = 0

# this loop will check the different clusters in the contour_points list. if it
# doesn't find a new cluster, it will add up the x and y coordinates which will
# allow for me to find the mid point of each of the clusters/cones. if the method
# finds a new cluster, it will calculate the midpoint of the previous cluster and 
# reset all the values to 0 to start over for the new cluster
for i in range(len(contour_points)):
    if abs(contour_points[i][0]-check_x) > width*.05 and abs(contour_points[i][1]-check_y) > height*.0015:
        contour_cluster.append([int(mid_x_sum/mid_x_entry), int(mid_y_sum/mid_y_entry)])
        check_x = contour_points[i][0]
        check_y = contour_points[i][1]
        mid_x_sum = 0
        mid_y_sum = 0
        mid_x_entry = 0
        mid_y_entry = 0
    else:
        mid_x_sum = mid_x_sum + contour_points[i][0]
        mid_y_sum = mid_y_sum + contour_points[i][1]
        mid_x_entry = mid_x_entry + 1
        mid_y_entry = mid_y_entry + 1

# records the x difference between two points
dif_max = 0

# records the index at which there is the greatest x difference
dif_max_index = 0

# sorts the contour_cluster array so that the coordinates go in ascending order
contour_cluster.sort()

# finds the index with the biggest leap indicating that that index is the last point
# that represents the left side of the cones
for i in range(len(contour_cluster)-1):
    if contour_cluster[i+1][0] - contour_cluster[i][0] > dif_max:
        dif_max = contour_cluster[i+1][0] - contour_cluster[i][0]
        dif_max_index = i

# left side slope of cones
left_slope = (contour_cluster[dif_max_index][1] - contour_cluster[0][1]) / (contour_cluster[dif_max_index][0] - contour_cluster[0][0])

# right side slope of cones
right_slope = (contour_cluster[len(contour_cluster)-1][1] - contour_cluster[dif_max_index + 1][1]) / (contour_cluster[len(contour_cluster)-1][0] - contour_cluster[dif_max_index + 1][0])

# bottom left point on the left line 
btm_left_x = 0
btm_left_y = int(left_slope * (btm_left_x - contour_cluster[0][0])) + contour_cluster[0][1]

# top right point on the left line 
top_right_y = 0
top_right_x = int((top_right_y - contour_cluster[dif_max_index][1]) / left_slope) + contour_cluster[dif_max_index][0]

# top left point on the right line
top_left_x = int(contour_cluster[dif_max_index + 1][0] - (contour_cluster[dif_max_index + 1][1] / right_slope))
top_left_y = 0

# bottom right point on the right line
btm_right_x = 600
btm_right_y = int((600 - contour_cluster[len(contour_cluster)-1][0]) * right_slope + contour_cluster[len(contour_cluster)-1][1])

# draws the two lines
cv2.line(original_image, (btm_left_x, btm_left_y), (top_right_x, top_right_y), (0,0,255), 2)
cv2.line(original_image, (top_left_x, top_left_y), (btm_right_x, btm_right_y), (0,0,255), 2)


# displays image with the lines
cv2.imshow('Contours', original_image) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 
