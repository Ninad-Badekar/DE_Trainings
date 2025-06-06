from datetime import datetime, date, time, timedelta

# 1. Current local datetime using now()
now = datetime.now()
print("Current local datetime (now):", now)

# 2. Current local datetime using today()
today = datetime.today()
print("Current local datetime (today):", today)

# 3. Convert string to datetime (strptime)
date_str = "2025-06-06"
dt_from_str = datetime.strptime(date_str, "%Y-%m-%d")
print("Datetime from string:", dt_from_str)

# 4. Convert datetime to string (strftime)
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted datetime string:", formatted)

# 5. Create a date object
my_date = date(2025, 6, 6)
print("Date object:", my_date)

# 6. Create a time object
my_time = time(14, 30)
print("Time object:", my_time)

# 7. Use timedelta to add 5 days to current datetime
five_days = timedelta(days=5)
future_date = now + five_days
print("5 days from now:", future_date)

# 8. Combine date and time into datetime
combined = datetime.combine(my_date, my_time)
print("Combined datetime:", combined)

# 9. Get current UTC datetime
utc_now = datetime.utcnow()
print("Current UTC datetime:", utc_now)

# 10. Access datetime attributes
print("Year:", now.year)
print("Month:", now.month)
print("Day:", now.day)
print("Hour:", now.hour)
print("Minute:", now.minute)
print("Second:", now.second)
