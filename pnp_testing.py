import numpy as np
import cv2


image_path = 'frame0.png' 
img = cv2.imread(image_path) 


def pnp(img):


    # REAL WORLD POINTS, REAL OBJECT POINTS
    # the bottom front left corner of the box will be origin
    # you have to know these measurements before hand
    object_points = np.array([
        [0, 0, 0], # bottom front left    
        [0, 0, -4.8], # bottom back left 
        [6.5, 0, -4.8], # bottom back right 
        [6.5, 0, 0], # bottom front right

        [0, 15.5, 0], # top front left
        [0, 15.5, -4.8], # top back left
        [6.5, 15.5, -4.8], # top back right
        [6.5, 15.5, 0] # top front right
    ], dtype=np.float32)  # cm dimensions

    # 2D picture of image with their pixel values, I used MS paint to measure the pixel values
    # I had to manually find the pixel values but can use algorithms
    image_points = np.array([
        [245, 465], # bottom front left
        [165, 435], # bottom back left 
        [270, 400], # bottom back right
        [350, 420], # bottom front right  

        [230, 55],  # top front left
        [150, 60], # top back left
        [255, 60],  # top back right
        [350, 420], # top front right 
    ], dtype=np.float32)

    # loading calibration
    calibration_data = np.load("calibration_parameters.npz")
    camera_matrix = calibration_data["camera_matrix"]
    dist_coeffs = calibration_data["dist_coeffs"]
    rvecs = calibration_data["rvecs"]
    tvecs = calibration_data["tvecs"]
    rms = calibration_data["rms_error"]
    # getting rotational and translation vectors
    success, rotational_vec, translational_vec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)
    # rotational vector applied to know how object is rotated relative to camera
    # translational vector applied to know how object is positioned relative to camera

    if success:
        print("Rotation Vector:\n", rotational_vec)
        print("Translation Vector:\n", translational_vec)
    else:
        print("pnp solver failed")

    def draw_axes(img, rotational_vec, translational_vec, camera_matrix, dist_coeffs):
        
        axis_length = 5  
        # 3 points for x y z
        axis = np.float32([[axis_length, 0, 0], [0, axis_length, 0], [0, 0, axis_length]])

        # projecting 3D axis points onto the image plane
        imgpts, _ = cv2.projectPoints(axis, rotational_vec, translational_vec, camera_matrix, dist_coeffs)

        # convert image points to integer as pixel coordinates must be WHOLE numbers, reshaping into any number of rows and 2 columns
        imgpts = np.int32(imgpts).reshape(-1, 2)

        # using bottom-front-left corner (first point in image_points) as origin, must be int for pixel values
        origin = tuple(image_points[0].astype(int))

        # drawing axes BGR format
        img = cv2.line(img, origin, tuple(imgpts[0]), (0, 0, 255), 5)  # red - x
        img = cv2.line(img, origin, tuple(imgpts[1]), (0, 255, 0), 5)  # green - y
        img = cv2.line(img, origin, tuple(imgpts[2]), (255, 0, 0), 5)  # blue - z

        cv2.imshow('Img', img)
        return img
        
    img_with_axes = draw_axes(img, rotational_vec, translational_vec, camera_matrix, dist_coeffs)




cap = cv2.VideoCapture(0)

while True:
    
    ret, frame = cap.read()
    if not ret:
        break
    # In the main loop, before displaying the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=7, qualityLevel=0.01, minDistance=50)
    if corners is not None:
        corners = np.int0(corners)
        for i in corners:
            x, y = i.ravel()
            cv2.circle(frame, (x, y), 3, 255, -1)
    cv2.imshow('test', frame)
        # Use the corners as image points for PnP
       
        # Ensure you have corresponding object points for PnP

    # pnp(frame)
    
    key = cv2.waitKey(1)

    if key == 27:
        print("Exiting")
        break
    

    


cap.release()
cv2.destroyAllWindows()