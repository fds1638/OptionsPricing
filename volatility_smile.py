import matplotlib.pyplot as plt
from datetime import date
import Black_Scholes_closed_form_02 as bscf
from types import FunctionType

class VolatilitySmile:
    def __init__(self, ticker:int):
        self.ticker = ticker
        self.vtolerance = 0.0001
        self.data = {
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
        self.delta = self.data[self.ticker]["exercise_date"] - self.data[self.ticker]["cur_date"]
        self.current_price = self.data[self.ticker]["current_price"]

    def binarysearch(self, vlo:float, vhi:float, vtolerance:float, search_value:float, f:FunctionType, **kwargs) -> float:
        while vhi - vlo > vtolerance:
            vmi = 1.0 * (vhi + vlo) / 2.0
            calced_price = f([kwargs["cur_S"]], 0, 0, kwargs["percent_of_year"], kwargs["strike_price"], vmi, kwargs["r"])[0]
            if calced_price < search_value:
                vlo = vmi
            else:
                vhi = vmi
        return vlo

    def func_run(self) -> None:

        strikes_prices = []
        min_strike = 10000000
        max_strike = 0
        with open(self.data[self.ticker]["data_file"], "r") as f:
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
            kwargs = {
                "strike_price": float(s),
                "percent_of_year" : 1.0 * self.delta.days / 360.0,
                "cur_S" : self.current_price,
                "r" : self.data[self.ticker]["one_month_rate"]
            }
            vlo = self.binarysearch(0.00001, 0.99999, self.vtolerance, float(c), bscf.BlackScholesCallValue, **kwargs)
            volatilities.append(vlo) # currently not used
            strikes.append(float(s)) # currently not used
            if float(s) < self.current_price:
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
            f'Implied volatility smile {self.ticker.upper()} as of {self.data[self.ticker]["cur_date"].strftime("%d-%b-%Y")}\nCurrent price = ${self.current_price}, Expiry {self.data[self.ticker]["exercise_date"].strftime("%d-%b-%Y")}'
        )
        plt.show()
        return

if __name__=="__main__":
    vs = VolatilitySmile("aapl")
    vs.func_run()

