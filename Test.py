import numpy as np

from Option import Options
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# df = pd.read_excel(r"C:\Users\Marilyn\Desktop\Optionpython.xlsx")
# # df = df[['Strike','Spot', 'Maturity','Volatility','Type']]
# df['Option Price'] = df[['Strike','Spot', 'Maturity','Volatility','Type']].apply(lambda x: x['Strike']*2 )
# print(df)

with PdfPages('Option_graph.pdf') as pdf:
    with plt.style.context('seaborn-v0_8-darkgrid'):
        spot = np.arange(1, 100)

        # Greek plot

        fig, axes = plt.subplots(5, 1, figsize=(10, 25))
        fig.suptitle('Greeks', ha='center', fontweight='bold', fontsize=15)
        fig.tight_layout(pad=7.0)
        strike = [37, 54, 71]

        for s in strike:
            del_call = [Options(float(s), float(x), 5.0, 0.1).delta('CALL') for x in spot]
            del_put = [Options(float(s), float(x), 5.0, 0.1).delta('PUT') for x in spot]
            axes[0].plot(del_call, linestyle='--', label=("Delta Call K=%s" % s))
            axes[0].plot(del_put, label=("Delta Put K=%s" % s))

        axes[0].set_ylabel('Delta')
        axes[0].legend()

        for s in strike:
            gam = [Options(float(s), float(x), 5.0, 0.1).gamma() for x in spot]
            axes[1].plot(gam, linestyle='--', label=("Options Gamma K=%s" % s))

        axes[1].set_ylabel('Gamma')
        axes[1].legend()

        for s in strike:
            veg = [Options(float(s), float(x), 5.0, 0.1).vega() for x in spot]
            axes[2].plot(veg, label=("Options Vega K=%s" % s))

        axes[2].set_ylabel('Vega')
        axes[2].set_title('Volatility = 0.1 ')
        axes[2].legend()

        for s in strike:
            theta_call = [Options(float(s), float(x), 5.0, 0.1).theta('CALL') for x in spot]
            theta_put = [Options(float(s), float(x), 5.0, 0.1).theta('PUT') for x in spot]
            axes[3].plot(theta_call, linestyle='--', label=("Theta Call K=%s" % s))
            axes[3].plot(theta_put, label=("Theta Put K=%s" % s))

        axes[3].set_ylabel('Theta')
        axes[3].set_title('Maturity = 5 years')
        axes[3].legend()

        # Option plot

        call_val = [Options(37.0, float(x), 1.0, 0.5).bsm('CALL') for x in spot]
        put_val = [Options(37.0, float(x), 1.0, 0.5).bsm('PUT') for x in spot]

        axes[4].set_title(f'Change in option value with stock price'
                          f'\n \n Strike: 37, t: 1 an, sigma: 0.5, r: 5%, q: 4%', fontweight="bold")
        axes[4].set_xlabel('Stock Price')
        axes[4].set_ylabel("Option price")
        axes[4].plot(spot, call_val, color='green', label='Call')
        axes[4].plot(spot, put_val, color='blue', label='Put')
        axes[4].legend()

    pdf.savefig()
    plt.close()
