from bs4 import BeautifulSoup
import requests
import csv

def get_html(base_url): # возвращает html текст по заданному url (т.е. страницы, которую необходимо парсить)
    some = requests.get(base_url)
    return some.text

def get_pages(html): # возвращает колличество страниц, которое можно проверить
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-root-2oCjZ').find_all('span', class_='pagination-item-1WyVp')[-2].text
    return int(pages)

def get_page_data(html): # находит необходимые данные на заданной странице
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_ = 'js-catalog_serp').find_all('div', class_ = 'item__line') # ищет все объявления
    for ad in ads: # в каждом из них находит нужные параметры
        try:
            title = ad.find('h3', class_ = 'snippet-title').text.strip()
        except:
            title = ''
        try:
            price = ad.find('span', class_ = 'price price_highlight').text.strip()
        except:
            price = ''
        try:
            adress = ad.find('span', class_ = 'item-address-georeferences-item__content').text.strip()
        except:
            adress = ''
        try:
            url = 'https://www.avito.ru' + ad.find('h3', class_ = 'snippet-title').find('a').get('href')
        except:
            url = ''
        # записывает их в словарь
        data = {
            'title' : title,
            'price' : price,
            'metro' : adress,
            'ref' : url
        }
        write_csv(data) # запись данных из каждого объявления

def write_csv(data): # записывает все в csv формат
    with open('avito_phone.csv', 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], data['price'], data['metro'], data['ref']))

def main():
    first_url = 'https://www.avito.ru/moskva/telefony/iphone?p=1'
    html_text = get_html(first_url)
    pages = get_pages(html_text)
    base_url = 'https://www.avito.ru/moskva/telefony/iphone?p='
    for i in range(1, pages + 1):
        html = get_html(base_url + str(i))
        get_page_data(html)

if __name__ == '__main__':
    main()