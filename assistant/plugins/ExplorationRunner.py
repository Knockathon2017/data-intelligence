from ExplorationEngine import eda
from pymongo import MongoClient
CLIENT = MongoClient('localhost',27017)
db = CLIENT['ExzeoSmartUnderWriting']

# perform EDA 
collname = "knock"

#key can be any variable
key = "f2" 

field_type = eda.identify_variable_type(key,db,collname)
print field_type
uni = eda.univariate_analysis(key,db,collname, central_tendencies = False)
print uni
print eda.get_std_dev(key,db,collname)
# vis.create_univariate_table(uni, key)

# key1 = "f1"
# key2 = "f2"
# bi = eda.bivariate_analysis(key1, key2, collname)
# print 'std_dev',eda.get_std_dev(key1,collname)
# print 'outlier detection',eda.get_outliers(key1,collname)
# vis.createBiTable(bi, key1, key2)