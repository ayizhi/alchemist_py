#coding utf-8

from abc import ABCMeta,abstractmethod
import datetime
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message

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
		print("Server Error: %s" % msg)


	def _reply_handler(self,msg):
		#Handler open order orderId processing
		if msg.typeName == "openOrder" and msg.orderId == msg.orderId and not self.fill_dict.has_key(msg.orderId):
			self.create_fill_dict_entry(msg)

		#Handle Fills
		if msg.typeName == "orderStatus" and msg.status == "Filled" and self.fill_dict[msg.orderId]['filled'] == False:
			self.create_fill(msg)

		print("Server Response: %s , %s\n" % (msg.typeName,msg))

	def create_tws_connection(self):
		"""
        Connect to the Trader Workstation (TWS) running on the
        usual port of 7496, with a clientId of 100.
        The clientId is chosen by us and we will need
        separate IDs for both the execution connection and
        market data connection, if the latter is used elsewhere.
        """
		tws_conn = ibConnection()
		tws_conn.connect()
		return tws_conn

	def create_initial_order_id(self):
		# There is scope for more logic here, but we
        # will use "1" as the default for now.
		return 1

	def register_handlers(self):
		self.tws_conn.register(self._error_handler, "Error")
		self.tws_conn.registerAll(self._reply_handler)

	def create_contract(self, symbol, sec_type, exch, prim_exch, curr):
		contract = Contract()
		contract.m_symbol = symbol
		contract.m_secType = sec_type
		contract.m_exchange = exch
		contract.m_primaryExch = prim_exch
		contract.m_currency = curr
		return contract

	def create_order(self, order_type, quantity, action):
		order = Order()
		order.m_orderType = order_type
		order.m_totalQuantity = quantity
		order.m_action = action
		return order

	def create_fill_dict_entry(self,msg):
		self.fill_dict[msg.orderId] = {
			'symbol': msg.contract.m_symbol,
			'exchange': msg.contract.m_exchange,
			'direction': msg.order.m_action,
			'filled': False
		}

	def create_fill(self,msg):
		fd = self.fill_dict[msg.orderId]

		symbol = fd['symbol']
		exchange = fd['exchange']
		filled = msg.filled
		direction = fd['direction']
		fill_cost = msg.avgFillprice

		fill = FillEvent(
			datetime.datetime.utcnow(), symbol, exchange, filled, direction, fill_cost
			)
		self.fill_dict[msg.orderId]['filled'] = True
		self.events.put(fill_event)

	def execute_order(self,event):
		if event.type == 'ORDER':
			asset = event.symbol
			asset_type = "STK"
			order_type = event.order_type
			quantity = event.quantity
			direction = event.direction

			ib_contract = self.create_contract(asset, asset_type, self.order_routing, self.order_routing, self.currency)

			ib_order = self.create_order(order_type,quantity, direction)

			self.tws_conn.placeOrder(
				self.order_id, ib_contract, ib_order)

			time.sleep(1)
			self.order_id += 1
