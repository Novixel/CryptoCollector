from CryptoCollecter import CollectionRing as collect
from CryptoCollecter import getSome
from AccountSorting import MainQuote,mlist
from time import sleep
import threading
from subprocess import call

def thread_second():
    call(["python", "..\Gui.py"])
processThread = threading.Thread(target=thread_second)
processThread.start()

while True:
    print("\nReading Accounts!")
    sleep(1)
    Accounts,GPB,BTC = getSome()
    totalmain = sum(GPB)
    print('\nCollecting Coins!')
    c,newgpb = collect()
    totalafter = sum(newgpb)
    print("Total Before","%.2f"%totalmain,MainQuote)
    print("Total After","%.2f"%totalafter,MainQuote)
    print('\nAccounts Change: ',"%.2f"%(totalmain-totalafter),MainQuote)
    print("Waiting 5 Min")
    sleep(299)
    print("loop restarting")
    sleep(1)