import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

import pandas as pd
from pandastable import Table

from Option import Options


class BsmGUI:
    """
    Black and Scholes model GUI
    """

    def __init__(self, root):

        # Root configuration
        self.root = root
        self.root.title("Black-Scholes-Merton pricer")
        self.root.iconbitmap('assassins_creed.ico')
        self.root.geometry("525x505")
        # self.root.configure(bg='#FF7F50')
        self.root.minsize(525, 505)

        # self.filename = tk.PhotoImage(file=r"C:\Users\Marilyn\Downloads\data-flow.png")
        # # self.background_label = ttk.Label(master=self.root, image=self.filename)
        # # self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # self.canvas = tk.Canvas(master=self.root, width=800, height=600)
        # self.canvas.pack(side='top', fill='both', expand='yes')
        # self.canvas.create_image(0, 0, image=self.filename)

        # Frame
        self.main_frame = ttk.Frame(master=self.root, relief='ridge')
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.minor_frame = ttk.Frame(master=self.root, relief='ridge')
        self.minor_frame.grid(row=0, column=0, sticky="nsew")

        # Widget Minor Frame
        self.label_title = ttk.Label(master=self.minor_frame, text="BSM Model on selected option")
        self.label_title.grid(row=0, column=1, padx=5, pady=25, columnspan=2)

        self.lbl_type = ttk.Label(master=self.minor_frame, text="Type")
        self.lbl_type.grid(row=1, column=0, padx=1, pady=1)
        self.ent_type = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_type.grid(row=1, column=1, padx=1, pady=3)

        self.lbl_strike = ttk.Label(master=self.minor_frame, text="Strike")
        self.lbl_strike.grid(row=2, column=0, padx=1, pady=1)
        self.ent_strike = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_strike.grid(row=2, column=1, padx=1, pady=3)

        self.lbl_spot = ttk.Label(master=self.minor_frame, text='Spot:')
        self.lbl_spot.grid(row=3, column=0, padx=1, pady=1)
        self.ent_spot = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_spot.grid(row=3, column=1, padx=1, pady=3)

        self.lbl_maturity = ttk.Label(master=self.minor_frame, text='maturity date:')
        self.lbl_maturity.grid(row=4, column=0, padx=1, pady=1)
        self.ent_maturity = ttk.Entry(master=self.minor_frame, width=10)
        self.ent_maturity.grid(row=4, column=1, padx=1, pady=3)

        self.lbl_vol = ttk.Label(master=self.minor_frame, text='volatility:')
        self.lbl_vol.grid(row=5, column=0, padx=1, pady=1)
        self.ent_vol = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_vol.grid(row=5, column=1, padx=1, pady=3)

        self.lbl = ttk.Label(master=self.minor_frame, text='Optional (in %)')
        self.lbl.grid(row=6, column=0, columnspan=2, pady=18)

        self.lbl_rf = ttk.Label(master=self.minor_frame, text='risk free rate:')
        self.lbl_rf.grid(row=7, column=0, padx=1, pady=1)
        self.ent_rf = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_rf.grid(row=7, column=1, padx=1, pady=3)

        self.lbl_div = ttk.Label(master=self.minor_frame, text='dividend yield:')
        self.lbl_div.grid(row=8, column=0, padx=2, pady=1)
        self.ent_div = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_div.grid(row=8, column=1, padx=1, pady=3)

        self.btn_compute = ttk.Button(master=self.minor_frame, text='Compute', command=Options.option_chart)
        self.btn_compute.grid(row=9, column=0, columnspan=2, padx=7, pady=22)

        self.label_result = ttk.Label(master=self.minor_frame, text='Result:')
        self.label_result.grid(row=10, column=0, columnspan=2)
        self.label_price = ttk.Label(master=self.minor_frame, text='Price:')
        self.label_price.grid(row=12, column=0)
        self.ent_price = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_price.grid(row=12, column=1, pady=2)

        self.label_delta = ttk.Label(master=self.minor_frame, text='Delta:')
        self.label_delta.grid(row=11, column=2)
        self.ent_delta = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_delta.grid(row=11, column=3, pady=2)

        self.label_gamma = ttk.Label(master=self.minor_frame, text='Gamma:')
        self.label_gamma.grid(row=12, column=2)
        self.ent_gamma = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_gamma.grid(row=12, column=3, pady=2)

        self.label_vega = ttk.Label(master=self.minor_frame, text='Vega:')
        self.label_vega.grid(row=13, column=2)
        self.ent_vega = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_vega.grid(row=13, column=3, pady=2)

        self.label_theta = ttk.Label(master=self.minor_frame, text='Theta:')
        self.label_theta.grid(row=14, column=2)
        self.ent_theta = ttk.Entry(master=self.minor_frame, width=8)
        self.ent_theta.grid(row=14, column=3, pady=2)

        self.var1 = tk.IntVar()
        self.chk_ticker_ent = ttk.Entry(master=self.minor_frame, width=7)
        self.chk_ticker_ent.grid(row=3, column=3)
        self.chk_ticker_lbl = ttk.Label(master=self.minor_frame, text='Ticker:')
        self.chk_ticker_lbl.grid(row=3, column=2)
        self.chk_ticker = ttk.Checkbutton(master=self.minor_frame, text='Download spot', variable=self.var1,
                                          onvalue=1, offvalue=0, command=self.fetch_spot)
        self.chk_ticker.grid(row=2, column=2, columnspan=2, padx=40, sticky="nsew")

        # Widget Main frame
        self.lbl_title = ttk.Label(master=self.main_frame, text="BSM model on random Portfolio")
        self.lbl_title.grid(row=0, column=1, padx=5, pady=25, columnspan=3)

        self.btn_run = ttk.Button(master=self.main_frame, text='Run', command=self.run_bsm_ptf)
        self.btn_run.grid(row=5, column=1, columnspan=2, padx=7, pady=22)

        self.var2 = tk.IntVar()
        self.chk_report = ttk.Checkbutton(master=self.main_frame, text="Export to Excel", variable=self.var2,
                                          onvalue=1, offvalue=0)
        self.chk_report.grid(row=6, column=1, columnspan=2, padx=7, pady=20, sticky='nsew')

        self.btn_chart = ttk.Button(master=self.main_frame, text="Generate Options' chart", command=self.chart_op)
        self.btn_chart.grid(row=7, column=1, columnspan=2, padx=7, pady=20)

    def calculate(self):
        """
        Compute the option price.
        Use Options class - function bsm
        Return: float
        -------
        """

        try:
            option_type = str(self.ent_type.get().upper())
            if option_type == "":
                messagebox.showerror("showerror", "Please enter Option type")
            strike_price = float(self.ent_strike.get())
            spot_price = float(self.ent_spot.get())
            maturity = (datetime.strptime(self.ent_maturity.get(), '%d/%m/%Y') - datetime.now()).days / 365
            volatility = float(self.ent_vol.get())
        except Exception as e:
            print(e.args)
            messagebox.showerror("showerror", "Attribute missing, please check your input")

        try:
            rf = float(self.ent_rf.get()) / 100
            div = float(self.ent_div.get()) / 100
        except ValueError:
            rf = 0.05
            div = 0.04

        op = Options(strike_price, spot_price, maturity, volatility, rf, div)
        price = op.bsm(option_type)
        delta = op.delta(option_type)
        gamma = op.gamma()
        vega = op.vega()
        theta = op.theta(option_type)

        self.ent_price.delete(0, tk.END)
        self.ent_price.insert(0, str(price))

        self.ent_delta.delete(0, tk.END)
        self.ent_delta.insert(0, str(delta))

        self.ent_gamma.delete(0, tk.END)
        self.ent_gamma.insert(0, str(gamma))

        self.ent_vega.delete(0, tk.END)
        self.ent_vega.insert(0, str(vega))

        self.ent_theta.delete(0, tk.END)
        self.ent_theta.insert(0, str(theta))

    def fetch_spot(self):
        """
        Get stock price from yahoo finance
        Returns
        -------
        """

        # get spot if the box is checked
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

    # @staticmethod
    def manage_pdtable(self, data: pd.DataFrame):
        """
        Create a new window and display data in an Excel way , plot are feasible by using the plot button on the new
        interface

        Parameters
        ----------
        data : Dataframe the need to be displayed in the new window
        -------
        """

        window = tk.Toplevel(self.root)
        # window.iconbitmap('assassins_creed.ico')
        window.focus_force()  # put the focus on the new window

        frame = tk.Frame(master=window)
        frame.pack(fill='both', expand=True)

        pt = Table(frame, showtoolbar=True, showstatusbar=True)
        pt.show()

        pt.model.df = data

    @staticmethod
    def generate_excel(data: pd.DataFrame):
        data.to_excel("BSM_portfolio.xlsx", sheet_name='Portfolio', index=False)

    def run_bsm_ptf(self):
        """
        Lunch BSM model computation of option price, delta, gamma and vega
        Returns: dataframe with all options infos
        -------
        """

        stock_price = Options.retrieve_ticker()  # retrieve the ticker and spot
        df = Options.get_option(stock_price)  # retrieve option data from yahoo finance

        df['Price'] = 0
        df['Delta'] = 0
        df['Gamma'] = 0
        df['Vega'] = 0
        df['Theta'] = 0

        # Computing Option price, delta, gamma and vega
        for i in range(len(df)):
            #  Instantiation of Options class
            op = Options(strike=df['Strike'].loc[i], spot=df['Spot'].loc[i], sigma=df['Volatility'].loc[i],
                         t=(datetime.strptime(df['Maturity'].loc[i], '%Y-%m-%d') - datetime.now()).days / 365)

            df['Price'].loc[i] = op.bsm(option_type=df['Type'].loc[i].upper())
            df['Delta'].loc[i] = op.delta(option_type=df['Type'].loc[i].upper())
            df['Theta'].loc[i] = op.theta(option_type=df['Type'].loc[i].upper())
            df['Gamma'].loc[i] = op.gamma()
            df['Vega'].loc[i] = op.vega()

        if self.var2.get() == 1:
            self.generate_excel(data=df)

        self.manage_pdtable(data=df)

    @staticmethod
    def chart_op():
        try:
            Options.option_chart()
            messagebox.showinfo("info", "PDF successfully generated!")
        except Exception as e:
            print(e)
            messagebox.showinfo("info", "unable to generate PDF")



