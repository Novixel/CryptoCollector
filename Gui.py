# Novixel's Simple Display GUI
# Gui.py
# CryptoCollector
# Version 1.2.1b
# May 5th, 2021

import tkinter as tk
import Setup as cfg
from AccountSorting import MainQuote

class MainApp(tk.Frame):
    def __init__(self, master):
        cfg.LogThis("Gui Started! Will update every 5 seconds")
        print("\nGui Started! Will update every 5 seconds")
        self.master = master
        master.title("Account Display")

        welcomeTxt = "CRYPTO COLLECTOR DISPLAY"
        self.welcomeLabel = tk.Label(master, text=welcomeTxt)
        self.welcomeLabel.grid(row=0, column=0, rowspan = 1, columnspan = 3)

        self.list = tk.Listbox(master,width=20,)
        self.list.grid(row=3, column=1, rowspan = 1, columnspan = 1)

        self.lister = tk.Listbox(master,width=20,height=1)
        self.lister.grid(row=6, column=1)
        root.after(1, self.start)

    def start(self):
        keys = []
        values = []
        data = cfg.ReadALLDisplay()
        for k,v in data.items():
            keys.append(k.upper())
            values.append(float(v))
        count = 0
        self.list.delete(0,"end")
        self.lister.delete(0,"end")
        for z in keys:
            self.list.insert(tk.END,(str(keys[count]) + " ="+ str(values[count])))
            count +=1
        self.lister.insert(tk.END,"Total: " + str("%.2f"%sum(values) + MainQuote))
        root.after(5000, self.start)

root = tk.Tk()
Main = MainApp(root)
root.mainloop()