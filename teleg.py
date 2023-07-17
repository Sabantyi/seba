import time, datetime
import telepot
from telepot.loop import MessageLoop
import requests
from bs4 import BeautifulSoup

name_doc_final = ""

url_doctor = "https://medkarta.online/local/widgets/record/?STEP=service&EMPLOYEE=14349&SHOW=employee&guid=%7B14D8C54B-DE23-4119-89BC-084E2CF0CAFC%7D&COMPANY=554674"
#init(autoreset=True)
headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84"}

now = datetime.datetime.now()

def doctor():
    global name_doc_final
    url = requests.get(url_doctor, headers=headers)
    soup = BeautifulSoup(url.text, features="lxml")
    vot = soup.find_all(class_="hours clearfix")

    flag_i = 0
    flag_name_a = 0

    name_doc = soup.find('span', class_="last-name")
    name_doc_final = name_doc.text
    #print(name_doc_final)

    for i in vot:
        name_a = i.find_all("a")
        flag_i + 1
        if name_a == []:
            flag_i + 1
        else:
            for sap in name_a:
                hour_pr = sap.attrs
                date_doc = hour_pr['data-date']
                time_doc = hour_pr['data-time']
                yield date_doc, time_doc
    if flag_name_a == flag_i:
        date_doc = "Бродовикова "
        time_doc = "Записи нет"
        yield date_doc, time_doc



def action(msg):
    global name_doc_final
    chat_id = msg['chat']['id']
    command = msg['text']
    print ('Received: %s' % command)
    if command == '/doctor':
        #telegram_bot.sendMessage (chat_id, str(name_doc_final))
        flag_name = True
        for date_doc, time_doc in doctor():
            #print(date_doc, time_doc, name_doc_final)
            if flag_name == True:
                telegram_bot.sendMessage(chat_id, str(name_doc_final))
                flag_name = False
            telegram_bot.sendMessage (chat_id, str(date_doc)+str("  ")+str(time_doc))
    elif command == '/time':
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    # elif command == '/logo':
    #     telegram_bot.sendPhoto (chat_id, photo = "https://i.pinimg.com/avatars/circuitdigest_1464122100_280.jpg")
    # elif command == '/file':
    #     telegram_bot.sendDocument(chat_id, document=open('/home/pi/Aisha.py'))
    # elif command == '/audio':
    #     telegram_bot.sendAudio(chat_id, audio=open('/home/pi/test.mp3'))

telegram_bot = telepot.Bot('5339647993:AAGT_fR_R8ptXMp9gzaBD2fSBt-VzfcFuF8') #5339647993:AAGT_fR_R8ptXMp9gzaBD2fSBt-VzfcFuF8    /////   6356623443:AAFRCK4VNdkHsU1nJQwvihRHF72jSzrXF9U
print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running....')
while 1:
    time.sleep(10)