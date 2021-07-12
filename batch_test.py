from pyspark.conf import SparkConf
from pyspark.sql import SQLContext
from pyspark import SparkContext
import findspark
import pandas as pd
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb



class sql_connect : 
    
    def __init__(self, host, dbname,jdbcPort,user,password,query):
            
        self.host = host
        self.dbname = dbname
        self.jdbcPort = jdbcPort
        self.user = user
        self.password = password
        self.query = query
        
#    def spark_sql_to_pandas(self,host,jdbcPort,dbname,user,password,query):
    def spark_sql_to_pandas(self):
        
        findspark.add_packages('mysql:mysql-connector-java:8.0.25') # mysql connecter
        conf = SparkConf().setAll([('spark.driver.extraClassPath',
                            '/usr/share/java/mysql-connector-java-8.0.25.jar')])  # jar path추가.
        sc = SparkContext(appName="TestPySparkJDBC", conf=conf)
        sqlContext = SQLContext(sc)        
        jdbc_url = "jdbc:mysql://{0}:{1}/{2}?user={3}&password={4}".format(self.host,self.jdbcPort,self.dbname,self.user,self.password)
        df = sqlContext.read.format('jdbc').options(driver='com.mysql.jdbc.Driver', url=jdbc_url, dbtable=query).load().toPandas()
        return df
   
    def create_table(self):
        engine = create_engine("mysql+mysqldb://{0}:{1}@{2}:{3}/{4}".format(self.user, self.password,self.host,self.jdbcPort,self.dbname),encoding='utf-8')
        conn = engine.connect()
        return conn




host = "localhost"
dbname = "sims"
jdbcPort = 3307
user = "smt_csl_prd"
password = "WpYrPRCwoPTx5NcQcucE"
query= '(select * from pet) AS t'



AWS_server_mysql = sql_connect(host,dbname,jdbcPort,user,password,query)

Pet_DataFrame = AWS_server_mysql.spark_sql_to_pandas()



Pet_kinds = list(Pet_DataFrame[['breed']]['breed'])
temp = {}
temp2 = {}
for i in Pet_kinds:
    if i in temp: 
        temp[i] = temp[i] + 1
    else:
        temp[i] = 1 #없을 때
Pet_names = list(Pet_DataFrame[['name']]['name'])
for i in Pet_names:
    if i in temp2: 
        temp2[i] = temp2[i] + 1
    else:
        temp2[i] = 1 #없을 때
        
data = pd.DataFrame(list(temp.items()),columns = ['pet_kind', 'count'])

data2 = pd.DataFrame(list(temp2.items()),columns = ['pet_name', 'n_count'])

Final_df = pd.merge(data,data2, how ='outer',left_index= True, right_index= True)




Final_df = Final_df.fillna('-')



# 로컬용
host = "172.23.0.1"
dbname = "testdb"
jdbcPort = 3306
user = "root"
password = "root"
query = '.'




temp = sql_connect(host,dbname,jdbcPort,user,password,query)



engine = temp.create_table()


Final_df.to_sql(name='temp', con=engine, if_exists='replace')





















# hostname = "localhost" #local주소 컨테이너내에서 환경이기 때문에 ip주소가 필요
# dbname = "sims"
# jdbcPort = 3307
# username = "smt_csl_prd"
# password = "WpYrPRCwoPTx5NcQcucE"

# class file_batch :
        
#     def __init__(self, query, host = "localhost", dbname = "sims", jdbcPort = 3307, user = "smt_csl_prd", password = "WpYrPRCwoPTx5NcQcucE"):
#         findspark.add_packages('mysql:mysql-connector-java:8.0.25') # mysql connecter
#         conf = SparkConf().setAll([('spark.driver.extraClassPath',
#                             '/usr/share/java/mysql-connector-java-8.0.25.jar')])  # jar path추가.
#         sc = SparkContext(appName="TestPySparkJDBC", conf=conf)
#         sqlContext = SQLContext(sc)        
#         jdbc_url = "jdbc:mysql://{0}:{1}/{2}?user={3}&password={4}".format(host,jdbcPort,dbname,user,password)
# #         query = '(select * from pet) AS t'
#         self.loadsql = sqlContext.read.format('jdbc').options(driver='com.mysql.jdbc.Driver', url=jdbc_url, dbtable=query).load()

        
    
        
        

#     def execute(self,query):
#         df = self.loadsql(query = query)
#         return df





# Pet_kinds = list(Pet_DataFrame[['breed']]['breed'])
# temp = {}
# temp2 = {}
# for i in Pet_kinds:
#     if i in temp: 
#         temp[i] = temp[i] + 1
#     else:
#         temp[i] = 1 #없을 때
# Pet_names = list(Pet_DataFrame[['name']]['name'])
# for i in Pet_names:
#     if i in temp2: 
#         temp2[i] = temp2[i] + 1
#     else:
#         temp2[i] = 1 #없을 때
        
# data = pd.DataFrame(list(temp.items()),columns = ['pet_kind', 'count'])

# data2 = pd.DataFrame(list(temp2.items()),columns = ['pet_name', 'n_count'])

# final_df = pd.merge(data,data2, how ='outer',left_index= True, right_index= True)





# engine = create_engine("mysql+mysqldb://root:"+"root"+"@172.23.0.1:3306/testdb", encoding='utf-8')
# conn = engine.connect()

# final_df.to_sql(name='abc', con=engine, if_exists='replace')
