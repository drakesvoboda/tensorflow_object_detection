import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import numpy
from numpy.random import shuffle
from subprocess import call

def xml_to_csv(file_list):
    xml_list = []
    for xml_file in file_list:
        tree = ET.parse(xml_file)
        image_file = tree.find('filename').text
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
    base_path = 'data'
    sets =  ["train", "val"]

    for set in sets:
        files = [os.path.join(base_path, set, 'Annotations', file) for file in os.listdir(os.path.join(base_path, set, "Annotations"))]
        xml_df = xml_to_csv(files)
        xml_df.to_csv(os.path.join(base_path, (set + '_labels.csv')), index=None)
        print('Successfully converted xml to csv.')
        print('Now creating .record file')
        call(("python generate_tfrecord.py " +
        "--image_dir=%s " +
        "--csv_input=%s " +
        "--output_path=%s") % (os.path.join(base_path, set, "JPEGImages"), os.path.join(base_path, (set + '_labels.csv')), os.path.join(base_path, (set + '.record'))))

if __name__ == '__main__':
    main()
