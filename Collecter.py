import CollectAuth

class Collecter():
    def __init__(self,port):
        print("\nInitializing Collecter")
        self.port = port
        self.port.cfg._Set("LOG", "","" , "Collecter Started") 
        self.Coins = []
        self.Values = []
        AllAvailable = port.AllAvailable
        AvailableValues = port.AvailableValues
        count = 0 
        for i in AllAvailable:
            self.Coins.append(i)
            self.Values.append(float(AvailableValues[count]))
            print(i,"=",float(AvailableValues[count]))
            count+=1
        #self.Collect()
    
    def Collect(self):
        self.port.cfg._Set("LOG", "","" , "Collect(Checking Ranges)")
        print("\nCollecting Coins!")
        lows = [100,200,300,400] 
        highs = [120,220,320,420]
        count = 0
        tempvalues = []
        for value in self.Values:
            if (lows[0] <= value <= highs[0]):
                tempValue = value - lows[0]
            elif (lows[1] <= value <= highs[1]):
                tempValue = value - lows[1]
            elif (lows[2] <= value <= highs[2]):
                tempValue = value - lows[2]
            elif (lows[3] <= value <= highs[3]):
                tempValue = value - lows[3]
            else:
                tempValue = value

            if tempValue == value or self.Coins[count] == "BTC":
                if self.Coins[count] == "BTC":
                    pass
                    #print("We pass by Bitcoin:",self.Coins[count],value,self.port.quote)
                else:
                    print(self.Coins[count],"is not in range with",value,self.port.quote)
                self.port.cfg._Set("LOG", "","" , ("Not In Range","%.2f"%tempValue,self.port.quote,"from",self.Coins[count]))
            else:
                tempvalues.append(tempValue)
                print(self.Coins[count],value,"is within range!")
                print("Collecting","%.2f"%tempValue,self.port.quote,"from",self.Coins[count])
                self.port.cfg._Set("LOG", "","" , ("Within Range","%.2f"%tempValue,self.port.quote,"from",self.Coins[count]))
                self.CollectCoin(self.Coins[count],tempValue)
            count +=1
        if sum(tempvalues) > 0:
            print("we collected",sum(tempvalues),self.port.quote)
            self.port.cfg._Set("LOG", "","" , ("we collected",sum(tempvalues),self.port.quote))
        else:
            self.port.cfg._Set("LOG", "","" , "Nothing Collected")
            print("Nothing Was Collected!")
        # End of Check
    
    def CollectCoin(self,Coin,Amount):
        self.port.cfg._Set("LOG", "","" , ("CollectCoin(",Coin,Amount,")"))

        product_id = (Coin + "-" + self.port.quote)
        current = self.port.GetTicker(product_id)
        cur1 = 1 / current
        size = float("%.4f"%(Amount * cur1))

        Custom = ["1INCH","ADA","ALGO","ANKR","BTC","ETC","ETH","LINK","LTC","MATIC","NU","SNX","SUSHI"]
        
        if Coin in Custom:
            print(Coin,"is Custom")
            for coin in Custom:
                if coin == Coin:
                    if  10 <= size < 11:
                        size = float("%.0f"%size)
                    elif 1 <= size <= 9:
                        size = float("%.1f"%size)
                    elif 0.1 <= size <= 0.9:
                        size = float("%.2f"%size)
                    elif 0.01 <= size <= 0.09:
                        size = float("%.3f"%size)
                    elif 0.001 <= size <= 0.009:
                        size = float("%.4f"%size)
                    elif 0.0001 <= size <= 0.0009:
                        size = float("%.5f"%size) 
                    else:
                        print("price Error")
            self.port.cfg._Set("LOG", "","" , (Coin,"is Custom with",size))
        else:
            self.port.cfg._Set("LOG", "","" , (Coin,"Not In Custom with",size))
            print(Coin,"Not In Custom")

        if size > 0.00001:
            self.port.cfg._Set("LOG", "","" , ("Send Trade Of",product_id, "sell", current, size))
            trade = self.port.SendTrade(product_id, "sell", current, size)
            self.lastTrade = trade
        else:
            self.port.cfg._Set("LOG", "","" , (size,"Is Not Enough To Make A Trade!"))
            print(size,"Is Not Enough To Make A Trade!")
            print("WTF")

if __name__ == "__main__":
    port = CollectAuth.Connect("test")
    Collecter(port)