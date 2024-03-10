import pyjokes
import random
from aiogram import types, F, Router
import requests
from utils import get_fruits

# Символи погоди
WEATHER_SYMBOL = {
    "Unknown":             "❓",
    "Clouds":              "☁️",
    "Scattered Clouds":    "☁️",
    "Drizzle":             "🌧",
    "Rain":                "🌧",
    "Thunderstorm":        "⛈",
    "Snow":                "❄️",
    "Mist":                "🌫",
    "Smoke":               "🌫",
    "Haze":                "🌫",
    "Dust":                "🌫",
    "Fog":                 "🌫",
    "Sand":                "🌫",
    "Ash":                 "🌫",
    "Squall":              "🌪",
    "Tornado":             "🌪",
    "Clear":               "☀️",
    "Sunny":               "☀️",
}

test_router = Router()

# Тести
@test_router.message(F.text == 'test')
async def test(message: types.Message):
    await message.answer('test')

@test_router.message(F.text == 'anekdot')
async def anekdot(message: types.Message):
    joke = pyjokes.get_joke()
    await message.answer(joke)

@test_router.message(F.text == 'Second button')
async def rand_int(message: types.Message):
    ran = random.randint(1, 100000)
    await message.answer(str(ran))

@test_router.message(F.text == 'Категорії')
async def category(message: types.Message):
    if message.text == 'Категорії':
        await message.answer('Зачекайте будь-ласка...')
        for item in get_fruits():
            card = (
                f'ID - {item["id"]}\n'
                f'Назва фрукта - {item["name"]}\n'
                f'Сімейство -  {item["family"]}\n'
                f'Нутриенти - {item["nutritions"]}\n'
            )
            await message.answer(card)

@test_router.message(F.text == 'Coffee')
async def coffee(message: types.Message):
    api = 'https://coffee.alexflipnote.dev/random.json'
    await message.answer('Зачекайте будь-ласка...')
    response = requests.get(api).json()
    card = f'Coffee : {response["file"]}'
    await message.answer(card)

# Отримання погоди
@test_router.message(F.text == 'Погода')
async def weather(message: types.Message):
    await message.answer("Введіть назву міста:")

@test_router.message()
async def process_weather(message: types.Message):
    city = message.text
    api_key = 'a8c0556856e69f039959bbda4588b830'
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
    data = res.json()
    if data['cod'] == 200:
        # Отримання інформації про погоду
        weather_info = (
            f"Координати: довгота {data['coord']['lon']}, широта {data['coord']['lat']}\n"
            f"Погодні умови: {WEATHER_SYMBOL.get(data['weather'][0]['main'], '❓')} {data['weather'][0]['description']}\n"
            f"Температура: {data['main']['temp']}°C\n"
            f"Відчувається як: {data['main']['feels_like']}°C\n"
            f"Мінімальна температура: {data['main']['temp_min']}°C\n"
            f"Максимальна температура: {data['main']['temp_max']}°C\n"
            f"Тиск: {data['main']['pressure']} hPa\n"
            f"Вологість: {data['main']['humidity']}%\n"
        )
        # Додавання додаткової інформації про погоду
        if 'sea_level' in data['main']:
            weather_info += f"Рівень моря: {data['main']['sea_level']} hPa\n"
        if 'grnd_level' in data['main']:
            weather_info += f"Рівень ґрунту: {data['main']['grnd_level']} hPa\n"
        weather_info += (
            f"Видимість: {data['visibility']} метрів\n"
            f"Швидкість вітру: {data['wind']['speed']} м/с\n"
            f"Напрям вітру: {data['wind']['deg']}°\n"
        )
        if 'gust' in data['wind']:
            weather_info += f"Пориви вітру: {data['wind']['gust']} м/с\n"
        weather_info += (
            f"Хмарність: {data['clouds']['all']}%\n"
            f"Дата та час: {data['dt']}\n"
            f"Країна: {data['sys']['country']}\n"
            f"Схід сонця: {data['sys']['sunrise']}\n"
            f"Захід сонця: {data['sys']['sunset']}\n"
            f"Часовий пояс: {data['timezone']}\n"
            f"ID: {data['id']}\n"
            f"Назва: {data['name']}\n"
            f"Код: {data['cod']}"
        )
        await message.answer(weather_info)
    else:
        await message.answer("Не вдалося отримати інформацію про погоду. Будь ласка, перевірте правильність введеного міста.")



