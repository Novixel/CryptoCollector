from CryptoCollecter import CollectionRing as collect
from CryptoCollecter import getSome
from time import sleep

while True:
    a,b,c = getSome()
    c = collect()
    print(c)
    sleep(300)
