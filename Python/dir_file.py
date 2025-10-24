import os, sys

ERR_OK = 0

ERR_IN_PARAMS = -1

ERR_DIR_NOT_EXIST = -2
 

def main():
    argc = len(sys.argv)
    if argc != 2:
        frame = sys.argv[0]
        print(f"usage: {frame} DIR")
        exit(ERR_IN_PARAMS)

    dir_name = sys.argv[1]
    if not os.path.exists(dir_name):
        print(f"Directory not exist: {dir_name}")
        




if __name__ == "__main__":
    main()