from CryptoCollecter import CollectionRing as collect
from CryptoCollecter import getSome
from AccountSorting import MainQuote,mlist
from time import sleep
import threading
from subprocess import call
import datetime

def thread_second():
    call(["python", "..\Gui.py"])
processThread = threading.Thread(target=thread_second)
processThread.start()

print("LOADING CRYPTO COLLECTOR V1.1 ....")
sleep(1)

while True:
    print("\nREADING ACCOUNTS!")
    sleep(1)
   #Accounts,GPB,BTC = getSome()
    #totalmain = sum(GPB)
    #print('\nCollecting Coins!')
    c,newgpb = collect()
    totalafter = sum(newgpb)
    #print("Total Before","%.2f"%totalmain,MainQuote)
    #print("Total After","%.2f"%totalafter,MainQuote)
    #print('\nAccounts Change: ',"%.2f"%(totalmain-totalafter),MainQuote)

    now = datetime.datetime.now()    
    print ("\nFINISHED AT: ",now.strftime("%H:%M:%S"))
    print("WAITING 2 MINS")
    sleep(119)
    print("\n LOOP RESTARTING")