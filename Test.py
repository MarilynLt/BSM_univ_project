from Option import Options
from datetime import datetime
import pandas as pd

df = pd.read_excel(r"C:\Users\Marilyn\Desktop\Optionpython.xlsx")
# df = df[['Strike','Spot', 'Maturity','Volatility','Type']]
df['Option Price'] = df[['Strike','Spot', 'Maturity','Volatility','Type']].apply(lambda x: x['Strike']*2 )
print(df)


