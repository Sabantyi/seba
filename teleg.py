import time, datetime
import telepot
from telepot.loop import MessageLoop
import requests
from bs4 import BeautifulSoup

url_doctor = "https://medkarta.online/local/widgets/record/?STEP=service&EMPLOYEE=14349&SHOW=employee&guid=%7B14D8C54B-DE23-4119-89BC-084E2CF0CAFC%7D&COMPANY=554674"
init(autoreset=True)

now = datetime.datetime.now()

def doctor():
    url = requests.get(url_doctor, headers=headers)
    soup = BeautifulSoup(url.text, features="lxml")
    vot = soup.find_all(class_="hours clearfix")

    name_doc = soup.find('span', class_="last-name")
    print(name_doc.text)

    for i in vot:
        name_a = i.find_all("a")
        if name_a == []:
            pass
        else:
            for sap in name_a:
                hour_pr = sap.attrs
                date_doc = hour_pr['data-date']
                time_doc = hour_pr['data-time']
                yield date_doc, time_doc

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print ('Received: %s' % command)
    if command == '/hi':
        for date_doc, time_doc in doctor():
            sleep(3)
            telegram_bot.sendMessage (chat_id, date_doc, time_doc)
    elif command == '/time':
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    elif command == '/logo':
        telegram_bot.sendPhoto (chat_id, photo = "https://i.pinimg.com/avatars/circuitdigest_1464122100_280.jpg")
    elif command == '/file':
        telegram_bot.sendDocument(chat_id, document=open('/home/pi/Aisha.py'))
    elif command == '/audio':
        telegram_bot.sendAudio(chat_id, audio=open('/home/pi/test.mp3'))

telegram_bot = telepot.Bot('6356623443:AAFRCK4VNdkHsU1nJQwvihRHF72jSzrXF9U')
print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running....')
while 1:
    time.sleep(10)