from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import os

def parse_news(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Ошибка запроса")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    # Заголовок новости
    title = soup.find('a', class_='title').text.strip()
    
    # Дата новости
    date = soup.find('div', class_='date').text.strip()
    print(f'Заголовок: {title}\nДата: {date}')

    # Ссылка новой страницы при нажатии на заголовок
    link = urljoin(url, soup.find('a', class_='title')['href'])
    new_response = requests.get(link)

    if new_response.status_code != 200:
        print("Ошибка запроса")
        return
        
    new_soup = BeautifulSoup(new_response.text, 'html.parser')
    # Текст новости
    paragraphs = new_soup.find_all('p')

    print("Текст:")
    for index in range(1, len(paragraphs)):
        # Если без условия, то выводится в конце какой-то Консультантонлайн
        if paragraphs[index].text.strip() != 'Консультантонлайн':
            print(paragraphs[index].text.strip())

    image_tag = new_soup.find('a', class_='gallery-item')
    # Имя папки с картинкой
    folder_name = 'images/'

    # Если папки нет создаем её
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Путь к картинке
    image_url = urljoin(url, image_tag['href'])
    image_name = os.path.join(folder_name, image_url.split('/')[-1])
    print(image_name)

    # Картинка в виде бинарных данных
    image_data = requests.get(image_url).content

    # Запись картинки в файл
    with open(image_name, 'wb') as file:
        file.write(image_data)
        
    print("Изображение скачано")

if __name__ == '__main__':
    url = 'https://www.pgups.ru/news'
    parse_news(url)