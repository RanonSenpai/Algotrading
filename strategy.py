from pyalgotrade import strategy
from pyalgotrade.strategy import position

# Importing Strategies and Banks
from bank import Bank
from Strategies.IchimokuCloudStrategy import IchimokuCloudStrategy

# Strategy Compiler
class Strategy(strategy.BacktestingStrategy):

    def __init__(self, feed, instrument, starting_equity):
        super(Strategy, self).__init__(feed, starting_equity)
        # Banks and Config
        self.__instrument = instrument
        self.__bank = Bank()
        
        # Strategies
        close_data_series = feed[instrument].getCloseDataSeries()
        self.__ichimioku_cloud = IchimokuCloudStrategy(close_data_series)

    def onBars(self, bars):
        bar = bars[self.__instrument]
        bank_positions_snapshot = self.__bank.getPositions()

        # Checking if long position is not open
        if bank_positions_snapshot["long"] is None:
            # Checking for a Long Signal
            if self.__ichimioku_cloud.enterLongSignal(bar):
                shares = 10
                self.__bank.setLongPosition(self.enterLong(self.__instrument, shares, True))
        # Checking for a exit signal, if long position exist in inventory
        elif self.__ichimioku_cloud.exitLongSignal(bar) and not bank_positions_snapshot["long"].exitActive():
            bank_positions_snapshot["long"].exitMarket()

        # Checking if long position is not open
        if  bank_positions_snapshot["short"] is None:
            # Checking for a Long Signal
            if self.__ichimioku_cloud.enterShortSignal(bar):
                shares = 10
                self.__bank.setShortPosition(self.enterShort(self.__instrument, shares, True))
        # Checking for a exit signal, if long position exist in inventory
        elif  self.__ichimioku_cloud.exitShortSignal(bar) and not bank_positions_snapshot["short"].exitActive():
            bank_positions_snapshot["short"].exitMarket()

    def onEnterOk(self, position):
        execution_info = position.getEntryOrder().getExecutionInfo()
        order_price = execution_info.getPrice()
        bank_positions_snapshot = self.__bank.getPositions()
        # Printing the logs based on the type of position
        if position == bank_positions_snapshot["long"]:
            self.info("BUY LONG POSITION at $%.2f" % order_price)
        elif position == bank_positions_snapshot["short"]:
            self.info("BUY SHORT POSITION at $%.2f" % order_price)
    
    def onEnterCanceled(self, position):
        bank_positions_snapshot = self.__bank.getPositions()
        # Clearing long or short position from variables
        if position == bank_positions_snapshot["long"]:
            self.__bank.setLongPosition(None)
        elif position == bank_positions_snapshot["short"]:
            self.__bank.setShortPosition(None)
    
    def onExitOk(self, position):
        execution_info = position.getExitOrder().getExecutionInfo()
        order_price = execution_info.getPrice()
        bank_positions_snapshot = self.__bank.getPositions()
        # Clearing long or short position from variables
        if position == bank_positions_snapshot["long"]:
            self.__bank.setLongPosition(None)
            self.info("SELL LONG POSTION at $%.2f" % order_price)
        elif position == bank_positions_snapshot["short"]:
            self.__bank.setShortPosition(None)
            self.info("SELL SHORT POSITION at $%.2f" % order_price)

    # If the exit was canceled, re-submit it
    def onExitCanceled(self, position):
        bank_positions_snapshot = self.__bank.getPositions()
        # Clearing long or short position from variables
        if position == bank_positions_snapshot["long"]:
            bank_positions_snapshot["long"].exitMarket()
        elif position == bank_positions_snapshot["short"]:
            bank_positions_snapshot["short"].exitMarket()