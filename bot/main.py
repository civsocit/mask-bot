import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

from bot.config import Config
from bot.services import impose_masks


config = Config.from_env()
bot = Bot(config.TOKEN, parse_mode='html')
bot.config = config
dp = Dispatcher(bot)


logging.basicConfig(level=config.LOG_LEVEL)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.answer(message.bot.config.HELP_TEXT)


@dp.message_handler(commands=['profile'])
async def from_profile(message: types.Message):
    await message.answer_media_group(
        await impose_masks(message.from_user)
    )


@dp.message_handler(content_types=ContentType.PHOTO)
async def from_photo(message: types.Message):
    await message.answer_media_group(await impose_masks(message))


async def on_startup(dp: Dispatcher):
    await dp.bot.set_my_commands([types.BotCommand(
            'profile',
            'сгенерировать картинку из нынешнего аватара'
        ), types.BotCommand(
            'help',
            'информация о том, как работает бот'
        )
    ])


def main():
    executor.start_polling(dp, on_startup=on_startup)


if __name__ == '__main__':
    main()
