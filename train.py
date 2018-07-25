import os
from subprocess import call, Popen, CREATE_NEW_CONSOLE

def main():
    dir = os.getcwd()
    
    RESEARCH_LIBRARY_PATH='C:/tensorflow/models/research'
    PIPELINE_CONFIG_PATH=os.path.join(dir, 'models/model/faster_rcnn_inception_v2_pets.config')
    MODEL_DIR=os.path.join(dir, 'train_dir')
    EVAL_DIR=os.path.join(dir, 'eval_dir')
    
    os.chdir(RESEARCH_LIBRARY_PATH)

    Popen("tensorboard --logdir=train:%s,eval:%s" % (MODEL_DIR, EVAL_DIR), creationflags=CREATE_NEW_CONSOLE)

    call(("python object_detection/legacy/train.py " +
    "--pipeline_config_path=%s " +
    "--train_dir=%s " +
    "--logtostderr") % (PIPELINE_CONFIG_PATH, MODEL_DIR))
    


if __name__ == '__main__':
    main()
