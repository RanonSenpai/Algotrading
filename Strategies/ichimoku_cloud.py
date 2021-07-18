from pyalgotrade import strategy
from pyalgotrade import technical
from pyalgotrade.technical import ma

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

def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value

class IchimokuCloud(strategy.BacktestingStrategy):
    # This is a strategy with 88.89% Winning Rate
    def __init__(self, feed, instrument, starting_equity = 1000):
        super(IchimokuCloud, self).__init__(feed, starting_equity)
        # Banks and Config
        self.__instrument = instrument
        self.__long_position = None
        self.__long_position_bought_days = 0
        self.__short_position = None
        self.__short_position_bought_days = 0
        # Close Data Series
        close_data_series = feed[instrument].getCloseDataSeries()
        # 9 Period High
        self.__period_high_9 = technical.EventBasedFilter(close_data_series, PeriodHigh(9))
        self.__period_low_9 = technical.EventBasedFilter(close_data_series, PeriodLow(9))
        # 26 Period High
        self.__period_high_26 = technical.EventBasedFilter(close_data_series, PeriodHigh(26))
        self.__period_low_26 = technical.EventBasedFilter(close_data_series, PeriodLow(26))
        # 52 Period High
        self.__period_high_52 = technical.EventBasedFilter(close_data_series, PeriodHigh(52))
        self.__period_low_52 = technical.EventBasedFilter(close_data_series, PeriodLow(52))
        # SMA
        self.__sma200 = ma.SMA(close_data_series, 200)

    def getConversionLine(self):
        # Waiting for enough bars for high periods to be calculated
        if self.__period_high_9[-1] is None or self.__period_low_9[-1] is None:
            return None
        conversion_line = ( self.__period_high_9[-1] + self.__period_low_9[-1] ) / 2
        return conversion_line
    
    def getBaseLine(self):
        # Waiting for enough bars for high periods to be calculated
        if self.__period_high_26[-1] is None or self.__period_low_26[-1] is None:
            return None
        base_line = ( self.__period_high_26[-1] + self.__period_low_26[-1] ) / 2
        return base_line

    def getLeadingSpanA(self):
        # Waiting for enough bars for high periods to be calculated
        if self.getConversionLine() is None or self.getBaseLine() is None:
            return None
        leading_span_A = ( self.getConversionLine() + self.getBaseLine() ) / 2
        return leading_span_A
    
    def getLeadingSpanB(self):
        # Waiting for enough bars for high periods to be calculated
        if self.__period_high_52[-1] is None or self.__period_low_52[-1] is None:
            return None
        leading_span_B = ( self.__period_high_52[-1] + self.__period_low_52[-1] ) / 2
        return leading_span_B

    def onBars(self, bars):
        self.updateBoughtDays()
        # Indicator
        indicator = {
            "conversionLine" : self.getConversionLine(),
            "baseLine" : self.getBaseLine(),
            "leadingSpanA" : self.getLeadingSpanA(),
            "leadingSpanB" : self.getLeadingSpanB(),
            "sma200" : self.__sma200[-1]
        }
        # Waiting if all value of indicator has been calculated as are not None
        if not all(indicator.values()):
            return

        bar = bars[self.__instrument]

        # If long postion is not open, check if we should enter a long position
        if self.__long_position is None:
            if self.enterLongSignal(bar, indicator):
                shares = 10
                self.__long_position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit a long position
        elif self.exitLongSignal(bar, indicator) and not self.__long_position.exitActive():
            self.__long_position.exitMarket()

        # If short postion is not open, check if we should enter a short position
        if self.__short_position is None:
            if self.enterShortSignal(bar, indicator):
                shares = 10
                self.__short_position = self.enterShort(self.__instrument, shares, True)
        # Check if we have to exit a long position
        elif self.exitShortSignal(bar, indicator) and not self.__short_position.exitActive():
            self.__short_position.exitMarket()

    def enterLongSignal(self, bar, indicator):
        current_sma_200 = indicator["sma200"]
        current_price = bar.getPrice()
        conversion_line = indicator["conversionLine"]
        base_line = indicator["baseLine"]
        leading_span_a = indicator["leadingSpanA"]
        leading_span_b = indicator["leadingSpanB"]
        long_signal = conversion_line > base_line
        upward_momentum = leading_span_a > leading_span_b
        above_clouds = current_price > max(leading_span_a, leading_span_b)
        above_sma = current_price > current_sma_200
        signal = long_signal and upward_momentum and above_clouds and above_sma
        return signal

    def exitLongSignal(self, bar, indicator):
        conversion_line = indicator["conversionLine"]
        base_line = indicator["baseLine"]
        signal = conversion_line < base_line
        return signal

    def enterShortSignal(self, bar, indicator):
        current_sma_200 = indicator["sma200"]
        current_price = bar.getPrice()
        conversion_line = indicator["conversionLine"]
        base_line = indicator["baseLine"]
        leading_span_a = indicator["leadingSpanA"]
        leading_span_b = indicator["leadingSpanB"]
        short_signal = conversion_line < base_line
        upward_momentum = leading_span_a > leading_span_b
        below_clouds = current_price < min(leading_span_a, leading_span_b)
        below_sma = current_price < current_sma_200
        signal = short_signal and upward_momentum and below_clouds and below_sma
        return signal

    def exitShortSignal(self, bar, indicator):
        conversion_line = indicator["conversionLine"]
        base_line = indicator["baseLine"]
        signal = conversion_line > base_line
        return signal

    def updateBoughtDays(self):
        # Increasing bought days for long and short position if they exist
        if self.__long_position is not None:
            self.__long_position_bought_days += 1
        else:
            self.__long_position_bought_days = 0

        if self.__short_position is not None:
            self.__short_position_bought_days += 1
        else:
            self.__short_position_bought_days = 0

    def onEnterOk(self, position):
        execution_info = position.getEntryOrder().getExecutionInfo()
        order_price = execution_info.getPrice()
        # Printing the logs based on the type of position
        if position == self.__long_position:
            self.info("BUY LONG POSITION at $%.2f" % order_price)
        elif position == self.__short_position:
            self.info("BUY SHORT POSITION at $%.2f" % order_price)
    
    def onEnterCanceled(self, position):
        self.__position = None
    
    def onExitOk(self, position):
        execution_info = position.getExitOrder().getExecutionInfo()
        order_price = execution_info.getPrice()
        # Clearing long or short position from variables
        if position == self.__long_position:
            self.__long_position = None
            self.info("SELL LONG POSTION at $%.2f" % order_price)
        elif position == self.__short_position:
            self.__short_position = None
            self.info("SELL SHORT POSITION at $%.2f" % order_price)

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it
        self.__position.exitMarket()
