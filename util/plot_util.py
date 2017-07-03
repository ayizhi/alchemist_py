#coding: utf-8
#数据工具库

import pandas as pd
import numpy as np
import pyqtgraph as pg
import pyqtgraph.examples
from pyqtgraph.Qt import QtGui
import matplotlib.pyplot as plt



class Plot_util(object):
    def __init__(self):
        self.win = pg.GraphicsWindow()
        self.win.resize(1000,600)

    def plot_line(self,np_normal):
        pg = self.win.addPlot(title="plot a line")
        pg.plot(np_normal,pen=(255,0,0))
        QtGui.QApplication.exec_()

    def plot_point(self,np_normal):
        pg = self.win.addPlot(title="plot points")
        pg.plot(np_normal,pen=(200,200,200), symbolBrush=(255,255,0), symbolPen='w')
        QtGui.QApplication.exec_()

    def plot_k(self,np_normal,np_short,np_middle,np_long,title):
        pg = self.win.addPlot(title="Multiple curves")
        pg.plot(np_normal, pen='w', name="normal")
        pg.plot(np_short, pen=(255,0,0), name="short")
        pg.plot(np_middle,pen=(0,255,0), name="middle")
        pg.plot(np_long,pen=(0,0,255),name="long")
        QtGui.QApplication.exec_()

    def plot_learning_curve(self,estimator,title,X,y,ylim=None,cv=None,n_jobs=1,train_sizes=np.linspace(0.05,1,20),verbose=0,plot=True):
        train_sizes,train_scores,test_scores = learning_curve(estimator,X,y,cv=cv,n_jobs=n_jobs,train_sizes=train_sizes,verbose=verbose)
        train_scores_mean = np.mean(train_scores,axis=1)
        train_scores_std = np.std(train_scores,axis=1)
        test_scores_mean = np.mean(test_scores,axis=1)
        test_scores_std = np.std(test_scores,axis=1)


        if plot:
            plt.figure()
            plt.title(title)
            if ylim is not None:
                plt.ylim(*ylim)
            plt.xlabel('symbol num')
            plt.ylabel('score')
            # plt.gca().invert_yaxis()
            plt.grid()

            plt.fill_between(train_sizes,test_scores_mean - test_scores_std,test_scores_mean + test_scores_std, alpha=0.1,color='r')
            plt.fill_between(train_sizes,train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1,color='b')

            plt.plot(train_sizes, train_scores_mean, 'o-',color='b',label=u'score on train_data')
            plt.plot(train_sizes, test_scores_mean, 'o-',color="r",label=u'score on cross validation')
            plt.legend(loc="best")
            plt.draw()
            plt.show()
            plt.gca().invert_yaxis()

        midpoint = ((train_scores_mean[-1] + train_scores_std[-1]) + (test_scores_mean[-1] - test_scores_std[-1]))/2
        diff = (train_scores_mean[-1] + train_scores_std[-1]) - (test_scores_mean[-1] - test_scores_std[-1])
        return midpoint, diff



# plt = PlotUtil()
# plt.plot()

# pyqtgraph.examples.run()