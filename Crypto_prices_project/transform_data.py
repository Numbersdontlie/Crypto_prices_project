#Import the neccesary packages 
import pandas as pd 
import glob 

path = "../raw_data/*.csv"
def transform_data(path):
    """Clean each csv file, transform time columns and drop unwanted columns. Return a csv file

    Args:
        path: folder from where read the data 

    Returns: 
        csv file to be uploaded
    """
    for file in glob.glob(path):
        df = pd.read_csv(file, index_col=None, header=0)
        #Transform the date to datetime object from unix 
        df["time"] = pd.to_datetime(df["time"], unit='s')

        #Drop unwanted columns 
        df.drop('Unnamed: 0', inplace=True, axis=1)
        df.drop('conversionType', inplace=True, axis=1)
        df.drop('conversionSymbol', inplace=True, axis=1)
        df.to_csv((f"../raw_data/{file}"))

transform_data(path)