import cv2
import os
import numpy as np

def run():
    output_folder = os.path.join(os.getcwd(), "images")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    elif len(os.listdir(output_folder)) != 0:
        print("""!!!!!WARNING!!!!!
    IMAGES ALREADY EXIST IN THE images/ DIRECTORY
    ANY NEW IMAGES WILL OVERWRITE THE OLD ONES!!!""")
        
    # change this number around to capture which webcam you are using
    cap = cv2.VideoCapture(0)

    img_num = 0

    while True:
        
        ret, frame = cap.read()
        if not ret:
            break

        key = cv2.waitKey(1)

        if key == ord('p'):
            cv2.imwrite(f"{output_folder}/frame{img_num}.png", frame)
            print(f"Frame #{img_num} saved to {output_folder}")
            img_num += 1
        elif key == 27:
            print("Exiting")
            break
        cv2.imshow("Image", frame)
        


    cap.release()
    cv2.destroyAllWindows()

run()