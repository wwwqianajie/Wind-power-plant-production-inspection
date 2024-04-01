import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
import seaborn as sns

# 加载数据
file_path = 'Power_detection.csv'  # 请替换为你的数据文件路径
data = pd.read_csv(file_path)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# 计算日均值并清理NaN值
daily_avg_data = data.resample('D').mean().dropna()

# 多变量回归分析
X = daily_avg_data[['active_power_raw', 'generator_speed', 'wind_speed_raw']]
y = daily_avg_data['active_power_calculated_by_converter']

model = LinearRegression()
model.fit(X, y)

# 获取模型系数和截距
coefficients = model.coef_
intercept = model.intercept_

# 准备三维散点图数据
X_axis = daily_avg_data['active_power_raw']
Y_axis = daily_avg_data['generator_speed']
Z_axis = daily_avg_data['wind_speed_raw']

# 绘制三维散点图
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(X_axis, Y_axis, Z_axis, c=daily_avg_data['active_power_calculated_by_converter'], cmap='viridis')

ax.set_xlabel('Active Power Raw')
ax.set_ylabel('Generator Speed')
ax.set_zlabel('Wind Speed Raw')
colorbar = fig.colorbar(scatter, ax=ax)
colorbar.set_label('Active Power Calculated by Converter')

plt.title('3D Scatter Plot of Variables vs Active Power Calculated by Converter')
plt.show()
simplified_time_series_plot_path = '/root/recommend/hotel/static/3d'
plt.savefig(simplified_time_series_plot_path)
