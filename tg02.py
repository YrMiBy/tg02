import asyncio
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY
from aiogram import Bot, Dispatcher, F, types
from gtts import gTTS
import os
from googletrans import Translator

api_key = WEATHER_API_KEY
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Сохранение фоток в папке img
@dp.message(F.photo)
async def react_photo(message: Message):
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')

# перевод текста на английский
@dp.message()
async def message(message: Message):
    try:
        translator = Translator()
        text = message.text  # Получаем текст сообщения от пользователя
        translation = translator.translate(text, dest='en')  # Переводим текст на английский
        translated_text = translation.text  # Получаем переведенный текст
        await message.answer(translated_text)  # Отправляем переведенный текст обратно пользователю
    except Exception as e:
        #logging.error(f"Ошибка при переводе: {e}")
        await message.answer("Произошла ошибка при переводе. Попробуйте позже.")


# Отправка голосового сообщения
@dp.message(Command('voise'))
async def voise(message: Message):
    try:
       await message.answer(f"Примите сообщение\n ")
       tts = gTTS(text='Всем привет', lang='ru')
       tts.save('voise.ogg') # Сохранение голосового сообщения
       voise = FSInputFile('voise.ogg') # переменная с названием файла
       await message.answer(voise=voise) # отправляем сообщение
       os.remove("voise.ogg") # Удаляем файл после отправки
    except Exception as e:
        await message.answer("Произошла ошибка при выполнении сообщения. Попробуйте позже.")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

