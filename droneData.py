class DroneData:
    def __init__(self, droneImage, droneCoords: list):
        self.droneImage = droneImage
        self.droneCoords = droneCoords

    def getImage(self):
        return self.droneImage
    
    def getCoords(self):
        return self.droneCoords[0], self.droneCoords[1]