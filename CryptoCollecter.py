from AccountSorting import AllAccounts, quote, MainQuote, GetTicker
import Setup as cfg

curList = []

#lets call this once TO start
def getSome():
    global curList
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

def CollectCoins(currency, amount):
    product_id = currency + "-BTC"
    current = float(GetTicker(product_id))
    minTrade = current * 5
    new = amount * current

    print("\nBot Has Collected!:","%.8f"%new,quote)

    price = current
    size = amount
    if new > minTrade: # last trade check before the request
        trade = auth.place_order(
            product_id= product_id,
            side= 'sell', 
            order_type= 'limit',
            price= price, 
            size= size)
        print("\nNewest Trade")
        for k,v in trade.items():
                print(k,"=\t",v)
    print("\n")
    print(product_id,"%.8f"%price,"%.2f"%size)

def CollectionRing():
    global curList
    Accounts, Main_Values, BTC_Values = getSome()
    l1 = 102
    h1 = 120

    l2 = 202
    h2 = 220

    l3 = 302
    h3 = 320
    count = 0
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
            print(Accounts[count] + ": is collecting:","%.2f"%tempValue,MainQuote)
            cur = str(Accounts[count])
            CollectCoins(cur,tempValue)
            print("\n")
        count +=1

    ncount = 0
    for i in curList:
        cfg.SaveDisplay(str(i),str(cfg.ReadAccount(i,"usd_value")))
    return curList
    print("All Coins Collected!")
# lets check it again