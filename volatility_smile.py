import matplotlib.pyplot as plt
from datetime import date
import Black_Scholes_closed_form_02 as bscf

ticker = "tsla"
vtolerance = 0.0001

data = {
    "aapl": {
        "cur_date" : date(2025, 3, 19),
        "exercise_date" : date(2025, 4, 17),
        "current_price" : float(215.24),
        "data_file" : "./options_chains/aapl_call_20250319_20250417",
        "one_month_rate" : float(0.0437)
    },
    "tsla": {
        "cur_date": date(2025, 3, 20),
        "exercise_date": date(2025, 4, 25),
        "current_price": float(236.26),
        "data_file": "./options_chains/tsla_call_20250320_20250425",
        "one_month_rate": float(0.0439)
    }
}

delta = data[ticker]["exercise_date"] - data[ticker]["cur_date"]
current_price = data[ticker]["current_price"]

strikes_prices = []
min_strike = 10000000
max_strike = 0
with open(data[ticker]["data_file"], "r") as f:
    for line in f:
        line_array = line.strip().split()
        strikes_prices.append((line_array[4],line_array[5]))
        min_strike = min(min_strike, int(line_array[4]))
        max_strike = max(max_strike, int(line_array[4]))

strikes_prices.sort()
strikes = [] # currently not used
volatilities = [] # currently not used
strikes_out_money = []
volatilities_out_money = []
strikes_in_money = []
volatilities_in_money = []
for s,c in strikes_prices:
    vlo = 0.00001
    vhi = 0.99999
    while vhi - vlo > vtolerance:
        vmi = 1.0*(vhi+vlo)/2.0
        calced_price = bscf.BlackScholesCallValue([current_price], 0, 0, 1.0*delta.days/360.0, float(s), vmi, data[ticker]["one_month_rate"])[0]
        if calced_price < float(c):
            vlo = vmi
        else:
            vhi = vmi
    volatilities.append(vlo) # currently not used
    strikes.append(float(s)) # currently not used
    if float(s) < current_price:
        volatilities_in_money.append(vlo)
        strikes_in_money.append(float(s))
    else:
        volatilities_out_money.append(vlo)
        strikes_out_money.append(float(s))

plt.plot(strikes_in_money, volatilities_in_money, 'o')
plt.plot(strikes_out_money, volatilities_out_money, 'o')
plt.legend(['in the money', 'out of the money'])
plt.xlabel("Strike Price")
plt.ylabel("Implied Volatility")
plt.xticks([50*i for i in range(min_strike//50, max_strike//50+2)])
plt.title(
    f'Implied volatility smile {ticker.upper()} as of {data[ticker]["cur_date"].strftime("%d-%b-%Y")}\nCurrent price = ${current_price}, Expiry {data[ticker]["exercise_date"].strftime("%d-%b-%Y")}'
)
plt.show()

