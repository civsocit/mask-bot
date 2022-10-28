import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

from config import LOGGING_LEVEL, TEXT, TOKEN
from services import impose_masks
from services.date import get_date_and_name
from services.image import set_text

bot = Bot(TOKEN, parse_mode='html')
dp = Dispatcher(bot)


logging.basicConfig(level=LOGGING_LEVEL.upper())


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.answer(TEXT)


@dp.message_handler(commands=['profile'])
async def from_profile(message: types.Message):
    await message.answer_media_group(await impose_masks(user=message.from_user))


@dp.message_handler(content_types=ContentType.PHOTO)
async def from_photo(message: types.Message):
    await message.answer_media_group(await impose_masks(message=message))


@dp.message_handler(commands=["days"])
async def send_image(message: types.Message):
    await types.ChatActions.upload_photo()
    media = types.MediaGroup()
    date, text = get_date_and_name()
    media.attach_photo(types.InputFile(set_text(str(date), str(text))), "")

    await message.reply_media_group(media=media)


async def on_startup(dp: Dispatcher):
    await dp.bot.set_my_commands([
            types.BotCommand('profile',
                             'сгенерировать картинку из нынешнего аватара'),
            types.BotCommand('days',
                             'получить картинку сколько Дмитрий Иванов сидит'),
            types.BotCommand('help', 'информация о том, как работает бот')])


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
