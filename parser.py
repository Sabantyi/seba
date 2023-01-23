import requests
from bs4 import BeautifulSoup
from time import sleep
from art import text2art, tprint
from colorama import init, Fore, Back, Style

print(text2art("Dimka", font='varsity'))
print("\nПрограмма по поиску в Промэлектронике и ChipDip\n")
init(autoreset=True)
headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84"}


def promelec_url():
    url = requests.get(
        'https://www.promelec.ru/search/?query=' +
        input_url,
        headers=headers)
    soup = BeautifulSoup(url.text, features="lxml")
    print("Промэлектроника")
    data = soup.find_all("div", class_="table-list__item")
    for i in data:
        if i.find("div", class_="col-table col-table_2-5"):
            name = i.find("a", class_="product-preview__title link-title").text
            print(f"{name}, отсутствует")
        elif i.find("div", class_="col-table col-table_2"):
            link_item_span = i.find("span", class_="product-preview__text")
            link_item = link_item_span.find("a").get("href")
            yield link_item


def promelec():
    for link_item in promelec_url():
        sleep(1)
        url = requests.get(link_item, headers=headers)
        soup = BeautifulSoup(url.text, features="lxml")
        name_item = soup.find("h1").text
        prise_item = soup.find(
            "span", class_="table-list__total-price price-color").text

        value_item_window = soup.find_all("div", class_="js-accordion-wrap")
        value_sklad_item = ""
        value_extarnel_item = ""
        value_shop_item = ""
        for q in value_item_window:
            dash = q.find(
                "div", class_="popup-product-table__title hide-sm-mob")
            value_item = q.find("div", class_="col-table col-table_4")

            if q.find(
                "div",
                    class_="popup-product-table__title hide-sm-mob").text == "Оптовый склад «Промэлектроника»":
                value_sklad_item = "," + Fore.GREEN + "Оптовый склад: " + Fore.RED + \
                    value_item.find("span", class_="table-list__counter").text

            elif q.find("div", class_="popup-product-table__title hide-sm-mob").text == "Внешние склады, поставка под заказ":
                try:
                    value_extarnel_item = "," + Fore.GREEN + "Внешние склады: " + Fore.RED + \
                        value_item.find("span", class_="table-list__counter jsAmountInWarehouse").text
                except AttributeError:
                    value_extarnel_item = ""
            else:
                try:
                    value_shop_item = "," + Fore.GREEN + "Магазин: " + Fore.RED + \
                        value_item.find("span", class_="table-list__counter jsAmountInWarehouse").text
                except AttributeError:
                    value_shop_item = ""

        print(
            f"{name_item}, " +
            Fore.GREEN +
            f"Стоимость: " +
            Fore.BLUE +
            f"{prise_item}" +
            value_shop_item +
            value_sklad_item +
            value_extarnel_item +
            Fore.BLUE +
            f",{link_item}")


def chipdip():
    print("\nChip&Dip")
    flag_nal = True
    url = requests.get(
        'https://www.chipdip.ru/search?searchtext=' +
        input_url,
        headers=headers)
    soup = BeautifulSoup(url.text, features="lxml")
    data = soup.find_all("tr", class_="with-hover")
    for i in data:
        name = i.find("a", class_="link").text
        price = i.find("span", class_="price").text
        link_item = "https://www.chipdip.ru" + i.find("a").get("href")
        value = i.find_all("span", class_="nw")
        for st in value:
            if flag_nal:
                value_mix_1 = st.text
            else:
                value_mix_2 = st.text
            flag_nal = not flag_nal

        print(f"{name}, " + Fore.GREEN + f"Стоимость: " + Fore.BLUE + f"{price}, " + Fore.GREEN + f"Наличие: " + Fore.RED + f"{value_mix_1}{value_mix_2}, " + Fore.BLUE + f"{link_item}")

def main():
    promelec()
    chipdip()
    #input("\n\nНажмите Enter!")

while True:
    input_url = input("\nЧто ищим: ")
    if __name__ == '__main__':
        main()