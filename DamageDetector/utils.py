element_colors = dict()
element_colors['anemo'] = (208, 255, 120)
element_colors['geo'] = (105, 198, 243)
element_colors['electro'] = (255, 139, 222)
element_colors['physical'] = (255, 255, 255)
element_colors['pyro'] = (0, 158, 243)
element_colors['cyro'] = (255, 255, 164)
element_colors['hydro'] = (251, 216, 63)
element_color_HSV = dict()
element_color_HSV['anemo'] = (112, 141, 255)
element_color_HSV['geo'] = (29, 147, 250)
element_color_HSV['electro'] = (200, 124, 248)
element_color_HSV['physical'] = (71, 3, 255)
element_color_HSV['pyro'] = ( 27, 253, 240)
element_color_HSV['cyro'] = (128,  94, 255)
element_color_HSV['hydro'] = (136, 194, 250)

import cv2

templates = []
for i in range(10):
  templates.append(cv2.resize(cv2.imread('./DamageDetector/templates/' + str(i) + '.png', 0), (36, 36)))

def matching_number(im):
  maxVal_All = 999999999999999
  num_dsp = 0
  resizedIm = cv2.resize(im, (36, 36))
  for i in range(10):

    result= abs(resizedIm - templates[i]).sum()
    maxVal=result  
        
    if maxVal < maxVal_All:
        num_dsp = i
        maxVal_All = maxVal
    
  return num_dsp