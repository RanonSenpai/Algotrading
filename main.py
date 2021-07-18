from typing import final
from pyalgotrade.barfeed import quandlfeed

from Strategies.pullback_strategies import LarryConnorPullbackStrategy

# Importing CSV as a bar feed
feed = quandlfeed.Feed()
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2000-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2001-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2002-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2003-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2004-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2005-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2006-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2007-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2008-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2009-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2010-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2011-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2012-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2013-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2014-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2015-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2016-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2017-quandl.csv")
feed.addBarsFromCSV("msft", "Data/Msft/WIKI-Msft-2018-quandl.csv")

# Evaluating Strategy
starting_equity = 1000
strategy = LarryConnorPullbackStrategy(feed, "msft", starting_equity)
strategy.run()
final_equity = strategy.getBroker().getEquity()

print('''
    2000 - 2018 (MSFT)
    -------------------------
    Starting Equity : %.2f
    Final Equity : %.2f
''' % (starting_equity, final_equity))