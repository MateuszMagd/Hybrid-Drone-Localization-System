from utils.labaling import label_zoom17_with_zoom19_box
from utils.image_handler import get_all_photo_paths

import csv

if __name__ == '__main__':
    pairs = get_all_photo_paths('./database/ready_to_label')

    data_to_label = []

    # LOAD DATA
    with open('./database/ReadyPhotoData.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        to_save = []
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            
            to_save.append(row)

            if idx % 2 == 0:
                data_to_label.append(to_save)
                to_save = []
    
    # APPLY BOX

    # SAVE PHOTOS