from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import col
# 初始化 Spark 配置
def lis():
    conf = SparkConf().setAppName("HDFSFileStreamExample")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)  # 以10秒为批处理间隔

    # 定义输入数据源
    hdfs_directory = "hdfs:///user/root"  # HDFS 上的路径
    stream = ssc.textFileStream(hdfs_directory)
    global df
    def process_rdd(rdd):
        if not rdd.isEmpty():
            spark = SparkSession.builder.config(conf=conf).getOrCreate()
            header = rdd.first()  # 获取第一行作为列名
            data = rdd.filter(lambda x: x != header)  # 过滤掉第一行
            global df
            df = spark.createDataFrame(data.map(lambda line: line.split(',')), header.split(','))
                # 将列转换为适当的数据类型
            for column in df.columns:
                if column not in ['timestamp', 'turbine_id']:
                    df = df.withColumn(column, col(column).cast('float'))

            # 处理缺失值
            df = df.na.drop()
            # 使用regexp_extract函数提取数字部分，并将列重命名为"numeric_column"
            df = df.withColumn("numeric_column", regexp_extract(df["turbine_id"], r"\d+", 0).cast(IntegerType()))

            # 删除原始的"turbine_id"列
            df = df.drop("turbine_id")
            # 假设时间戳列名为"timestamp_col"，将其转换为Spark的时间戳类型
            df = df.withColumn("timestamp", to_timestamp(df["timestamp"], "yyyy/MM/dd HH:mm:ss"))
            df = df.drop("timestamp")
            csv_path = "/root/output.csv"
            df.write.mode("overwrite").option("header", "true").csv(csv_path)
            df.show()
    stream.foreachRDD(process_rdd)
    # 启动流处理
    ssc.start()
    ssc.awaitTermination(20)
    ssc.stop()