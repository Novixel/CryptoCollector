# Novixel's Bot Authenticated Connection
# Version 1.1
# BotAuth.py
# May 18, 2021

from time import sleep
import cbpro
import os
from pathlib import Path
from configparser import ConfigParser
from datetime import datetime

# Coinbase Connection For Our Config Data
class Connect():
    """ Connection To Coinbase Portfolio API """
    # This will do everything involving the coinbase api!
    auth = None
    quote = None
    def __init__(self,name): # Set up on creation
        self.initTime = datetime.now()
        self.cfg = Config(name)
        self.cfg._Set("LOG", "","" , ("Initializing Portfolio",name))
        print("\nInitializing Portfolio:",name)
        self.paths = self.cfg.PathList
        self.Pnames = self.cfg.PathNames
        self.SATS = 0
        # Read & Set API Auth For Coinbase
        if self.cfg._Get("API", "key", "key") == "CoinbaseProAPI key":
            self.cfg._Set("LOG", "","" , "NO API Keys Found")
            print("No API Keys Have Been Set!\nPlease Enter Your Coinbase Pro Portfolio API Info!\n")
            key = input("Enter API KEY:\n")
            secret = input("Enter API SECRET:\n")
            passphrase = input("Enter API PASSPHRASE:\n")
            quote = input("Enter Your Main Quote Currency\n")
            self.cfg._Set("API","API","key",key)
            self.cfg._Set("API","API","secret",secret)
            self.cfg._Set("API","API","passphrase",passphrase)
            self.cfg._Set("API","API","quote",quote)
            self.cfg._Set("LOG", "","" , "API KEYS SAVED")
        else: # Read your already set key
            self.cfg._Set("LOG", "","" , "Reading API KEYS")
            key = self.cfg._Get("API", "key", "key") 
            secret = self.cfg._Get("API", "secret", "secret") 
            passphrase = self.cfg._Get("API", "passphrase", "passphrase")
            quote = self.cfg._Get("API", "quote", "quote")
            self.cfg._Set("LOG", "","" , ("Current Quote:",quote))  
        # Create a authenticated client for the coinbase api
        self.auth = cbpro.AuthenticatedClient(key,secret,passphrase)  
        self.quote = quote
        if float(self.cfg._Get("ACCOUNT", "OVERVEIW", "last_update")) == self.initTime.minute:
            self.cfg._Set("LOG", "","" , "Reading Account Overveiw") 
            
            self.AllAccounts = self.cfg._Get("ACCOUNT", "OVERVEIW", "AllAccounts").replace('\'', '').lstrip('[').rstrip(']').split(", ")

            AB = self.cfg._Get("ACCOUNT", "OVERVEIW", "AllBalances").replace('\'', '').lstrip('[').rstrip(']').split(", ")
            self.AllBalances = [float(i) for i in AB]

            self.AllAvailable = self.cfg._Get("ACCOUNT", "OVERVEIW", "AllAvailable").replace('\'', '').lstrip('[').rstrip(']').split(", ")

            AV = self.cfg._Get("ACCOUNT", "OVERVEIW", "AvailableValues").replace('\'', '').lstrip('[').rstrip(']').split(", ")
            self.AvailableValues = [float(i) for i in AV]

            BV = self.cfg._Get("ACCOUNT", "OVERVEIW", "BTCValues").replace('\'', '').lstrip('[').rstrip(']').split(", ")
            self.BTCValues = [float(i) for i in BV]

            self.TOTAL_QUOTE = float(self.cfg._Get("ACCOUNT","OVERVEIW", "total_quote"))
        else:
            self.cfg._Set("LOG", "","" , "Updating Accounts") 
            self.CheckAllAccounts()
        

    def GetLastTrade(self,product_id):
        """Return: Side,Price,Size"""
        self.cfg._Set("LOG", "","" , ("GettingLastTrade For",product_id)) 
        filled = self.auth.get_fills(product_id)
        side = None
        price = 0 
        size = 0
        for i in filled:
            side = i["side"]
            price = i['price']
            size = i['size']
            break
        self.lastSide = str(side)
        self.lastPrice = float(price)
        self.lastSize = float(size)
        self.lastProduct = product_id
        return float(price)

    def SendTrade(self,product_id,side,price,size):
        '''SendMarketTrade(pair,side,price,size)'''
        self.cfg._Set("LOG", "","" , ("Sending Trade With",product_id,side,price,size)) 
        trade = self.auth.place_order(
            product_id= product_id,
            side= side, 
            order_type= 'limit',
            price= price , 
            size= size)
        print("\nTrade Request Sent!")
        for k,v in trade.items():
            print(k,"=\t",v)
            self.cfg._Set("TRADE","TRADE",str(k),str(v))
        print("\n")
        return trade

    def UpdateAccount(self,currency):
        self.cfg._Set("LOG", "","" , ("Updating Account:",currency)) 
        Account_id = self.cfg._Get("ACCOUNT", currency, "id")
        account = self.auth.get_account(Account_id)
        if 'available' in account:
            AvailableBalance = account['available']
        else:
            AvailableBalance = 0 
        return "%.8f"%float(AvailableBalance)  

    def GetTicker(self,product_id):
        self.cfg._Set("LOG", "","" , ("Getting Ticker:",product_id)) 
        tick = self.auth.get_product_ticker(product_id)
        for k , v in tick.items():
            self.cfg._Set("API","TICKER",str(k),str(v))
        self.cfg._Set("LOG", "","" , ("Price",tick["price"])) 
        return float(tick["price"])

    def CheckAllAccounts(self):
        self.cfg._Set("LOG", "","" , "Checking All Accounts") 
        # Hey Coinbase! May I have my accounts please.
        a = self.auth.get_accounts()
        MainQuote = self.quote # usd, usdc ,eur .. etc

        self.AllAccounts = []
        self.AllBalances = []
        self.AllAvailable = []
        self.AvailableValues = []
        self.BTCValues = []

        print("\n\tSorting All Accounts!\n\nPlease Wait..\n")
        # Lets Check Every Single Account Available!
        accountCount = 0
        avaicount = 0
        for i in a: 
            # Count Accounts And Grab Data
            accountCount += 1
            cur = str(i["currency"]) # Grab the Accounts Currency Name "BTC"
            avai = float(i["available"]) # Grab The Accounts Available Balance

            # Add Data To List
            self.AllAccounts.append(cur.upper())
            self.AllBalances.append(avai)

            # Save Everything From The Account To Account File
            for k,v in i.items():
                self.cfg._Set("ACCOUNT",str(cur),str(k),str(v))
                
            # Now Sort And Get The Prices For All The Accounts
            Quotes = ["USD","USDC","USDT","EUR","GBP"]
            NoBTC = ["BTC","CVC","DAI","DNT","GNT","LOOM","OXT"]
            BrokenQuotes = ["XRP","OXT"]
            # Account Sorting !
            if avai > 0 and cur not in BrokenQuotes:
                avaicount +=1
                self.AllAvailable.append(cur.upper())
                if cur in Quotes:
                    product_id = ( "BTC" + "-" + cur )
                    p = self.GetTicker(product_id)
                    price = 1 / p
                    btcValue = avai * price        
                elif cur in NoBTC:
                    if cur == "BTC":
                        price = 1
                        btcValue = avai
                    else:
                        self.cfg._Set("LOG", "", "", ( "NoBTCPair:",cur + "-" + MainQuote ))
                        product_id = ( cur + "-" + MainQuote )
                        p = self.GetTicker(product_id)
                        price = 1 / p
                        btcValue = 0 
                else:
                    product_id = ( cur + "-" + "BTC" )
                    price = self.GetTicker(product_id)
                    btcValue = avai * price  
                self.SATS += btcValue
                self.BTCValues.append(btcValue)
                p = self.GetTicker( ("BTC" + "-" + MainQuote) )
                self.AvailableValues.append(("%.2f"%(btcValue*p)))
                self.cfg._Set("ACCOUNT",str(cur), "QUOTE_VALUE", str("%.2f"%(btcValue*p)))
                self.cfg._Set("ACCOUNT",str(cur),"BTC_VALUE",str("%.8f"%btcValue))
            else:
                self.cfg._Set("ACCOUNT",str(cur), "QUOTE_VALUE", str(0.0))
                self.cfg._Set("ACCOUNT",str(cur),"BTC_VALUE",str(0.0))
            self.cfg._Set("LOG", "","" , (cur,"Checked")) 

            sleep(0.2)

        # End of Account Check loop
        print("\nPORTFOLIO OVERVEIW:\n")
        print("Total Accounts:\t",accountCount)
        print("Available Avvounts:\t",avaicount)
        time = datetime.now()
        minute = time.minute
        count = 0
        for aa in self.AllAccounts:
            av = self.AllBalances[count]
            if av > 0:
                print(aa , "%.8f"%(self.AllBalances[count]))
            count += 1
        print("\n")
        p = self.GetTicker( ("BTC" + "-" + MainQuote) )
        self.TOTAL_QUOTE = (self.SATS * p)
        self.cfg._Set("LOG", "","" , ("Setting Overveiw")) 
        self.cfg._Set("ACCOUNT", "OVERVEIW", "AllAccounts",str(self.AllAccounts))
        self.cfg._Set("ACCOUNT", "OVERVEIW", "AllBalances",str(self.AllBalances))
        self.cfg._Set("ACCOUNT", "OVERVEIW", "AllAvailable",str(self.AllAvailable))
        self.cfg._Set("ACCOUNT", "OVERVEIW", "AvailableValues",str(self.AvailableValues))
        self.cfg._Set("ACCOUNT", "OVERVEIW", "BTCValues",str(self.BTCValues))
        self.cfg._Set("ACCOUNT","OVERVEIW", "total_quote", "%.2f"%(self.TOTAL_QUOTE))
        self.cfg._Set("ACCOUNT","OVERVEIW", "total_accounts", str(accountCount))
        self.cfg._Set("ACCOUNT","OVERVEIW",  "last_update", str(minute))
        self.cfg._Set("LOG", "","" , ("Updated minute:",minute)) 
        print("TOTAL:\t",("%.2f"%(self.TOTAL_QUOTE)),MainQuote)
        print("Finished @",time)

