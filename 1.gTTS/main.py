from gtts import gTTS
import os

text = "Вчими програмування і насолоджуємося цим процесо. ;)"

tts = gTTS(text=text, lang='uk')
tts.save('my.mp3')

os.system("start my.mp3")