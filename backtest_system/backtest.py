#coding: utf-8

from __future__ import print_function

import datetime
import pprint
try:
    import Queue as queue
except ImportError:
    import queue
import time


class Backtest(object):
    def __init__(
        self,symbol_list,initial_capital,
        heartbeat,start_date,data_handler,execution_handler,portfolio,
        strategy
        ):
        """
        Initialises the backtest.

        Parameters:
        csv_dir - The hard root to the CSV data directory.
        symbol_list - The list of symbol strings.
        intial_capital - The starting capital for the portfolio.
        heartbeat - Backtest "heartbeat" in seconds
        start_date - The start datetime of the strategy.
        data_handler - (Class) Handles the market data feed.
        execution_handler - (Class) Handles the orders/fills for trades.
        portfolio - (Class) Keeps track of portfolio current and prior positions.
        strategy - (Class) Generates signals based on market data.
        """
        self.symbol_list = symbol_list
        self.initial_capital = initial_capital
        self.heartbeat = heartbeat
        self.start_date = start_date

        self.data_handler_db = data_handler
        self.execution_handler_db = execution_handler
        self.portfolio_db = portfolio
        self.strategy_db = strategy

        self.events = queue.Queue()

        self.signals = 0
        self.orders = 0
        self.fills = 0
        self.num_strats = 1

        self._generate_trading_instances()

    def _generate_trading_instances(self):
        print("Creating DataHandler, Strategy, Portfolio and ExecutionHandler")
        self.data_handler = self.data_handler_db(self.events, self.symbol_list)
        self.strategy = self.strategy_db(self.data_handler, self.events)
        self.portfolio = self.portfolio_db(self.data_handler, self.events, self.start_date, self.initial_capital)
        self.execution_handler = self.execution_handler_db(self.events)

    def _run_backtest(self):
        i = 0
        while True:
            i += 1
            print(i)
            if self.data_handler.continue_backtest == True:
                self.data_handler.update_bars()
            else:
                break

            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == 'MARKET':
                            self.strategy.calculate_signals(event)
                            self.portfolio.update_timeindex(event)

                        elif event.type == 'SIGNAL':
                            self.signals += 1
                            self.portfolio.update_signal(event)

                        elif event.type == 'ORDER':
                            self.orders += 1
                            self.execution_handler.execute_order(event)

                        elif event.type == 'FILL':
                            self.fills += 1
                            self.portfolio.update_fill(event)

            time.sleep(self.heartbeat)

    def _output_performance(self):
        self.portfolio.create_equity_curve_dataframe()

        print('Creating summary stats...')
        stats = self.portfolio.output_summary_stats()

        print("Creating equity curve...")
        print(self.portfolio.equity_curve.tail(10))

        pprint.pprint(stats)

        print("Signals: %s" % self.signals)
        print("Orders: %s" % self.orders)
        print("Fills: %s" % self.fills)

    def simulate_trading(self):
        self._run_backtest()
        self._output_performance()
