import random
from translate import Translator
import requests
import telebot
import re

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


def get_clothes_link(temp):
    rng = random.randint(0, 1)
    if temp < 0:
        return get_random_jacket() + "\n" + get_random_hoodie()
    elif temp < 10:
        return get_random_light_jacket() + "\n" + get_random_hoodie()
    elif temp < 20:
        if rng == 0:
            return get_random_hoodie()
        else:
            return get_random_light_jacket() + "\n" + get_random_tshirt()
    elif temp < 30:
        return get_random_tshirt()
    else:
        return get_random_maika()


def get_shoes_type(temp):
    if temp < 0:
        return "Утеплённые ботинки"
    elif temp < 15:
        return "Кроссовки или ботинки"
    elif temp < 25:
        return "Кроссовки"
    else:
        return "Лёгкая обувь или сандалии"


def get_shoes_link(temp):
    rng = random.randint(0, 1)
    if temp < 0:
        return get_random_boots()
    elif temp < 15:
        if rng == 0:
            return get_random_boots()
        else:
            return get_random_sneakers()
    elif temp < 25:
        return get_random_sneakers()
    else:
        return get_random_slippers()


def get_underwear_type(temp):
    if temp < 0:
        return "Теплое термобельё и утепленные штаны"
    elif temp < 10:
        return "Теплое термобелье с легкими штанами или утепленные штаны"
    elif temp < 20:
        return "Шорты или легкие штаны"
    else:
        return "Шорты"


def get_underwear_link(temp):
    rng = random.randint(0, 1)
    if temp < 0:
        return get_random_pants() + "\n" + get_random_underwear()
    elif temp < 10:
        if rng == 0:
            return get_random_pants() + "\n" + get_random_underwear()
        else:
            return get_random_pants()
    elif temp < 20:
        if rng == 0:
            return get_random_shorts()
        else:
            return get_random_pants()
    else:
        return get_random_shorts()


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
        if contains_english_letter(weather_desc) == 1:
            weather_desc = translate_text(weather_desc)
            i = 0
        response_msg = f"В городе {city} сейчас {weather_desc}. Температура {temp}°C, скорость ветра {wind_speed} м/с. \nРекомендуемая одежда: {clothes_type}. \nРекомендуемая обувь: {shoes_type}. \nРекомендуемая нижняя одежда: {underwear_type}."
        bot.reply_to(message, response_msg)
        links = f"Ссылка на подборку верхней одежды: {get_clothes_link(temp)} \n Ссылка на подборку остальных предметов одежды: {get_underwear_link(temp)} \n Ссылка на подборку обуви: {get_shoes_link(temp)}"
        bot.reply_to(message, links)
        ending = f"Если вы хотите поменять город, то просто напишите его название"
        bot.reply_to(message, ending)
    except:
        bot.reply_to(message,
                     "Извините, не удалось получить данные о погоде. Пожалуйста, попробуйте ещё раз с другим названием города.")


def contains_english_letter(string):
    pattern = r'[a-zA-Z]'
    match = re.search(pattern, string)
    if match:
        return 1
    else:
        return 0


def translate_text(text):
    translator = Translator(to_lang="ru")
    translation = translator.translate(text)
    return translation

def get_random_link(clothing_type):
    with open('database.txt', 'r') as file:
        lines = file.readlines()

    links = []
    current_type = None

    for line in lines:
        line = line.strip()
        if line.endswith(':'):
            current_type = line[:-1]
        elif current_type == clothing_type:
            links.append(line)

    if links:
        return random.choice(links)
    else:
        return None


def get_random_jacket():
    return get_random_link('jacket')


def get_random_light_jacket():
    return get_random_link('light_jacket')


def get_random_pants():
    return get_random_link('pants')


def get_random_tshirt():
    return get_random_link('t-shirt')


def get_random_shorts():
    return get_random_link('shorts')


def get_random_sneakers():
    return get_random_link('sneakers')


def get_random_underwear():
    return get_random_link('underwear')


def get_random_hoodie():
    return get_random_link('hoodie')


def get_random_slippers():
    return get_random_link('slippers')


def get_random_boots():
    return get_random_link('boots')


def get_random_maika():
    return get_random_link('maika')


bot.polling()
