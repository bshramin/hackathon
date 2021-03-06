import numpy as np
import imutils
import requests
import cv2
import time


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

number_of_regions = []
start_time = time.time()

while True:
    response = requests.get(url="http://esp-WiFi.local:80/capture")
        
    img_str = response.content

    nparr = np.frombuffer(img_str, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if response.status_code == 200:
        image = imutils.resize(
            image,
            width=min(400, image.shape[1])
        )
        image = imutils.rotate(
            image,
            180
        )

        # Detecting all the regions
        # in the Image that has a
        # pedestrians inside it
        (regions, _) = hog.detectMultiScale(
            image,
            winStride=(4, 4),
            padding=(4, 4),
            scale=1.05
        )

        # Drawing the regions in the
        # Image
        number_of_regions.append(len(regions))
        for (x, y, w, h) in regions:
            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

        # Showing the output Image
        cv2.imshow("Image", image)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        if int(time.time() - start_time) >= 10:
            if number_of_regions == 0:
                print(f"no data in {int(time.time() - start_time)} seconds")
                continue
            print(round(sum(number_of_regions)/len(number_of_regions)))
            number_of_regions = []
            start_time = time.time()
            time.sleep(0.5)
        
    else:
        break
