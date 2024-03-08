from Config import TG_TOKEN, OPENAI_API_KEY, FFMPEG_PATH
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
import speech_recognition as sr
from aiogram.types import Message
import subprocess
import asyncio
import os

bot = Bot(TG_TOKEN)
dp = Dispatcher()
r = sr.Recognizer()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")

@dp.message(F.voice)
async  def conwertWoiceToText(messege: Message) -> None:
    file_info = await bot.get_file(messege.voice.file_id)
    path = os.path.splitext(file_info.file_path)[0]
    fname = os.path.basename(path)
    file_name = f'{fname}_{messege.from_user.full_name}.aga'
    file_name_wav = f'{fname}_{messege.from_user.full_name}.wav'
    await bot.download(messege.voice.file_id, file_name)
    subprocess.run([FFMPEG_PATH, '-i', file_name, file_name_wav])
    with sr.AudioFile(file_name_wav) as source:
        audio = r.record(source)
    text = r.recognize_google_cloud(audio, OPENAI_API_KEY, 'ru-RU')
    await messege.reply(text)

    os.remove(file_name)
    os.remove(file_name_wav)
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())