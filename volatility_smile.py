import matplotlib.pyplot as plt
from datetime import date
import Black_Scholes_closed_form_02 as bscf

delta = date(2025, 4, 17) - date(2025, 3, 19)

current_price = float(215.24)

strikes_prices = []
strikes = []
call_prices = []
with open("./options_chains/aapl_call_20250319_20250417","r") as f:
    for line in f:
        line_array = line.strip().split()
        strikes_prices.append((line_array[4],line_array[5]))

strikes_prices.sort()
volatilities = []
for s,c in strikes_prices:
    vlo = 0.00001
    vhi = 0.99999
    while vhi - vlo > 0.0001:
        vmi = 1.0*(vhi+vlo)/2.0
        calced_price = bscf.BlackScholesCallValue([current_price], 0, 0, 1.0*delta.days/360.0, float(s), vmi, 0.0437)[0]
        if calced_price < float(c):
            vlo = vmi
        else:
            vhi = vmi
    volatilities.append(vlo)
    strikes.append(float(s))
    call_prices.append(float(c))

plt.plot(strikes, volatilities, 'o')
plt.xlabel("Strike Price")
plt.ylabel("Implied Volatility")
plt.xticks([100,150,200,250,300,350])
plt.title(f"Implied volatility smile AAPL as of 19 March 2025\nCurrent price = ${current_price}, Expiry 17 April 2025")
plt.show()

