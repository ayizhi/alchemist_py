#coding utf-8

from abc import ABCMeta,abstractmethod
import datetime

try:
	import Queue as queue
except ImportError:
	import queue

from event import FillEvent,OrderEvent


class ExecutionHandler(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def execute_order(self,event):
		raise NotImplementedError("Should implement execute_order()")

class SimulatedExecutionHandler(ExecutionHandler):
	def __init__(self,events):
		"""
		Parameters:
		events - The Queue of Event objects.
		"""
		self.events = events

	def execute_order(self,event):
		if event.type == "ORDER":
			fill_event = FillEvent(datetime.datetime.utcnow(), event.symbol, 'ABCA', event.quantity, event.direction, None)
			self.events.put(fill_event)

