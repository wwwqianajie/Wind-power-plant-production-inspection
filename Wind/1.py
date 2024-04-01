from flask import Flask, render_template, request
from  machine import machine_learning 
import pandas as pd
from pyspark.sql import SparkSession
import numpy as np
import json
from listen import lis
# from listen import machine_learning
app = Flask(__name__)

# 路由1：显示用户输入界面
from send_data import send
@app.route('/')
def index():
    # lis()
    turbine_ids = [1,  10,  13,  14,  15,  18,  19,  20,  97, 103, 105, 108, 120,
       123, 139, 158]  # 替换为您要提供给用户选择的 turbine_id 列表
    return render_template('index.html', turbine_ids=turbine_ids)

# 路由2：接收用户输入并进行模型预测
@app.route('/prediction', methods=['GET','POST'])
def prediction():

    # 从用户提交的表单中获取输入数据
    active_power_raw = float(request.form['active_power_raw'])
    ambient_temperature = float(request.form['ambient_temperature'])
    generator_speed = float(request.form['generator_speed'])
    generator_winding_temp_max = float(request.form['generator_winding_temp_max'])
    grid_power10min_average = float(request.form['grid_power10min_average'])
    nc1_inside_temp = float(request.form['nc1_inside_temp'])
    nacelle_temp = float(request.form['nacelle_temp'])
    reactive_power_calculated_by_converter = float(request.form['reactive_power_calculated_by_converter'])
    reactive_power = float(request.form['reactive_power'])
    wind_direction_raw = float(request.form['wind_direction_raw'])
    wind_speed_raw = float(request.form['wind_speed_raw'])
    wind_speed_turbulence = float(request.form['wind_speed_turbulence'])
    numeric_column = float(request.form['turbine_id'])
    Target = float(request.form['target'])
    active_power_calculated=machine_learning(active_power_raw,ambient_temperature,generator_speed,generator_winding_temp_max,grid_power10min_average,nc1_inside_temp,nacelle_temp,reactive_power_calculated_by_converter,reactive_power,wind_direction_raw,wind_speed_raw,wind_speed_turbulence,Target,numeric_column)
    return render_template('predictions.html',
                        active_power_raw=active_power_raw,
                        ambient_temperature=ambient_temperature,
                        generator_speed=generator_speed,
                        generator_winding_temp_max=generator_winding_temp_max,
                        grid_power10min_average=grid_power10min_average,
                        nc1_inside_temp=nc1_inside_temp,
                        nacelle_temp=nacelle_temp,
                        reactive_power_calculated_by_converter=reactive_power_calculated_by_converter,
                        reactive_power=reactive_power,
                        wind_direction_raw=wind_direction_raw,
                        wind_speed_raw=wind_speed_raw,
                        wind_speed_turbulence=wind_speed_turbulence,
                        turbine_id=numeric_column,
                        target=Target,
                        active_power_calculated=active_power_calculated)
@app.route('/analysis_zhexian_sandian', methods=['GET','POST'])
def analysis_zhexian_sandian():
    # 这里添加您的图片路径和分析内容
    images_info = {
        "时间序列关系": {
            "img_path": "static/zhexian.png",
            "analysis": "Daily Avg: Active Power Raw vs Active Power Calculated by Converter:日均值数据显示，active_power_raw与active_power_calculated_by_converter之间保持了很强的正相关性。这表明，在日均值水平上，原始活动功率与计算所得的活动功率之间的关系更为明显和稳定。Daily Avg: Generator Speed vs Active Power Calculated by Converter:发电机速度与通过转换器计算的活动功率之间的正相关性在日均值数据上同样显著。这进一步证明了发电机的运行速度是影响活动功率计算的重要因素。Daily Avg: Wind Speed Raw vs Active Power Calculated by Converter:日均值数据上，原始风速与通过转换器计算的活动功率之间的正相关性非常强，这强调了风速对风力发电性能的直接影响。"
        },
        "重要因素与目标关系分析": {
            "img_path": "static/sandian.png",
            "analysis": "Active Power Raw vs Active Power Calculated by Converter:active_power_raw与active_power_calculated_by_converter之间存在明显的正相关性。这表明原始活动功率与通过转换器计算的活动功率之间有着紧密的联系，且二者变化趋势相似。Generator Speed vs Active Power Calculated by Converter:发电机速度（generator_speed）与通过转换器计算的活动功率之间也显示出一定程度的正相关性，尽管这种相关性可能不如活动功率原始值与计算值之间的相关性那么强。这表明发电机的运行速度对活动功率的产生有影响，但可能还有其他因素在起作用。Wind Speed Raw vs Active Power Calculated by Converter:原始风速（wind_speed_raw）与通过转换器计算的活动功率之间的关系图展示了较强的正相关性，暗示风速是影响活动功率计算的一个关键因素。随着风速的增加，活动功率的计算值也相应增加，这与风力发电的基本原理相符。"
        }
    }
    return render_template('analysis_zhexian_sandian.html', images_info=images_info)

# 新增路由 - 展示3D图和相关性分析图的分析
@app.route('/analysis_3d_sangeguanxi', methods=['GET','POST'])
def analysis_3d_sangeguanxi():
    # 这里添加您的图片路径和分析内容
    images_info = {
        "相关性分析": {
            "img_path": "static/sangeguanxi.png",
            "analysis": "基于相关性分析的结果，我们可以观察到以下几点关于active_power_raw、generator_speed、和wind_speed_raw与数据集中其他列的关系：active_power_raw:与active_power_calculated_by_converter、grid_power10min_average、reactive_power、和wind_speed_raw呈现出非常高的正相关性，这表明这些变量与活动功率的原始值紧密相关，特别是风速对活动功率的影响非常显著。与ambient_temperature、nc1_inside_temp、和nacelle_temp呈现出轻微的负相关性，表明温度变化对活动功率的影响相对较小。generator_speed:与active_power_calculated_by_converter、active_power_raw、grid_power10min_average、reactive_power、和wind_speed_raw呈现出高正相关性，说明发电机速度与这些电力和风速指标密切相关。对于generator_winding_temp_max也有相对较高的正相关性，这可能表明发电机速度的增加会导致绕组温度上升。wind_speed_raw:与active_power_raw、generator_speed、和grid_power10min_average有非常高的正相关性，强调了风速对发电性能的直接影响。同样，reactive_power和reactice_power_calculated_by_converter也显示出较高的正相关性，进一步证实了风速对电力产生的影响。"
        },
        "重要因素与目标组合分析": {
            "img_path": "static/3d.png",
            "analysis": "根据三维散点图，我们能从数据中得到以下几个分析点：变量间的关系：三维散点图展示了active_power_raw、generator_speed、和wind_speed_raw三个变量与active_power_calculated_by_converter之间的复杂关系。颜色的变化（代表active_power_calculated_by_converter的值）揭示了当这三个变量改变时，计算得到的活动功率如何变化，提供了一个直观的多维度关系视图。风速对活动功率的影响：图中可以观察到，随着wind_speed_raw（风速）的增加，点的颜色变化可能表明active_power_calculated_by_converter（通过转换器计算的活动功率）的增加。这强调了风速是影响风力发电效率的重要因素。发电机速度的作用：generator_speed（发电机速度）的变化也对活动功率有一定的影响，但这种影响可能与active_power_raw和wind_speed_raw相比更为复杂。发电机速度的增加通常意味着更高的能量转换效率，但这也受到风速和其他操作条件的影响。"
        }
    }
    return render_template('analysis_3d_sangeguanxi.html', images_info=images_info)
if __name__ == '__main__':
    app.debug = True
    app.run()