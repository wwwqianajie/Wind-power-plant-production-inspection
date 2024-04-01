import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset again
file_path = 'Power_detection.csv'
data = pd.read_csv(file_path)
correlation_matrix = data.corr()

# 提取与目标变量相关的相关系数
target_variables = ['active_power_raw', 'generator_speed', 'wind_speed_raw']
correlations = correlation_matrix[target_variables]
plt.figure(figsize=(12, 10))
sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Target Variables with Dataset Columns')
simplified_time_series_plot_path = '/root/recommend/hotel/static/sangeguanxi'
plt.savefig(simplified_time_series_plot_path)