# AI WASTE SORTER
import cv2
import requests
import numpy as np
import os

# Create folders to store your images if they don't exist
for folder in ['plastic', 'paper', 'background']:
    if not os.path.exists(folder):
        os.makedirs(folder)

url = "http://162.16.0.99:8080/shot.jpg"
count = 0

print("Controls: 'p' = Plastic, 'r' = Paper, 'b' = Background, 'q' = Quit")

while True:
    try:
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        frame = cv2.resize(frame, (640, 480))

        display_frame = frame.copy()
        cv2.putText(display_frame, f"Images Captured: {count}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow("Data Collector", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('p'):
            cv2.imwrite(f"plastic/img_{count}.jpg", frame)
            count += 1
            print("Saved Plastic")
        elif key == ord('r'):
            cv2.imwrite(f"paper/img_{count}.jpg", frame)
            count += 1
            print("Saved Paper")
        elif key == ord('b'):
            cv2.imwrite(f"background/img_{count}.jpg", frame)
            count += 1
            print("Saved Background (Empty Station)")
        elif key == ord('q'):
            break
            
    except Exception as e:
        print(f"Error: {e}")
        break

cv2.destroyAllWindows()