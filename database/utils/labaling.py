from PIL import ImageDraw, Image
import math

def label_zoom17_with_zoom19_box(
    zoom17_img: Image.Image,
    center_lat: float,
    center_lon: float,
    small_lat: float,
    small_lon: float
) -> Image.Image:
    def latlon_to_pixel(lat, lon, zoom=17, tile_size=640):
        scale = 2 ** zoom * tile_size / 256
        siny = math.sin(lat * math.pi / 180)
        siny = min(max(siny, -0.9999), 0.9999)
        x = 256 * (0.5 + lon / 360)
        y = 256 * (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi))
        return x * scale, y * scale

    zoom17_px = latlon_to_pixel(center_lat, center_lon)
    zoom19_px = latlon_to_pixel(small_lat, small_lon)

    dx = zoom19_px[0] - zoom17_px[0]
    dy = zoom19_px[1] - zoom17_px[1]

    center_x = 640 // 2 + dx
    center_y = 640 // 2 + dy

    half_box = 640 // 2
    x1 = int(center_x - half_box)
    y1 = int(center_y - half_box)
    x2 = int(center_x + half_box)
    y2 = int(center_y + half_box)

    draw = ImageDraw.Draw(zoom17_img)
    draw.rectangle([x1, y1, x2, y2], outline='red', width=3)
    return zoom17_img
