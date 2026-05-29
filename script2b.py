import cv2 as cv
import numpy as np


def map_arena():

    """
    Task 2B: Perspective Transformation and Coordinate Mapping
    """

    result = {
        "corner_points_detected": [],
        "robot_pixel_coord": [],
        "robot_real_world_coord": []
    }

    # ==========================================
    # STEP 1: Corner Detection (Color Tracking)
    # ==========================================

    image=cv.imread("test_images/angled_arena.png")
    hsv=cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_red=np.array([0,120,70])
    upper_red=np.array([10,255,255])

    lower_green=np.array([40,50,50])
    upper_green=np.array([80,255,255])

    lower_blue= np.array([100,150,0])
    upper_blue= np.array([140,255,255])

    lower_yellow= np.array([20,100,100])
    upper_yellow= np.array([35,255,255])

    mask_red=cv.inRange(hsv,lower_red,upper_red)

    mask_green=cv.inRange(hsv,lower_green,upper_green)

    mask_blue=cv.inRange(hsv,lower_blue,upper_blue)

    mask_yellow=cv.inRange(hsv,lower_yellow,upper_yellow)

    def find_center(mask):

        contours, _ =cv.findContours(
            mask,
            cv.RETR_EXTERNAL,
            cv.CHAIN_APPROX_SIMPLE
        )

        biggest=max(contours,key=cv.contourArea)

        M=cv.moments(biggest)

        cx=int(M["m10"]/M["m00"])

        cy=int(M["m01"]/M["m00"])

        return [cx,cy]

    red_center=find_center(mask_red)

    green_center=find_center(mask_green)

    blue_center=find_center(mask_blue)

    yellow_center=find_center(mask_yellow)

    result["corner_points_detected"]=[
        red_center,
        green_center,
        blue_center,
        yellow_center
    ]

    # ==========================================
    # STEP 2: Perspective Transformation
    # ==========================================

    src_pts=np.float32([
        red_center,
        green_center,
        blue_center,
        yellow_center
    ])

    dst_pts=np.float32([
        [0,0],
        [499,0],
        [499,499],
        [0,499]
    ])

    matrix=cv.getPerspectiveTransform(
        src_pts,
        dst_pts
    )

    warped=cv.warpPerspective(
        image,
        matrix,
        (500,500)
    )

    # ==========================================
    # STEP 3: Robot Detection on Warped Arena
    # ==========================================

    aruco_dict=cv.aruco.getPredefinedDictionary(
        cv.aruco.DICT_4X4_50
    )

    parameters=cv.aruco.DetectorParameters()

    detector=cv.aruco.ArucoDetector(
        aruco_dict,
        parameters
    )

    corners,ids,rejected = detector.detectMarkers(
        warped
    )

    # robot id=1
    if ids is not None:

        for i in range(len(ids)):

            if ids[i][0] == 1:

                pts=corners[i][0]

                cx=int(np.mean(pts[:,0]))

                cy=int(np.mean(pts[:,1]))

                result["robot_pixel_coord"] = [cx, cy]

                # ==========================================
                # STEP 4: Real-World Coordinate Conversion
                # ==========================================

                x_cm=round((cx/500)*200,1)

                y_cm =round((cy/500)*200,1)

                result["robot_real_world_coord"]=[
                    x_cm,
                    y_cm
                ]

    return result


if __name__ == "__main__":

    output = map_arena()

    print("Task 2B Output:")

    print(output)