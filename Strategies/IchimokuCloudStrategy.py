from pyalgotrade.technical import ma

# Importing Indicators
from Indicators.IchimokuCloud import IchimokuCloud

class IchimokuCloudStrategy:
    def __init__(self, close_data_series) -> None:
        # Indicators
        self.__sma200 = ma.SMA(close_data_series, 200)
        self.__ichimoku_cloud = IchimokuCloud(close_data_series)

    # Checks if all indicators and prerequisites have been calculated
    def isReady(self):
        # Getting Indicator
        indicator = self.__ichimoku_cloud.getIndicator()
        # Checking
        is_indicators_calculated = all(indicator.values())
        is_sma200_calculated = self.__sma200[-1] is not None
        # Validating
        is_ready = is_indicators_calculated and is_sma200_calculated
        return is_ready

    def enterLongSignal(self, bar):
        # Getting Indicator
        indicator = self.__ichimoku_cloud.getIndicator()
        # Waiting for all indicators to be calculated and SMA 200 to be calculated
        if not self.isReady():
            return None
        # Getting Current Price
        current_price = bar.getPrice()
        # Conditions
        long_signal = indicator["conversionLine"] > indicator["baseLine"]
        upward_momentum = indicator["leadingSpanA"] > indicator["leadingSpanB"]
        above_clouds = current_price > max(indicator["leadingSpanA"], indicator["leadingSpanB"])
        above_sma = current_price > self.__sma200[-1]
        # Validation
        signal = long_signal and upward_momentum and above_clouds and above_sma
        return signal

    def exitLongSignal(self, bar):
        # Getting Indicator
        indicator = self.__ichimoku_cloud.getIndicator()
        # Waiting for all indicators to be calculated and SMA 200 to be calculated
        if not self.isReady():
            return None
        # Conditions
        signal = indicator["conversionLine"] < indicator["baseLine"]
        return signal

    def enterShortSignal(self, bar):
        # Getting Indicator
        indicator = self.__ichimoku_cloud.getIndicator()
        # Waiting for all indicators to be calculated and SMA 200 to be calculated
        if not self.isReady():
            return None
        # Getting Current Price
        current_price = bar.getPrice()
        # Conditions
        short_signal = indicator["conversionLine"] < indicator["baseLine"]
        downward_momentum = indicator["leadingSpanA"] < indicator["leadingSpanB"]
        below_clouds = current_price < min(indicator["leadingSpanA"], indicator["leadingSpanB"])
        below_sma = current_price < self.__sma200[-1]
        # Validation
        signal = short_signal and downward_momentum and below_clouds and below_sma
        return signal

    def exitShortSignal(self, bar):
        # Getting Indicator
        indicator = self.__ichimoku_cloud.getIndicator()
        # Waiting for all indicators to be calculated and SMA 200 to be calculated
        if not self.isReady():
            return None
        # Conditions
        signal = indicator["conversionLine"] > indicator["baseLine"]
        return signal