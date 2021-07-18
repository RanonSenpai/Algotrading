# A organised class system for a Bank
class Bank:
    positions = {
        "long": None,
        "short": None,
        "long_bought_days": 0,
        "short_bought_days": 0
    }

    def getPositions(self):
        return self.positions
    
    def setLongPosition(self, value):
        self.positions["long"] = value
        return True
    
    def setShortPosition(self, value):
        self.positions["short"] = value

    def increaseLongBoughtDays(self):
        self.positions["long_bought_days"] += 1
    
    def increaseShortBoughtDays(self):
        self.positions["short_bought_days"] += 1