from Config import TG_TOKEN, OPENAI_API_KEY, FFMPEG_PATH
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
import speech_recognition as sr
from aiogram.types import Message
from openai import OpenAI
import subprocess
import asyncio
import os

bot = Bot(TG_TOKEN)
dp = Dispatcher()
r = sr.Recognizer()
client = OpenAI(api_key=OPENAI_API_KEY)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")

@dp.message(F.voice)
async  def conwertWoiceToText(messege: Message) -> None:
    file_info = await bot.get_file(messege.voice.file_id)
    short_name = os.path.basename(os.path.splitext(file_info.file_path)[0])
    file_name = f'{short_name}_{messege.from_user.full_name}.aga'
    file_name_wav = f'{short_name}_{messege.from_user.full_name}.wav'
    await bot.download(messege.voice.file_id, file_name)
    subprocess.run([FFMPEG_PATH, '-i', file_name, file_name_wav])

    audio = open(file_name_wav, 'rb')
    text = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio,
        response_format="text",
    )
    audio.close()
    await messege.reply(str(text))

    os.remove(file_name)
    os.remove(file_name_wav)
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())