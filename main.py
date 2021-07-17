from typing import final
from pyalgotrade.barfeed import quandlfeed

from Strategies.pullback_strategies import LarryConnorPullbackStrategy

# Importing CSV as a bar feed
feed = quandlfeed.Feed()
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2000-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2001-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2002-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2003-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2004-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2005-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2006-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2007-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2008-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2009-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2010-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2011-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2012-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2013-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2014-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2015-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2016-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2017-quandl.csv")
feed.addBarsFromCSV("orcl", "Data/Orcl/WIKI-ORCL-2018-quandl.csv")

# Evaluating Strategy
starting_equity = 1000
strategy = LarryConnorPullbackStrategy(feed, "orcl", starting_equity)
strategy.run()
final_equity = strategy.getBroker().getEquity()

print('''
    2000 - 2018 (ORCL)
    -------------------------
    Starting Equity : %.2f
    Final Equity : %.2f
''' % (starting_equity, final_equity))