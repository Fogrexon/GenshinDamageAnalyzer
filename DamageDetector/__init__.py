import cv2
from DamageDetector.utils import element_color_HSV, matching_number
import numpy as np

counter = 0

class Detector:
  def __init__(self, scale, key):
    self.scale = scale
    self.key = key

  def restore_rect(self, rect):
    return (int(rect[0] / self.scale), int(rect[1] / self.scale), int(rect[2] / self.scale), int(rect[3] / self.scale))
  
  def binarize(self, image):
    color = element_color_HSV[self.key]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    binarized = cv2.inRange(hsv_image,
      (max(color[0] - 5, 0), max(color[1] - 25, 0), max(color[2] - 20, 0)),
      (min(255, color[0] + 5), min(255, color[1] + 25), min(color[2] + 20, 255))
    )
    return binarized
  
  def get_number(self, image):
    global counter
    height, _, _ = image.shape
    binarized = self.binarize(image)
    closing = cv2.dilate(binarized,(2, 2),iterations = 1)
    thresh = cv2.adaptiveThreshold(closing, 255, 1, 1, 5, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) < 4:
      return 0
    lists = []
    for cnt in contours:
      nextRect = cv2.boundingRect(cnt)
      x2, y2, w2, h2 = nextRect
      if h2 < 0.8 * height or w2 / h2 > 1:
        continue
      num = matching_number(closing[y2:y2+h2,x2:x2+w2])
      lists.append((num, x2))
    
    lists.sort(key=lambda x: -x[1])
    total = 0
    for i, value in enumerate(lists):
      total += value[0] * (10 ** i) 

    return total

  def get_damage_outline(self, image):
    height, width, _ = image.shape
    resized = cv2.resize(image, (int(width * self.scale), int(height * self.scale)))
    binarized = self.binarize(resized)
    thresh = cv2.adaptiveThreshold(binarized, 255, 1, 1, 7, 2)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    number_outlines = []
    for cnt in contours:
      rect = cv2.boundingRect(cnt.astype(np.int32))
      x, y, w, h = self.restore_rect(rect)
      

      if h < height / 30 or w / (h * 0.8) < 3:
        continue
      number_outlines.append((x, y, w, h))

    return number_outlines

  def get_damages(self, image):
    outlines = self.get_damage_outline(image)
    result = []
    for rect in outlines:
      x, y, w, h = rect
      
      cropped = image[y:y+h, x:x+w, :]
      num = self.get_number(cropped)
      if num < 1000:
        continue
      result.append({
        "number": num,
        "rect": rect
      })
    return result




