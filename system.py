import cv2
import torch
from AI.model import SiameseNetwork
from GPSMapGetter.gps import get_google_maps_image
from Utils.imageoperations import convert_pil_to_opencv, display_image, transform
from droneData import DroneData
from matcher import placeMatcher
from PIL import Image

def findCorrectLocalization(droneData):
    '''
    Return values:
        [] - 
    '''
    # --------------- Data preparation ---------------
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    drone_image = droneData.getImage()

    # Change openCV to PIL
    lat, lon = droneData.getCoords()
    image_from_gps_data = get_google_maps_image(lat=lat, lon=lon, zoom=19)
    rgb_image = cv2.cvtColor(drone_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image).convert("RGB")

    # --------------- Transformations ---------------
    large_image = transform(image_from_gps_data).unsqueeze(0).to(device)
    small_image = transform(pil_image).unsqueeze(0).to(device)
    
    # --------------- AI Search for localization ---------------
    model = SiameseNetwork().to(device)

    model.load_state_dict(torch.load("siamese.pth", map_location=device))
    model.eval()    
    
    # --------------- Predict bounding box ---------------
    with torch.no_grad():
        bbox = model(large_image, small_image)
    
    # Result
    return bbox.cpu().numpy()

def calcCoords():
    pass


def droneLocalizationSystem(droneData):
    '''
    This is main function that will be used to localize drone
    Reture values:
        0 - Everything is good
        1-  GPS coords was in diffrent place but we was able to localize drone
        2 - Drone is lost - lost mean that we are not able to localize drone,
            propably we are not able to find any matching points
        3 - Drone is in wrong place - we are able to localize drone but we are not able to find any matching points
        -1 - Unexpected error
    '''
    try:
        # Place Matcher
        result = placeMatcher(droneData)
        if(result > 75):
            # Here we matched so we are on good way
            return 0
        
        # If no matched
        # AI Search for localization
        result = findCorrectLocalization(droneData)
        
        # Result
        return 1
    except Exception as e:
        print(f"Error in droneLocalizationSystem: {e}")
        return -1

def answerChecker(result):
    if(result == 0):
        print("Everything is good")
    elif(result == 1):
        print("GPS coords was in diffrent place but we was able to localize drone")
    elif(result == 2):
        print("Drone is lost - lost mean that we are not able to localize drone, propably we are not able to find any matching points")
    elif(result == 3):
        print("Drone is in wrong place - we are able to localize drone but we are not able to find any matching points")
    elif(result == -1):
        print("Unexpected error")


if __name__ == "__main__": 
    print("~~~~~~~~~~~~~ TESTS ~~~~~~~~~~~~~")
    # This is place that should be changed to real data takeon from drone. 
    # After data processing it should be passed to droneLocalizationSystem
    # Data preparation
    latitude = 41.97857895498957
    longitude = -87.89513690994697

    new_latitude = 41.9778443835732
    new_longitude = -87.89758305545212

    display_image(get_google_maps_image(lat=latitude, lon=longitude, zoom=18))
    display_image(get_google_maps_image(lat=new_latitude, lon=new_longitude, zoom=18))

    print("Test nr 1 - Drone is found without problem")
    cvImage = convert_pil_to_opencv(get_google_maps_image(lat=latitude, lon=longitude, zoom=19))
    drone_data = DroneData(cvImage, [latitude, longitude])
    # This is where we start the system
    result = droneLocalizationSystem(drone_data)
    answerChecker(result)

    print("Test nr 2 - Drone is found but GPS coords was in diffrent place")
    cvImage = convert_pil_to_opencv(get_google_maps_image(lat=new_latitude, lon=new_longitude, zoom=19))
    drone_data = DroneData(cvImage, [latitude, longitude])
    result = droneLocalizationSystem(drone_data)
    answerChecker(result)
