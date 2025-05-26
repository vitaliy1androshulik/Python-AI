import sqlite3
import pandas as pd

df = pd.read_csv('usd_uah_table.csv', parse_dates=['date'])

conn = sqlite3.connect('uah_usd.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS exchange_rates (
    date TEXT PRIMARY KEY,
    usd_rate REAL
)
''')

for _, row in df.iterrows():
    cursor.execute('''
        INSERT OR REPLACE INTO exchange_rates (date, usd_rate)
        VALUES (?, ?)
    ''', (row['date'].strftime('%Y-%m-%d'), row['usd_rate']))

conn.commit()
conn.close()

print("Дані з CSV успішно імпортовані в 'uah_usd.db'")