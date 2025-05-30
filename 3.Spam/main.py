import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

texts = [
    "Купити зараз", "Зустрінемося в 15:00", "Отримай знижку 70% вже сьогодні", "Як справи?",
    "Термінова пропозиція тільки сьогодні", "Можеш передзвонити пізніше?",
    "Пройди опитування та виграй iPhone", "Надішли, будь ласка, файл",
    "Зароби 1000 грн за день", "Не забудь про зустріч завтра",
    "Твоя карта заблокована, натисни тут", "Де ти зараз?",
    "Отримай миттєвий кредит онлайн", "Скинь адресу, будь ласка",
    "Купуй вигідно, акція діє до вечора", "Чекаю тебе біля входу",
    "Пройди реєстрацію та отримай бонус", "Мама вже вдома?",
    "Виграй подорож до Єгипту", "Завтра буде контрольна з математики"
]

labels = [
    1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
    1, 0, 1, 0, 1, 0, 1, 0, 1, 0
]

conn = sqlite3.connect('phrases.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS phrases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phrase TEXT NOT NULL,
        is_spam INTEGER NOT NULL
    )
''')

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)

phrase = input("Вкажіть фразу: ")
test_vector = vectorizer.transform([phrase])
prediction = model.predict(test_vector)[0]

print("Це спам" if prediction else "Це не спам")
cursor.execute("INSERT INTO phrases (phrase, is_spam) VALUES (?, ?)", (phrase, int(prediction)))
for row in cursor.execute("SELECT phrase, is_spam FROM phrases"):
    print(f"Фраза: {row[0]} — {'Спам' if row[1] else 'Не спам'}")
conn.commit()
conn.close()

