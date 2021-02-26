import os
import shutil
import random
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-dir', '--directory', type=str, default=None, help='path to directory')
ap.add_argument('-keep', '--keep_number', type=int, default=12, help='number of remaining images')

args = vars(ap.parse_args())
working_directory = args['directory']
keep_images = args['keep_number']
images_list = os.listdir(working_directory)
random.shuffle(images_list)

print("Number of images in folder: ", len(images_list))
print("Number of remain images: ", keep_images)

for image in images_list[keep_images:]:
    os.remove(os.path.join(working_directory, image))


print("Removed {} images. Done.".format(len(images_list) - keep_images))




