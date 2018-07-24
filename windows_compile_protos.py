import os
import glob
from subprocess import call

def main():
    RESEARCH_LIBRARY_PATH='C:/tensorflow/models/research'
    os.chdir(RESEARCH_LIBRARY_PATH)
    protofiles = glob.glob('object_detection/protos/*.proto')
    command = "protoc %s --python_out=." % (' '.join(protofiles))
    print(command)
    call(command)


if __name__ == '__main__':
    main()
