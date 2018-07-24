import sys
import pandas as pd

def main(argc, argv):
    if(argc != 2):
        print("Usage: python %s <csv file>" % argv[0])
        return
    
    df = pd.read_csv(argv[1])
    print(df['filename'].nunique())
    return

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
