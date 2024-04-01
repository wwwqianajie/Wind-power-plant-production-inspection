import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset again
file_path = 'Power_detection.csv'
data = pd.read_csv(file_path)

# Convert the 'timestamp' column to datetime format and set it as index
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Resample data to daily averages for the scatter plot variables
daily_avg_data = data.resample('D').mean().reset_index()

# 重新绘制散点图
fig, axes = plt.subplots(3, 1, figsize=(10, 15))

# active_power_raw 与 active_power_calculated_by_converter 的关系
sns.scatterplot(ax=axes[0], data=daily_avg_data, x='active_power_raw', y='active_power_calculated_by_converter')
axes[0].set_title('Daily Avg: Active Power Raw vs Active Power Calculated by Converter')
axes[0].set_xlabel('Active Power Raw')
axes[0].set_ylabel('Active Power Calculated by Converter')

# generator_speed 与 active_power_calculated_by_converter 的关系
sns.scatterplot(ax=axes[1], data=daily_avg_data, x='generator_speed', y='active_power_calculated_by_converter')
axes[1].set_title('Daily Avg: Generator Speed vs Active Power Calculated by Converter')
axes[1].set_xlabel('Generator Speed')
axes[1].set_ylabel('Active Power Calculated by Converter')

# wind_speed_raw 与 active_power_calculated_by_converter 的关系
sns.scatterplot(ax=axes[2], data=daily_avg_data, x='wind_speed_raw', y='active_power_calculated_by_converter')
axes[2].set_title('Daily Avg: Wind Speed Raw vs Active Power Calculated by Converter')
axes[2].set_xlabel('Wind Speed Raw')
axes[2].set_ylabel('Active Power Calculated by Converter')

plt.tight_layout()
plt.show()
# Save the simplified scatter plots
simplified_scatter_plot_avg_path = '/root/recommend/hotel/static/sandian'
plt.savefig(simplified_scatter_plot_avg_path)

simplified_scatter_plot_avg_path