from pyalgotrade import technical

class PeriodHigh(technical.EventWindow):
    def getValue(self):
        ret = None
        if self.windowFull():
            ret = self.getValues().max()
        return ret

class PeriodLow(technical.EventWindow):
    def getValue(self):
        ret = None
        if self.windowFull():
            ret = self.getValues().min()
        return ret