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

class IBExecutionHandler(ExecutionHandler):
	def __init__(
		self, events, order_routing="SMART", currency="USD"):
		self.events = events
		self.order_routing = order_routing
		self.currency = currency
		self.fill_dict = {}

		self.tws_conn = self.create_tws_connection()
		self.order_id = self.create_initial_order_id()
		self.register_handlers()


	def _error_handler(self, msg):
		if msg.typeName == "openOrder" and msg.orderId == self.order_id and not self.fill_dict.has_key(msg.orderId):
			self.create_fill_dict_entry(msg)