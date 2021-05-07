# Novixel's Coinbase Connection
# Connect.py
# CryptoCollector
# Version 1.2.1b
# May 5th, 2021
# 
import Setup as cfg
import cbpro
import os

# Coinbase Connection For Our Config Data
class CoinConnect:

    # This will do everything involving the coinbase api!
    auth = None

    def __init__(self): # Set up on creation
        # Build directory for our config file if not already done
        cfg.BuildBotNest() 

        if os.path.isfile(cfg.pathStr): # if file is a file! We continue!
            pass # File was found so all is well 
        else: 
            print("\nConfig File Not Found!\nBuilding Setup File!\n") # else: we make a file
            cfg.BuildBotSettings()
            print("\nThe Config File Was Created!\n")

        # This set Our API Keys for the Coinbase Pro account we want to use.

        # Set your api key --------- if not already set
        if cfg.ReadConfig("key") == "CoinbaseProAPI key": 
            key = input("Enter API KEY:\n")
            secret = input("Enter API SECRET:\n")
            passphrase = input("Enter API PASSPHRASE:\n")
            cfg.SaveNewApi(key,secret,passphrase)
        else: # Read your already set key
            key = cfg.ReadConfig("key")
            secret = cfg.ReadConfig("b64secret")
            passphrase = cfg.ReadConfig("passphrase")

        # Create a authenticated client for the coinbase api
        self.auth = cbpro.AuthenticatedClient(key,secret,passphrase)
