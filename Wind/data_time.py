import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset again
file_path = 'Power_detection.csv'
data = pd.read_csv(file_path)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)
daily_data = data.resample('D').mean()

plt.figure(figsize=(18, 12))

# Plot Daily Average of Active Power Raw
plt.subplot(3, 1, 1)
daily_data['active_power_raw'].plot(title='Daily Average of Active Power Raw', xlabel='Date', ylabel='Active Power Raw')

# Plot Daily Average of Generator Speed
plt.subplot(3, 1, 2)
daily_data['generator_speed'].plot(title='Daily Average of Generator Speed', xlabel='Date', ylabel='Generator Speed')

# Plot Daily Average of Wind Speed Raw
plt.subplot(3, 1, 3)
daily_data['wind_speed_raw'].plot(title='Daily Average of Wind Speed Raw', xlabel='Date', ylabel='Wind Speed Raw')

plt.tight_layout()

# Save the simplified time series plots
simplified_time_series_plot_path = '/root/recommend/hotel/static/zhexian'
plt.savefig(simplified_time_series_plot_path)

simplified_time_series_plot_path
# 根据生成的三张折线图，我们可以得出以下结论：

# 日平均原始活动功率(active_power_raw): 此图展示了风力发电机日平均原始活动功率的变化趋势。活动功率是风力发电的直接输出，代表了实际转化为电能的功率。此曲线的波动可能与风速、风向、环境温度等因素密切相关。如果曲线显示出明显的周期性波动，这可能反映了特定时间段内风力条件的变化或季节性影响。

# 日平均发电机转速(generator_speed): 发电机转速是风力发电效率的关键指标之一，直接影响到发电量。此图表展示了日平均发电机转速的变化情况，反映了发电机响应风力变化的能力。转速的变化可能受多种因素影响，包括风力发电机的设计、控制策略以及风速的变化。

# 日平均原始风速(wind_speed_raw): 风速是影响风力发电量最直接的因素之一。此图展示了日平均风速的变化趋势，对于评估风力发电潜力具有重要意义。风速的增加通常会导致活动功率和发电机转速的提高，但如果风速超过风力发电机的设计极限，可能会触发安全停机措施以保护设备。

# 从这三张图中，我们可以进一步分析风力发电机的性能和运行效率，例如，通过比较活动功率和风速的关系，可以评估风力发电机对不同风速的响应能力。同时，发电机转速的变化可以帮助我们理解风力发电机的运行状态和可能的维护需求。

# 此外，如果数据显示出明显的季节性或时间相关的模式，这可能对于风力发电场的规划和管理具有参考价值，比如在风速较高的季节调整运营策略，以最大化发电效率和产出。

# 综上所述，通过对这些关键指标的监测和分析，可以有效地评估和优化风力发电场的性能，提高能源产出效率，同时也为未来的规划和开发提供数据支持。