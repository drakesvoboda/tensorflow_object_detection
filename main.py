import os
from subprocess import call, Popen, CREATE_NEW_CONSOLE

def main():
    dir = os.getcwd()
    
    RESEARCH_LIBRARY_PATH='C:/tensorflow/models/research'
    PIPELINE_CONFIG_PATH=os.path.join(dir, 'models/model/faster_rcnn_inception_v2_pets.config')
    MODEL_DIR=os.path.join(dir, 'test_model')
    
    os.chdir(RESEARCH_LIBRARY_PATH)

    Popen("tensorboard --logdir=train:%s" % MODEL_DIR, creationflags=CREATE_NEW_CONSOLE)

    call(("python object_detection/model_main.py " +
    "--pipeline_config_path=%s " +
    "--modal_dir=%s " +
    "--num_train_steps=50000 " +
    "--num_eval_steps=2000 " +
    "--alsologtostderr") % (PIPELINE_CONFIG_PATH, MODEL_DIR))
    
if __name__ == '__main__':
    main()
