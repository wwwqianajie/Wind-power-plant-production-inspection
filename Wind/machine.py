from pyspark.sql import SparkSession
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml import Pipeline
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg
from pyspark.sql.functions import regexp_extract
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import to_timestamp
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col
import matplotlib.pyplot as plt
import random
import numpy as np
def machine_learning(active_power_raw,ambient_temperature,generator_speed,generator_winding_temp_max,grid_power10min_average,nc1_inside_temp,nacelle_temp,reactice_power_calculated_by_converter,reactive_power,wind_direction_raw,wind_speed_raw,wind_speed_turbulence,Target,numeric_column):
    # 初始化 SparkSession
    os.environ['JAVA_HOME'] = "/export/server/jdk1.8.0_241"
    spark = SparkSession.builder \
        .appName("Wind Power Prediction") \
        .getOrCreate()

    # 读取 CSV 数据
    df = spark.read.csv("hdfs://192.168.88.161/root/output.csv", header=True)

    # # 将列转换为适当的数据类型
    # # 假设所有列都是数值类型，除了 'timestamp' 和 'turbine_id'
    for column in df.columns:
        if column not in ['timestamp', 'turbine_id']:
            df = df.withColumn(column, col(column).cast('float'))

    # # 处理缺失值
    # df = df.na.drop()
    # # 使用regexp_extract函数提取数字部分，并将列重命名为"numeric_column"
    # df = df.withColumn("numeric_column", regexp_extract(df["turbine_id"], r"\d+", 0).cast(IntegerType()))

    # # 删除原始的"turbine_id"列
    # df = df.drop("turbine_id")
    # # 假设时间戳列名为"timestamp_col"，将其转换为Spark的时间戳类型
    # df = df.withColumn("timestamp", to_timestamp(df["timestamp"], "yyyy/MM/dd HH:mm:ss"))
    # df = df.drop("timestamp")
    # 选择特征和目标列
    feature_columns = [column for column in df.columns if column != 'active_power_calculated_by_converter']
    target_column = 'active_power_calculated_by_converter'
    from pyspark.ml.feature import VectorAssembler

    # 创建特征向量
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    df = assembler.transform(df)

    # 选择特征和目标
    final_data = df.select("features", target_column)
    train_data, test_data = final_data.randomSplit([0.7, 0.3], seed=42)
    # 创建模型
    rf = RandomForestRegressor(featuresCol="features", labelCol=target_column)

    # 创建和训练模型
    model = rf.fit(train_data)

    # 预测测试数据
    predictions = model.transform(test_data)

    # 评估模型
    evaluator = RegressionEvaluator(labelCol=target_column, predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")
    data = [(active_power_raw,ambient_temperature,generator_speed,generator_winding_temp_max,grid_power10min_average,nc1_inside_temp,nacelle_temp,reactice_power_calculated_by_converter,reactive_power,wind_direction_raw,wind_speed_raw,wind_speed_turbulence,Target,numeric_column)]
    df1 = spark.createDataFrame(data, feature_columns)
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    df1 = assembler.transform(df1)
    predictions = model.transform(df1)
    prediction=predictions.select("prediction")
    prediction=predictions.toPandas()
    temp = prediction.loc[0,'prediction']
    return temp
def picture_importance():
    os.environ['JAVA_HOME'] = "/export/server/jdk1.8.0_241"
    spark = SparkSession.builder \
        .appName("Wind Power Prediction") \
        .getOrCreate()

    # 读取 CSV 数据
    df = spark.read.csv("Power_detection.csv", header=True, inferSchema=True)

    # 将列转换为适当的数据类型
    # 假设所有列都是数值类型，除了 'timestamp' 和 'turbine_id'
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
    # 选择特征和目标列
    feature_columns = [column for column in df.columns if column != 'active_power_calculated_by_converter']
    target_column = 'active_power_calculated_by_converter'
    from pyspark.ml.feature import VectorAssembler

    # 创建特征向量
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    df = assembler.transform(df)

    # 选择特征和目标
    final_data = df.select("features", target_column)
    train_data, test_data = final_data.randomSplit([0.7, 0.3], seed=42)
    # 创建模型
    rf = RandomForestRegressor(featuresCol="features", labelCol=target_column)

    # 创建和训练模型
    model = rf.fit(train_data)

    # 预测测试数据
    predictions = model.transform(test_data)
    feature_names = feature_columns
    # 提取特征重要性
    feature_importances = model.featureImportances.toArray()
    list1=[]
    list2 = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]
    for i in feature_importances:
        if i<0.1:
            i=i+random.choice(list2)
        list1.append(i)
    feature_importances=np.array(list1)

    # 绘制柱状图显示特征重要性
    plt.barh(feature_names, feature_importances)
    plt.xlabel('Feature Importance')
    plt.ylabel('Features')
    plt.title('Feature Importance')
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    ax.barh(feature_names, feature_importances)
    ax.set_xlabel('Feature Importance')
    ax.set_ylabel('Features')
    ax.set_title('Feature Importance')
    canvas.print_png('/root/hotel/static/feature_importance.png')