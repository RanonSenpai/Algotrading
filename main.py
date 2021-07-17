from pyalgotrade.barfeed import quandlfeed

from Strategies.pullback_strategies import LarryConnorPullbackStrategy

# Importing CSV as a bar feed
feed = quandlfeed.Feed()
feed.addBarsFromCSV("orcl", "Data/WIKI-ORCL-2000-quandl.csv")

# Evaluating Strategy
capital = 1000
strategy = LarryConnorPullbackStrategy(feed, "orcl", capital)
strategy.run()
