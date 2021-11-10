import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

img = cv2.imread('./source/s1.jpg')
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

plt.show()