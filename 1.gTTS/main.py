from gtts import gTTS
import smtplib
import ssl
from email.message import EmailMessage

with open("text.txt", "r", encoding="utf-8") as file:
    text = file.read()
tts = gTTS(text=text, lang='uk')
tts.save('my.mp3')

sender = input("Введіть емейл відправника :: ")
to = input("Введіть емейл отримувача :: ")

subject = "Лист з файлом"
body = "Привіт!"
filename = "my.mp3"
message = EmailMessage()
message["From"] = sender
message["To"] = to
message["Subject"] = subject
message.set_content(body)

with open(filename, "rb") as f:
    file_data = f.read()
    file_name = f.name
message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender, "huek ijci cvrw fcee")
    server.send_message(message)

print("Лист надіслано успішно!")