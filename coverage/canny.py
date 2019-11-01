# OpenCV program to perform Edge detection in real time 
# import libraries of python OpenCV  
# where its functionality resides 
import cv2  
  
# np is an alias pointing to numpy library 
import numpy as np 
  
img = cv2.imread('testing-images/image048.jpg')
cv2.imshow('img', img)

# finds edges in the input image image and 
# marks them in the output map edges 
edges = cv2.Canny(img,100,200) 

# Display edges in a frame 
cv2.imshow('Edges', edges) 

cv2.waitKey(0)
# De-allocate any associated memory usage 
cv2.destroyAllWindows()