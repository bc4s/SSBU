import sys
import os
import json
import colorsys
import array

from PIL import Image

def process_image(path):

    try:
        img = Image.open(path)
        img = img.convert('RGB')
        pixels = img.load()
    except IOError as err:
        print('cannot open file' + err)
        sys.exit()

    colors = list()
    colors.append(pixels[0, 0])

    for i in range(0, img.width):
        for j in range(0, img.height):
            if pixels[i, j] not in colors:
                colors.append(pixels[i, j])
    data[path[path.rfind('\\') + 1:]] = colors

def get_sorted_rgb_by_brightness(json_path):
    data = []
    dictionary = {}

    with open(json_path) as f:
      data = json.load(f)
    
    for key, value in data.items():
      hsl_colors = [(colorsys.rgb_to_hls(*rgb)[1], rgb) for rgb in value]

      # Sort by lightness value
      sorted_colors = [color[1] for color in sorted(hsl_colors, reverse=True)]
      dictionary[key] = sorted_colors
    return dictionary

def transform_clustered_images_to_rgb(image_colors, path):

    tumor = (0, 255, 0)  # green
    stroma = (0, 0, 255)  # blue
    others = (255, 0, 0)  # red

    try:
        img = Image.open(path)
        img = img.convert('RGB')
        pixels = img.load()
    except IOError as err:
        print('cannot open file' + err)
        sys.exit()

    image_key = path.split("\\", 1)[1]

    for i in range(0, img.width):
        for j in range(0, img.height):

            pixel_array = array.array('i', pixels[i, j])
            
            if len(image_colors[image_key]) == 1:
                pixels[i, j]  = others
            elif pixel_array == array.array('i', image_colors[image_key][0]):
                pixels[i, j] = stroma
            elif pixel_array == array.array('i', image_colors[image_key][1]):
                pixels[i, j]  = tumor
            else:
                pixels[i, j]  = others
    img.save(path)

def write_into_json(json_path):
    for filename in os.listdir(clustered_cells):
        f = os.path.join(clustered_cells, filename)
        if os.path.isfile(f):
            process_image(f)

    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=1)

    json_file.close()

if __name__ == '__main__':
    clustered_cells = "clustered_images"
    clustered_images_colors_cells = "sorted_roi-level-cells.json"

    data = {}

    write_into_json(clustered_images_colors_cells)

    image_colors = get_sorted_rgb_by_brightness(clustered_images_colors_cells)

    for filename in os.listdir(clustered_cells):
        f = os.path.join(clustered_cells, filename)
        if os.path.isfile(f):
            transform_clustered_images_to_rgb(image_colors, f)
