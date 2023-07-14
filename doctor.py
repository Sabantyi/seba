import requests
from bs4 import BeautifulSoup
from art import text2art, tprint
from colorama import init, Fore, Back, Style

url_doctor = "https://medkarta.online/local/widgets/record/?STEP=service&EMPLOYEE=14349&SHOW=employee&guid=%7B14D8C54B-DE23-4119-89BC-084E2CF0CAFC%7D&COMPANY=554674"

print(text2art("Dimka", font='varsity'))
print("\nDOCTOR\n")
init(autoreset=True)

headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84"}

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
                print(hour_pr['data-date'], hour_pr['data-time'])



def main():
    doctor()
    input("\n\nНажмите Enter!")

while True:
    if __name__ == '__main__':
        main()