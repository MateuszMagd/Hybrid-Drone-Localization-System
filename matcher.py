import cv2
import numpy as np
from droneData import DroneData
from GPSMapGetter.gps import get_google_maps_image
from Utils.imageoperations import convert_pil_to_opencv, displey_two_images


def placeMatcher(drone_data: DroneData):
    
    image = drone_data.getImage()
    lat, lon = drone_data.getCoords()

    goolge_image = convert_pil_to_opencv(get_google_maps_image(lat=lat, lon=lon, zoom=19))

    sift =  cv2.SIFT_create()

    # Descriptors
    keypoints_1, des_1 = sift.detectAndCompute(image, None)
    keypoints_2, des_2 = sift.detectAndCompute(goolge_image, None)

    # Descriptors Matching with BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    match = bf.knnMatch(des_1, des_2, k=2)

    # Filtr w Lowes metchod
    good_match = []
    for m, n in match:
        if m.distance < 0.75 * n.distance:
            good_match.append(m)

    # If too little matching - return 0%
    if len(good_match) < 4:
        return 0
    
    # Get matchiung poitns
    src_pts = np.float32([keypoints_1[m.queryIdx].pt for m in good_match]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints_2[m.trainIdx].pt for m in good_match]).reshape(-1, 1, 2)

    # Using RANSAC to find homography matrix
    _, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    inliners = mask.ravel().sum()
    total = len(good_match)
    match_prec = (inliners / total) * 100

    return match_prec

if __name__ == "__main__":
    print("~~~~~~~~~~~~~ TESTS ~~~~~~~~~~~~~")
    latitude = 51.7500000
    longitude = 19.4666700

    im1 = get_google_maps_image(lat=latitude, lon=longitude, zoom=17)
    im2 = get_google_maps_image(lat=latitude, lon=longitude, zoom=19)

    displey_two_images(im1, im2)

    cvImage = convert_pil_to_opencv(get_google_maps_image(lat=latitude, lon=longitude, zoom=18))

    drone_data = DroneData(cvImage, [latitude, longitude])

    result = placeMatcher(drone_data)

    print(result)
