import matplotlib.pyplot as plt

class PlotHandler():

    def __init__(self):
        return

    def make_plots(self, plots):
        legend = []
        for plot in plots:
            plt.plot(plots[plot][0], plots[plot][1])
            legend.append(plot)
        plt.legend(legend)
        plt.show()

