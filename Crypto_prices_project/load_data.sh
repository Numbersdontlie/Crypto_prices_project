#!/usr/bin/bash

#Delete all the files in the folder
#aws s3 rm s3://crypto-price-project --recursive

#Upload the files recursively to my bucket 
aws s3 cp /home/luis/code/Numbersdontlie/Crypto_prices_project/raw_data s3://crypto-price-project --recursive
