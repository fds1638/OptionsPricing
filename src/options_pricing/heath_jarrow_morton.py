import matplotlib.pyplot as plt
from scipy.optimize import fmin
import math
import nelson_siegel_svensson

class HeathJarrowMorton():
    def __init__(self, short_rate_model = "ho_lee"):
        self.short_rate_model = short_rate_model
        self.interest_rate_curve = []

    def get_interest_rate_curve(self):
        nss = nelson_siegel_svensson.NelsonSiegelSvensson()
        yields_20250321 = nss.get_interest_rates()
        opt_func = nss.minimize_NSS_closure(yields_20250321)
        opt2 = opt_func()
        return yields_20250321, [nss.NSS(opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5], yields_20250321[i][0]) for i in
                  range(len(yields_20250321))]

if __name__=="__main__":
    # plot
    hjm = HeathJarrowMorton()
    yyy,aaa = hjm.get_interest_rate_curve()
    legend = []
    plt.plot([yyy[i][0] for i in range(len(yyy))], [yyy[i][1] for i in range(len(yyy))],'o-')
    legend.append("yields 21 March 2025")
    plt.plot([yyy[i][0] for i in range(len(yyy))], aaa,'o-')
    legend.append("closure approximation")
    plt.legend(legend)
    plt.show()

