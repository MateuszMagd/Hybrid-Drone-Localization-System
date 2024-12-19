This is database folder containing photos for AI learning. 

To use it, you should run script.py in folder Script - This will generate photos around the world using BasicCityCoords.csv.
Put BasicCityCoords.csv (your version) and clear_coords.csv to backup folder for safety reasons. Do it AFTER you generate photos with script.py.

After that you have to find and delete (read to the end!) unwanted photos - like photos that represent nothing, one-color photos ect.
Before you delete them, put them in photos_to_delete folder and run clear_coords - this will clear coordinates.csv and make new file update_coords.csv.
If you dont want to to that:
    1. You will have problems with model learning.
    2. You have to change open file in training model (check AI folder)

After that you can delete photos from photos_to_delete.




