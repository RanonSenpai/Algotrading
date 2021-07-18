from pyalgotrade import plotter
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.stratanalyzer import returns
from Strategies.pullback_strategies import LarryConnorPullbackStrategy

# Load the bar feed from the CSV file
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

# Evaluate the strategy with the feed's bars.
starting_equity = 1000
myStrategy = LarryConnorPullbackStrategy(feed, "msft", starting_equity)

# Attach a returns analyzers to the strategy.
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)

# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(myStrategy)
# Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
# plt.getInstrumentSubplot("msft").addDataSeries("SMA", myStrategy.getSMA())
# Plot the simple returns on each bar.
plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

# Run the strategy.
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

# Plot the strategy.
plt.plot()