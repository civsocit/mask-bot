import os


TOKEN = os.environ.get('TOKEN')
MASKS_PATH = 'masks/{}.png'  # путь до папки с масками, лучше не трогать

# Прозрачность маски
MASK_ENHANCE = 1  # число от 0 до 1

LOGGING_LEVEL = 'info'  # CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET

# Поясняющий текст, отправляется по  командам /help и /start
TEXT = ('Отправьте мне изображение и я наложу на него маску "Russian Lives '
        'Matter". Или используйте /profile, чтобы наложить на ваш нынешний '
        'аватар.\n\n'
        '<i>Чтобы картинка смотрелась привлекательнее, скадрируйте изображние '
        'до квадрата, поместив лицо в центр.</i>')

# Подпись под готовым/готовыми фото
CAPTION = ('Время объединяться. Только все вместе, отбросив разногласия, мы '
           'сможем победить. Становитесь Гражданами. Вступайте в '
           '<a href="civsoc.net">Гражданское Общество</a>!')
