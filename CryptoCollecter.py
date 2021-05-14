# Novixel's Crypto Collecter
# CryptoCollecter.py
# CryptoCollector
# Version 1.2.1b
# May 5th, 2021
from AccountSorting import AllAccounts, quote, MainQuote, GetTicker, auth
import Setup as cfg
curList = []
Custom = ["1INCH","ADA","ALGO","ANKR","BTC","ETC","ETH","LINK","LTC","MATIC","NU","SNX","SUSHI"]
CustomSIZE = [0.1,1,1,10,0.0001,0.1,0.0001,0.1,0.01,5,10,0.1,0.1]
#lets call this once TO start
def getSome():
    cfg.LogThis(("GET SOME CALLED",""))
    """accounts , main_values, btc_values"""
    global curList
    curList = []
    Accounts = AllAccounts()
    BTC_Values = []
    Main_Values = []
    # read data from file
    acNum = 0
    for Account in Accounts:
        BTC_Values.append( float(cfg.ReadAccount(Accounts[acNum],str(quote + "_value"))) )
        Main_Values.append( float(cfg.ReadAccount(Accounts[acNum],str(MainQuote + "_value"))) )
        curList.append(str(cfg.ReadAccount(Accounts[acNum],"currency")))
        acNum +=1
    # got the values from our accounts!!
    return Accounts, Main_Values, BTC_Values


def funTimes(x):
    cfg.LogThis(("FUN TIMES CALLED",x))
    if x >= 10:
        return float("%.0f"%x)
    elif x >= 5:
        return float("%.0f"%x)
    elif x >= 1:
        return float("%.0f"%x)
    elif x >= 0.1:
        return float("%.1f"%x)
    elif x >= 0.01:
        return float("%.2f"%x)
    elif x >= 0.001:
        return float("%.4f"%x)
    elif x >= 0.0001:
        return float("%.4f"%x) 

def CollectCoins(currency, value):
    cfg.LogThis(("COLLECT COINS CALLED WITH",currency,value))
    product_id = currency + "-" + MainQuote # Currency pair
    current = float(GetTicker(product_id)) # Current Price For that
    cur1 = 1 / current
    size = float("%.4f"%(value * cur1))

    if currency in Custom:
        for i in Custom:
            if i == currency:
                size = funTimes(size)
    
    if size > 0:
        trade = auth.place_order(
            product_id= product_id,
            side= 'sell', 
            order_type= 'limit',
            price= current, 
            size= size)
        #print("\nNewest Trade")
        cfg.LogThis((trade))
        for k,v in trade.items():
            print(k,"=\t",v)
        print("Bot Has Attempted Collecting!:","%.4f"%size,currency,"at market price:",current)   
        cfg.LogThis(("Bot Has Attempted Collecting!:","%.4f"%size,currency,"at market price:",current))
        cfg.SaveTrade(currency,(size / cur1)) 
        #print("\n")
        return size
    else:
        cfg.LogThis((size,"is not > 0"))
        cfg.LogThis(("%.4f"%size,"Is Not Enough To Make A Trade!"))
        print(size,"Is Not Enough To Make A Trade!")
        return 0 

def CollectionRing():
    cfg.LogThis(("COLLECTION RING CALLED",""))
    global curList
    Accounts, Main_Values, BTC_Values = getSome()
    l1 = 100
    h1 = 120

    l2 = 200
    h2 = 220

    l3 = 300
    h3 = 320
    count = 0
    cfg.LogThis(("Checking Ranges"))
    for value in Main_Values:
        if (l1 <= value <= h1):
            tempValue = value - l1
        elif (l2 <= value <= h2):
            tempValue = value - l2
        elif (l3 <= value <= h3):
            tempValue = value - l3
        else:
            tempValue = 0

        if tempValue != 0: # we made it this far and it not 0 
            print("\n####",Accounts[count] + ": needs collecting of :","%.8f"%tempValue,MainQuote)
            cfg.LogThis((Accounts[count] + ": needs collecting of :","%.8f"%tempValue,MainQuote))
            cur = str(Accounts[count])
            s = CollectCoins(cur,tempValue)
            Main_Values[count] = Main_Values[count] - s
            #print("\n")
        count +=1
    cfg.LogThis(("Finished Checking Ranges"))
    ncount = 0
    for i in curList:
        cfg.SaveDisplay(str(i),str(cfg.ReadAccount(i,(MainQuote + "_value"))))
    return curList, Main_Values
    print("All Coins Collected!")
    cfg.LogThis(("All Coins Collected!"))
# lets check it again