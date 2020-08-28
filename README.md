# Бот для создания аватарок
[![Supported python versions](https://img.shields.io/badge/Python-3.7%20%7C%203.8-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-lightgrey?style=flat-square&logo=telegram)](https://core.telegram.org/bots/api/)
[![Aiogram](https://img.shields.io/badge/Aiogram-blue?style=flat-square)](https://github.com/aiogram/aiogram/)
[![Docker](https://img.shields.io/badge/Docker-lightgray?style=flat-square&logo=docker)](https://docker.com/)

Бот для создания аватарок для акций. Накладывает изображение/изображения (маску) поверх другого изображения.
## Настройка
1. Загрузите изображения в формате png в папку `masks`. Они должны быть пронумерованы от 0. Размер может любым (больше - лучше, но перебарщивать не стоит), однако пропорции сторон должны быть 1 к 1;
2. Укажите в свой токен бота в файле `vars.env`;
3. Отредактируйте конфигурационный файл (`config.py`) для своих нужд.
### Возможные уровник логгирования
<p align="center">
    <img src="readme-images/logging_levels.png" />
</p>