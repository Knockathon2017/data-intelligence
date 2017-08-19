from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

class AnalysisPlugin(WillPlugin):
	def __init__(self):
		self.HOST = 'localhost'
		self.PORT = 27017
		self.DB = 'ExzeoSmartUnderWriting'
		self.hci_col = ''
	
	def set_host(self, host_name):
		self.HOST = host_name
	
	def set_port(self, port_no):
		self.PORT = port_no 
	
	def set_db(self, db_name):
		self.DB = db_name

	def connect(self):
		from pymongo import MongoClient
		client = MongoClient(self.HOST,self.PORT)
		db = client[self.DB]
		return db

	@respond_to("award (?P<num_stars>\d)+ gold stars? to (?P<mention_name>.*)")
	def gold_stars(self, message, num_stars=1, mention_name=None):
		self.reply(message,"%s stars awarded to %s"%(str(num_stars),mention_name))

	@respond_to("connect to host (?P<host_name>[a-zA-Z]+)")
	def get_host_from_query(self, message, host_name='localhost'):
		try:
			self.set_host(host_name)
			self.reply(message,"connecting to %s"%(str(host_name)))
			self.reply(message,"Connected")
		except Exception as e:
			self.reply(message,str(e))

	@respond_to("connect to port (?P<port_no>\d+)")
	def get_port_from_query(self, message, port_no=27017):
		try:
			self.set_port(int(port_no))
			self.reply(message,"connecting to %s"%(str(port_no)))
			self.reply(message,"Connected")
		except Exception as e:
			self.reply(message,str(e))

	@respond_to("connect to db (?P<db_name>[a-zA-Z]+)")
	def get_db_from_query(self, message, db_name):
		try:
			self.set_db(db_name)
			self.reply(message,"connecting to %s"%(db_name))
			db_object = self.connect()
			if db_object:
				self.DB = db_object
				self.reply(message,str(db_object))
				self.reply(message,"All set!")
				self.reply(message,"which collection to look?")
			else:
				self.reply("Currently unable to connect")
		except Exception as e:
			self.reply(message,str(e))

	# analyse\s[a-zA-Z]+\sdataset
	# @respond_to(".* analyse (?P<dataset_name>.*)+ dataset? .*")
	@respond_to("collection (?P<col_name>[a-zA-Z]+)")
	def get_col_from_query(self, message, col_name='hci'):
		self.hci_col = self.DB[col_name]
		self.reply(message,str(self.hci_col))

	@respond_to("analyse\s(?P<dataset_name>[a-zA-Z]+)\sdataset?")
	def analyse_query_reponse(self, message, dataset_name=None):
		self.reply(message, "Will is analysing %s" %dataset_name)
		self.reply(message, "Please give Will some time to analyse %s dataset" %dataset_name)

	@respond_to("list of states that HCI expanded")
	def get_first_query_response(self, message):
		self.reply(message,"Sure, Give Titan some time")
		return self.reply(message,str(self.hci_col.find_one()))

	@respond_to("can you visualize")
	def get_second_query_response(self, message):
		self.reply(message,"Sure, which template")

	@respond_to("3d network")
	def get_first_vis(self, message):
		self.reply(message,"https://news.ycombinator.com/news")

	@respond_to("can you visualize 2d map")
	def get_second_vis(self, message):
		self.reply(message,"https://news.ycombinator.com/news")

	@respond_to("can you also visualize globe")
	def get_second_vis(self, message):
		self.reply(message,"https://news.ycombinator.com/news")