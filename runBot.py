from Config import PROXY_URL ,TG_TOKEN, OPENAI_API_KEY
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.session.aiohttp import AiohttpSession
from openai import OpenAI
from moviepy.editor import AudioFileClip
import asyncio
import os

session = AiohttpSession(proxy=(PROXY_URL))
bot = Bot(token=TG_TOKEN, session=session)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")

@dp.message(F.voice)
async  def conwertWoiceToText(messege: Message) -> None:
    file_info = await bot.get_file(messege.voice.file_id)   # Знаходимо інфу про файл
    short_name = os.path.basename(os.path.splitext(file_info.file_path)[0])    # Формуємо скороочене імя файлу
    file_name = f'{short_name}_{messege.from_user.full_name}.aga'   # Формуємо повне імя файлів
    file_name_wav = f'{short_name}_{messege.from_user.full_name}.wav'
    await bot.download(messege.voice.file_id, file_name)    # Скачуємо файл в розширенні .aga
    audio_clip = AudioFileClip(file_name)   # Конвертуємо файз з формату .oga в .wav
    audio_clip.write_audiofile(file_name_wav, codec='pcm_s16le', fps=44100)

    audio = open(file_name_wav, 'rb')   # Відкриваємо файл .wav
    text = client.audio.transcriptions.create(  # Робота з OpenAI API
        model="whisper-1",
        file=audio,
        response_format="text",
    )
    audio.close()   # Закриваємо файл .wav
    await messege.reply(str(text))  # Відпрвляємо текст в бота

    os.remove(file_name)    # Видаляємо створені файли
    os.remove(file_name_wav)
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

