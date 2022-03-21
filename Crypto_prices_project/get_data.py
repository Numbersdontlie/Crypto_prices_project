#import the neccesary packages to get the data 
import requests
import pandas as pd 
import os
from dotenv import load_dotenv

#point to .env file 
load_dotenv('../.env')
cryptocompare_api_key = os.getenv('CRYPTOCOMPARE_API_KEY')

#define a function to get the data 
def get_data(from_currency): 
    """Get data from the cryptocompare API, flat the json object from the response and return 
    csv files from every asset passed as argument. 

    Args:
      from_currency: iterable in the list of cryptos that we want the data from. 

    Returns:
      Csv files  
    """
    url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym={0}&tsym=USD&limit=190'.format(from_currency)
    headers = {'authorization': cryptocompare_api_key}
    response = requests.get(url, headers=headers)
    df = response.json()
    new_df = pd.json_normalize(df['Data']['Data'])
    new_df["time"] = pd.to_datetime(new_df["time"], unit='s')
    new_df["name"] = from_currency
    new_df.to_csv(f"../raw_data/{from_currency}.csv")

#define the list of crypto 
crypto_list = ["BTC", "ETH", "BNB", "USDT", "SOL", "ADA", "USDC", "XRP", "LUNA", "DOT"] 

#call the function and get the data 
for from_currency in crypto_list:
    get_data(from_currency) 