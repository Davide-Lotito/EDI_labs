import os ##to use bash command


# folder path
dirPath = './results/'

dirCount = 0

for path in os.listdir(dirPath):
    # check if current path is a file
    if os.path.isfile(os.path.join(dirPath, path)):
        dirCount += 1
    print(path)