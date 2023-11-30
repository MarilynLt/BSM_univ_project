#University python project on the black and scholes model with dividend included
  Options pricer (include greeks)


#used libraries (must be installed before runing the code): 
  -random
  -numpy
  -scipy
  -bs4
  -pandas
  -requests
  -yfinance
  -tkinter
  -datetime
  -pandastable

Structure : 3 files (Interface, Option, Main)
  -Interface : Class BsmGui (the tkinter interface)
  -Option: Class Options (all functions and attribute on the option class)
  -Main

How to use the interface (2 Frames):
  *Main frame, for launching the BSM model on an random option portfolio. Open a tkinter window with the porfolio and the result (price,     delta, gamma, vega) ; generate an excel with containing the random portfolio ; generate chart report on option ( include greeks).
  *Minor frame, allow to compute a option price based on BSM model (no Greck in this one)
    ** maturity should be in following format: DD/MM/YYYY (for the pricer)
