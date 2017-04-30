#coding: utf-8

class Event(object):
	pass

class MarketEvent(Event):
	def __init__(self):
		self.type = "MARKET"

class SignalEvent(Event):
	"""
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """
	def __init__(self,strategy_id,symbol,datetime,signal_type,strength):
		self.strategy_id = strategy_id
		self.type = 'SIGNAL'
		self.symbol = symbol
		self.datetime = datetime
		self.signal_type = signal_type
		self.strength = strength

class OrderEvent(Event):
	def __init__(self,symbol,order_type,quantity,direction):
	"""
	Parameters:
        symbol - The instrument to trade.
        order_type - 'MKT' or 'LMT' for Market or Limit.
        quantity - Non-negative integer for quantity.
        direction - 'BUY' or 'SELL' for long or short.
    """
		self.type = "ORDER"
		self.symbol	= symbol
		self.order_type  = order_type
		self.quantity = quantity
		self.direction = direction

	def print_order(self):
		print ("Order: Symbol=%s, Type=%s, Quantity=%s,Direction=%s") % (self.symbol,self.order_type,self.quantity,self.direction)

class FillEvent(Event):
	def __init__(self,timeindex,symbol,exchange,quantity,direction,fill_cost,commisson=None):
			"""
	Parameters:
        timeindex - The bar-resolution when the order was filled.
        symbol - The instrument which was filled.
        exchange - The exchange where the order was filled.
        quantity - The filled quantity.
        direction - The direction of fill ('BUY' or 'SELL')
        fill_cost - The holdings value in dollars.
        commission - An optional commission sent from IB.
    """
   		self.type = "FILL"
   		self.timeindex = timeindex
   		self.symbol = symbol
   		self.exchange = exchange
   		self.quantity = quantity
   		self.direction = direction
   		self.fill_cost = fill_cost

   		#calculate the commission
   		if commisson is None:
   			self.commisson = self.calculate_ib_commission()
   		else self.commisson = commisson

   	def calculate_ib_commission(self):
   		full_cost = 1.3
   		if self.quantity <= 500:
   			full_cost = max(1.3, 0.013 * self.quantity)
   		else:
   			full_cost = max(1.3,0.013 * self.quantity)

   		return full_cost
