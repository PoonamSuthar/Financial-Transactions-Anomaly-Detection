import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Sample data
data = {
    'transaction_id': ['TRX001', 'TRX002', 'TRX003', 'TRX004', 'TRX005', 'TRX006', 'TRX007'],
    'date': ['2024-06-01', '2024-06-01', '2024-06-01', '2024-06-02', '2024-06-02', '2024-06-03', '2024-06-03'],
    'category': ['Food', 'Utilities', 'Entertainment', 'Food', 'Transport', 'Utilities', 'Food'],
    'amount': [25.00, 150.00, 200.00, 3000.00, 45.00, 135.00, 20.00]
}

# Create DataFrame
df = pd.DataFrame(data)

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Data Preprocessing
# Handle missing or corrupt data entries
df.dropna(inplace=True)

# Calculate basic statistical metrics by category
grouped = df.groupby('category')['amount']
stats_df = grouped.agg(['mean', 'median', 'std']).reset_index()

# Set thresholds for anomaly detection
thresholds = {}
for _, row in stats_df.iterrows():
    category = row['category']
    mean = row['mean']
    std = row['std']
    thresholds[category] = {'upper': mean + 3*std, 'lower': mean - 3*std}

# Anomaly Detection
anomalies = []

for _, row in df.iterrows():
    category = row['category']
    amount = row['amount']
    if amount > thresholds[category]['upper'] or amount < thresholds[category]['lower']:
        reason = f"{amount:.2f} is more than 3 standard deviations from the mean in {category}"
        anomalies.append({
            'transaction_id': row['transaction_id'],
            'date': row['date'],
            'category': row['category'],
            'amount': row['amount'],
            'reason_for_anomaly': reason
        })

# Generate anomaly report
anomalies_df = pd.DataFrame(anomalies)

# Output the report
print("Anomaly Report")
print(anomalies_df)

# Save the report to a CSV file
anomalies_df.to_csv('anomaly_report.csv', index=False)

# Visualization
plt.figure(figsize=(10, 6))
for category in df['category'].unique():
    category_df = df[df['category'] == category]
    plt.scatter(category_df['date'], category_df['amount'], label=category)
plt.xlabel('Date')
plt.ylabel('Amount')
plt.title('Transactions Over Time')
plt.legend()
plt.show()
