#!/usr/bin/python3
from datetime import datetime
import argparse
import os
import sys
from glob import glob
from PIL import Image
import concurrent.futures


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='image or directory of images to be resized', required=True)
parser.add_argument('-t', '--type', help='image file type, e.g. jpg png, only required if destination = dir')
parser.add_argument('-o', '--output', help='image or directory of images to save resize to', required=True)
parser.add_argument('-q', '--quality', help='0-100, lowest to highest quality compression', default=90)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--height', help='target height of resized images', type=int)
group.add_argument('--width', help='target width of resized images', type=int)
args = parser.parse_args()


SRC = args.input
FTYPE = args.type
DST = args.output
QUALITY = args.quality
TARGETHEIGHT = args.height
TARGETWIDTH = args.width


img_meta = {
        'quality':int(QUALITY),
        'subsampling': 0}


def compute_height(img):
    height_percent = (TARGETHEIGHT/float(img.size[1]))
    target_width = int(float(height_percent) * float(img.size[0]))
    return (target_width, TARGETHEIGHT)


def compute_width(img):
    width_percent = (TARGETWIDTH/float(img.size[0]))
    target_height= int(float(width_percent) * float(img.size[1]))
    return (TARGETWIDTH, target_height)


def resize_image(src_img):
    img = Image.open(src_img)
    if(TARGETHEIGHT):
        img_width, img_height = compute_height(img)
    if(TARGETWIDTH):
        img_width, img_height = compute_width(img)
    img_resized = img.resize((img_width,img_height), Image.LANCZOS)
    img_resized.save(DST, subsampling=img_meta["subsampling"], quality=img_meta["quality"])


def resize_image_to_dir(src_img):
    image_name = os.path.basename(src_img)
    img = Image.open(src_img)
    if(TARGETHEIGHT):
        img_width, img_height = compute_height(img)
    if(TARGETWIDTH):
        img_width, img_height = compute_width(img)
    img_resized = img.resize((img_width,img_height), Image.LANCZOS)
    img_resized.save(DST + image_name, subsampling=img_meta["subsampling"], quality=img_meta["quality"])


def get_image_paths(src_dir, FTYPE):
    img_paths = [f for f in glob(f"{src_dir}*.{FTYPE}")]
    return img_paths


def resize_all_images(img_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(resize_image_to_dir, img_list)


def main():
    if os.path.isdir(SRC):
        if FTYPE is None:
            print("specify a file type when sourcing from a directory")
            sys.exit()
        img_list = get_image_paths(SRC, FTYPE)
        resize_all_images(img_list)
    elif os.path.isfile(SRC):
        resize_image(SRC)


if __name__ == "__main__":
    main()
