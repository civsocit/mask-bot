import os
from typing import Union


class Config:
    _fields = ['TOKEN', 'MASKS_PATH', 'MASK_ENHANCE', 'LOG_LEVEL',
               'HELP_TEXT', 'CAPTION']

    TOKEN: str
    MASKS_PATH: str
    MASK_ENHANCE: int
    LOG_LEVEL: str
    HELP_TEXT: str
    CAPTION: str

    @staticmethod
    def validate_log_level(log_level: str) -> str:
        log_level = log_level.upper()
        if log_level not in ('CRITICAL',
                             'ERROR',
                             'WARNING',
                             'INFO',
                             'DEBUG',
                             'NOTSET'):
            raise ValueError('Invalid logging level.')
        return log_level

    @classmethod
    def from_env(cls):
        dictionary = {}
        for field in cls._fields:
            field_result = os.getenv(field)
            if field_result:
                dictionary[field.lower()] = field_result
        return cls(**dictionary)

    def __init__(self,
                 token: str,
                 help_text: str,
                 caption: str,
                 log_level: str = 'INFO',
                 mask_enhance: Union[int, str] = 1,
                 masks_path: str = 'masks/{}.png'):
        self.TOKEN = token
        self.HELP_TEXT = help_text
        self.CAPTION = caption
        self.LOG_LEVEL = self.validate_log_level(log_level)
        self.MASK_ENHANCE = int(mask_enhance)
        self.MASKS_PATH = masks_path
