import matplotlib.pyplot as plt


class Analiz:
    def __init__(self):
        self.grabbers = []
        self.line_names = []
        self.times = []

    def showTimePlot(self):
        N = len(self.times[0])
        plt.figure()
        for i in range(len(self.times)):
            plt.plot(range(1, N+1, 1), self.times[i])
            if len(self.line_names) != 0:
                x_text = N // 2
                y_text = self.times[i][len(self.times[i]) // 2]
                plt.annotate(self.line_names[i], xy=(x_text, y_text), xytext=(x_text + 2, y_text + 2),
                             arrowprops=dict(facecolor='black', shrink=0.005), )
        plt.xlabel("N")
        plt.ylabel("Execution time")
        plt.show()