from fredapi import Fred
from sklearn.linear_model import LinearRegression
import pandas as pd
import math
from plot_handler import PlotHandler

class CoxIngersollRossDiscrete():
    """
    Gets weekly 30 Year Morgage data from FRED API,
    includes only weeks between start_date and end_date,
    and provides a weekly CoxIngersollRoss model prediction of future rates for prediction_weeks ahead.
    """

    def __init__(self, input_start_date: str = '2023-06-30', input_end_date: str = '9999-12-30', input_weeks: int = 52*2):
        self.start_date: str = input_start_date
        self.end_date: str   = input_end_date
        self.prediction_weeks = input_weeks

    def cox_ingersoll_ross_mortgage_prediciton(self):
        """
        Calculate and plot CoxIngersollRoss predictions.
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
        lagged = filtered.shift(1)[1:]
        lagged = lagged.apply(lambda x: math.sqrt(x)) # rescale by dividing by sqrt of lagged rate
        cnstnt = filtered.shift(1)[1:]
        cnstnt = cnstnt.apply(lambda x: 1.0/math.sqrt(x)) # rescale by dividing by sqrt of lagged rate
        deltas = filtered.diff()
        deltas = deltas[1:]
        deltas = deltas / lagged # rescale by dividing by sqrt of lagged rate


        # Reshape data and do linear regression fit.
        X = pd.DataFrame({'Col1': lagged, 'Col2': cnstnt})
        y = deltas.to_frame()
        model = LinearRegression(fit_intercept=False) # in C-I-R the cnstnt functions as the intercept
        model.fit(X, y)

        # Extract CoxIngersollRoss parameters from model output.
        current_rate = filtered.values[-1]
        c_i_s_a = (-1.0 * model.coef_[0])[0]
        c_i_s_b = (1.0 * model.coef_[0])[1] / c_i_s_a
        # Make c_i_s predictions.
        c_i_s_prediction = lambda r0, a, b, t: r0 * math.exp(-a * t) + b * (1 - math.exp(-a * t))
        c_i_s_predictions = [c_i_s_prediction(current_rate, c_i_s_a, c_i_s_b, t) for t in range(self.prediction_weeks)]
        c_i_s_dates = [deltas.index[-1] + pd.Timedelta(weeks=t) for t in range(self.prediction_weeks)]
        c_i_s_equilibrium_dates = deltas.index.to_list() + c_i_s_dates
        c_i_s_equilibrium_values = [c_i_s_b for _ in range(len(deltas.index) + len(c_i_s_dates))]

        # Plot
        plots = {}
        plots["FRED 30-year rates"] = (filtered.index, filtered.values)
        plots["CoxIngersollRoss prediction"] = (c_i_s_dates, c_i_s_predictions)
        plots["CoxIngersollRoss equilibrium"] = (c_i_s_equilibrium_dates, c_i_s_equilibrium_values)
        plothandler = PlotHandler()
        plothandler.make_plots(plots)

if __name__=="__main__":
    c_i_r = CoxIngersollRossDiscrete()
    c_i_r.cox_ingersoll_ross_mortgage_prediciton()