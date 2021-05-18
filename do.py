import numpy as np
import requests
import cv2


while True:
  response = requests.get(url="http://esp-WiFi.local:80/capture")
  img_str = response.content

  nparr = np.frombuffer(img_str, np.uint8)
  frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

  cv2.imshow('image', frame)
  cv2.waitKey(1)
