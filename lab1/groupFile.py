import os
import pandas as pd
from glob import glob

# folder path
dirPath = './results/'

"""
https://stackoverflow.com/questions/67996882/creating-pandas-dataframe-from-multiple-json-files
"""

def group(dirPath):
    allFiles = glob(os.path.join(dirPath, "*.txt"))
    indDf = (pd.read_json(f) for f in allFiles)
    df = pd.concat(indDf, ignore_index=True)
    return df

dataframe = group(dirPath)
print(dataframe)