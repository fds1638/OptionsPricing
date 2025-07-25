from fredapi import Fred
from sklearn.linear_model import LinearRegression
import pandas as pd
import math
from plot_handler import PlotHandler

class VasicekDiscrete():
    """
    Gets weekly 30 Year Morgage data from FRED API,
    includes only weeks between start_date and end_date,
    and provides a weekly Vasicek model prediction of future rates for prediction_weeks ahead.
    """

    def __init__(self, input_start_date: str = '2021-06-30', input_end_date: str = '9999-12-30', input_weeks: int = 52*2):
        self.start_date: str = input_start_date
        self.end_date: str   = input_end_date
        self.prediction_weeks = input_weeks

    def vasicek_mortgage_prediciton(self):
        """
        Calculate and plot Vasicek predictions.
        """
        # Get data from FRED API
        api_key_file = '/Users/filipsain/PycharmProjects/OptionsPricing/FRED_API'
        with open(api_key_file, 'r') as f:
            api_key = f.read()
        fred = Fred(api_key=api_key)
        data = fred.get_series('MORTGAGE30US')

        # Filter data based on start and end dates, calculated deltas and lagged values.
        filtered = data[data.index.strftime('%Y-%m-%d') >= self.start_date]
        filtered = filtered[filtered.index.strftime('%Y-%m-%d') <= self.end_date]
        deltas = filtered.diff()
        deltas = deltas[1:]
        lagged = filtered.shift(1)[1:]

        # Reshape data and do linear regression fit.
        X = lagged.to_frame()
        y = deltas.to_frame()
        model = LinearRegression()
        model.fit(X, y)

        # Extract Vasicek parameters from model output.
        current_rate = lagged.values[-1]
        vasicek_a = (-1.0 * model.coef_[0])[0]
        vasicek_b = model.intercept_[0] / vasicek_a
        # Make Vasicek predictions.
        vasicek_prediction = lambda r0, a, b, t: r0 * math.exp(-a * t) + b * (1 - math.exp(-a * t))
        vasicek_predictions = [vasicek_prediction(current_rate, vasicek_a, vasicek_b, t) for t in range(self.prediction_weeks)]
        vasicek_dates = [deltas.index[-1] + pd.Timedelta(weeks=t) for t in range(self.prediction_weeks)]
        vasicek_equilibrium_dates = deltas.index.to_list() + vasicek_dates
        vasicek_equilibrium_values = [vasicek_b for _ in range(len(deltas.index) + len(vasicek_dates))]

        # Plot
        plots = {}
        plots["FRED 30-year rates"] = (deltas.index, lagged.values)
        plots["Vasicek prediction"] = (vasicek_dates, vasicek_predictions)
        plots["Vasicek equilibrium"] = (vasicek_equilibrium_dates, vasicek_equilibrium_values)
        plothandler = PlotHandler()
        plothandler.make_plots(plots)

if __name__=="__main__":
    vasicek = VasicekDiscrete()
    vasicek.vasicek_mortgage_prediciton()