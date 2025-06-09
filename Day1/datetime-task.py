from datetime import datetime
from dateutil.relativedelta import relativedelta

now = datetime.now()

delta = relativedelta(years=2, months=3, days=12)
past_date = now - delta

day = past_date.day
month = past_date.month
year = past_date.year

print("Day:", day)
print("Month:", month)
print("Year:", year)

