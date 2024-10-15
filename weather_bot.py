import os
import telebot
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
WEATHERAPI_KEY = os.environ.get('WEATHERAPI_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте! Введите название города, чтобы узнать текущую погоду.")

@bot.message_handler(content_types=['text'])
def send_weather(message):
    city = message.text.strip()
    weather = get_weather(city)
    if weather:
        bot.reply_to(message, weather, parse_mode='Markdown')
    else:
        bot.reply_to(message, "Не удалось получить информацию о погоде для указанного города.")

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
        # Проверка на наличие предупреждений
        alerts = get_alerts(city)
        alert_message = f"\n\n⚠️ *Предупреждение:*\n{alerts}" if alerts else ""

        weather_info = (
            f"*Погода в городе {location}:*\n"
            f"🌡 Температура: *{temp_c}°C*\n"
            f"💧 Влажность: *{humidity}%*\n"
            f"☁ Описание: *{condition}*"
            f"{alert_message}"
        )
        return weather_info
    else:
        return None

def get_alerts(city):
    url = f"http://api.weatherapi.com/v1/alerts.json"
    params = {
        'key': WEATHERAPI_KEY,
        'q': city,
        'lang': 'ru'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'alerts' in data and data['alerts']['alert']:
            alerts = data['alerts']['alert']
            alert_texts = []
            for alert in alerts:
                headline = alert.get('headline', 'Без заголовка')
                desc = alert.get('desc', 'Нет описания')
                alert_texts.append(f"*{headline}*\n{desc}")
            return "\n\n".join(alert_texts)
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
