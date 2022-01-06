from abc import ABC, abstractmethod
from telegram import ReplyKeyboardMarkup
from app.multi_language_text import MultiLanguageText


class BaseKey(ABC):
    @property
    @abstractmethod
    def text(self):
        pass


class Key(BaseKey):
    def __init__(self, text: str):
        self._text = text

    @property
    def text(self):
        return self._text

    def __str__(self):
        return self._text


class MultiLanguageKey(MultiLanguageText, BaseKey):
    def __init__(self, multi_language_keys_text: dict, **kwargs):
        super().__init__(multi_language_keys_text, **kwargs)


class MyKeyboardError(Exception): pass


class MyReplyKeyboardMarkup:
    def __init__(self, lang, keys=None, one_time=True, input_field_placeholder='', fallback_keys=None):
        self._keys = keys if keys else []
        self._one_time = one_time
        self._input_field_placeholder = input_field_placeholder
        self._fallback_keys = fallback_keys if fallback_keys else []
        self._lang = lang

    @property
    def keys(self):
        for key in self._keys:
            key.current_language = self._lang
        return self._keys

    @keys.setter
    def keys(self, keys: list):
        self._keys = keys

    @property
    def _keys_text(self):
        keys_text = []
        for line in self._keys:
            keys_text_line = []
            for key in line:
                keys_text_line.append(key.text)
            keys_text.append(keys_text_line)
        return keys_text

    @property
    def keys_number(self):
        return len(self.keys)

    @property
    def fallback_keys(self):
        return self._fallback_keys

    @fallback_keys.setter
    def fallback_keys(self, keys: list):
        self._fallback_keys = keys

    @property
    def _fallback_keys_text(self):
        fallback_keys_text = []
        for key in self._fallback_keys:
            fallback_keys_text.append(key.text)
        return fallback_keys_text

    @property
    def fallback_keys_number(self):
        return len(self.fallback_keys)

    @property
    def one_time(self):
        return self._one_time

    @one_time.setter
    def one_time(self, val: bool):
        self._one_time = val

    @property
    def input_field_placeholder(self):
        return self._input_field_placeholder

    @input_field_placeholder.setter
    def input_field_placeholder(self, msg: str):
        self._input_field_placeholder = msg

    @property
    def keyboard(self):
        keyboard_with_fallback_keys = self._keys_text[:]
        keyboard_with_fallback_keys.append(self._fallback_keys_text)

        return ReplyKeyboardMarkup(keyboard_with_fallback_keys, one_time_keyboard=self.one_time,
                                   input_field_placeholder=self.input_field_placeholder)

    def add_key(self, key: BaseKey, row=0):
        if row > self.keys_number:
            raise MyKeyboardError(f'Incorrect row value. Keyboard has only {self.keys_number} rows!')
        if key.text in self._keys_text[row]:
            raise MyKeyboardError('This key is already on this line of keyboard!')
        self._keys[row].append(key)

    def remove_key(self, key_text: str, row=0):
        if row > self.keys_number:
            raise MyKeyboardError(f'Incorrect row value. Keyboard has only {self.keys_number} rows!')
        if key_text in self._keys_text[row]:
            key_index = self._keys_text[row].index(key_text)
            del self._keys[row][key_index]
        else:
            raise MyKeyboardError('This key is not on the keyboard!')

    def add_fallback_key(self, key: BaseKey):
        if key.text in self._fallback_keys_text:
            raise MyKeyboardError('This key is already in the fallback keyboard!')
        self._fallback_keys.append(key)

    def remove_fallback_key(self, key_text: str):
        if key_text in self._fallback_keys_text:
            key_index = self._fallback_keys_text.index(key_text)
            del self._fallback_keys[key_index]
        else:
            raise MyKeyboardError('This key is not on the fallback keyboard!')

    def reset(self, fallback_keys_too=False):
        self._keys = []
        self._input_field_placeholder = ''
        if fallback_keys_too:
            self.fallback_keys = []
