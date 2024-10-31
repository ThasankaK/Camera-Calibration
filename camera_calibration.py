import cv2
import numpy as np
import glob

# TO CHANGE DEPENDING ON YOUR SCENARIO
###################
board_size = (6, 6)
image_size = (640, 480)
square_size_mm = 20
###################



# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)

# preparing object points
object_point = np.zeros((board_size[0]*board_size[1], 3), np.float32)
object_point[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)

object_point = object_point * square_size_mm
# storing object poitns and image points from the images
object_points = []
image_points = []

images = glob.glob("images/*.png")
print(f"Found {len(images)} images.")

for image in images:
    img = cv2.imread(image)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # getting board corners
    ret, corners = cv2.findChessboardCorners(gray_img, board_size, None)

    if ret == True:
    # found, add object points and image points after refining them
        object_points.append(object_point)
        corners2 = cv2.cornerSubPix(gray_img, corners, (11, 11), (-1, -1), criteria)
        image_points.append(corners2)
        cv2.drawChessboardCorners(img, board_size, corners2, ret)
        cv2.imshow("img", img)
        cv2.waitKey(500)
    else:
        print(f"Could not find corners in image: {image}")  # Add this line

cv2.destroyAllWindows()


ret, camera_matrix, distance, rotation_vecs, translation_vecs = cv2.calibrateCamera(object_points, image_points, gray_img.shape[::-1], None, None)

### IMPORTANT ### Saving camera calibration results for later use
# Save the calibration parameters as a .npz file
np.savez('calibration_parameters.npz', 
         camera_matrix=camera_matrix, 
         dist_coeffs=distance, 
         rvecs=rotation_vecs, 
         tvecs=translation_vecs,
         rms_error=ret)

print("Camera calibration parameters saved to 'calibration_parameters.npz'")

# errror not to osure how it owrks got from oepncv2 doc
# mean_error = 0
# for i in range(len(object_points)):
#     image_points2, _ = cv2.projectPoints(object_points[i], rotation_vecs[i], translation_vecs[i], camera_matrix, distance)
#     error = cv2.norm(image_points[i], image_points2, cv2.NORM_L2/len(image_points2))
#     mean_error += error 

# print("total error: {}".format(mean_error/len(object_points)))
