#coding: utf-8
import numpy as np
import pandas as pd


def create_sharpe_ratio(returns,periods=252):
    return np.sqrt(periods) * (np.mean(returns))/np.std(returns)


def create_drawdowns(pnl):
    hwm = [0]

    #create the drawdown and duration series
    idx = pnl.index
    drawdown = pd.Series(index = idx)
    duration = pd.Series(index = idx)

    #loop
    for i in range(1,len(idx)):
        hwm.append(max(hwm[i - 1],pnl[i]))
        drawdown[i] = (hwm[i] - pnl[i])
        duration[i] = (0 if drawdown[t] == 0 else duration[i - 1] + 1)
    return drawdown,drawdown.max(),duration.max()

