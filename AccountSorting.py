from Connect import CoinConnect
import configparser
import Setup as cfg
from time import sleep

bot = CoinConnect()

auth = bot.auth

quote = "BTC" # Change me ONLY if your a big boy!

MainQuote = "GBP"

mlist = []

def GetTicker(product_id):
    product_id = product_id
    #print("\n #####",product_id,"TICKER")
    tick = auth.get_product_ticker(product_id)
    for k , v in tick.items():
        cfg.SaveTicker(str(k),str(v))
        #print(k, "=\t",v)
    return tick["price"]

def GetTotal(available):
    price = float(GetTicker(("BTC" + "-" + MainQuote )))
    x = available * price
    return x

def AllAccounts():
    # Lets Check All Of The Accounts With Available Funds
    global mlist
    a = auth.get_accounts()
    Specials = ["USD","USDC","EUR","GBP"]
    mlist = []
    alist = []
    acList = []
    print("\n AVAILABLE FUNDS:")
    for i in a: # Lets Check Every Account
        avai = float(i["available"]) # Grab The Funds
        cur = i["currency"] # And the Ticker Name
        # Save The Useful Stuff
        if avai > 0 and cur == "BTC": # First check if we have Bitcoin!!!
            acList.append(cur)
            price = float(GetTicker("BTC-USD"))
            mlist.append(float("%.4f"%(avai * price)))
            #print("\n",cur)
            for k,v in i.items():
                cfg.SaveAccount(str(cur),str(k),str(v))
                #print(cur,k,"=\t",v)
            cfg.SaveAccount(str(cur),str(quote + "_value"),str("%.8f"%avai))
            cfg.SaveAccount(str(cur),str(MainQuote + "_value"),str("%.2f"%(GetTotal(avai))))

        elif avai > 0 and cur != quote: # if we have funds and its NOT bitcoin
            acList.append(cur)
            print("\n####\t" + cur + "-"+ quote)
            for k,v in i.items():
                cfg.SaveAccount(str(cur),str(k),str(v)) # save stuff
                if k == "available":
                    print("      We Have =\t",v,cur)
                #print(k,"=\t",v)

            # convert the coin if special
            if cur in Specials:
                temPro = ( quote + "-" + cur )
                price = float(GetTicker(temPro))
                price = 1 / price
            else:
                temPro = ( cur + "-" + quote )
                price = float(GetTicker(temPro))

            product_id = temPro

            convert = avai * price

            exchange = GetTotal(float(convert))

            mlist.append(float("%.4f"%exchange))

            # Magic Time

            cfg.SaveAccount(str(cur),str(quote + "_value"),str("%.8f"%convert))
            cfg.SaveAccount(str(cur),str(MainQuote + "_value"),str("%.2f"%exchange))

            alist.append(convert) # add to list of totals balances in BTC
            convert = convert # make it look pretty for the camera
            print(" Market Price =\t", "%.8f"%price, quote)
            print("  Total Value =\t", "%.8f"%convert, quote)
            print("  Total Quote =\t", "%.2f"%exchange, MainQuote)
            sleep(1)
            #Now Lets Send This To a Bot! to check ranges
    #alist.append(float(cfg.ReadAccount("BTC","available")))
    QuoteTotal = GetTotal(sum(alist))
    print("\n\tTotal Bitcoin\t", "%.8f"%sum(alist), quote)
    print("\tFor a Total of\t", ("%.2f"%QuoteTotal), MainQuote)
   # print("\n")
    return acList