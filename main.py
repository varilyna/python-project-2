import telebot
import requests
import json
import math

bot = telebot.TeleBot('6949308842:AAHLMDWxNy-rbKfBHu-iZPNVK_78pvcgV6E')
API = '7303cdb3e9fb4921f339daffe170e1c9'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Пожалуйста, введите название города:')


code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, я не понимаю, что там за погода..."
        bot.reply_to(message, f'*{city}*\n'
                              f'{wd}\n'
                              f'_температура:_ {temp}°C\n'
                              f'*Дополнительная информация*\n'
                              f'_влажность:_ {humidity}%\n'
                              f'_давление:_ {math.ceil(pressure / 1.333)} мм.рт.ст\n'
                              f'_скорость ветра:_ {wind} м/с', parse_mode="Markdown")
    else:
        bot.reply_to(message, 'Город указан неверно')


bot.polling(none_stop=True)

