from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load data
df = pd.read_parquet("monthly_review_count.parquet")
df.review_month = df.review_month.dt.to_timestamp()

# Get unique store names
target_stores = df.store_name.unique()

# Streamlit selector for store name
store_name = st.selectbox(
    '리뷰 내용이 궁금한 레스토랑을 선택해주세요',
    target_stores
)

# Filter data for the selected store, calculate cumulative sum
store_data = df[df.store_name == store_name].sort_values('review_month')
store_data['cumulative_reviews'] = store_data['size'].cumsum()

# Filter the data to the specified date range (July 2024 to November 2024)
start_date = pd.Timestamp('2024-07-01')
end_date = pd.Timestamp('2024-11-30')
store_data = store_data[(store_data['review_month'] >= start_date) & (store_data['review_month'] <= end_date)]

# Reindex to show points at 10-day intervals
all_dates = pd.date_range(start=start_date, end=end_date, freq='10D')
store_data = store_data.set_index('review_month').reindex(all_dates).interpolate(method='linear').reset_index()
store_data.columns = ['review_month', 'cumulative_reviews']

# Define target date
target_date = pd.Timestamp('2024-09-17')

# Plotting
fig = plt.figure()
# Scatter plot for cumulative review count
plt.scatter(store_data['review_month'], store_data['cumulative_reviews'], label='Cumulative Review Count')
# Line plot to connect the points
plt.plot(store_data['review_month'], store_data['cumulative_reviews'], linestyle='-', color='b')

# Additional plot settings
plt.xlabel('Date')
plt.ylabel('Cumulative Review Count')
plt.axvline(x=target_date, color='r', linestyle='--', label='2024-09-17')
plt.xticks(pd.date_range(start=start_date, end=end_date, freq='10D'), rotation=20)
plt.legend()
st.pyplot(fig)

#djWjrh