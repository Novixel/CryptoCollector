# Novixel's Config File Setup
# ConfigSetup.py
# CryptoCollector
# Version 1.2.1b
# May 5th, 2021

import os
from pathlib import Path
from configparser import ConfigParser
from datetime import datetime

# (Build Directory)
        # Build A place for the bots config files to be stored 
def BuildBotNest():
    fullPath = os.path.realpath(__file__) # Get Exact Path to this file
    thisDir = os.path.dirname(fullPath) # Get Exact Directory of this File
    botFold = thisDir + '\BOT' # Create a new folder path for setup 
    Path(botFold).mkdir(parents=True, exist_ok=True) # Check for folder or make if not there
    os.chdir(botFold) # change Directory to save setup files
    return botFold

path = str(BuildBotNest()) # we need this for all the settings :)

pathStr = (path + '\info.ini') # create the file string for repeat
pathTra = (path + '\_trades.ini')
pathLog = (path + "\log.log")

# (Build Config File)
        # Build a config file in that folder we just made for later use.
def BuildBotSettings():
    config_object = ConfigParser()
    config_object["API"] = {            
        "key"           :   "CoinbaseProAPI key",
        "b64secret"     :   "CoinbaseProAPI b64secret",
        "passphrase"    :   "CoinbaseProAPI passphrase"
    }
    config_object["TICKER"] = {
            "trade_id"  :   "Trade ID Number",
            "price"     :   "Current Price",
            "size"      :   "0.000000000000000",
            "time"      :   "2021-05-01T12:00:00.578544Z",
            "bid"       :   "0.000000000000000",
            "ask"       :   "0.000000000000000",
            "volume"    :   "0.000000000000000"
    }
    #Write to a file!!
    with open(pathStr,'w') as conf:
        config_object.write(conf)

# (Edit That Config File)
        # Save to new data to The Config File we just made
        # these need to be compacted in to one function
def SaveNewApi(key,b64secret,passphrase):
    c = ConfigParser()
    c.read(pathStr)
    #Get the api from config
    API = c["API"]
    API["key"] = str(key)
    API["b64secret"] = str(b64secret)
    API["passphrase"] = str(passphrase)
    #Write changes back to file
    with open(pathStr, 'w') as conf:
        c.write(conf)

def SaveDisplay(x,d):
    c = ConfigParser()
    c.read(pathStr)
    #Get the api from config
    if c.has_section(str("DISPLAY")):
        pass
    else:
        c.add_section(str("DISPLAY"))
    #then edit it
    display = c[str("DISPLAY")]
    display[str(x)] = d
    with open(pathStr, 'w') as conf:
        c.write(conf)

def SaveAccount(cur, x,d):
    c = ConfigParser()
    c.read(pathStr)
    #Get the api from config
    if c.has_section(str(cur + "ACCOUNT")):
        pass
    else:
        c.add_section(str(cur + "ACCOUNT"))
    #then edit it
    account = c[str(cur + "ACCOUNT")]
    account[str(x)] = d
    with open(pathStr, 'w') as conf:
        c.write(conf)

def SaveTicker(x , d ):
    c = ConfigParser()
    c.read(pathStr)
    #Get the api from config
    TICKER = c["TICKER"]
    TICKER[str(x)] = d
    with open(pathStr, 'w') as conf:
        c.write(conf)

def SaveTrade(cur,amount):
    now = datetime.now()
    time = now.strftime("%m/%d/%Y, %H:%M:%S")
    with open(pathTra, 'a') as conf:
        Text = (time +","+ cur + ",PROFIT," + ("%.4f"%amount))
        conf.writelines(Text + "\n")
        conf.close

def LogThis(message):
    message = str(message)
    now = datetime.now()
    time = now.strftime("%m/%d/%Y, %H:%M:%S")
    with open(pathLog, 'a') as log:
        Text = (time + ":DEBUG: " + message)
        log.writelines(Text + "\n")
        log.close

# (Read That Config File)
# Read the file and assign variables to the values
# these need to be compacted in to one function
def ReadConfig(x):
    """x should be what you want from the config file as a string"""
    c = ConfigParser()
    c.read(pathStr)
    #Get Info from config
    API = c["API"]
    return API[x]

def ReadTICKER(x):
    """x = 'price',etc """
    c = ConfigParser()
    c.read(pathStr)
    #Get Info from config
    TICKER = c["TICKER"]
    return TICKER[x]

def ReadAccount(cur,x):
    """x = 'available',etc """
    c = ConfigParser()
    c.read(pathStr)
    #Get Info from config
    ACCOUNT = c[str(cur + "ACCOUNT")]
    return ACCOUNT[x]

def ReadDisplay(x):
    """x = 'currency',etc """
    c = ConfigParser()
    c.read(pathStr)
    #Get Info from config
    DISPLAY = c["DISPLAY"]
    return DISPLAY[x]

def ReadALLDisplay():
    c = ConfigParser()
    c.read(pathStr)
    #Get Info from config
    DISPLAY = c["DISPLAY"]
    return DISPLAY