import asyncio
from aiogram import Bot, Dispatcher, F

from config import TOKEN
from config import API_WEATHER

from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import requests


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n /start \n /help \n /city")
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я бот-предсказатель погоды!")

@dp.message(Command('city'))
async def city(message: Message):
    await message.answer("Введите город для прогноза погоды.")

@dp.message()
async def get_weather(message: Message):
    city = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric&lang=ru"

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        await message.answer("Город не найден. Пожалуйста, попробуйте снова.")
        return

    city = data["name"]
    weather_description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    weather_message = (f"Погода в городе {city}:\n"
                       f"Описание: {weather_description}\n"
                       f"Температура: {temperature}°C\n"
                       f"Ощущается как: {feels_like}°C\n"
                       f"Влажность: {humidity}%\n"
                       f"Скорость ветра: {wind_speed} м/с")

    await message.answer(weather_message)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())