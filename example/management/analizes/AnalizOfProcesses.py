from example.management.analizes.Analiz import Analiz
from example.management.grabbers.events.TwoDoTwoGoGrabber import Grabber
from example.management.grabbers.multi_start import *
from datetime import datetime


class AnalizOfProcesses(Analiz):
    def optimum_amount(self):
        """ searching quantity of parallely running browsers
        """
        self.times.append([])

        for i in range(1, 15):
            print i
            t0 = datetime.now()
            multi_start(Grabber(), 'phantomjs', i)
            t1 = datetime.now()
            self.times[0].append(t1 - t0)
            print t1 - t0
        self.showTimePlot()