class Config():
    '''Portfolio Config Setup'''
    
    PathList = None
    PathNames = None

    def __init__(self,name):
        print("Setting Up!:",name)

        self.name = name
        self.path = self._BuildNest(self.name)

        self.ConfigPath = (self.path + '\Config.ini')
        self.AccountPath = (self.path + '\Accounts.ini')
        self.TradePath = (self.path + '\Trades.ini')
        self.LogPath = (self.path + '\Log.ini')
        self.PathList = [self.ConfigPath,self.AccountPath,self.TradePath,self.LogPath]
        self.PathNames = ["Config","Account","Trade","Log"]

        self._BuildSettings()

    def _BuildNest(self,name):
        '''Create Directory Next To File'''
        fullPath = os.path.realpath(__file__) 
        thisDir = os.path.dirname(fullPath)
        botFold = thisDir + '\_' + str(name)
        Path(botFold).mkdir(parents=True, exist_ok=True)
        os.chdir(botFold)
        return botFold

    def _BuildSettings(self):
        '''Check For Data Files'''
        count = 0 
        for i in self.PathList:
            if os.path.isfile(i):
                print(self.PathNames[count],"File Found!")
            else: 
                print(self.PathNames[count],"Not Found!\nBuilding File!\n")
                self._BuildSettingFile(i)
                print(self.PathNames[count],"File Was Created!\n")
            count +=1

    def _BuildSettingFile(self,path):
        '''Build Data File'''
        c = ConfigParser()
        if path in self.PathList:
            if path == self.PathList[0]: # Config
                c["API"] = {            
                        "key"           :   "CoinbaseProAPI key",
                        "secret"        :   "CoinbaseProAPI secret",
                        "passphrase"    :   "CoinbaseProAPI passphrase",
                        "quote"         :   "Selected Quote Currency"
                }
                c["TICKER"] = {
                        "trade_id"  :   "Trade ID Number",
                        "price"     :   "Current Price",
                        "size"      :   "0.000000000000000",
                        "time"      :   "2021-05-01T12:00:00.578544Z",
                        "bid"       :   "0.000000000000000",
                        "ask"       :   "0.000000000000000",
                        "volume"    :   "0.000000000000000"
                }
            elif path == self.PathList[1]:
                c["OVERVEIW_ACCOUNT"] = {            
                        "TOTAL"    :   0,
                        "last_update" : 0,
                }
            elif path == self.PathList[2]:
                c["TRADE"] = {            
                        "TRADE"    :   "TRADE",
                }
            elif path == self.PathList[3]:
                c["LOG"] = {self.name : self.PathNames}

            with open(path,'w') as conf:
                    c.write(conf)
        else:
            print("Error Building Setting File @",path)

    def _Get(self,item,key,value):
        '''Get Item Form Config'''
        c = ConfigParser()
        if item == "API":
            APIkeys = ["key","secret","passphrase","quote"]
            c.read(self.ConfigPath)
            API = c["API"]
            if key in APIkeys:
                return API[key]
            else:
                return "config key not found"
        elif item == "ACCOUNT":
            ACCkeys = ["id","currency","balance","hold","available","profile_id","trading_enabled","quote_value","btc_value"]
            c.read(self.AccountPath)
            if key == "OVERVEIW":
                ACCOUNT = c["OVERVEIW_ACCOUNT"]
                return ACCOUNT[value]
            ACCOUNT = c[str(key + "_ACCOUNT")]
            if value in ACCkeys:
                return ACCOUNT[value]
            else:
                return "account key not found"
        elif item == "TRADE":
            c.read(self.TradePath)
            TRADE = c["TRADE"]
            return TRADE[value]
        elif item == "LOG":
            c.read(self.LogPath)
            LOG = c[str(key + "LOG")]
            return LOG[value]
        else:
            print("Error @ _Get")
    
    def _Set(self,pathname,item,key,value):
        '''Set Item In The Config File'''
        c = ConfigParser()
        if pathname == "API":
            path = self.ConfigPath
            c.read(path)
            API = c[str(item)]
            API[str(key)] = str(value)
        elif pathname == "ACCOUNT":
            path = self.AccountPath
            c.read(path)
            if c.has_section(str(item + "_ACCOUNT")):
                pass
            else:
                c.add_section(str(item + "_ACCOUNT"))
            ACCOUNT = c[str(item + "_ACCOUNT")]
            ACCOUNT[str(key)] = str(value)
        elif pathname == "TRADE":
            path = self.TradePath
            c.read(path)
            if c.has_section(str(item)):
                pass
            else:
                c.add_section(str(item))
            TRADE = c[str(item)]
            TRADE[str(key)] = str(value) 
        elif pathname == "LOG":
            path = self.LogPath
            NowTime = datetime.now()
            date = NowTime.strftime("%x")
            time = NowTime.strftime("(%H %M %S %f)")
            c.read(self.LogPath)
            if c.has_section((date)):
                pass
            else:
                c.add_section(date)
            display = c[date]
            display[time] = str(value)
        else:
            print("ERROR @ _Set")
            exit()

        with open(path, "w" ) as conf:
            c.write(conf)


if __name__=="__main__":
    Default = Connect("Default")