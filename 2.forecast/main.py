#для оброки табличних даних
import pandas as pd
#для числових масивів
import numpy as np
#для побудови графіків
import matplotlib.pyplot as plt

#для машиного навчання
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#для обчислення майбутніх дат.
from datetime import timedelta

#Читаємо файл із вхідними даних для навчання
df = pd.read_csv('usd_uah.csv', parse_dates = ['date'])
#Сортування дані за датою
df = df.sort_values('date')

df['days'] = (df['date'] - df['date'].min()).dt.days

# x - дні, y - курс на даний день
X = df[['days']]
y = df['usd_rate']

#80% - навання
#20% - перевірка
#shuffle - дані перемішувати не потрібно, бо це є дати
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

#Тренування моделі - лінійна регрсія
model = LinearRegression()
model.fit(X_train, y_train)

#Прогноз на тестових даних
y_pred = model.predict(X_test)
#Середньо квадратична похибка
mse = mean_squared_error(y_test, y_pred)
print(f'MSE: {mse:.4f}')

last_day = df['days'].max()

future_days = np.array([last_day + i for i in range(1, 16)]).reshape(-1, 1)

#отримати прогноз на 10 днів
future_pred = model.predict(future_days)

#Створюємо список майбутніх дат, відповідних до future_days.
last_date = df['date'].max()
future_dates = [last_date + timedelta(days=i) for i in range(1, 16)]

# 6. Графік
#Малюємо графік історії курсу.
plt.plot(df['date'], df['usd_rate'], label='Історичні дані')
#Малюємо прогноз моделі на тестових (відкладених) даних.
plt.plot(df['date'].iloc[-len(y_test):], y_pred, label='Прогноз на тесті', linestyle='--')
#Малюємо червону лінію з прогнозом на майбутні 10 днів.
plt.plot(future_dates, future_pred, label='Прогноз на 10 днів', color='red')
#Оформлення графіка: підписи осей, заголовок, сітка, легенда — і відображення.
plt.title('Прогноз курсу USD/UAH')
plt.xlabel('Дата')
plt.ylabel('Курс')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()