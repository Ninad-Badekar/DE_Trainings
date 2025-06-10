# MySQL Triggers 

## Trigger Creation Syntax
```sql
CREATE TRIGGER trigger_name
{BEFORE|AFTER} {INSERT|UPDATE|DELETE}
ON table_name FOR EACH ROW
[trigger_body]
```

# Time Series Analysis with pandas

This guide provides an overview of key pandas functions and methods for handling and analyzing time series data. Whether you're working with daily, monthly, or custom time intervals, these tools will help you manipulate, aggregate, and visualize temporal datasets effectively.

---

## Date and Time Functions

### `day_name()`
- **Purpose**: Extracts the day of the week as a string (e.g., 'Monday', 'Tuesday').
- **Usage**: `df['date_column'].dt.day_name()`

### `sum()`, `count()`, `min()`, `max()`, `std()`, `mean()`, `median()`
- **Purpose**: Perform aggregation operations on numerical data.
  - `sum()`: Total sum of values.
  - `count()`: Number of non-null entries.
  - `min()`: Minimum value.
  - `max()`: Maximum value.
  - `std()`: Standard deviation.
  - `mean()`: Mean (average) value.
  - `median()`: Median value.
- **Usage**: `df['value_column'].sum()`, `df['value_column'].mean()`, etc.

---

##  Time Series Functions

### `date_range()`
- **Purpose**: Generates a range of dates with a specified frequency.
- **Usage**:
  ```python
  pd.date_range(start='2025-01-01', end='2025-12-31', freq='M')
- start: Start date.

- end: End date.

- freq: Frequency string (e.g., 'D' for daily, 'M' for monthly).

##  `to_datetime()`

**Purpose**: Converts a series or list of date-like objects to pandas `datetime` objects.

**Usage**:

```python
import pandas as pd

# Convert a single date string to datetime
date = pd.to_datetime('2025-06-10')

# Convert a list of date strings to datetime
dates = pd.to_datetime(['2025-06-10', '2025-06-11', '2025-06-12'])

# Convert a date column in a DataFrame
df = pd.DataFrame({'date_column': ['2025-06-10', '2025-06-11', '2025-06-12']})
df['date_column'] = pd.to_datetime(df['date_column'])

# Convert with a specific date format
df['date_column'] = pd.to_datetime(df['date_column'], format='%Y-%m-%d')

# Convert using a specific origin and unit
df['date_column'] = pd.to_datetime(df['date_column'], unit='D', origin='unix')
```
# 🔄 Indexing and Resampling in pandas

## `set_index()` and `reset_index()`

**Purpose**: Set or reset the index of a DataFrame.

### Usage

```python
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'date_column': ['2025-06-10', '2025-06-11', '2025-06-12'],
    'value': [10, 20, 30]
})

# Convert 'date_column' to datetime
df['date_column'] = pd.to_datetime(df['date_column'])

# Set 'date_column' as the index
df.set_index('date_column', inplace=True)

# Reset the index
df.reset_index(inplace=True)
```
# 📅 `resample()` in pandas

**Purpose**: Resample time series data to a different frequency and apply aggregation functions.

## Usage

```python
import pandas as pd

# Sample DataFrame with daily data
df = pd.DataFrame({
    'date_column': pd.date_range('2025-06-01', periods=10, freq='D'),
    'value': range(10)
})

# Set 'date_column' as the index
df.set_index('date_column', inplace=True)

# Resample to monthly frequency and calculate the sum
monthly_sum = df.resample('M').sum()

# Resample to weekly frequency and calculate the mean
weekly_mean = df.resample('W').mean()

# Resample to daily frequency and apply multiple aggregation functions
daily_agg = df.resample('D').agg({
    'value': ['sum', 'mean', 'min', 'max']
})
```

## Frequency Aliases

| Alias | Frequency  |
|-------|------------|
| `D`   | Daily      |
| `W`   | Weekly     |
| `M`   | Monthly    |
| `Q`   | Quarterly  |
| `Y`   | Yearly     |
| `H`   | Hourly     |
| `T`   | Minute     |

# Rolling Window Theory

## Concept
A rolling window (or sliding window) is a data analysis technique that processes fixed-size subsets of sequential data by "rolling" through the dataset. The window moves incrementally, typically dropping the oldest data point while adding a new one with each iteration.

## Key Characteristics
- **Window Size**: Fixed number of time periods/observations (e.g., 7 days)
- **Step Size**: Movement interval (often 1 unit)
- **Overlap**: Retains N-1 data points between consecutive windows

## Common Applications
- Time-series analysis (moving averages, volatility measurement)
- Machine learning (feature engineering for temporal data)
- Real-time systems (stream processing)
- Performance metrics (trailing indicators)
