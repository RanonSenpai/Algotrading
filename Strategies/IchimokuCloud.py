from universal import PeriodHigh
from universal import PeriodLow
from pyalgotrade import technical
from pyalgotrade.technical import ma

class IchimokuCloud:
    def __init__(self, close_data_series) -> None:
        # 9, 26, 52 Period Highs and Period Lows 
        self.__period_high_low = {
            "high_9": technical.EventBasedFilter(close_data_series, PeriodHigh(9)),
            "low_9": technical.EventBasedFilter(close_data_series, PeriodLow(9)),
            "high_26": technical.EventBasedFilter(close_data_series, PeriodHigh(26)),
            "low_26": technical.EventBasedFilter(close_data_series, PeriodLow(26)),
            "high_52": technical.EventBasedFilter(close_data_series, PeriodHigh(52)),
            "low_52": technical.EventBasedFilter(close_data_series, PeriodLow(52))
        }
        # SMA
        self.__sma200 = ma.SMA(close_data_series, 200)

    def getIndicator(self):
        # Generating Indicator
        indicator = {
            "conversionLine" : self.getConversionLine(),
            "baseLine" : self.getBaseLine(),
            "leadingSpanA" : self.getLeadingSpanA(),
            "leadingSpanB" : self.getLeadingSpanB(),
            "sma200" : self.__sma200[-1]
        }
        return indicator

    def getConversionLine(self):
        # Waiting for all Period Highs and Period Lows to be calculated.
        if not all([ value[-1] for value in self.__period_high_low.values()]):
            return None
        # Calculating Conversion Line
        conversion_line = (self.__period_high_low["high_9"][-1] + self.__period_high_low["high_9"][-1]) / 2
        return conversion_line
    
    def getBaseLine(self):
        # Waiting for all Period Highs and Period Lows to be calculated.
        if not all([ value[-1] for value in self.__period_high_low.values()]):
            return None
        # Calculating Base Line
        base_line = (self.__period_high_low["high_26"][-1] + self.__period_high_low["low_26"][-1]) / 2
        return base_line

    def getLeadingSpanA(self):
        # Waiting for all Period Highs and Period Lows to be calculated.
        if not all([ value[-1] for value in self.__period_high_low.values()]):
            return None
        # Calclulating Leading Span A
        leading_span_A = (self.getConversionLine() + self.getBaseLine()) / 2
        return leading_span_A
    
    def getLeadingSpanB(self):
        # Waiting for all Period Highs and Period Lows to be calculated.
        if not all([ value[-1] for value in self.__period_high_low.values()]):
            return None
        # Calclulating Leading Span B
        leading_span_B = (self.__period_high_low["high_52"][-1] + self.__period_high_low["low_52"][-1] ) / 2
        return leading_span_B

    def enterLongSignal(self, bar):
        # Getting Indicator
        indicator = self.getIndicator()
        # Waiting for all indicators to be calculated
        if not all(indicator.values()):
            return None
        # Getting Indicator Lines
        current_price = bar.getPrice()
        # Conditions
        long_signal = indicator["conversionLine"] > indicator["baseLine"]
        upward_momentum = indicator["leadingSpanA"] > indicator["leadingSpanB"]
        above_clouds = current_price > max(indicator["leadingSpanA"], indicator["leadingSpanB"])
        above_sma = current_price > indicator["sma200"]
        # Validation
        signal = long_signal and upward_momentum and above_clouds and above_sma
        return signal

    def exitLongSignal(self, bar):
        # Getting Indicator
        indicator = self.getIndicator()
        # Waiting for all indicators to be calculated
        if not all(indicator.values()):
            return None
        # Conditions
        signal = indicator["conversionLine"] < indicator["baseLine"]
        return signal

    def enterShortSignal(self, bar):
        # Getting Indicator
        indicator = self.getIndicator()
        # Waiting for all indicators to be calculated
        if not all(indicator.values()):
            return None
        # Getting Indicators
        current_price = bar.getPrice()
        # Conditions
        short_signal = indicator["conversionLine"] < indicator["baseLine"]
        upward_momentum = indicator["leadingSpanA"] > indicator["leadingSpanB"]
        below_clouds = current_price < min(indicator["leadingSpanA"], indicator["leadingSpanB"])
        below_sma = current_price < indicator["sma200"]
        # Validation
        signal = short_signal and upward_momentum and below_clouds and below_sma
        return signal

    def exitShortSignal(self, bar):
        # Getting Indicator
        indicator = self.getIndicator()
        # Waiting for all indicators to be calculated
        if not all(indicator.values()):
            return None
        # Conditions
        signal = indicator["conversionLine"] > indicator["baseLine"]
        return signal