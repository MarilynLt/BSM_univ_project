import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

from Option import Options


class BsmGUI:
    """
    Black and scholes model GUI
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Black-Scholes-Merton pricer")
        self.root.iconbitmap('assassins_creed.ico')
        self.root.geometry("600x400")
        self.root.minsize(250, 300)

        # Frame
        self.main_frame = ttk.Frame(master=self.root, relief='raised')
        self.main_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.minor_frame = ttk.Frame(master=self.root, relief='sunken')
        self.minor_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Widget Minor Frame
        self.lbl_type = ttk.Label(master=self.minor_frame, text="Type")
        self.lbl_type.grid(row=0, column=0, padx=1, pady=1)
        self.ent_type = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_type.grid(row=0, column=1, padx=1, pady=3)

        self.lbl_strike = ttk.Label(master=self.minor_frame, text="Strike")
        self.lbl_strike.grid(row=1, column=0, padx=1, pady=1)
        self.ent_strike = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_strike.grid(row=1, column=1, padx=1, pady=3)

        self.lbl_spot = ttk.Label(master=self.minor_frame, text='Spot:')
        self.lbl_spot.grid(row=2, column=0, padx=1, pady=1)
        self.ent_spot = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_spot.grid(row=2, column=1, padx=1, pady=3)

        self.lbl_maturity = ttk.Label(master=self.minor_frame, text='maturity date:')
        self.lbl_maturity.grid(row=3, column=0, padx=1, pady=1)
        self.ent_maturity = ttk.Entry(master=self.minor_frame, width=10)
        self.ent_maturity.grid(row=3, column=1, padx=1, pady=3)

        self.lbl_vol = ttk.Label(master=self.minor_frame, text='volatility:')
        self.lbl_vol.grid(row=4, column=0, padx=1, pady=1)
        self.ent_vol = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_vol.grid(row=4, column=1, padx=1, pady=3)

        self.lbl = ttk.Label(master=self.minor_frame, text='Optional (in %)')
        self.lbl.grid(row=5, column=0, columnspan=2, pady=18)

        self.lbl_rf = ttk.Label(master=self.minor_frame, text='risk free rate:')
        self.lbl_rf.grid(row=6, column=0, padx=1, pady=1)
        self.ent_rf = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_rf.grid(row=6, column=1, padx=1, pady=3)

        self.lbl_div = ttk.Label(master=self.minor_frame, text='dividend yield:')
        self.lbl_div.grid(row=7, column=0, padx=1, pady=1)
        self.ent_div = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_div.grid(row=7, column=1, padx=1, pady=3)

        self.btn_compute = ttk.Button(master=self.minor_frame, text='Compute', command=self.calculate)
        self.btn_compute.grid(row=8, column=0, columnspan=2, padx=7, pady=22)

        self.label_result = ttk.Label(master=self.minor_frame, text='Result:')
        self.label_result.grid(row=9, column=0, columnspan=2)
        self.ent_result = ttk.Entry(master=self.minor_frame, width=12)
        self.ent_result.grid(row=10, column=0, columnspan=2, padx=7, pady=6)

        self.var1 = tk.IntVar()
        self.chk_ticker_ent = ttk.Entry(master=self.minor_frame, width=7)
        self.chk_ticker_ent.grid(row=2, column=3)
        self.chk_ticker_lbl = ttk.Label(master=self.minor_frame, text='Ticker:')
        self.chk_ticker_lbl.grid(row=2, column=2)
        self.chk_ticker = ttk.Checkbutton(master=self.minor_frame, text='Download spot', variable=self.var1,
                                          onvalue=1, offvalue=0, command=self.fetch_spot)
        self.chk_ticker.grid(row=1, column=2, columnspan=2, padx=40, sticky="nsew")

        #Widget Main frame


    def calculate(self):
        """
        Compute the option price.
        Use Options class - function bsm
        Return: float
        -------
        """
        option_type = str(self.ent_type.get().upper())
        strike_price = float(self.ent_strike.get())
        spot_price = float(self.ent_spot.get())
        maturity = (datetime.strptime(self.ent_maturity.get(), '%d/%m/%Y') - datetime.now()).days / 365
        volatility = float(self.ent_vol.get())
        try:
            rf = float(self.ent_rf.get()) / 100
            div = float(self.ent_div.get()) / 100
        except ValueError:
            rf = 0.05
            div = 0.04

        price = Options(strike_price, spot_price, maturity, volatility, rf, div).bsm(option_type)

        self.ent_result.delete(0, tk.END)
        self.ent_result.insert(0, str(price))

    def fetch_spot(self):
        """
        Get stock price from yahoo finance
        Returns
        -------
        """
        if self.var1.get() == 1:
            try:
                option_ticker = str(self.chk_ticker_ent.get().upper())
                spot = Options.get_spot(option_ticker)

                self.ent_spot.delete(0, tk.END)
                self.ent_spot.insert(0, str(spot))
            except Exception as e:
                print(e.args)
                messagebox.showerror("showerror", "You are using an incorrect  TICKER, please check")
        else:
            self.chk_ticker_ent.delete(0, tk.END)
            self.ent_spot.delete(0, tk.END)

