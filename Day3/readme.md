# 📊 Time Series Analysis with pandas

This guide provides an overview of key pandas functions and methods for handling and analyzing time series data. Whether you're working with daily, monthly, or custom time intervals, these tools will help you manipulate, aggregate, and visualize temporal datasets effectively.

---

## 🕒 Date and Time Functions

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

## 📅 Time Series Functions

### `date_range()`
- **Purpose**: Generates a range of dates with a specified frequency.
- **Usage**:
  ```python
  pd.date_range(start='2025-01-01', end='2025-12-31', freq='M')
- start: Start date.

- end: End date.

- freq: Frequency string (e.g., 'D' for daily, 'M' for monthly).
