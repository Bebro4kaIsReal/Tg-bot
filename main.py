from pprint import pprint
import requests
import pytesseract
from PIL import Image
import easyocr
from googletrans import Translator
import moviepy.editor
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, ContentType, InputFile


TOKEN ="6204961019:AAFpbcafBe0FPIgJXbO43NzHw43CmAJtkv4"
open_weather_token='909416efb243c60baae87798bab1dadc'

bot=Bot(token=TOKEN)
dp=Dispatcher(bot=bot)

def text_trans(text='Hello', dest='ru'):
    try:
        translator=Translator()
        translation=translator.translate(text=text,dest=dest)
        return translation.text
    except Exception as ex:
        return ex

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    first_name=message.from_user.first_name
    await message.reply(f"Привет, {first_name}!\nНапиши /help, чтобы узнать, что я могу")
@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.reply('Если хочешь, чтобы я вырезал звуковую дорожку, скинь мне видео.\nЕсли тебе нужен перевод текста с картинки, отправь мне фото.\nЕсли нужна сводка погоды, напиши название города')
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    user_id=message.from_user.id
    await message.reply('Секундочку')
    photo_path=f'media/test({user_id}).jpg'
    await message.photo[-1].download(photo_path)
    def first_var():
        img = Image.open(f'media/test({message.from_user.id}).jpg')
        pytesseract.pytesseract.tesseract_cmd = r'D:\tess\tesseract.exe'
        text = pytesseract.image_to_string(img)
        text=text.replace("\n"," ")
        text = text.replace("|", "i")
        if len(text) == 0:
            return second_var()
        else:
            return text
    def second_var():
        photo_path = f'media/test({message.from_user.id}).jpg'
        reader = easyocr.Reader(['en'])
        result = reader.readtext(photo_path, detail=0)
        return ' '.join(result)
    def text_trans(text='Hello', dest='ru'):
        try:
            translator = Translator()
            translation = translator.translate(text=text, dest=dest)
            return translation.text
        except Exception as ex:
            return ex
    ready_txt=text_trans(text=first_var(),dest='ru')
    await message.reply(text_trans(text=first_var(),dest='ru'))
@dp.message_handler(content_types=ContentType.VIDEO_NOTE)
async def save_video(message: types.Message):
    user_id=message.from_user.id
    await message.reply('Секундочку')
    await message.video_note.download(f'media/vid({user_id}).mp4')
    video=moviepy.editor.VideoFileClip(f'media/vid({user_id}).mp4')
    audio=video.audio
    audio.write_audiofile(f'media/vid({user_id}).mp3')
    audio_path=InputFile(path_or_bytesio=f'media/vid({message.from_user.id}).mp3')
    await dp.bot.send_audio(chat_id=message.from_user.id, audio=audio_path)
@dp.message_handler(content_types=ContentType.VIDEO)
async def save_video(message: types.Message):
    user_id=message.from_user.id
    await message.reply('Секундочку')
    await message.video.download(f'media/vid({user_id}).mp4')
    video=moviepy.editor.VideoFileClip(f'media/vid({user_id}).mp4')
    audio=video.audio
    audio.write_audiofile(f'media/vid({user_id}).mp3')
    audio_path=InputFile(path_or_bytesio=f'media/vid({message.from_user.id}).mp3')
    await dp.bot.send_audio(chat_id=message.from_user.id, audio=audio_path)
@dp.message_handler()
async def weather(message: types.Message):
    code_dis= {
        "Clear": "Ясно",
        "Clouds": "Облачно",
        "Rain": "Дождь",
        "Drizzle": "Дождь",
        "Thunderstorm": "Гроза",
        "Snow": "Снег",
        "Mist": "Туман"
    }
    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric')
        data = r.json()
        pprint(data)

        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']["speed"]
        weath = data["weather"][0]["main"]
        if weath in code_dis:
            wd = code_dis[weath]
        await message.reply(
            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n")

    except:
        await message.reply('Что-то я тебя не понимаю, напиши /help, чтобы узнать список команд')

if __name__== '__main__':
    executor.start_polling(dp)