from pyspark.sql import SparkSession
import pandas as pd
import csv

# preprocessing data csv
try:
    df = pd.read_csv("./deduplicated_data.csv")
    del df['Unnamed: 0']
    del df['Unnamed: 0.1']
    del df['Unnamed: 0.1.1']
    df.to_csv('deduplicated_data.csv')
    # print(df)
except:
    pass


# read file csv 
data = list()

with open('./deduplicated_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {row[1:]}')
            field = row[1:]
            line_count += 1
        else:
            # print(row[1:])
            line_count += 1
            data.append(row[1:])
    print(f'Processed {line_count} lines.')


# process with spark
input_uri = "mongodb://127.0.0.1/myDB.hiring"
output_uri = "mongodb://127.0.0.1/myDB.hiring"

myspark = SparkSession\
    .builder\
    .appName("job_hiring")\
    .config("spark.mongodb.input.uri", input_uri)\
    .config("spark.mongodb.output.uri", output_uri)\
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:2.4.2")\
    .getOrCreate()

# df = myspark.read.csv(path = "./deduplicated_data.csv", header=True, inferSchema=True)
# df = myspark.read.option("header",True) \
#      .csv("./deduplicated_data.csv")

# pandasDF = df.toPandas().copy()
# print(pandasDF['title'])

df = myspark.createDataFrame(data,field)

# df.printSchema()
df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("database","myDB").option("collection", "hiring").save()
