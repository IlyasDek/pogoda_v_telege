import os
import telebot
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
WEATHERAPI_KEY = os.environ.get('WEATHERAPI_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши название города, и я скажу тебе погоду.")

@bot.message_handler(content_types=['text'])
def send_weather(message):
    city = message.text.strip()
    weather = get_weather(city)
    if weather:
        bot.reply_to(message, weather)
    else:
        bot.reply_to(message, "Не получилось найти информацию о погоде для этого города.")

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json"
    params = {
        'key': WEATHERAPI_KEY,
        'q': city,
        'lang': 'ru'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        location = data['location']['name']
        temp_c = data['current']['temp_c']
        humidity = data['current']['humidity']
        condition = data['current']['condition']['text']

        weather_info = (
            f"Погода в городе {location}:\n"
            f"Температура: {temp_c}°C\n"
            f"Влажность: {humidity}%\n"
            f"Описание: {condition}"
        )
        return weather_info
    else:
        return None

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
