from fileinput import close
import json
from PIL import Image, ImageOps
from colorama import init, Fore, Back, Style
import requests
import re
import os
import hashlib
import base64

def main():
    print(Style.BRIGHT + Back.WHITE + Fore.BLACK + "=== GridMaker 1.0 ===")

    json_file = None
    output_file = None
    url_array = None
    grid_width = 100
    grid_height = 100
    grid_hor = 2
    grid_ver = 2
    cache_available = False

    # Get/Parse JSON

    while (True):
        json_file_loc = get_input("Location of the JSON list:  ")

        try:
            json_file = open(json_file_loc)

            try:
                url_array = json.load(json_file)

                json_file.close()

                if len(url_array) < 4:
                    print_error("List too short (< 4)")
                else:
                    break
            except:
                print_error('An exception occurred while parsing the file')
        except:
            print_error('An exception occurred while opening the file')

    # Get output file

    output_file = get_input("Output file path (with the name of the file): ")

    # Get individual size

    while (True):
        grid_width = get_input("Width of a grid image (min 10): ")

        try:
            grid_width = int(grid_width)

            if grid_width < 10:
                print_error("Value not in range (min 100)")
            else:
                break
        except ValueError:
            print_error("Value must be an integer")

    while (True):
        grid_height = get_input("Height of a grid image (min 10): ")

        try:
            grid_height = int(grid_height)

            if grid_height < 10:
                print_error("Value not in range (min 100)")
            else:
                break
        except ValueError:
            print_error("Value must be an integer")

    while (True):
        while (True):
            grid_hor = get_input("Horizontal size of the grid image (min 2): ")

            try:
                grid_hor = int(grid_hor)

                if grid_hor < 2:
                    print_error("Value not in range (min 2)")
                else:
                    break
            except ValueError:
                print_error("Value must be an integer")

        while (True):
            grid_ver = get_input("Vertical size of the grid image (min 2): ")

            try:
                grid_ver = int(grid_ver)

                if grid_ver < 2:
                    print_error("Value not in range (min 2)")
                else:
                    break
            except ValueError:
                print_error("Value must be an integer")

        if grid_hor * grid_ver > len(url_array):
            print_error("Grid size larger than supplied images")
        else:
            break

    images = []
    url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Init cache dir

    cache_dir = "./cache"

    try:
        if not os.path.isdir(cache_dir):
            os.mkdir(cache_dir)

        cache_available = True
    except OSError as error:
        print_error(f"Could not initialize cache directory: {error}")

    # Load Images

    for url in url_array:
        im = None

        encoded = base64.b64encode(bytes(url, "utf-8"))
        hash_obj = hashlib.sha256(encoded)
        hash_name = hash_obj.hexdigest()

        cf_path = os.path.join(cache_dir, hash_name + ".jpeg")

        print_info("Loading image : " + Style.DIM + url)

        try:
            if cache_available and os.path.isfile(cf_path):
                images.append(Image.open(cf_path))

                print_info("Found image in cache!")

                continue
        except:
            print_error("Could not access file cache")

        if re.match(url_regex, url) is None:
            print_error(f"Not a valid URL: {url}")
            continue

        try:
            im = Image.open(requests.get(url, stream=True).raw)
        except:
            print_error("Error while loading/processing image")
            continue

        if cache_available:
            try:
                im.save(cf_path)
                print_info("Saved image to cache")
            except:
                print_error("Could not save image to cache")

        images.append(im)

    if grid_hor * grid_ver > len(images):
        print_error("Grid size larger than loaded images")
        exit()

    # Create grid

    image = concat_images(images, (grid_width, grid_height), (grid_ver, grid_hor))

    try:
        image.save(output_file, 'JPEG')
        print_info(f"Saved image to {output_file}.jpeg")
    except:
        print_error("Could not save image")


# From: https://gist.github.com/njanakiev/1932e0a450df6d121c05069d5f7d7d6f

def concat_images(images, size, shape=None):
    # Open images and resize them
    width, height = size
    images = [ImageOps.fit(image, size, Image.ANTIALIAS)
              for image in images]

    # Create canvas for the final image with total size
    shape = shape if shape else (1, len(images))
    image_size = (width * shape[1], height * shape[0])
    image = Image.new('RGB', image_size)

    # Paste images into final image
    for row in range(shape[0]):
        for col in range(shape[1]):
            offset = width * col, height * row
            idx = row * shape[1] + col
            image.paste(images[idx], offset)

    return image

def get_input(prompt):
    response = ""

    while (response.strip() == ""):
        response = input(Style.NORMAL + Back.BLACK + Fore.WHITE + prompt)

    return response


def print_error(err):
    print(Style.BRIGHT + Back.BLACK + Fore.RED + f"[ERROR]  {err}")

def print_warn(warn):
    print(Style.BRIGHT + Back.BLACK + Fore.YELLOW + f"[WARN]   {warn}")

def print_info(info):
    print(Style.DIM + Back.BLACK + Fore.BLUE + f"[INFO]   {info}")

if __name__ == "__main__":
    init(autoreset=True)
    main()