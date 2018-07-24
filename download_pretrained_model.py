import six.moves.urllib as urllib
import os
import sys
import tarfile

base_path = './pretrained_models'
filename ='faster_rcnn_inception_v2_coco_2018_01_28.tar.gz' 

try:
    import urllib.request
except ImportError:
    raise ImportError('You should use Python 3.x')

if not os.path.exists(os.path.join(base_path, filename)):
    print('Downloading ' + filename)
    url_base = 'http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz'
    urllib.request.urlretrieve(url_base, os.path.join(base_path, filename))
    print("Download " + filename + " Done")
    
else:
    print("You already have " + filename)

file_tar, file_tar_ext = os.path.splitext(filename) # split into file.tar and .gz
file_untar, file_untar_ext = os.path.splitext(file_tar) #split into file and .tar
os.chdir(base_path)

if not os.path.isdir(os.path.join(os.getcwd(), file_untar)):
    if file_tar_ext == '.gz' and file_untar_ext == '.tar': # check if file had format .tar.gz 
        print('Unpacking ' + filename)
        tar = tarfile.open(filename) 
        tar.extractall(path='./') # untar file into same directory
        tar.close()
        os.chdir(file_untar) # This fails if file.tar.gz has different name compared to the untarred folder e.g.. file1 instead of file
        print('Unpack ' + filename + " Done")
    else:
        raise Exception("File must have '.tar.gz' extension")
else:
    print(filename + " has already been unpacked")
