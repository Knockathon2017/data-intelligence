import collections
import math
import csv

class Get:
	''' 	
	Funtion to return all documents from a collection

	params:
	collname: name of the collection 
	'''
	def get_documents(self, db, collname):
		return db[collname].find()

class EDA:
	def __init__(self, missing_types = [None, "NA", "N/A", "Null", "None", "", "NULL"]):
		self.missing_types = missing_types

	def check_data_type(self, var):
		''' 
		Variable Identification - Data Type 
		Function to detect the variable type
		'''
		if type(var) == float:
			return "Double"
		elif type(var) == int:
			return "Integer"
		elif type(var) == str:
			return "String"
		elif var.isdigit():
			return "Integer"
		elif var.isalnum():
			return "Alphanumeric"
		else:
			return type(var)

	def identify_variable_type(self, key, db, collname):
		'''
		Variable Identification - Continuous or Categorical
		'''
		distinct_count = self.get_distinct_count(key,db,collname)
		total_count = self.get_total_count(key,db,collname)
		ratio_unique = round((float(distinct_count) / total_count) * 100,2)
		# print ratio_unique
		if ratio_unique < 5.0:
			return "Categorical"
		else:
			return "Continuous"

	def univariate_analysis(self, key, db, collname, limit = False, sorting_order = "DESC", central_tendencies = True):
		''' 
		Variable Analysis - Univariate 

		Function to perform univariate analysis on a variable. Works directly for Categorical Variables. For Continuous
		Variables, one can use binning function first before univariate analysis. 

		params:
		key: Name of the key (variable) 
		collname: Name of the collection which contains the documents
		limit: Number of documents / rows to be analysed, Default is False (all documents)
		sorting_order: Arranging the results in asending or descending order (ASEC or DESC)
		central_tendencies: Boolean, True if you want to include mean, median and mode in the results
		'''

		sorter = -1
		if sorting_order != "DESC":
			sorter = 1

		if central_tendencies:
			pipe = [{'$group' : {'_id' : key, 'sum' : {'$sum':'$'+key}, 'mean':{'$avg':'$'+key},\
					'min':{'$min':'$'+key}, 'max':{'$max':'$'+key}}},{'$sort':{'sum':sorter}}]
		else:
			pipe = [{'$group' : {'_id' : '$'+key, 'freq' : {'$sum':1}}},
					{'$sort':{'sum':sorter}}]
		if limit:
			pipe.append({'$limit':limit})

		res = db[collname].aggregate(pipe)
		res = self.cursor_to_list(res)
		return res

	def get_distinct(self, key, db, collname):
		return db[collname].distinct(key)

	def get_distinct_count(self, key, db, collname):
		return len(self.get_distinct(key,db,collname))

	def get_total_count(self, key, db, collname):
		return db[collname].find().count()

	def cursor_to_list(self, cursor):
		return 	[_ for _ in cursor]

	''' Get Missing Count '''
	def getMissingCount(self, key, db, collname, missing_type):
		if type(missing_type) == list:
			count = 0
			for miss_type in missing_type:
				count += db[collname].find({key:missing_type}).count()
			return count
		else:
			return db[collname].find({key:missing_type}).count()

	# Complete This Function
	def get_outliers(self, key, db, collname, thresholds = [0.05,0.95]):
		key_docs = self.get_all_values(key,db,collname)
		q1 = self.get_pth_quantile(key_docs,thresholds[0])
		q2 = self.get_pth_quantile(key_docs,thresholds[1])
		std_dev_away = self.get_std_dev_away(key,db,collname,key_docs)
		print q1,q2,key_docs
		if (any(not((q1 < val) and (val < q2)) for val in key_docs)) and std_dev_away:
			return True
		return False
	
	def get_pth_quantile(self, x, p):
		p_index = int(p * len(x))
		return sorted(x)[p_index]
	
	def get_std_dev_away(self, key, db, collname, datapoints):
		std_dev = self.get_std_dev(key,db,collname)
		mean = self.get_mean(key,db,collname)
		boundary = mean + 3 * abs(std_dev)
		if all((point <= boundary for point in datapoints)):
			return False
		return True

	def get_all_values(self, key, db, collname):
		'''
			get all values of a column
			
			params:
			key : column name
			collname : collection name
		'''
		docs = self.cursor_to_list(Get().get_documents(db,collname))
		docs = [doc[key] for doc in docs]
		return docs

	def get_mean(self, key, db, collname):
		list_dict = self.get_all_values(key,db,collname)
		pipe = [{'$group' : {'_id' : key, 'mean':{'$avg':'$'+key}}}]
		mean = db[collname].aggregate(pipe)
		mean = self.cursor_to_list(mean)
		mean = mean[0]['mean']
		print 'mean',mean
		return mean

	def de_mean(self, key, db, collname):
		'''
			function to return the difference of list values and their mean
		'''
		list_dict = self.get_all_values(key,db,collname)
		mean = self.get_mean(key,db,collname)
		# print [each for each in list_dict]
		return [(each-mean) for each in list_dict]

	def dot(self, list1, list2):
		'''
			dot product of two vectors
		'''
		return sum([ u*v for u,v in zip(list1,list2)])

	def get_std_dev(self, key, db, collname):
		'''
			function to return  the standard deviation for a key
		'''
		pipe = [{'$group':{'_id' :key, 'keyStdDev': { '$stdDevSamp': '$'+key }}}]
		std_dev=self.cursor_to_list(db[collname].aggregate(pipe))[0]['keyStdDev']
		return std_dev
	
# 	def bivariate_analysis(self, key1, key2, db, collname, limit = False, sorting_order = "DESC"):
# 		''' 
# 		Variable Analysis - BiVariate 

# 		Function to perform bivariate analysis on a variable. 

# 		params:
# 		key1: Name of the key1 (variable)
# 		key2: Name of the key2 (variable) 
# 		collname: Name of the collection which contains the documents
# 		limit: Number of documents / rows to be analysed, Default is False (all documents)
# 		sorting_order: Arranging the results in asending or descending order (ASEC or DESC)
# 		'''
# 		type_key1 = self.identify_variable_type(key1,db,collname)
# 		type_key2 = self.identify_variable_type(key2,db,collname)
# 		if type_key1 == 'Continuous' and type_key2 == 'Continuous':
# 			std_dev_key1=self.get_std_dev(key1,db,collname)
# 			std_dev_key2=self.get_std_dev(key2,db,collname)
# 			freq=db[collname].find().count()
# 			cov_key1_key2=self.dot(self.de_mean(key1,db,collname),self.de_mean(key2,db,collname))/(freq-1)
# 			return cov_key1_key2/(std_dev_key1)/(std_dev_key2)
# 		elif key1 == 'Categorical' and key2 == 'Categorical':
# 			pass
# 		else:
			
#  		sorter = -1
# 		if sorting_order != "DESC":
# 			sorter = 1

# 		# pipe = [{'$group' : {'_id' : {'key1':'$'+key1,'key2':'$'+key2}, 'sum' : {'$sum':'$'+group_key}, 'mean':{'$avg':'$'+group_key}, 'min':{'$min':'$'+group_key}, 'max':{'$max':'$'+group_key} }}, 
# 		# 		{'$sort':{'sum':sorter}}]

# 		# pipe = [{'$group' : {'_id' : '$'+group_key, ''}}]
# 		# if limit:
# 		# 	pipe.append({'$limit':limit})
	
# 		# res = db[collname].aggregate(pipe)
# 		# res = self.cursor_to_list(res)
# 		res = ''
# 		# print res
# 		return res 
   


get = Get()
eda = EDA()