from setuptools import setup


setup(name='mask-bot',
      packages=['bot'],
      entry_points={'console_scripts': ['mask-bot = bot.main:main']})
