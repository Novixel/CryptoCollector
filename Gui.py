# Novixel's Simple Display GUI
# Gui.py
# CryptoCollector
# Version 1.2.1b
# May 5th, 2021

import tkinter as tk
import CollectAuth
import Collecter

class MainApp(tk.Frame):
    def __init__(self, master):
        print("\nGui Started!\nUpdate every 5 seconds")
        self.master = master
        master.title("Account Display")

        welcomeTxt = "CRYPTO COLLECTOR DISPLAY"
        self.welcomeLabel = tk.Label(master, text=welcomeTxt)
        self.welcomeLabel.grid(row=0, column=0, rowspan = 1, columnspan = 3)

        self.list = tk.Listbox(master,width=20,)
        self.list.grid(row=3, column=1, rowspan = 1, columnspan = 1)

        self.lister = tk.Listbox(master,width=20,height=1)
        self.lister.grid(row=6, column=1)
        self.port = CollectAuth.Connect("test")
        self.count = 0
        root.after(1, self.start)

    def start(self):
        self.count +=1
        Avail = self.port.AllAvailable
        avail = self.port.AvailableValues
        count = 0
        self.list.delete(0,"end")
        self.lister.delete(0,"end")
        for i in Avail:
            self.list.insert(tk.END,(str(i.upper()) + " = "+ str(avail[count])))
            count +=1
        self.lister.insert(tk.END,"Total: " + str("%.2f"%self.port.TOTAL_QUOTE + self.port.quote))
        if self.count == 12:
            self.count = 0
            self.Collect()
        root.after(5000, self.start)

    def Collect(self):
        self.port = CollectAuth.Connect("test")
        Collecter.Collecter(self.port).Collect()

if __name__=="__main__":
    root = tk.Tk()
    Main = MainApp(root)
    root.mainloop()