import os
import glob
import xml.etree.ElementTree as ET
import numpy
from numpy.random import shuffle
import ntpath
from subprocess import call

base_path = 'data'
RESEARCH_LIBRARY_PATH='C:/tensorflow/models/research'

def make_dir(dir):
    print("Making path %s" % dir)
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            print("Path %s created" % dir)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    else:
        print("%s Already exists" % dir)

def move_files_to_directory(dir, file_list):
    make_dir(dir)
    for file in file_list:
        os.rename(file, os.path.join(dir, ntpath.basename(file)))

def get_image_fFilesiles_from_xml(file_list):
    image_files = []
    for xml_file in file_list:
        tree = ET.parse(xml_file)
        image_files.append(os.path.join(base_path, tree.find('folder').text, "JPEGImages", tree.find('filename').text))

    return image_files


def main():
    current_dir = os.getcwd()
    govs =  ["Adachi", "Chiba", "Ichihara", "Muroran", "Nagakute", "Numazu", "Sumida"]

    train_ratio = .99
    valid_ratio = .01

    train_files = []
    for gov in govs:
        train_files.extend([os.path.join(base_path, gov, 'Annotations', file) for file in os.listdir(os.path.join(base_path, gov, 'Annotations'))])

    shuffle(train_files)

    start_train = 0
    start_valid = int(len(train_files) * train_ratio)

    sets = {};
    
    sets['train'] = train_files[start_train:start_valid]
    sets['val'] = train_files[start_valid:]

    for name, xml_files in sets.items():
        image_files = get_image_files_from_xml(xml_files)

        print('Moving %s annotations' % name)
        move_files_to_directory(os.path.join(base_path, name, "Annotations"), xml_files)

        print('Moving %s images' % name)
        move_files_to_directory(os.path.join(base_path, name, "JPEGImages"), image_files) 

        print('Finished moving %s files' % name)

if __name__ == '__main__':
    main()
