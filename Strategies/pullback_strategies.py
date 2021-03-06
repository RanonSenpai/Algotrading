from pyalgotrade import strategy
from pyalgotrade.strategy import position
from pyalgotrade.technical import rsi
from pyalgotrade.technical import ma

def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value

class LarryConnorPullbackStrategy(strategy.BacktestingStrategy):
    # This is a strategy with 88.89% Winning Rate
    def __init__(self, feed, instrument, starting_equity):
        super(LarryConnorPullbackStrategy, self).__init__(feed, starting_equity)
        # Banks and Config
        self.__instrument = instrument
        self.__long_position = None
        self.__long_position_bought_days = 0
        self.__short_position = None
        self.__short_position_bought_days = 0
        # Indicators
        close_data_series = feed[instrument].getCloseDataSeries()
        self.__rsi10 = rsi.RSI(close_data_series, 10)
        self.__sma200 = ma.SMA(close_data_series, 200)

    def enterLongSignal(self, bar):
        current_rsi_10 = safe_round(self.__rsi10[-1], 2)
        current_sma_200 = safe_round(self.__sma200[-1], 2)
        current_price = bar.getPrice()
        signal = current_rsi_10 < 30 and current_price > current_sma_200
        return signal

    def exitLongSignal(self, bar):
        current_rsi_10 = safe_round(self.__rsi10[-1], 2)
        signal = current_rsi_10 > 40 or self.__long_position_bought_days >= 10
        return signal

    def enterShortSignal(self, bar):
        current_rsi_10 = safe_round(self.__rsi10[-1], 2)
        current_sma_200 = safe_round(self.__sma200[-1], 2)
        current_price = bar.getPrice()
        signal = current_rsi_10 > 40 and current_price > current_sma_200
        return signal

    def exitShortSignal(self, bar):
        current_rsi_10 = safe_round(self.__rsi10[-1], 2)
        signal = current_rsi_10 < 30 or self.__long_position_bought_days >= 10
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

    def onBars(self, bars):
        self.updateBoughtDays()
        # Waiting for enough bars to calculate RSI 10 and SMA 200
        if self.__rsi10[-1] is None or self.__sma200[-1] is None:
            return
        bar = bars[self.__instrument]

        # If long postion is not open, check if we should enter a long position
        if self.__long_position is None:
            if self.enterLongSignal(bar):
                shares = 10
                self.__long_position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit a long position
        elif self.exitLongSignal(bar) and not self.__long_position.exitActive():
            self.__long_position.exitMarket()

        # If short postion is not open, check if we should enter a short position
        if self.__short_position is None:
            if self.enterShortSignal(bar):
                shares = 10
                self.__short_position = self.enterShort(self.__instrument, shares, True)
        # Check if we have to exit a long position
        elif self.exitShortSignal(bar) and not self.__short_position.exitActive():
            self.__short_position.exitMarket()

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