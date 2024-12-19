import pandas as pd
import os



if __name__ == '__main__':
    coords = pd.read_csv('coordinates.csv')
    photos_dir = 'photos_to_delete'

    i = 0
    for photos in os.listdir(photos_dir):
        f = os.path.join(photos_dir, photos)

        if os.path.isfile(f):
            # Clear string
            data = f.replace('\\', ' ').strip(' ').replace('photos_to_delete ', '').replace('_', ' ').split()
            for idx, row in coords.iterrows():
                city_name = row['CityName']
                index = row['index']

                if city_name == data[0] and index == int(data[1]):
                    coords = coords.drop(idx)

        if i % 100 == 0:
            print(f"Photo: {i}")
        i += 1
    
    coords.to_csv('updated_coords.csv', index=False)