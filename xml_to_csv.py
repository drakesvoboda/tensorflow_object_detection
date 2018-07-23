import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import numpy
from numpy.random import shuffle


def xml_to_csv(file_list):
    xml_list = []
    for xml_file in file_list:
        tree = ET.parse(xml_file)
        image_file = os.path.join(tree.find('folder').text + "/JPEGImages/", tree.find('filename').text)
        image_width = int(tree.find('size').find('width').text)
        image_height = int(tree.find('size').find('height').text)
        root = tree.getroot()
        for obj in root.findall('object'):
            xmlbox = obj.find('bndbox')           
            class_name = obj.find('name').text
            if class_name == 'D30': continue # Competition said to ignore the 'D30' label

            value = (image_file,
                     image_width,
                     image_height,
                     obj.find('name').text,
                     int(int(xmlbox.find('xmin').text)),
                     int(int(xmlbox.find('ymin').text)),
                     int(int(xmlbox.find('xmax').text)),
                     int(int(xmlbox.find('ymax').text)))

            xml_list.append(value)

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    base_path = './road_damage_dataset/'
    govs =  ["Adachi/", "Chiba/", "Ichihara/", "Muroran/", "Nagakute/", "Numazu/", "Sumida/"]

    train_ratio = .9
    valid_ratio = .05
    test_ratio = .05

    file_list = []
    for gov in govs:
        file_list.extend([base_path + gov + 'Annotations/' + file for file in os.listdir(base_path + gov + 'Annotations/')])

    shuffle(file_list)

    start_train = 0
    start_valid = int(len(file_list) * train_ratio)
    start_test = int(len(file_list) * valid_ratio) + start_valid

    files = {};
    
    files['train'] = file_list[start_train:start_valid]
    files['valid'] = file_list[start_valid:start_test]
    files['test'] = file_list[start_test:]

    for name, files in files.items():
        xml_df = xml_to_csv(files)
        xml_df.to_csv(os.path.join(base_path, (name + '_labels.csv')), index=None)
        print('Successfully converted xml to csv.')


main()
