from utils.image_handler import load_photo, get_all_photo_paths, get_all_placeholders, display_image, image_similarity, is_mostly_one_color, save_ready_to_label
from pathlib import Path
import csv

if __name__ == "__main__":
    ##                              ##
    # ------- DOWNLOAD IMAGES ------ #
    ##                              ##
    pairs = get_all_photo_paths('./database/raw_photos')

    ##                              ##
    # ---- DELETE  PLACEHOLDERS ---- #
    # ----- DELETE SAME COLOUR ----- #
    ##                              ##
    placeholders = get_all_placeholders()
    photos_to_save = []
    for pair in pairs:
        flag = True
        for photo in pair:
            for placeholder in placeholders:
                similiraty = image_similarity(load_photo(photo), placeholder)
                if similiraty > .85:
                    flag = False
            if is_mostly_one_color(photo):
                flag = False
            
        if flag == True:
            photos_to_save.append(pair)

    ##                              ##
    # ---- SAVE READY TO LABEL ----- #
    ##                              ##
    CURRENT_DIFF = Path(__file__).resolve().parent / 'ready_to_label'

    for pair in photos_to_save:
        save_ready_to_label(pair[0], CURRENT_DIFF)
        save_ready_to_label(pair[1], CURRENT_DIFF)

    ready_to_label = []
    with open('./database/RawPhotoData.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for idx, row in enumerate(reader):
            if idx == 0:
                ready_to_label.append(row)
                continue
            
            path_created = f'{row[0]}_{row[1]}_zoom{row[4]}.png'
            for pair in photos_to_save:
                name_zoom17 = pair[0].split('\\')[-1]
                name_zoom19 = pair[1].split('\\')[-1]

                if name_zoom17 == path_created or name_zoom19 == path_created:
                    ready_to_label.append(row)
    
    with open('./database/ReadyPhotoData.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(ready_to_label)