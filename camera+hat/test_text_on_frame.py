import cv2

image = cv2.imread('/home/ama/disertation_project/camera+hat/test.jpg')
text = "Sample Text"
org = (50, 50)  # Bottom-left corner of the text string in the image
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (255, 0, 0)  # Blue color in BGR
thickness = 2

cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()