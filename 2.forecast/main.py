import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

conn = sqlite3.connect('uah_usd.db')
df = pd.read_sql_query('SELECT * FROM exchange_rates', conn)
conn.close()

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

df['days'] = (df['date'] - df['date'].min()).dt.days


X = df[['days']]
y = df['usd_rate']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'MSE: {mse:.4f}')

last_date = df['date'].max()
end_date = datetime(2025, 12, 31)
future_dates = pd.date_range(start=last_date + timedelta(days=1), end=end_date)
future_days = (future_dates - df['date'].min()).days.values.reshape(-1, 1)
future_pred = model.predict(future_days)

plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['usd_rate'], label='Історичні дані')
plt.plot(future_dates, future_pred, label='Прогноз до кінця 2025', color='red')
plt.title('Прогноз курсу USD/UAH')
plt.xlabel('Дата')
plt.ylabel('Курс')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()