import random

import requests
import telebot
from bs4 import BeautifulSoup

weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
bot_token = "6150125244:AAE-nJdL9NAmMWdsr26HOA5y2xDJW7da56w"
bot = telebot.TeleBot(bot_token)


def get_weather(city):
    api_key = "85c25c01124f6f3f356825a8fe530ba9"
    final_url = weather_url.format(city, api_key)
    weather_response = requests.get(final_url).json()
    temp = int(weather_response["main"]["temp"] - 273.15)
    wind_speed = weather_response["wind"]["speed"]
    weather_desc = weather_response["weather"][0]["description"]
    return temp, wind_speed, weather_desc


def get_clothes_type(temp):
    if temp < 0:
        return "Тёплая зимняя куртка и свитер"
    elif temp < 10:
        return "Осенняя куртка и свитер"
    elif temp < 20:
        return "Легкая куртка или кофта"
    elif temp < 30:
        return "Футболка"
    else:
        return "Майка или купальник"


def get_shoes_type(temp):
    if temp < 0:
        return "Утеплённые ботинки"
    elif temp < 15:
        return "Кроссовки или ботинки"
    elif temp < 25:
        return "Кроссовки или лёгкие ботинки"
    else:
        return "Лёгкая обувь или сандалии"


def get_underwear_type(temp):
    if temp < 0:
        return "Теплое термобельё и утепленные штаны"
    elif temp < 10:
        return "Теплое термобелье с легкими штанами или утепленные штаны"
    elif temp < 20:
        return "Шорты или легкие штаны"
    else:
        return "Шорты"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я могу помочь тебе определить, какую одежду надеть на основе погоды. Просто отправь мне название города.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    city = message.text

    try:
        temp, wind_speed, weather_desc = get_weather(city)
        clothes_type = get_clothes_type(temp)
        shoes_type = get_shoes_type(temp)
        underwear_type = get_underwear_type(temp)
        response_msg = f"В городе {city} сейчас {weather_desc}. Температура {temp}°C, скорость ветра {wind_speed} м/с. \nРекомендуемая одежда: {clothes_type}. \nРекомендуемая обувь: {shoes_type}. \nРекомендуемая нижняя одежда: {underwear_type}."
        bot.reply_to(message, response_msg)

    except:
        bot.reply_to(message,
                     "Извините, не удалось получить данные о погоде. Пожалуйста, попробуйте ещё раз с другим названием города.")




def get_sneakers_url():
    sneakers_url = 'https://www.asos.com/men/shoes-boots-trainers/sneakers/cat/?cid=4208&currentpricerange=5-535&nlid=mw|shoes|shop%20by%20product&page=1&refine=attribute_1047:97149&sort=freshness'
    sneakers_response = requests.get(sneakers_url)
    sneakers_soup = BeautifulSoup(sneakers_response.content, 'html.parser')
    sneaker_links = sneakers_soup.find_all('a', class_='product-link')
    sneakers_random_link = random.choice(sneaker_links)['href']
    return sneakers_random_link


def get_pants_url():
    pants_url = 'https://www.asos.com/men/pants-chinos/cat/?cid=4910&currentpricerange=5-495&nlid=mw%7Cclothing%7Cshop%20by%20product&page=1&refine=attribute_1047:97149&sort=freshness'
    pants_response = requests.get(pants_url)
    pants_soup = BeautifulSoup(pants_response.content, 'html.parser')
    pants_links = pants_soup.find_all('a', class_='product-link')
    pants_random_link = random.choice(pants_links)['href']
    return pants_random_link


def get_jacket_url():
    jacket_url = 'https://www.asos.com/men/jackets-coats/cat/?cid=3606&currentpricerange=5-815&nlid=mw|clothing|shop%20by%20product&page=1&refine=attribute_1047:97149&sort=freshness'
    jacket_response = requests.get(jacket_url)
    jacket_soup = BeautifulSoup(jacket_response.content, 'html.parser')
    jacket_links = jacket_soup.find_all('a', class_='product-link')
    jacket_random_link = random.choice(jacket_links)['href']
    return jacket_random_link


def get_t_shirt_url():
    t_shirt_url = 'https://www.asos.com/men/t-shirts-vests/cat/?cid=7616&currentpricerange=5-365&nlid=mw|clothing|shop%20by%20product&page=1&refine=attribute_1047:97149&sort=freshness'
    t_shirt_response = requests.get(t_shirt_url)
    t_shirt_soup = BeautifulSoup(t_shirt_response.content, 'html.parser')
    tshirt_links = t_shirt_soup.find_all('a', class_='product-link')
    t_shirt_random_link = random.choice(tshirt_links)['href']
    return t_shirt_random_link


def get_shorts_url():
    shorts_url = 'https://www.asos.com/men/shorts/cat/?cid=9267&currentpricerange=5-275&nlid=mw%7Cclothing%7Cshop%20by%20product&page=1&refine=attribute_1047:97149&sort=freshness'
    shorts_response = requests.get(shorts_url)
    shorts_soup = BeautifulSoup(shorts_response.content, 'html.parser')
    shorts_links = shorts_soup.find_all('a', class_='product-link')
    shorts_random_link = random.choice(shorts_links)['href']
    return shorts_random_link

print("asdasdsa")
print(get_shorts_url())

bot.polling()
