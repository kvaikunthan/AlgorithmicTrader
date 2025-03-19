import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8')

class BackTester:
    def __init__(self, ticker, strategy, start='2000-01-01', end='2025-01-01'):
        self.ticker = ticker
        self.strategy = strategy
        self.start = start
        self.end = end

        self.tested = False

        self.data = yf.download(ticker, start=start, end=end).Close.copy()
        self.data['B&H return'] = np.log(self.data[self.ticker] / self.data[self.ticker].shift())
        self.data.dropna(inplace=True)
    
    def test(self):
        # Determining positions
        self.data['Strategy return'] = self.data['B&H return'] * self.strategy(self.data[self.ticker])

        logReturns = self.data[['B&H return', 'Strategy return']]

        # Calculating all statistics
        self.totalLogReturn = logReturns.sum()
        self.totalDollarReturn = self.totalLogReturn.apply(np.exp)
        self.risks = logReturns.std() * np.sqrt(252) * 100
        self.cumReturns = logReturns.cumsum().apply(np.exp)
        self.drawdowns = self.cumReturns.cummax() - self.cumReturns
        self.drawdownsPct = self.drawdowns / self.cumReturns.cummax() * 100

        self.tested = True

        return self
    
    def checkTested(self):
        if not self.tested:
            raise Exception('Must test strategy first using self.test()')

    
    def displayStats(self):
        self.checkTested()

        print(f'Dollar Returns for B&H: ${self.totalDollarReturn.iloc[0]:.2f} per dollar invested') 
        print(f'Dollar Returns for strategy: ${self.totalDollarReturn.iloc[1]:.2f} per dollar invested')

        print(f'Risk (standard deviation) for B&H: {self.risks.iloc[0]:.2f}%')
        print(f'Risk (standard deviation) for strategy: {self.risks.iloc[1]:.2f}%')

        maxDrawdowns = self.drawdownsPct.max()
        print(f'Maximum Drawdowns Percentage for B&H: {maxDrawdowns.iloc[0]:.2f}%')
        print(f'Maximum Drawdowns Percentage for strategy: {maxDrawdowns.iloc[1]:.2f}%')
        
    def plotReturns(self, start=None, end=None):
        self.checkTested()
        if start is None:
            start = self.start
        if end is None:
            end = self.end

        self.cumReturns.loc[start:end,].plot(figsize=(10,6), title='Cumulative returns - B&H | Tested Strategy')
        plt.legend(fontsize=10)
        plt.ylabel('Dollar return per dollar invested')
        plt.show()
