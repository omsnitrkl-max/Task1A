import cv2 as cv
import numpy as np
import glob

def localize_bot():
    """
    Task 2A: Camera Calibration and ArUco Pose Estimation
    """
    # Initialize the output dictionary with exact keys required by the evaluator
    result = {
        "camera_matrix_trace": 0.0,
        "markers": {}
    }

    # ==========================================
    # STEP 1: Camera Calibration
    # ==========================================

    rows=6
    cols=9
    square_size=2.5
    
    objp=np.zeros((rows * cols,3),np.float32)
    objp[:, :2] = np.mgrid[0:cols,0:rows].T.reshape(-1,2)
    objp=objp*square_size
    objpoints=[]
    imgpoints=[]
    img_shape=None

    images = sorted(
        glob.glob("calibration_images/*.png")
        
    )

    for img_name in images:
        img=cv.imread(img_name)
        if img is None:
            continue
        gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        img_shape=gray.shape[::-1]

        
        ret,corners =cv.findChessboardCorners(gray,(cols,rows),None)
        if ret==True:
            criteria=(cv.TERM_CRITERIA_EPS+ cv.TERM_CRITERIA_MAX_ITER,30,0.001)
            corners=cv.cornerSubPix(gray,corners,(11, 11),(-1, -1),criteria)
            objpoints.append(objp)
            imgpoints.append(corners)

    ret,mtx,dist,rvecs,tvecs=cv.calibrateCamera(
        objpoints,
        imgpoints,
        img_shape,
        None,
        None
    )

    trace_value=np.trace(mtx)
    result["camera_matrix_trace"]=round(float(trace_value),2)


    # ==========================================
    # STEP 2: Image Undistortion
    # ==========================================
    
    image=cv.imread("test_images/test_arena.jpg")
    if image is None:
        image=cv.imread("test_images/test_arena.png")
    if image is None:
        image=cv.imread("test_arena.jpg")
    if image is None:
        image=cv.imread("test_arena.png")

    h,w=image.shape[:2]
    new_mtx,roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    undistorted=cv.undistort(image,mtx,dist,None,new_mtx)

    # ==========================================
    # STEP 3: ArUco Detection & Pose Estimation
    # ==========================================

    aruco_dict=cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
    parameters=cv.aruco.DetectorParameters()
    detector=cv.aruco.ArucoDetector(aruco_dict,parameters)
    corners,ids,rejected=detector.detectMarkers(undistorted)

    marker_size=5.0
    marker_points=np.array([
        [-marker_size / 2, marker_size / 2, 0],
        [marker_size / 2, marker_size / 2, 0],
        [marker_size / 2, -marker_size / 2, 0],
        [-marker_size / 2, -marker_size / 2, 0]
    ], dtype=np.float32)

    if ids is not None:
        for i in range(len(ids)):
            success, rvec, tvec = cv.solvePnP(
                marker_points,
                corners[i][0],
                new_mtx,
                dist
            )
            marker_id=ids[i][0]
            distance_z=tvec[2][0]
            x_offset=tvec[0][0]
            result["markers"][f"id_{marker_id}"]={
                "distance_z":round(float(distance_z),1),
                "x_offset":round(float(x_offset),1)
            }

    # ==========================================
    # SORT MARKERS BY ARUCO ID
    # ==========================================
    result["markers"]=dict(
        sorted(
            result["markers"].items(),
            key=lambda item: int(item[0].split("_")[1]),
            reverse=True
        )
    )

    return result

if __name__ == "__main__":
    output = localize_bot()
    print("Task 2A Output:")
    print(output)