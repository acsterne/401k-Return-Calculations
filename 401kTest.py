
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read in file that contains historic S&P data
df = pd.read_csv('^GSPC.csv')

# Convert columns to array for manipulation
columns_list = df.columns.tolist()

# Print out existing columns in file
print(df.columns)

# Count the number of differences between 'Close' and 'Adjusted Close'
differences_count = (df['Close'] != df['Adj Close']).sum()

# Print the result
print(f'Number of differences: {differences_count}')

# Drop unecessary columns
df = df.drop(['Volume'], axis=1) 

# Print the revised columns
print(df.columns)
print(df.head(2))

# Convert the Date column to standard date format
df['Date'] = pd.to_datetime(df['Date'])

# Create new columns for month and year
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Print the updated DataFrame
print(df.head(2))

# Define investment amount
investment_amount = 12000

# Create columns for different investment scenarios
df['equally_invested'] = investment_amount / 12  # Equally invested every month
df['all_in_first_month'] = 0  # Initialize column
df['all_in_last_month'] = 0  # Initialize column

# Calculate total investment for each month
for year in df['Year'].unique():
    # Set the 'all_in_first_month' column to $12000 in January
    df.loc[(df['Year'] == year) & (df['Month'] == 1), 'all_in_first_month'] = investment_amount
    
    # Set the 'all_in_last_month' column to $12000 in December
    df.loc[(df['Year'] == year) & (df['Month'] == 12), 'all_in_last_month'] = investment_amount

# Print the updated DataFrame with investment scenarios
print(df[['Date', 'equally_invested', 'all_in_first_month', 'all_in_last_month']])

# Create a new DataFrame for results
results_df = pd.DataFrame(columns=['Year', 'equally_invested', 'all_in_first_month', 'all_in_last_month'])

# Calculate annual return for each investment scenario
for year in df['Year'].unique():
    annual_return = {}

    for strategy in ['equally_invested', 'all_in_first_month', 'all_in_last_month']:
        # Calculate the number of shares bought
        df[f'{strategy}_shares'] = df[strategy] / df['Close']

        # Sum the shares bought for the calendar year
        shares_bought = df.loc[df['Year'] == year, f'{strategy}_shares'].sum()

        # Multiply by the January close in the following year if there are rows
        next_year_close_rows = df.loc[(df['Year'] == year + 1) & (df['Month'] == 1), 'Close']
        if not next_year_close_rows.empty:
            next_year_close = next_year_close_rows.values[0]
            gross_dollars = shares_bought * next_year_close
        else:
            gross_dollars = 0

        # Calculate the annual return
        annual_return[strategy] = (gross_dollars / investment_amount) - 1

    # Add the results to the new DataFrame
    results_df = pd.concat([results_df, pd.DataFrame([{'Year': year, **annual_return}])], ignore_index=True)

# Print the final results DataFrame
print(results_df)

# Calculate relative performance columns
results_df['rel_perf_first_month'] = results_df['all_in_first_month'] - results_df['equally_invested']
results_df['rel_perf_last_month'] = results_df['all_in_last_month'] - results_df['equally_invested']

# Calculate average relative performance
avg_rel_perf_first_month = results_df['rel_perf_first_month'].mean()
avg_rel_perf_last_month = results_df['rel_perf_last_month'].mean()

# Plotting the returns for each strategy by year
plt.figure(figsize=(10, 6))

# Equally Invested
plt.plot(results_df['Year'], results_df['equally_invested'], label='Equally Invested', marker='o')

# All in the First Month
plt.plot(results_df['Year'], results_df['all_in_first_month'], label='All in First Month', marker='o')

# All in the Last Month
plt.plot(results_df['Year'], results_df['all_in_last_month'], label='All in Last Month', marker='o')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Annual Return')
plt.title('Annual Return by Year for Each Strategy')
plt.legend()
plt.grid(True)
plt.show()

# Display the updated DataFrame with relative performance and average
print(results_df[['Year', 'equally_invested', 'all_in_first_month', 'all_in_last_month', 'rel_perf_first_month', 'rel_perf_last_month']])
print(f'\nAverage Relative Performance (All in First Month): {avg_rel_perf_first_month:.2%}')
print(f'Average Relative Performance (All in Last Month): {avg_rel_perf_last_month:.2%}')


