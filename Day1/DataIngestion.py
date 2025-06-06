import pandas as pd
import pymysql
from sqlalchemy import create_engine ,select,MetaData,Table,func
cars = pd.read_csv("C:/Users/user/Downloads/archive/CarsData.csv")

engine = create_engine("mysql+pymysql://root:ninad123@localhost/de_training")
conn = engine.connect()
cars.to_sql(name='cars', con=engine, if_exists='replace', index=False)

metadata = MetaData()
metadata.reflect(bind=engine)
cars_table = metadata.tables['cars']

# stmt = select(cars_table).where(cars_table.c.mpg > 10)

# result = conn.execute(stmt)

# for row in result:
#     print(row)

avg = select(func.count(),cars_table.c.fuelType).group_by(cars_table.c.fuelType)
res = conn.execute(avg)
for row in res:
    print(row)