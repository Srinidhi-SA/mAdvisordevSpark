"""
functions to load data from various sources to create a dataframe
"""
from __future__ import print_function
from __future__ import absolute_import

from builtins import str
from builtins import range
from past.builtins import basestring
from builtins import object
from pyspark.sql import SparkSession, HiveContext
from pyspark import SparkContext, SparkConf
import random
from .decorators import accepts
import time
import re
from functools import reduce
import subprocess
import pandas as pd
import requests
import io
from io import StringIO

class DataLoader(object):

    @staticmethod
    @accepts(SparkSession, basestring, has_header=bool, interpret_data_schema=bool)
    def load_csv_file(spark_session, csv_file_path, has_header=True, interpret_data_schema=True):
        return spark_session.read.csv(csv_file_path, header=has_header, inferSchema=interpret_data_schema, escape='"',
                                      multiLine=True, ignoreTrailingWhiteSpace=True, nullValue=None and 'na' and 'nan')

    @staticmethod
    def load_csv_file_pandas(csv_file_path, has_header=True):
        s=requests.get(csv_file_path).content
        df=pd.read_csv(io.StringIO(s.decode('utf-8')))
        return df

    @staticmethod
    @accepts(SparkSession, basestring, dict)
    def create_dataframe_from_jdbc_connector(spark_session, datasource_type, dbConnectionParams):
        datasource_type = datasource_type.lower()
        print("~"*100)
        print("Data Source :- ",datasource_type)
        print("Database Connection Params :- ",dbConnectionParams)
        print("~"*100)
        if "hana" == datasource_type:
            return DataLoader.create_dataframe_from_hana_connector(spark_session, dbConnectionParams)
        elif "mysql" == datasource_type:
            return DataLoader.create_dataframe_from_mysql_db(spark_session, dbConnectionParams)
        elif "mssql" == datasource_type:
            return DataLoader.create_dataframe_from_mssql_db(spark_session, dbConnectionParams)
        elif "oracle" == datasource_type:
            return DataLoader.create_dataframe_from_oracle_db(spark_session, dbConnectionParams)
        elif "hive" == datasource_type:
            return DataLoader.create_dataframe_from_hive(spark_session, dbConnectionParams)
        elif "s3" == datasource_type:
            return DataLoader.create_dataframe_from_s3(spark_session, dbConnectionParams)

    @staticmethod
    @accepts(SparkSession, dict)
    def create_dataframe_from_mysql_db(spark_session, dbConnectionParams):
        df = None
        # change jdbc_url

        jdbc_url = "jdbc:mysql://{}:{}/{}".format(dbConnectionParams["host"], dbConnectionParams["port"], DataLoader.get_db_name(dbConnectionParams))
        print(jdbc_url)

        table_name = dbConnectionParams.get("tablename")
        username = dbConnectionParams.get("username")
        password = dbConnectionParams.get("password")
        try:
            df = spark_session.read.format("jdbc").option(
                "url", jdbc_url).option(
                "dbtable", "{}".format(table_name)).option(
                "user", username).option("password", password).load()
            return df
        except Exception as e:
            print("couldn't connect to database")
            print(e)
        return df

    @staticmethod
    @accepts(SparkSession, dict)
    def create_dataframe_from_mssql_db(spark_session, dbConnectionParams):
        df = None
        # change jdbc_url
        jdbc_url = "jdbc:sqlserver://{}:{};databaseName={};".format(dbConnectionParams["host"], dbConnectionParams["port"],
                                                                    DataLoader.get_db_name(dbConnectionParams))
        try:
            df = spark_session.read.format("jdbc").option("url", jdbc_url).option("dbtable", "{}".format(
                dbConnectionParams.get("tablename"))).option("user", dbConnectionParams.get("username")).option(
                "password", dbConnectionParams.get("password")).load()

        except Exception as e:
            print("couldn't connect to database")
        return df

    @staticmethod
    @accepts(SparkSession, dict)
    def create_dataframe_from_oracle_db(spark_session, dbConnectionParams):
        pass

    @staticmethod
    @accepts(SparkSession, dict)
    def create_dataframe_from_hana_connector(spark_session, dbConnectionParams):
        df = None
        jdbc_url = "jdbc:sap://{}:{}/?currentschema={}".format(dbConnectionParams["host"], dbConnectionParams["port"], DataLoader.get_db_name(dbConnectionParams))
        table_name = dbConnectionParams.get("tablename")
        username = dbConnectionParams.get("username")
        password = dbConnectionParams.get("password")
        try:
            df = spark_session.read.format("jdbc").option(
                "url", jdbc_url).option("driver", "com.sap.db.jdbc.Driver").option(
                "dbtable", table_name).option("user", username).option("password", password).load()
        except Exception as e:
            print("couldn't connect to hana")
            raise e
        return df

    @staticmethod
    @accepts(SparkSession, dict)
    def create_dataframe_from_hive(spark_session, dbConnectionParams):
        df = None
        try:
            sc = SparkSession.builder.appName("Testing").config(conf=SparkConf()).enableHiveSupport().getOrCreate()
            sqlContext = HiveContext(sc)
            sqlContext.setConf("hive.metastore.uris", "thrift://{}:{}".format(dbConnectionParams.get("host"),dbConnectionParams.get("port")))

            tdf=sqlContext.sql("show databases")
            tdf.show()

            schema = DataLoader.get_db_name(dbConnectionParams)
            table_name = dbConnectionParams.get("tablename")
            df = sqlContext.table(".".join([schema,table_name]))

        except Exception as e:
            print("couldn't connect to hive")
            raise e
        return df

    @staticmethod
    @accepts(SparkSession, dict)
    def create_dataframe_from_s3(spark_session, dbConnectionParams):
        df = None

        file_name = dbConnectionParams.get("file_name")
        dst_file_name = str(random.randint(10000,99999)) + '_' + file_name
        #try:
        import boto3

        myAccessKey = dbConnectionParams.get("access_key_id")
        mySecretKey = dbConnectionParams.get("secret_key")
        s3_bucket_name = dbConnectionParams.get("bucket_name")
        datasetname = dbConnectionParams.get("new_dataset_name")

        client = boto3.client('s3', aws_access_key_id=myAccessKey,
        aws_secret_access_key=mySecretKey)

        bucket_name = s3_bucket_name

        object_key = file_name
        csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string))

        #
        # def get_boto_session():
        #     return boto3.Session(aws_access_key_id=myAccessKey, aws_secret_access_key=mySecretKey)
        #
        # def get_boto_resourse():
        #     session = get_boto_session()
        #     return session.resource('s3')
        #
        # def get_boto_bucket():
        #     resource = get_boto_resourse()
        #     return resource.Bucket(s3_bucket_name)
        #
        # def upload_file(src_path, dest_name):
        #     bucket = get_boto_bucket()
        #     bucket.upload_file(src_path, dest_name)
        #
        # def download_file(file_name, dest_name):
        #     bucket = get_boto_bucket()
        #     bucket.download_file(file_name, dest_name)
        #
        # # subprocess.Popen(['hdfs', 'dfs', '-put', dest_name, '/dev/dataset'])
        #
        # def read_file(src_name):
        #     bucket = get_boto_bucket()
        #
        # download_file(file_name,'/tmp/'+dst_file_name)
        #
        # try:
        #     if df is None:
        #         df = spark_session.read.csv('file:///tmp/'
        #                 + dst_file_name, header=True, inferSchema=True)
        # except Exception as e:
        #     print(e)
        #
        #     try:
        #         if df is None:
        #             df = spark_session.read.csv('/tmp/'
        #                     + dst_file_name, header=True,
        #                     inferSchema=True)
        #     except Exception as e:
        #         print(e)
        #
        #     try:
        #         if df is None:
        #             df = \
        #                 spark_session.read.csv('hdfs://172.31.64.29:9000/dev/dataset/'
        #                      + dst_file_name, header=True,
        #                     inferSchema=True)
        #     except Exception as e:
        #         print(e)
        #
        #         try:
        #             if df is None:
        #                 df = spark_session.read.csv('/dev/dataset/'
        #                         + dst_file_name, header=True,
        #                         inferSchema=True)
        #         except Exception as e:
        #             print(e)
        #         cols = [re.sub("[[]|[]]|[<]|[\.]|[*]|[$]|[#]", '', col)
        #                 for col in df.columns]
        #         df = reduce(lambda data, idx: \
        #                     data.withColumnRenamed(df.columns[idx],
        #                     cols[idx]), range(len(df.columns)), df)
        df = spark_session.createDataFrame(df)
        return df


    @staticmethod
    def get_db_name(dbConnectionParams):
        if "schema" in list(dbConnectionParams.keys()):
            return dbConnectionParams.get("schema")
        elif "databasename" in list(dbConnectionParams.keys()):
            return dbConnectionParams.get("databasename")
